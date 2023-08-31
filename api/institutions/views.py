from django.shortcuts import render
from .serializers import InstitutionSerializer, InstitutionLevelSerializer
from rest_framework import status, viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response
from api.academic.serializers import CourseSerializer, LessonSerializer, SectionScheduleSerializer
from api.academic.models import LessonProgram
from api.users.models import User, Teacher
from api.users.serializers import UserSerializer, TeacherSerializer
from api.permissions import CustomPermission
from .models import Institution, InstitutionLevel

import pandas as pd

# Create your views here.


class InstitutionViewSet(viewsets.ModelViewSet):
    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()
    permission_classes = [CustomPermission]

    def list(self, request):
        try:
            if (request.user.role):
                if request.user.role == 'external_coordinator':
                    self.queryset = Institution.objects.filter(
                        id=request.user.coordinator_of.get().institution.id)           
                elif request.user.role.endswith('_teacher') and request.user.role != 'monitoring_teacher':
                    self.queryset = request.user.teacher_profile.institution.all()

                data = InstitutionSerializer(self.get_queryset(), many=True, context={'excluded_fields' : ['institution',]}).data

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error' : 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED, )
            
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk):
        try:
            if (request.user.role):
                inst = Institution.objects.get(pk=pk)
                
                if request.user.role == 'external_coordinator' and request.user.coordinator_of.get().institution.id != inst.id:
                    return Response({'error' : 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED) 
                elif request.user.role != 'monitoring_teacher' and request.user.role.endswith('_teacher') and inst not in request.user.teacher_profile.institution.all():
                    return Response({'error' : 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED) 

                data = InstitutionSerializer(inst, context={'excluded_fields' : ['institution']}).data

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error' : 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            if not 'institution_level' in data:
                return super().create(request, *args, **kwargs)
            
            levels = [InstitutionLevel(**level) for level in data['institution_level']]

            del data['institution_level']        

            if 'monitor' in data:
                data['monitor'] = User.objects.get(pk=data['monitor'])

            inst = Institution(**data)
            inst.save()
            
            for level in levels:
                level.institution = inst
                level.save()

            return Response({'message' : f'Institution {inst.id} created'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_teachers(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        data = request.data
        teachers = data['teachers']
        for t in teachers:
            institution.teachers.add(Teacher.objects.get(pk=t))
            institution.save()

        return Response({'message' : 'teachers added'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def levels(self, request, pk):
        try:
            institution = Institution.objects.get(pk=pk)
            levels = InstitutionLevelSerializer(institution.institution_levels.all(), many=True, context={'excluded_fields' : ['institution']})
            return Response(levels.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise e
            return Response({'error': str(e)})
        
    @action(detail=True, methods=['get'])
    def teachers(self, request, pk=None):
        try:
            institution = Institution.objects.get(pk=pk)
            teachers = TeacherSerializer(institution.teachers.all(), many=True, context={'excluded_fields' : ['institution']})
            return Response(teachers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)})

    @action(detail=True, methods=['GET'])
    def calendar(self, request, pk):
        try:
            institution = Institution.objects.get(pk=pk)
            levels = institution.institution_levels.all()
            courses = []
            for level in levels:
                for course in level.courses.all():
                    courses.append(course)

            schedules = []
            for c in courses:
                for s in c.sections.all():
                    for sch in s.schedule.all():
                        schedules.append(sch)

            data = SectionScheduleSerializer(schedules,many=True).data

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        try:
            institution = Institution.objects.get(pk=pk)
            levels = institution.institution_levels.all()
            courses = []
            for level in levels:
                for course in level.courses.all():
                    data = CourseSerializer(course).data
                    data['lessons'] = {}
                    for i in range(1, 4):
                        lesson_program = [k for k in LessonProgram.objects.filter(
                            program=course.program).filter(term=i)]
                        lessons = [k.lesson for k in lesson_program].sort(
                            key=lambda x: x.reference_number)
                        l_data = LessonSerializer(lessons, many=True).data
                        data['lessons'][f'term {i}'] = l_data

                    data['institution_level'] = course.institution_level.name
                    data['program'] = str(course.program)

                    courses.append(data)
            return Response(courses, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def upload(self, request):
        user = request.user
        if user:
            if user.role != 'IT' and not user.is_superuser:
                return Response({'message': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            uploaded_file = request.FILES.get("file")
            errors = {}
            if uploaded_file is not None:
                reader = pd.read_csv(uploaded_file)
                i = 0
                for _, row in reader.iterrows():
                    try:
                        institution = Institution(**row)
                        institution.save()
                    except Exception as e:
                        errors[f'Row {i}:'] = str(e)

                    i = i+1

                if errors == {}:
                    return Response({'status': 'Instituciones creadas'}, status=status.HTTP_201_CREATED)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'archivo no cargado'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



"""
API endpoint that allows institutions to be viewed or edited.

"""


class InstitutionLevelViewSet(viewsets.ModelViewSet):
    serializer_class = InstitutionLevelSerializer
    queryset = InstitutionLevel.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data
            data['institution'] = Institution.objects.get(pk=data['institution'])
            il = InstitutionLevel(**data)
            il.save()
            return Response({'message': 'InstitutionLevel created'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def upload(self, request):
        try:
            uploaded_file = request.FILES.get("file")
            errors = {}
            if uploaded_file is not None:
                reader = pd.read_csv(uploaded_file)
                i = 0
                for _, row in reader.iterrows():
                    try:
                        institution = Institution.objects.get(pk=int(row['institution']))
                        del row['institution']
                        level = InstitutionLevel(**row, institution=institution)
                        level.save()
                    except Exception as e:
                        errors[f'Row {i}:'] = str(e)

                    i = i+1

                if errors == {}:
                    return Response({'status': 'Niveles creados'}, status=status.HTTP_201_CREATED)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error' : 'file error'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)