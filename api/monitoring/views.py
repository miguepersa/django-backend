from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet
from api.users.models import User
from .models import *
from .serializers import *
from api.permissions import CustomPermission
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

# Create your views here.


class AnnouncementViewSet(ModelViewSet):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        data = {}
        try:
            new_data = {**request.data}
            groups = []

            for key in new_data:
                data[key] = new_data[key][0]

            uploaded_image = request.FILES.get("image")
            data["image"] = uploaded_image

            if 'groups' in data:
                groups = data['groups'].split(',')
                del data['groups']

            institutions = []
            if 'institutions' in data:
                institutions = data['institutions'].split(',')
                del data['institutions']

            announcement = Announcement(**data)
            announcement.created_by = User.objects.get(username=request.user)
            announcement.save()

            users = User.objects.none()

            if groups != [] and groups != [""]:
                for group_id in groups:
                    group = Group.objects.get(pk=group_id)
                    users = users | group.user_set.all()
            else:
                users = User.objects.all()

            for user in users:
                if institutions != []:
                    '''
                        If institutions are passed, we check the institutions related to the user.
                        If an institution of the user is in the list of institutions passed,
                        the announcemenent is sent, else, we skip to the next user
                    '''
                    if 'teacher' in user.role or user.role == 'external_coordinator':
                        flag = False

                        if user.teacher_profile:
                            user_institutions = user.teacher_profile.institution.all()
                        else:
                            user_institutions = user.coordinator_of.all()

                        for institution in user_institutions:
                            if institution.id in institutions:
                                flag = True
                                break
                        if not flag:
                            continue

                au = AnnouncementUser(
                    user=user,
                    announcement=announcement,
                    status=AnnouncementUser.CREATED
                )
                au.save()

            return Response({'message': 'annnouncement sent'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            announcement = Announcement.objects.get(pk=pk)
            aus = AnnouncementUser.objects.filter(announcement=announcement, status=AnnouncementUser.READ)
            data = AnnouncementSerializer(announcement).data
            data['read_by'] = []
            for au in aus:
                data['read_by'].append({
                    'user_id' : au.user.id,
                    'user_name' : au.user.first_name,
                    'user_last_name' : au.user.last_name,
                    'read_at' : au.read_at
                })

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def send_institutions(self, request):
        try:
            data = request.data
            institutions = data['institutions']
            del data['institutions']

            announcement = Announcement(**data, created_by=request.user)
            announcement.save()

            for i in institutions:
                institution = Institution.objects.get(pk=i)
                for t in institution.teachers.all():
                    au = AnnouncementUser(announcement=announcement, user=t.user, status=AnnouncementUser.CREATED)
                    au.save()


            return Response({'message': 'announcement sent to institution teachers', 'announcement' : AnnouncementSerializer(announcement).data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=['GET'])
    def active(self, request):
        try:
            qs = Announcement.objects.filter(start_date__lte=datetime.now(), expiration_date__gt=datetime.now())
            data = AnnouncementSerializer(qs, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AnnouncementUserViewSet(ModelViewSet):
    serializer_class = AnnouncementUserSerializer
    queryset = AnnouncementUser.objects.all()
    permission_classes = [CustomPermission]

    def list(self, request):
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request)

    def partial_update(self, request, pk=None):
        try:
            au = AnnouncementUser.objects.get(pk=pk)
            if (au.user == request.user or request.user.role=='IT'):
                au.read_at = timezone.now()
                au.save()
                return Response({'message' : f'read at: {au.read_at}'})
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)    
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FormTemplateViewSet(ModelViewSet):
    serializer_class = FormTemplateSerializer
    queryset = FormTemplate.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data
            questions = []
            if 'form_questions' in data:
                questions = data['form_questions']
                del data['form_questions']

            form = FormTemplate(**data)
            form.save()
            i = 1
            for question in questions:
                fq = FormTemplateQuestion(question=FormQuestion.objects.get(
                    pk=question), template=form, order=i)
                fq.save()
                i += 1

            return Response({'message': f'form template {form.name} created'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    def partial_update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)

            data = request.data
            FormTemplateQuestion.objects.filter(template=pk).delete()

            questions = []
            if 'form_questions' in data:
                questions = data['form_questions']
                del data['form_questions']
            
            i = 1
            for question in questions:
                fq = FormTemplateQuestion(question=FormQuestion.objects.get(
                    pk=question), template=instance, order=i)
                fq.save()
                i += 1

            self.perform_update(serializer)

            # return Response(FormTemplateSerializer(instance.parent).data)
            return Response({'message': f'form template {instance.name} updated'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['GET'])
    def answers(self, request, pk):
        try:
            data = []
            user_forms = FormTemplate.objects.get(pk=pk).forms.all()
            for uf in user_forms:
                a = {
                    'user' : uf.user.id,
                    'institution' : uf.institution.id,
                    'answers' : [],
                    'completed_date' : uf.completed_date
                }
                for answer in uf.answers.all():
                    a['answers'].append({
                        'id' : answer.id,
                        'content' : answer.answer_content,
                        'question' : answer.question.id
                    })

                data.append(a)

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserFormViewSet(ModelViewSet):
    serializer_class = UserFormSerializer
    queryset = UserForm.objects.all()
    permission_classes = [CustomPermission]

    def list(self, request):
        try:
            allowed_roles = ['academic_coordination', 'academy_coordination',
                             'directors', 'IT', 'monitoring_coordinator']
            user = User.objects.get(username=request.user)
            if user.role not in allowed_roles and user.teacher_profile:
                return Response({'error' : 'Not allowed to access'}, status=status.HTTP_403_FORBIDDEN)

            data = UserFormSerializer(self.queryset, many=True, context={
                'excluded_fields' : [
                    'teachers', 
                    'organization', 
                    'date_joined', 
                    'address', 
                    'city',
                    'state', 
                    'classrooms_per_level',
                    'students_per_classroom',
                    'ocupancy_rate',
                    'monitor',
                    'completed',
                    'questions',
                    'question',
                    'answers'
                ]
            }).data

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            template = FormTemplate.objects.get(pk=request.data['template'])
            template.status = FormTemplate.SENT
            template.save()
            users = request.data['users']

            for user in users:
                u = User.objects.get(pk=int(user))
                if u.teacher_profile and template.form_type == FormTemplate.TEACHER:
                    for i in u.teacher_profile.institution.all():
                        uf = UserForm(form_template=template,
                                        user=u, institution=i)
                        uf.save()
                
                elif u.employee_profile and template.form_type == FormTemplate.EMPLOYEE:
                    uf = UserForm(form_template=template, user=u)
                    uf.save()

            return Response({'message': 'UserForm created'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        try:
            if not pk:
                return Response({'error': 'null value for pk'}, status=status.HTTP_400_BAD_REQUEST)

            tf = UserForm.objects.get(pk=pk)
            context = {
                'excluded_fields' : [
                    'teachers',
                    'organization',
                    'date_joined',
                    'address',
                    'city',
                    'state',
                    'monitor',
                    'classrooms_per_level',
                    'students_per_classroom',
                    'ocupancy_rate',
                    'teacher_service',
                    'logo',
                    'completed',
                    'questions',
                    'question'
                ]
            }

            data = UserFormSerializer(tf, context=context).data
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['PATCH'])
    def submit_answers(self, request):
        try:
            data = request.data
            user_form = UserForm.objects.get(pk=data['user_form_id'])

            if user_form.form_template.end_date <= datetime.now():
                return Response({'error' : 'The form is closed'}, status=status.HTTP_403_FORBIDDEN)

            if user_form.completed:
                return Response({'error' : 'form is marked as completed'}, status=status.HTTP_403_FORBIDDEN)

            if not request.user.is_superuser and user_form.user != request.user:
                return Response({'error': 'user not authorized to submit answers to this form'}, status=status.HTTP_403_FORBIDDEN)

            user_form.completed = True
            user_form.completed_date = datetime.now()
            user_form.save()
            for answer in data['answers']:
                user_form_answer = UserFormAnswer(
                    question=FormQuestion.objects.get(
                        pk=answer['question_id']),
                    answer_content=answer['content'],
                    user_form=user_form
                )
                user_form_answer.save()
            
            return Response({'message': 'answers submitted'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def active(self, request):
        try:
            ufs = UserForm.objects.filter(user=request.user)
            surveys = [i.form_template for i in ufs if i.form_template.start_date <= datetime.now() and i.form_template.end_date > datetime.now()]
            data = FormTemplateSerializer(surveys, many=True).data

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def answers(self, request, pk=None):
        try:
            uf = UserForm.objects.get(pk=pk)
            answers = uf.answers.all()
            data = UserFormAnswerSerializer(answers, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FormQuestionViewSet(ModelViewSet):
    serializer_class = FormQuestionSerializer
    queryset = FormQuestion.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = {}
            options = []
            
            data = request.data

            if 'options' in data:
                options = data['options']
                del data['options']

            if 'licenss' in data and data['licenss'] is not None and data['licenss'] != "":
                data['licenss'] = License.objects.get(pk=int(data['licenss']))

            q = FormQuestion(**data, created_by=request.user)
            q.save()

            for op in options:
                option = FormQuestionOption(content=op, question=q)
                option.save()

            return Response({'message': 'Question created', 'id': q.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FormTemplateQuestionViewSet(ModelViewSet):
    serializer_class = FormTemplateQuestionSerializer
    queryset = FormTemplateQuestion.objects.all()
    permission_classes = [CustomPermission]


class FormQuestionOptionsViewSet(ModelViewSet):
    serializer_class = FormQuestionOptionsSerializer
    queryset = FormQuestionOption.objects.all()
    permission_classes = [CustomPermission]


class UserFormAnswerViewSet(ModelViewSet):
    serializer_class = UserFormAnswerSerializer
    queryset = UserFormAnswer.objects.all()
    permission_classes = [CustomPermission]

class ClassJournalViewSet(ModelViewSet):
    serializer_class = ClassJournalSerializer
    queryset = ClassJournal.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            data['lesson'] = Lesson.objects.get(pk=data['lesson'])
            data['section'] = CourseSection.objects.get(pk=data['section'])
            cj = ClassJournal(**data)
            cj.save()

            if cj.completed:
                cs = data['section']
                if cs.next_lesson is not None:
                    cs.next_lesson = cs.next_lesson.next_lesson
                    cs.save()
            
            return Response({'message' : f'ClassJournal created id: {cj.id}'}, status=status.HTTP_201_CREATED)
    
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'])
    def add_multiple(self, request):
        try:
            data = request.data
            cjs = []
            for journal in data:
                lesson = Lesson.objects.get(pk=int(journal['lesson']))
                del journal['lesson']
                section = CourseSection.objects.get(pk=int(journal['section']))
                del journal['section']
                cj = ClassJournal(**journal, lesson=lesson, section=section)
                cj.save()
                cjs.append(cj)
                if cj.completed and section.next_lesson is not None:
                    section.next_lesson = section.next_lesson.next_lesson
                    section.save()

            return Response({'message' : 'success', 'created journals' : ClassJournalSerializer(cjs, many=True).data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class MonitoringFormViewSet(ModelViewSet):
    serializer_class = MonitoringFormSerializer
    queryset = MonitoringForm.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data

            answers = data['answers']
            del data['answers']
            section = CourseSection.objects.get(pk=int(data['course_section']))
            del data['course_section']
            teacher = User.objects.get(pk=int(data['teacher']))
            del data['teacher']

            form = MonitoringForm(**data, course_section=section, teacher=teacher, monitor=request.user)
            form.save()

            for answer in answers:
                question = MonitoringFormQuestion.objects.get(pk=answer['question'])
                ans = MonitoringFormAnswer(question=question, form=form, answer=answer['answer'], comment=answer['comment'])
                ans.save()
                if ans.answer:
                    form.grade += question.weight
                    form.save()
                else:
                    if question.important:
                        
                        if question.dependent is None:
                            form.alert = True
                            form.save()

                        else:
                            d = question.dependent
                            if MonitoringFormAnswer.objects.filter(question=d, form=form).exists():
                                a = MonitoringFormAnswer.objects.get(question=d, form=form)
                                if not a.answer:
                                    form.alert = True
                                    form.save()
                            else:
                                continue
                            

            form.grade = (form.grade * 0.8) + (form.estimated_grade * 0.2)
            form.save()

            return Response({'message' : 'ok', 'form' : MonitoringFormSerializer(form).data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        
        # get_object function removed bc was not working with the ViewSet
        instance = MonitoringForm.objects.get(pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
    
    def partial_update(self, request, pk, *args, **kwargs):
        try:
            kwargs['partial'] = True
            return self.update(request, pk, *args, **kwargs)
        
        except Exception as e:
            raise e
    
    
    
    def retrieve(self, request, pk, *args, **kwargs):
        try:
            obj = MonitoringForm.objects.get(pk=pk)
            data = MonitoringFormSerializer(obj).data
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MonitoringFormAnswerViewSet(ModelViewSet):
    serializer_class = MonitoringFormAnswerSerializer
    queryset = MonitoringFormAnswer.objects.all()
    permission_classes = [CustomPermission]

class MonitoringFormQuestionViewSet(ModelViewSet):
    serializer_class = MonitoringFormQuestionSerializer
    queryset = MonitoringFormQuestion.objects.all()
    permission_classes = [CustomPermission]

    @action(detail=False, methods=['GET'])
    def active(self, request):
        try:
            qs = MonitoringFormQuestion.objects.filter(is_active=True)
            data = MonitoringFormQuestionSerializer(qs, many=True).data
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class TrainingViewSet(ModelViewSet):
    serializer_class = TrainingSerializer
    queryset = Training.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data
            programs = [Program.objects.get(pk=p) for p in data['programs']]
            del data['programs']
            teachers = [User.objects.get(pk=p) for p in data['teachers']]
            del data['teachers']
            t = Training(**data)
            t.save()
            t.teachers.set(teachers)
            t.programs.set(programs)
            t.save()
            return Response({'message' : 'created', 'training' : TrainingSerializer(t).data}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        try:
            user = request.user
            trainings = []
            if "monitoring" in user.role or "coordinator" in user.role or user.role == "IT":
                trainings = Training.objects.all()
                data = TrainingSerializer(trainings, many=True).data
                return Response(data, status=status.HTTP_200_OK)
            
            else:
                return Response({'error' : 'not authorized'}, status=status.HTTP_403_FORBIDDEN)
            
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk):
        try:
            training = Training.objects.get(pk=pk)
            data = TrainingSerializer(training).data
            tasks = TrainingTask.objects.filter(training=training)
            data['tasks'] = TrainingTaskSerializer(tasks, many=True).data

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def my_trainings(self, request):
        try:
            trainings = Training.objects.filter(teachers=request.user)
            data = []
            for t in trainings:
                d = TrainingSerializer(t).data
                d['tasks'] = TrainingTaskSerializer(t.assigned_tasks.filter(teacher=request.user), many=True).data
                data.append(d)

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TrainingTaskViewSet(ModelViewSet):
    serializer_class = TrainingTaskSerializer
    queryset = TrainingTask.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data
            training = Training.objects.get(pk=int(data['training']))
            del data['training']
            
            reviewer = None
            if 'reviewer' in data.keys():
                reviewer = User.objects.get(pk=int(data['reviewer']))
                del data['reviewer']

            teacher = User.objects.get(pk=int(data['teacher']))
            del data['teacher']

            date = str(data['date'])
            del data['date']

            file = data['file']
            del data['file']

            tt = TrainingTask(**data, file=file, date=date, training=training, reviewer=reviewer, teacher=teacher)
            tt.save()

            return Response({'message' : 'created', 'task' : TrainingTaskSerializer(tt).data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        
        # get_object function removed bc was not working with the ViewSet
        instance = TrainingTask.objects.get(pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
    
    def partial_update(self, request, pk, *args, **kwargs):
        try:
            kwargs['partial'] = True
            return self.update(request, pk, *args, **kwargs)
        
        except Exception as e:
            raise e
    
    def retrieve(self, request, pk, *args, **kwargs):
        try:
            obj = TrainingTask.objects.get(pk=pk)
            data = TrainingTaskSerializer(obj).data
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class MonitoringPictureViewSet(ModelViewSet):
    serializer_class = MonitoringPictureSerializer
    queryset = MonitoringPicture.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = request.data
            picture = request.FILES.get('file')
            institution = Institution.objects.get(pk=int(data['institution'][0]))
            pic = MonitoringPicture(created_by=request.user, picture=picture, institution=institution)
            pic.save()

            context = {
                'excluded_fields' : [
                    'teachers',
                    'organization',
                    'date_joined',
                    'address',
                    'city',
                    'state',
                    'monitor',
                    'classrooms_per_level',
                    'students_per_classroom',
                    'ocupancy_rate',
                    'teacher_service',
                    'type'
                ]
            }

            data = MonitoringPictureSerializer(pic, context=context).data
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        try:
            qs = self.get_queryset()
            context = {
                'excluded_fields' : [
                    'teachers',
                    'organization',
                    'date_joined',
                    'address',
                    'city',
                    'state',
                    'monitor',
                    'classrooms_per_level',
                    'students_per_classroom',
                    'ocupancy_rate',
                    'teacher_service',
                    'type'
                ]
            }
            data = MonitoringPictureSerializer(qs, many=True, context=context).data
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk):
        try:
            obj = MonitoringPicture.objects.get(pk=pk)
            context = {
                    'excluded_fields' : [
                        'teachers',
                        'organization',
                        'date_joined',
                        'address',
                        'city',
                        'state',
                        'monitor',
                        'classrooms_per_level',
                        'students_per_classroom',
                        'ocupancy_rate',
                        'teacher_service',
                        'type'
                    ]
                }
            data = MonitoringPictureSerializer(obj, context=context).data

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)