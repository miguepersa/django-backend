from tokenize import blank_re
from django.db import models
from django.core.validators import MinValueValidator
from api.users.models import User, Teacher
from cloudinary.models import CloudinaryField
# Create your models here.


BACHILLERATO = 'Bachillerato'
PRIMARIA_MENOR = 'Primaria Menor'
PRIMARIA_MAYOR = 'Primaria Mayor'
PREESCOLAR = 'Preescolar'

INSTITUTION_STAGES = [
    (BACHILLERATO, 'Bachillerato'),
    (PRIMARIA_MENOR, 'Primaria Menor'),
    (PRIMARIA_MAYOR, 'Primaria Mayor'),
    (PREESCOLAR, 'Preescolar')
]


class Institution(models.Model):
    INTERNAL = 'INT'
    EXTERNAL = 'EXT'
    MIXED = 'MIX'

    TEACHER_SERVICE_CHOICES = [
        (INTERNAL, "Internal"),
        (EXTERNAL, "External"),
        (MIXED, "Mixed")
    ]
    teachers = models.ManyToManyField(
        Teacher, related_name='institution', blank=True)
    short_name = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    monitor = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='institutions', blank=True, null=True)
    classrooms_per_level = models.PositiveIntegerField(default=1,
                                                       validators=[MinValueValidator(1)], blank=True, null=True)
    students_per_classroom = models.PositiveIntegerField(default=1,
                                                         validators=[MinValueValidator(1)], blank=True, null=True)
    ocupancy_rate = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True)
    teacher_service = models.CharField(
        max_length=20,
        choices=TEACHER_SERVICE_CHOICES,
    )
    logo = models.ImageField(
        upload_to='logos', null=True, default=None, blank=True)
    
    TYPE_A = 'A'
    TYPE_B = 'B'
    TYPE_C = 'C'

    TYPE_CHOICES = [
        (TYPE_A, "Tipo A"),
        (TYPE_B, "Tipo B"),
        (TYPE_C, "Tipo C")
    ]

    type = models.CharField(choices=TYPE_CHOICES, max_length=8, blank=True, null=True)

    # logo = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.short_name


class InstitutionLevel(models.Model):
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True, blank=True, related_name='institution_levels')

    name = models.CharField(max_length=45, blank=True)

    stage = models.CharField(max_length=45, blank=True,
                             choices=INSTITUTION_STAGES)

    reference_level = models.CharField(max_length=45,null=True, blank=True)

    student_sections = models.IntegerField(blank=True, default=1)

    students_per_section = models.IntegerField(blank=True, default=1)

    institution_coordinator = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='coordinator_of', blank=True, null=True)

    def __str__(self):
        return str(self.name) + " | " + str(self.institution)


class InstitutionCoordinator(models.Model):
    institution = models.OneToOneField(
        Institution, blank=True, null=True, related_name='coordinator', on_delete=models.DO_NOTHING)

    user = models.OneToOneField(User, blank=True, null=True,
                                related_name='coordinator_profile', on_delete=models.DO_NOTHING)

    stage = models.CharField(max_length=45, blank=True,
                             choices=INSTITUTION_STAGES)
