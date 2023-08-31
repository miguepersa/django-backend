from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import User, Employee, Teacher
from api.academic.serializers import *
from api.permissions import CustomPermission
from api.monitoring.models import UserForm, MonitoringForm
from api.monitoring.serializers import *
from api.institutions.models import Institution
from api.institutions.serializers import InstitutionSerializer
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config.settings.base import EMAIL_HOST_USER

import pandas as pd

# Create your views here.

"""
    Teacher CRUD view
"""


class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        teacher = Teacher()
        teacher.save()
        return Response({'message': 'Teacher profile created'}, status=status.HTTP_200_OK)

    def list(self, request):
        try:
            qs = Teacher.objects.all()
            data = []

            for t in qs:
                d = TeacherSerializer(t).data
                d['institution_name'] = []
                for i in t.institution.all():
                    d['institution_name'].append(i.name)

                u = User.objects.get(teacher_profile=t.id)

                trainings = u.trainings.all()
                tasks = u.training_tasks.all()
                d['total_trainings'] = len(trainings)
                d['completed_trainings'] = len(tasks)

                forms = u.forms.all()
                d['assigned_forms'] = len(forms)
                d['completed_forms'] = len(forms.filter(completed=True))
                d['form_alert'] = False
                forms = sorted(
                    forms, key=lambda x: x.form_template.start_date, reverse=True)
                if len(forms) >= 2 and (not forms[0].completed and not forms[1].completed):
                    d['form_alert'] = True

                try:
                    d['last_monitoring'] = None
                    forms = sorted(t.user.monitoring_forms.all(),
                                   key=lambda x: x.date, reverse=True)
                    if len(forms) > 0:
                        d['last_monitoring'] = forms[0].date

                    d['programs'] = [
                        {"id": c.program.id, "name": c.program.name} for c in t.courses.all()]

                except:
                    pass

                data.append(d)

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def institutions(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            institutions = teacher.institution.all()

            if request.user.role == 'monitoring_teacher':
                institutions = institutions | teacher.user.institutions.all()

            context = {
                'excluded_fields': [
                    'teachers'
                ]
            }

            data = InstitutionSerializer(
                institutions, many=True, context=context).data
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


"""
API endpoint that allows users to be viewed or edited.

"""

def send_new_user_email(user,request):
    from django_rest_passwordreset.models import ResetPasswordToken
    from django.conf import settings
    from django.urls import reverse
    from django.template.loader import render_to_string
    from django.core.mail import send_mail

    HTTP_USER_AGENT_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
    HTTP_IP_ADDRESS_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')

    token = ResetPasswordToken.objects.create(
            user=user,
            user_agent=request.META.get(HTTP_USER_AGENT_HEADER, ''),
            ip_address=request.META.get(HTTP_IP_ADDRESS_HEADER, ''),
        )

    context = {
        'user': f"{user.first_name} {user.last_name}",
        'email': user.email,
        'token': token.key,
        'reset_url': f"{reverse('password_reset:reset-password-request')}?token={token.key}"
    }

    template = 'users/user_create.html'
    email_plaintext_message = render_to_string(template, context)

    send_mail(
        # title:
        "Creación de contraseña - Plataforma Kurios",
        # message:
        '',
        # from:
        EMAIL_HOST_USER,
        # to:
        [user.email],
        False,
        html_message=email_plaintext_message

    )


class UserViewSet(viewsets.ModelViewSet):

    class UserPermissions(CustomPermission):
        def has_permission(self, request, view):
            if view.action == "forms" or view.action == "retrieve" or view.action == "contacts":
                return True
            return super().has_permission(request, view)

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserPermissions]

    def update(self, request):
        super().update(request)
        user = User.objects.get(pk=int(request.data["ID"]))
        groups = user.groups.all()
        if not groups.filter(name=user.role).exists():
            user.groups.clear()
            user.groups.add(name=user.role)
            user.save()

    def retrieve(self, request, pk=None):
        if request.user.has_perm('users.view_user'):
            return Response(UserSerializer(User.objects.get(pk=pk)).data, status=status.HTTP_200_OK)
        else:
            user = get_object_or_404(User.objects.all(), pk=pk)
            if user.username == request.user.username:
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return (Response({'status': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED))

    def create(self, request):
        try:
            u = User(
                username=request.data['username'],
                email=request.data['email'],
                role=request.data['role'],
            )
            u.set_password(request.data['password'])
            u.created_by = request.user

            if int(request.data['is_teacher']) == 1:
                teacher = Teacher()
                teacher.save()
                u.teacher_profile = teacher
                inst = Institution.objects.get(
                    pk=request.data['institution_id'])
                inst.teachers.add(teacher)

            if (request.data['phone'] != '' or request.data['address'] != '' or request.data['branch'] != ''):
                employee = Employee(
                    phone=request.data['phone'], address=request.data['address'], branch=request.data['branch'])
                employee.save()
                u.employee_profile = employee
            u.save()
            group = Group.objects.get(name=u.role)
            u.groups.add(group)
            u.save()

            send_new_user_email(u, request)

            return Response({'message': f'User \'{u.username}\' created'}, status=status.HTTP_200_OK)

        except Exception as e:
            raise e
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def forms(self, request):
        try:
            u = request.user
            uf = UserForm.objects.filter(user=u)
            data = UserFormSerializer(uf, many=True).data
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def employees(self, request):
        try:
            users = User.objects.exclude(employee_profile__isnull=True)
            data = UserSerializer(users, many=True).data
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def teachers(self, request):
        try:
            teachers = User.objects.exclude(teacher_profile__isnull=True)
            data = UserSerializer(teachers, many=True).data
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def contacts(self, request):
        try:
            contacts = User.objects.get(username=request.user).getContacts()
            data = ContactsSerializer(contacts, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


'''
    Employees CRUD view
'''


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [CustomPermission]


'''
    API endpoint to register multiple users from a csv file
'''


class UploadViewSet(viewsets.ViewSet):
    serializer_class = FileUploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):

        try:
            user = request.user
            if user:
                if not user.role or (user.role != 'IT' and not user.is_superuser):
                    return Response({'message': 'unauthorized'}, status=status.HTTP_403_FORBIDDEN)

            uploaded_file = request.FILES.get("file")
            errors = {}
            if uploaded_file is not None:
                reader = pd.read_csv(uploaded_file)
                i = 0
                for _, row in reader.iterrows():
                    try:
                        new_user = User(
                            username=row["username"],
                            first_name=row["first_name"],
                            last_name=row["last_name"],
                            role=row['role'],
                            email=row["email"]
                        )
                        new_user.set_password(str(row["password"]))
                        if (any(type(i) != type(float()) for i in [row['phone'], row['address'], row['branch']])):
                            employee = Employee(
                                phone=row['phone'], address=row['address'], branch=row['branch'])
                            employee.save()
                            new_user.employee_profile = employee
                        if row['is_teacher'] == 1:
                            new_teacher = Teacher()
                            new_teacher.save()
                            new_user.teacher_profile = new_teacher
                            new_user.save()
                            inst = Institution.objects.get(
                                pk=row['institution_id'])
                            inst.teachers.add(new_teacher)
                            inst.save()

                        new_user.save()
                        group = Group.objects.get(name=new_user.role)
                        new_user.groups.add(group)
                        new_user.save()
                        send_new_user_email(new_user, request)
                    except Exception as e:

                        errors[f'Row {i}:'] = str(e)
                    i += 1

                if errors == {}:
                    return Response({'status': 'Usuarios creados'}, status=status.HTTP_201_CREATED)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'archivo no cargado'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request, pk=None):
        try:

            if request.user.is_anonymous:
                return Response(
                    UserSerializer(request.user).data,
                    status=status.HTTP_200_OK
                )

            user = None
            if (pk and request.user.role):
                # Si se intenta ver un perfil ajeno, se revisa el rol
                if request.user.role == 'monitoring_teacher':
                    if request.user.isMonitorOf(User.objects.get(pk=pk)):
                        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

                elif request.user.role.endswith('_teacher'):
                    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
                elif request.user.role == 'external_coordinator':
                    if not request.user.isCoordinatorOf(User.objects.get(pk=pk)):
                        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
                elif request.user.role in ['purchases_and_inventory']:
                    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

                user = User.objects.get(pk=pk)

            elif not pk:
                user = request.user

            data = UserProfileSerializer(user).data

            forms = sorted(user.monitoring_forms.all(),
                           key=lambda x: x.date, reverse=True)

            if len(forms) > 0 and forms[0].reviewed:
                data['monitoring_form'] = MonitoringFormSerializer(forms[0], context={'excluded_fields': [
                                                                   'teacher', 'comments', 'grade', 'estimated_grade', 'answers', 'monitor', 'teacher_type']}).data
            else:
                data['monitoring_form'] = None

            surveys = UserForm.objects.filter(user=user)

            if surveys.exists():
                data['surveys'] = FormTemplateSerializer(
                    [s.form_template for s in surveys], many=True).data
            else:
                data['surveys'] = None

            return Response(
                data,
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [CustomPermission]
