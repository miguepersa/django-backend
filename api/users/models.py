from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from enum import Enum


class Teacher(models.Model):

    INTERNAL = "Internal"
    EXTERNAL = "External"

    TYPE_CHOICES = [
        (INTERNAL, "Interno"),
        (EXTERNAL, "Externo")
    ]

    I = 1
    II = 2
    III = 3

    LEVEL_CHOICES = [
        (I, "1"),
        (II, "2"),
        (III, "3")
    ]

    type = models.CharField(max_length=16, choices=TYPE_CHOICES, default=EXTERNAL)
    level = models.IntegerField(choices=LEVEL_CHOICES, default=I)
    # Model for teachers

    # pictures

    def __str__(self):
        try:
            return f"Teacher: {self.user.username}"
        
        except:
            return f"Teacher: {self.id}"

    def getStages(self):
        stages = []
        for course in self.courses.all():
            stages.append(course.institution_level.stage)

        return stages
'''
    Model for users that are employees
'''
class Employee(models.Model):
    # Model for employees

    CARACAS = 'CCS'
    MARACAIBO = 'MCB'
    PUERTO_LA_CRUZ = 'PLC'

    BRANCHES = [
        (CARACAS, "Caracas"),
        (MARACAIBO, "Maracaibo"),
        (PUERTO_LA_CRUZ, "Puerto la Cruz")
    ]

    phone = models.CharField(max_length=16, blank=False, unique=True)
    address = models.CharField(max_length=64, blank=False)
    branch = models.CharField(max_length=64, choices=BRANCHES, blank=False)

    def __str__(self):
        return str(self.id)


'''
    Base user
'''
class User(AbstractUser):
    # Base user model

    # will automatically add a timestamp as soon as the record is created and do not gets updated on updating the record
    created_at = models.DateTimeField(auto_now_add=True)
    # will add a timestamp as soon as the record is created as well as when the record is updated.
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    teacher_profile = models.OneToOneField(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name="user")

    employee_profile = models.OneToOneField(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="user")

    ACADEMIC_COORDINATION = 'academic_coordination'
    ACADEMY_COORDINATION = 'academy_coordination'
    DIRECTORS = 'directors'
    EXTERNAL_COORDINATOR = 'external_coordinator'
    EXTERNAL_TEACHER = 'external_teacher'
    INTERNAL_TEACHER = 'internal_teacher'
    IT = 'IT'
    MONITORING_COORDINATOR = 'monitoring_coordinator'
    MONITORING_TEACHER = 'monitoring_teacher'
    POST_SALES = 'post_sales'
    PURCHASES_AND_INVENTORY = 'purchases_and_inventory'

    ROLES = (
        (ACADEMIC_COORDINATION, "Coordinación Académica"),
        (ACADEMY_COORDINATION, "Coordinación de Academia"),
        (DIRECTORS, "Dirección"),
        (EXTERNAL_COORDINATOR, "Coordinador Externo"),
        (EXTERNAL_TEACHER, "Docente Externo"),
        (INTERNAL_TEACHER, "Docente Interno"),
        (IT, "IT"),
        (MONITORING_COORDINATOR, "Coordinador de Seguimiento"),
        (MONITORING_TEACHER, "Docente de Seguimiento"),
        (POST_SALES, "Post Ventas"),
        (PURCHASES_AND_INVENTORY, "Procura y Administracion")
    )
    
    role = models.CharField(max_length=32, choices=ROLES, blank=True, null=True)

    def __str__(self):
        return self.username
    
    def getContacts(self):
        '''
            Method that gets all the contacts for the current user.
        '''
        if self.role == 'IT':
            return list(User.objects.all())
        
        if self.employee_profile:
            if self.role.startswith('monitoring'):
                qs = list(User.objects.all())
                for i in self.institutions.all():
                    qs = qs + list(i.teachers.all())
            else:
                qs = User.objects.all().exclude(employee_profile=None)
            return list(qs)
        else:
            institutions = self.teacher_profile.institution.all()
            contacts = []
            for i in institutions:
                contacts.append(i.monitor)

            return contacts
                
    def isMonitorOf(self, monitored) -> bool:
        '''
            Method that checks if the current user (self) is a monitoring teacher 
            and monitors the specified user (monitored). It iterates over the institutions 
            of both users and returns True if there is a match.
        '''
        # Check if the user is a monitoring teacher and monitors a specific user
        if self.role != 'monitoring_teacher':
            return False
        
        flag = False
        for i1 in self.institutions.all():
            for i2 in monitored.teacher_profile.institution.all():
                if i1 == i2:
                    flag = True
                    break
            if flag:
                break
        return flag

    def isCoordinatorOf(self, coordinated) -> bool:
        '''
        The isCoordinatorOf method checks if the current user (self) is an external coordinator 
        and coordinates the specified user (coordinated). It retrieves the institution levels 
        of the coordinator and the courses of the coordinated user. It then checks 
        if any course's institution level matches with the coordinator's institution levels 
        and returns True in that case.
        '''
        try:
            if self.role != 'external_coordinator':
                return False
            
            flag = False

            institution_levels = self.coordinator_of.all()
            courses = Teacher.objects.get(pk=coordinated.teacher_profile.id).courses.all()

            for c in courses:
                for i in institution_levels:
                    if c.institution_level.id == i.id:
                        return True
        except Exception as e:
            raise e