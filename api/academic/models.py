from django.db import models
from api.institutions.models import InstitutionLevel
from api.users.models import Employee, Teacher, User

# Create your models here.


class License(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class AcademicYear(models.Model):
    start_date = models.DateField()

    end_date = models.DateField()

    active = models.BooleanField(default=False)

    name = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        # self.name = f"{self.start_date.year} - {self.end_date.year}"
        return self.name


SPANISH = 'ES'
ENGLISH = 'EN'


LANG_CHOICES = [
    (SPANISH, 'Español'),
    (ENGLISH, 'Ingles'),
]


class Program(models.Model):

    name = models.CharField(max_length=255, blank=False)

    # 'license' es una palabra reservada de Python, por lo tanto, este campo se llama lic
    licenss = models.ForeignKey(
        License, on_delete=models.DO_NOTHING, related_name='programs', null=True)

    description = models.CharField(max_length=45, blank=True)

    version = models.CharField(
        choices=(('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')), max_length=8)

    language = models.CharField(
        choices=LANG_CHOICES, max_length=8, default="ES")

    short = models.BooleanField(default=False)

    n_lessons = models.IntegerField(default=0, blank=True, null=True)

    course_outline = models.URLField(blank=True, null=True)

    planification_term1 = models.URLField(blank=True, null=True)

    planification_term2 = models.URLField(blank=True, null=True)

    planification_term3 = models.URLField(blank=True, null=True)

    inventory = models.URLField(default='')

    activity_guide = models.URLField(default='')

    employees = models.ManyToManyField(
        Employee, related_name='programs', blank=True)

    # data_entry = id of ProgramEntry object

    def __str__(self):
        return f"{self.name} - Version: {self.version if self.version else 'N/A'} - {self.language}{' - Short' if self.short else ''}"

    def getLessons(self):
        lessons = {}
        lessons['first_term'] = [lessonProgram.lesson for lessonProgram in sorted(LessonProgram.objects.filter(
            program=self).filter(term=LessonProgram.FIRST_TERM), key=lambda x:x.lesson_number)]
        lessons['second_term'] = [lessonProgram.lesson for lessonProgram in sorted(LessonProgram.objects.filter(
            program=self).filter(term=LessonProgram.SECOND_TERM), key=lambda x:x.lesson_number)]
        lessons['third_term'] = [lessonProgram.lesson for lessonProgram in sorted(LessonProgram.objects.filter(
            program=self).filter(term=LessonProgram.THIRD_TERM), key=lambda x:x.lesson_number)]

        return lessons


class Course(models.Model):

    CREATED = 'CREATED'
    SUSPENDED = 'SUSPENDED'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    FINISHED = 'FINISHED'

    COURSE_STATUSES = [
        (CREATED, "Creado"),
        (SUSPENDED, "Suspendido"),
        (ACTIVE, "Activo"),
        (INACTIVE, "Inactivo"),
        (FINISHED, "Finalizado")
    ]

    institution_level = models.ForeignKey(
        InstitutionLevel, on_delete=models.DO_NOTHING, related_name='courses', blank=True, null=True)

    program = models.ForeignKey(Program, null=True, on_delete=models.SET_NULL)

    start_date = models.DateField()

    end_date = models.DateField()

    year = models.ForeignKey(
        AcademicYear, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='year_courses')

    status = models.CharField(
        max_length=16, choices=COURSE_STATUSES, default=CREATED)

    group_numbers = models.IntegerField(default=1)

    trial = models.BooleanField(default=False)

    teachers = models.ManyToManyField(
        Teacher, related_name='courses', blank=True)

    is_curricular = models.BooleanField(default=True)

    # forum = course forum

    # course_blocks = blocks of the course

    def __str__(self):
        return f"{self.program.name} | {str(self.institution_level)} | {str(self.year)}"

    def next_lesson(self):
        sc = list(self.sections.all())
        if len(sc) > 0 and all(i.next_lesson != None for i in sc):
            sc = sorted(sc, key=lambda x: x.next_lesson.lesson_number)
            return sc[0].next_lesson
        else:
            return None


class Resource(models.Model):

    SCREENSHOT = 'SCREENSHOT'
    RESOURCE = 'RESOURCE'
    PROGRAM = 'PROGRAM'

    RES_TYPES = [
        (SCREENSHOT, "Captura"),
        (RESOURCE, "Recurso"),
        (PROGRAM, "Programa"),
    ]

    name = models.CharField(max_length=128)

    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)

    type = models.CharField(choices=RES_TYPES, max_length=50, default=RESOURCE)

    url = models.URLField(blank=True)

    image = models.ImageField(blank=True)

    file = models.FileField(blank=True)

    number = models.IntegerField(blank=False, null=True)

    # resource_of = lessons that uses this resource

    def __str__(self):
        return self.name


class ClassMaterial(models.Model):
    content = models.CharField(max_length=255)
    optional = models.BooleanField(default=False)

    def __str__(self):
        return self.content

# Curriculum


class Goal(models.Model):
    content = models.CharField(max_length=1024)

    def __str__(self):
        return self.content


class LearningSubject(models.Model):
    content = models.CharField(max_length=1024)

    def __str__(self):
        return self.content

# Bachillerato


class GeneratingTopic(models.Model):
    content = models.CharField(max_length=1024)
    learning_subject = models.ForeignKey(
        LearningSubject, on_delete=models.CASCADE, related_name='generating_topics', null=True)

    def __str__(self):
        return self.content


class Topic(models.Model):
    content = models.CharField(max_length=1024)
    generating_topic = models.ForeignKey(
        GeneratingTopic, on_delete=models.CASCADE, related_name='topics', null=True)

    def __str__(self):
        return self.content


class TPReference(models.Model):
    content = models.CharField(max_length=1024)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name='theoric_references', null=True)

    def __str__(self):
        return self.content

# Primaria/Preescolar


class LearningTopic(models.Model):
    content = models.CharField(max_length=1024)
    learning_subject = models.ForeignKey(
        LearningSubject, on_delete=models.CASCADE, related_name='learning_topics', null=True)

    def __str__(self):
        return self.content


class CurricularContent(models.Model):
    content = models.CharField(max_length=1024)
    component = models.ForeignKey(
        LearningTopic, on_delete=models.CASCADE, related_name='curricular_content', null=True)

    def __str__(self):
        return self.content

# Preescolar


class PreschoolGoal(models.Model):
    content = models.CharField(max_length=1024)
    component = models.ForeignKey(
        LearningTopic, on_delete=models.CASCADE, related_name='preeschool_goals', null=True)

    def __str__(self):
        return self.content


class LearningOutcome(models.Model):
    content = models.CharField(max_length=1024)
    goal = models.ForeignKey(PreschoolGoal, on_delete=models.CASCADE,
                             related_name='learning_outcomes', null=True)

    def __str__(self):
        return self.content


# Lessons
class Lesson(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)

    licens = models.ForeignKey(
        License, on_delete=models.SET_NULL, related_name='lessons', null=True)

    reference_number = models.FloatField(default=1.0)

    learning_outcomes = models.ManyToManyField(
        LearningOutcome, related_name='lessons', blank=True)

    curriculum_content = models.ManyToManyField(
        CurricularContent, related_name='lessons', blank=True)

    curriculum_references = models.ManyToManyField(
        TPReference, related_name='lessons', blank=True)

    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name='lessons', null=True)

    lesson_goal = models.CharField(max_length=1024, null=True)

    beginning = models.CharField(max_length=2048, blank=True, null=True)

    development = models.CharField(max_length=2048, blank=True, null=True)

    closure = models.CharField(max_length=2048, blank=True, null=True)

    script = models.URLField(blank=True, null=True)

    slides = models.URLField(blank=True, null=True)

    achievement_indicators = models.CharField(
        max_length=2048, blank=True, null=True)

    main_activities = models.CharField(max_length=2048, blank=True, null=True)

    resources = models.ManyToManyField(
        Resource, related_name='resource_of', blank=True)

    materials = models.ManyToManyField(
        ClassMaterial, related_name='materials', blank=True)

    recomended_year = models.IntegerField(blank=True, null=True)

    BACHILLERATO = 'Bachillerato'
    PRIMARIA_MENOR = 'Primaria Menor'
    PRIMARIA_MAYOR = 'Primaria Mayor'
    PREESCOLAR = 'Preescolar'

    STAGES = [
        (BACHILLERATO, 'Bachillerato'),
        (PRIMARIA_MENOR, 'Primaria Menor'),
        (PRIMARIA_MAYOR, 'Primaria Mayor'),
        (PREESCOLAR, 'Preescolar')
    ]

    stage = models.CharField(choices=STAGES, blank=True, max_length=32)

    # forum_topics = forum topics related with the lesson

    def __str__(self):
        return f"{self.title}"


class LessonProgram(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='lesson_program')

    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name='lesson_program')

    next_lesson = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, related_name='previous_lesson')

    FIRST_TERM = 1
    SECOND_TERM = 2
    THIRD_TERM = 3

    TERM_OPTIONS = [
        (FIRST_TERM, "Primer Lapso"),
        (SECOND_TERM, "Segundo Lapso"),
        (THIRD_TERM, "Tercer Lapso"),
    ]

    lesson_number = models.IntegerField(blank=True, default=1)

    term = models.IntegerField(choices=TERM_OPTIONS, default=-1)

    def __str__(self):
        return f"{str(self.program)} - {str(self.lesson)}"


class AchievementIndicator(models.Model):
    content = models.CharField(max_length=1024)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='achievement_indicator', null=True)

    def __str__(self):
        return self.content


# Secciones
class CourseSection(models.Model):

    name = models.CharField(max_length=32, blank=True, null=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='sections')

    next_lesson = models.ForeignKey(
        LessonProgram, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f"{str(self.course)} - Seccion: {self.name}"


class ClassSchedule(models.Model):
    course_section = models.ForeignKey(
        CourseSection, on_delete=models.CASCADE, related_name='schedule')

    MON = "MONDAY"
    TUE = "TUESDAY"
    WED = "WEDNESDAY"
    THU = "THURSDAY"
    FRI = "FRIDAY"

    DAYS = [
        (MON, "Lunes"),
        (TUE, "Martes"),
        (WED, "Miercoles"),
        (THU, "Jueves"),
        (FRI, "Viernes")
    ]

    day = models.CharField(choices=DAYS, max_length=16)
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(
        User, related_name='schedules', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.day}: {self.start_time} - {self.end_time}"
