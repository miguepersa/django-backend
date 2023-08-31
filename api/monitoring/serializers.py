from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from api.institutions.serializers import InstitutionSerializer, InstitutionLevelSerializer
from api.users.serializers import UserTeacherSerializer
# from api.academic.serializers import LessonSerializer


class AnnouncementSerializer(ModelSerializer):

    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementUserSerializer(ModelSerializer):

    data = AnnouncementSerializer(
        many=False, read_only=True, source="announcement")

    class Meta:
        model = AnnouncementUser
        fields = ('id', 'status', 'read_at', 'data')


class FormQuestionOptionsSerializer(ModelSerializer):
    class Meta:
        model = FormQuestionOption
        fields = (
            'id',
            'question',
            'content',
        )

    def get_fields(self):
        fields = super().get_fields()

        excluded_fields = self.context.get('excluded_fields', [])
        for field in excluded_fields:
            if field in fields:
                fields.pop(field, default=None)

        return fields


class FormQuestionSerializer(ModelSerializer):
    question_options = FormQuestionOptionsSerializer(many=True)

    class Meta:
        model = FormQuestion
        fields = (
            'id',
            'title',
            'description',
            'licenss',
            'created_by',
            'creation_date',
            'options_type',
            'file',
            'question_options'
        )

    def get_fields(self):
        fields = super().get_fields()

        excluded_fields = self.context.get('excluded_fields', [])
        for field in excluded_fields:
            fields.pop(field, default=None)

        return fields


class FormTemplateQuestionSerializer(ModelSerializer):
    question = FormQuestionSerializer()

    class Meta:
        model = FormTemplateQuestion
        fields = (
            'id',
            'question',
            'template',
            'order',
        )


class UserFormAnswerSerializer(ModelSerializer):
    class Meta:
        model = UserFormAnswer
        fields = '__all__'


class ClassJournalSerializer(ModelSerializer):

    lesson = serializers.CharField(source='lesson.title')
    lesson_id = serializers.IntegerField(source='lesson.id')
    section = serializers.CharField(source='section.__str__')
    # lesson = LessonSerializer()

    class Meta:
        model = ClassJournal
        fields = (
            'id',
            'date',
            'lesson',
            'lesson_id',
            'completed',
            'section',
            'notes',
        )


class FormTemplateSerializer(ModelSerializer):
    questions = FormTemplateQuestionSerializer(
        many=True, source='form_questions', required=False)

    class Meta:
        model = FormTemplate
        fields = (
            'id',
            'name',
            'form_type',
            'start_date',
            'status',
            'end_date',
            'questions',
        )

    def get_fields(self):
        fields = super().get_fields()

        excluded_fields = self.context.get('excluded_fields', [])
        for field in excluded_fields:
            fields.pop(field, default=None)

        return fields


class UserFormSerializer(ModelSerializer):
    institution = InstitutionSerializer()
    template = FormTemplateSerializer(source='form_template')
    answered_at = serializers.DateTimeField(source='completed_date')
    template_questions = FormQuestionSerializer(
        source='getQuestions', many=True)
    answers = UserFormAnswerSerializer(many=True)

    class Meta:
        model = UserForm
        fields = (
            'id',
            'template',
            'user',
            'institution',
            'completed',
            'answered_at',
            'template_questions',
            'answers'
        )

    def get_fields(self):
        fields = super().get_fields()

        excluded_fields = self.context.get('excluded_fields', [])
        for field in excluded_fields:
            fields.pop(field, default=None)

        return fields


class MonitoringFormQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringFormQuestion
        fields = (
            'id',
            'content',
            'important',
            'is_active',
            'mandatory_comment',
            'area',
            'weight',
            'type'
        )


class MonitoringFormAnswerSerializer(serializers.ModelSerializer):
    question = MonitoringFormQuestionSerializer()

    class Meta:
        model = MonitoringFormAnswer
        fields = (
            'id',
            'question',
            'answer',
            'comment',
            'form'
        )


class SectionSerializer(serializers.ModelSerializer):
    program = serializers.CharField(source='course.program.name')
    level = InstitutionLevelSerializer(source='course.institution_level')

    class Meta:
        model = CourseSection
        fields = (
            'id',
            'name',
            'program',
            'level',
            'course'
        )

    def get_fields(self):
        fields = super().get_fields()
        self.context["excluded_fields"] = ["reference_level",
                                           "student_sections", "students_per_section"]
        excluded_fields = self.context.get('excluded_fields', [])

        for field in excluded_fields:
            if field in fields:
                fields.pop(field, default=None)

        return fields


class MonitoringFormSerializer(serializers.ModelSerializer):
    course_section = SectionSerializer()
    teacher = UserTeacherSerializer()
    monitor = UserTeacherSerializer()
    answers = MonitoringFormAnswerSerializer(many=True)

    class Meta:
        model = MonitoringForm
        fields = (
            'id',
            'comments',
            'course_section',
            'teacher',
            'monitor',
            'grade',
            'estimated_grade',
            'teacher_type',
            'feedback',
            'reviewed',
            'date',
            'answers',
            'alert',
        )
        read_only_fields = ('course_section', )

    def get_fields(self):
        fields = super().get_fields()

        excluded_fields = self.context.get('excluded_fields', [])
        for field in excluded_fields:
            if field in fields:
                fields.pop(field, default=None)

        return fields


class TrainingSerializer(serializers.ModelSerializer):
    teachers = UserTeacherSerializer(many=True)
    tasks_number = serializers.IntegerField()

    class Meta:
        model = Training
        fields = (

            'id',
            'title',
            'video',
            'programs',
            'teachers',
            'stage',
            'start_date',
            'end_date',
            'task_info',
            'tasks_number'
        )


class TrainingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingTask
        fields = '__all__'

        
class MonitoringPictureSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer()
    class Meta:
        model = MonitoringPicture
        fields = (
            "id",
            "created_by",
            "picture",
            "date",
            "institution"
        )

    def get_fields(self):
        fields = super().get_fields()

        excluded_fields = self.context.get('excluded_fields', [])
        for field in excluded_fields:
            if field in fields:
                fields.pop(field, default=None)

        return fields