from django.db import models
from api.academic.models import *
from api.institutions.models import Institution
from api.users.models import User, Teacher
from cloudinary_storage.storage import RawMediaCloudinaryStorage

# Create your models here.


class Announcement(models.Model):

    title = models.CharField(max_length=128, blank=False)

    content = models.CharField(max_length=2048, blank=False)

    image = models.ImageField(blank=True, null=True)

    creation_date = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='announcements')

    start_date = models.DateTimeField()

    expiration_date = models.DateTimeField()

    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class AnnouncementUser(models.Model):

    CREATED = 'CREATED'
    UNREAD = 'UNREAD'
    READ = 'READ'
    EXPIRED = 'EXPIRED'

    ANNOUNCEMENT_STATUSES = [
        (CREATED, "Creado"),
        (UNREAD, "No leido"),
        (READ, "Leido"),
        (EXPIRED, "Expirado")]

    announcement = models.ForeignKey(
        Announcement, on_delete=models.SET_NULL, null=True, related_name='announcement_user')

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='announcement_user')

    status = models.CharField(
        choices=ANNOUNCEMENT_STATUSES, default="CREATED", max_length=45, blank=False)

    read_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return 'announcement: ' + str(self.announcement) + '| user: ' + str(self.user)


class FormTemplate(models.Model):
    TEACHER = 'Teacher'
    EMPLOYEE = 'Employee'

    FORM_TYPES = [
        (TEACHER, 'Teacher'),
        (EMPLOYEE, 'Employee'),
    ]

    name = models.CharField(max_length=64, blank=True)

    form_type = models.CharField(max_length=64, blank=True, choices=FORM_TYPES)

    start_date = models.DateTimeField()

    DRAFT = "Borrador"
    SENT = "Enviado"

    STATUS_CHOICES = [
        (DRAFT, "Borrador"),
        (SENT, "")
    ]

    status = models.CharField(
        max_length=128, choices=STATUS_CHOICES, default=DRAFT)

    end_date = models.DateTimeField()

    # form_questions = preguntas asociadas al template

    # teacher_form_answers

    def __str__(self):
        return f"{self.name} - {self.form_type}"


class UserForm(models.Model):
    form_template = models.ForeignKey(
        FormTemplate, on_delete=models.CASCADE, blank=True, null=True, related_name='forms')

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name='forms')

    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, related_name='teacher_Forms', blank=True, null=True)

    completed = models.BooleanField(default=False)

    completed_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Form: {str(self.form_template)} - {str(self.user)}"

    def getQuestions(self):
        return [form_question.question for form_question in FormTemplateQuestion.objects.filter(template=self.form_template)]


class FormQuestion(models.Model):
    title = models.CharField(max_length=64)

    description = models.CharField(max_length=512)

    licenss = models.ForeignKey(License, on_delete=models.DO_NOTHING,
                                related_name='form_questions', blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='created_form_questions', blank=True, null=True)

    creation_date = models.DateField(auto_now_add=True)

    NONE = 0
    SINGLE = 1
    MULTIPLE = 2

    OPTIONS_CHOICES = [
        (NONE, "No options"),
        (SINGLE, "Single"),
        (MULTIPLE, "Multiple")
    ]

    options_type = models.IntegerField(
        choices=OPTIONS_CHOICES, null=True, default=NONE)

    file = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"Pregunta: {self.title}"


class FormTemplateQuestion(models.Model):
    question = models.ForeignKey(
        FormQuestion, on_delete=models.DO_NOTHING, related_name='form_template')

    template = models.ForeignKey(
        FormTemplate, on_delete=models.CASCADE, related_name='form_questions')

    order = models.IntegerField()

    def __str__(self) -> str:
        return f"{str(self.template)} - {str(self.question)}"


class FormQuestionOption(models.Model):
    question = models.ForeignKey(
        FormQuestion, on_delete=models.DO_NOTHING, related_name='question_options')

    content = models.CharField(max_length=512)

    def __str__(self):
        return f"{str(self.question)} - Opcion: {self.content}"


class UserFormAnswer(models.Model):
    question = models.ForeignKey(
        FormQuestion, on_delete=models.DO_NOTHING, related_name='teacher_answers')

    answer_content = models.CharField(max_length=1024)

    user_form = models.ForeignKey(
        UserForm, on_delete=models.CASCADE, related_name='answers', null=True)


class ClassJournal(models.Model):
    date = models.DateField()
    lesson = models.ForeignKey(
        Lesson, related_name='class_journal', on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    section = models.ForeignKey(CourseSection, related_name='class_journal',
                                on_delete=models.CASCADE, null=True, blank=True)
    notes = models.CharField(max_length=512, blank=True)

    def __str__(self) -> str:
        return f"{self.lesson.title} - {self.date}"


class MonitoringForm(models.Model):
    comments = models.CharField(max_length=2048, blank=True)
    course_section = models.ForeignKey(
        CourseSection, related_name='forms', on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(
        User, related_name='monitoring_forms', on_delete=models.SET_NULL, null=True)
    monitor = models.ForeignKey(
        User, related_name='monitored_forms', on_delete=models.SET_NULL, null=True)
    grade = models.FloatField(default=0.0)
    estimated_grade = models.FloatField(default=0.0)
    teacher_type = models.CharField(
        choices=Teacher.TYPE_CHOICES, max_length=32)
    feedback = models.CharField(max_length=2048)
    reviewed = models.BooleanField(default=False)
    date = models.DateField()
    alert = models.BooleanField(default=False)

    def __str__(self):
        return f"Teacher: {self.teacher.first_name} - Monitor: {self.monitor.first_name}"


class MonitoringFormQuestion(models.Model):
    content = models.CharField(max_length=256)
    important = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    area = models.CharField(max_length=64, blank=True)
    weight = models.FloatField(default=0)
    type = models.CharField(choices=Teacher.TYPE_CHOICES,
                            max_length=32, blank=True)
    mandatory_comment = models.BooleanField(default=False)
    dependent = models.OneToOneField(
        'self',
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        active = "Active"
        if not self.is_active:
            active = "Not active"
        return f"{self.content} - {active}"


class MonitoringFormAnswer(models.Model):
    question = models.ForeignKey(
        MonitoringFormQuestion, related_name='answers', on_delete=models.SET_NULL, null=True)
    form = models.ForeignKey(
        MonitoringForm, related_name='answers', on_delete=models.CASCADE, null=True)
    answer = models.BooleanField(default=False)
    comment = models.CharField(max_length=2048, default='')
    not_applies = models.BooleanField(default=False)


class Training(models.Model):
    title = models.CharField(max_length=128, blank=True)
    video = models.URLField()
    programs = models.ManyToManyField(Program, related_name='trainings')
    teachers = models.ManyToManyField(User, related_name='trainings')
    stage = models.CharField(max_length=32, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    task_info = models.CharField(max_length=2048, blank=True)

    @property
    def tasks_number(self):
        return len(self.assigned_tasks.all())

    def __str__(self):
        return self.title


class TrainingTask(models.Model):
    training = models.ForeignKey(
        Training, related_name='assigned_tasks', on_delete=models.CASCADE)
    grade = models.IntegerField(default=0, blank=True, null=True)
    reviewed = models.BooleanField(default=False)
    reviewer = models.ForeignKey(
        User, related_name='reviewed_training_tasks', blank=True, null=True, on_delete=models.SET_NULL)
    comment = models.CharField(max_length=1024, blank=True, null=True)
    teacher = models.ForeignKey(
        User, related_name='training_tasks', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(blank=True, null=True)
    file = models.FileField(upload_to='raw/', blank=True,
                            null=True, storage=RawMediaCloudinaryStorage())

    def __str__(self):
        return f"Task from: {self.training.title}"

class MonitoringPicture(models.Model):
    created_by = models.ForeignKey(User, related_name='monitoring_pictures', on_delete=models.SET_NULL, null=True)
    picture = models.ImageField(upload_to='raw/', storage=RawMediaCloudinaryStorage())
    date = models.DateField(auto_now_add=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, related_name='monitoring_pictures')