from rest_framework import serializers
from api.academic.models import *
from api.users.serializers import UserTeacherSerializer
from api.forums.serializers import ForumSerializer
from api.monitoring.serializers import ClassJournalSerializer
from api.institutions.serializers import *


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    licenss = LicenseSerializer(read_only=True)

    class Meta():
        model = Program
        fields = '__all__'
        read_only_fields = ('n_lessons', 'licenss')

    def get_fields(self):
        fields = super().get_fields()
        excluded_fields = self.context.get('excluded_fields', [])

        for f in excluded_fields:
            if f in fields:
                del fields[f]

        return fields


class SectionScheduleSerializer(serializers.ModelSerializer):
    program = serializers.CharField(
        source='course_section.course.program.name')
    stage = serializers.CharField(
        source='course_section.course.institution_level.stage')
    section = serializers.CharField(source='course_section.name')
    teacher = serializers.CharField(source='teacher.first_name')

    class Meta:
        model = ClassSchedule
        fields = (
            'program',
            'stage',
            'section',
            'day',
            'start_time',
            'end_time',
            'teacher'
        )

        read_only_fields = (
            'program',
            'stage',
            'section',
            'teacher',
        )


class ClassScheduleSerializer(serializers.ModelSerializer):
    teacher_info = UserTeacherSerializer(source='teacher', required=False)

    class Meta:
        model = ClassSchedule
        fields = (
            'id',
            'day',
            'start_time',
            'end_time',
            'course_section',
            'teacher',
            'teacher_info'
        )
        read_only_fields = ('teacher_info', )

    def get_fields(self):
        fields = super().get_fields()
        excluded_fields = self.context.get('excluded_fields', [])

        for f in excluded_fields:
            if f in fields:
                del fields[f]

        return fields


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class AcademicYearSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    active = serializers.BooleanField()

    class Meta:
        model = AcademicYear
        fields = '__all__'


class AchievementIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementIndicator
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'


class LearningSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningSubject
        fields = '__all__'


class LearningTopicSerializer(serializers.ModelSerializer):
    learning_subject = LearningSubjectSerializer(read_only=True)

    class Meta:
        model = LearningTopic
        fields = '__all__'


class PreschoolGoalSerializer(serializers.ModelSerializer):

    component = LearningTopicSerializer(read_only=True)

    class Meta:
        model = PreschoolGoal
        fields = '__all__'


class LearningOutcomeSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = LearningOutcome
        fields = (
            'id',
            'data',
        )

    def get_data(self, instance):
        goal = PreschoolGoalSerializer(instance.goal).data
        learning_topic = goal['component']['content']
        learning_subject = goal['component']['learning_subject']['content']
        data = {}
        data = {
            "learning_outcome": instance.content,
            "goal": goal["content"],
            "learning_topic": learning_topic,
            "learning_subject": learning_subject
        }
        return data


class CurricularContentSerializer(serializers.ModelSerializer):
    component = LearningTopicSerializer()

    class Meta:
        model = CurricularContent
        fields = (
            'id',
            'content',
            'component',
        )


class GeneratingTopicSerializer(serializers.ModelSerializer):

    learning_subject = LearningSubjectSerializer()

    class Meta:
        model = GeneratingTopic
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    generating_topic = GeneratingTopicSerializer()

    class Meta:
        model = Topic
        fields = '__all__'


class TPReferenceSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = TPReference
        fields = (
            'id',
            'content',
            'topic',
        )


class ClassMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMaterial
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    preeschool_curriculum = serializers.SerializerMethodField()
    middle_curriculum = serializers.SerializerMethodField()
    highschool_curriculum = serializers.SerializerMethodField()
    # licens = LicenseSerializer(read_only=True)
    # materials = ClassMaterialSerializer(many=True)
    # resources = ResourceSerializer(many=True)

    class Meta:
        model = Lesson
        fields = (
            'id',
            'title',
            'licens',
            'reference_number',
            'beginning',
            'development',
            'closure',
            'lesson_goal',
            'script',
            'slides',
            'achievement_indicators',
            'main_activities',
            'resources',
            'materials',
            'preeschool_curriculum',
            'middle_curriculum',
            'highschool_curriculum',
        )

    def get_preeschool_curriculum(self, instance):

        outcomes = LearningOutcomeSerializer(
            instance.learning_outcomes, many=True, read_only=True).data

        data = {
            'subjects': []
        }

        subjects = set([outcome['data']["learning_subject"]
                        for outcome in outcomes])

        for sub in subjects:
            data['subjects'].append(
                {"title": sub, 'topics': []})

        for subject in data['subjects']:

            for outcome in outcomes:
                learning_topic = outcome['data']['learning_topic']
                topic_titles = [topic['title'] for topic in subject['topics']]

                if learning_topic not in topic_titles:
                    subject['topics'].append(
                        {"title": outcome['data']["learning_topic"], 'goals': []})

            for topic in subject['topics']:

                for outcome in outcomes:
                    goal = outcome['data']['goal']
                    goal_titles = [goal['title'] for goal in topic['goals']]

                    if goal not in goal_titles:
                        topic['goals'].append(
                            {"title": outcome['data']["goal"], 'learning_outcomes': []})

                for goal in topic['goals']:

                    for outcome in outcomes:
                        lo = outcome['data']['learning_outcome']
                        lo_titles = [lo['title']
                                     for lo in goal['learning_outcomes']]

                        if lo not in lo_titles:
                            goal['learning_outcomes'].append(
                                {"title": outcome['data']["learning_outcome"]})

        return None if len(data['subjects']) == 0 else data

    def get_middle_curriculum(self, instance):

        contents = CurricularContentSerializer(
            instance.curriculum_content, many=True, read_only=True).data

        data = {
            'subjects': []
        }

        print(contents)

        subjects = set([content["component"]['learning_subject']["content"]
                        for content in contents])

        for sub in subjects:
            data['subjects'].append(
                {"title": sub, 'topics': []})

        for subject in data['subjects']:

            for content in contents:
                # print(content['component'])
                learning_topic = content['component']['content']
                topic_titles = [topic['title'] for topic in subject['topics']]

                if learning_topic not in topic_titles:
                    subject['topics'].append(
                        {"title": content['component']["content"], 'curriculum_contents': []})

            for topic in subject['topics']:

                for content in contents:
                    curriculum_content = content['component']['content']
                    content_titles = [cc['title']
                                      for cc in topic['curriculum_contents']]

                    if curriculum_content not in content_titles:
                        topic['curriculum_contents'].append(
                            {"title": content['component']["content"], })

        return None if len(data['subjects']) == 0 else data

    def get_highschool_curriculum(self, instance):

        references = TPReferenceSerializer(
            instance.curriculum_references, many=True).data

        data = {
            'subjects': []
        }

        subjects = set([ref["topic"]["generating_topic"]["learning_subject"]['content']
                        for ref in references])

        for sub in subjects:
            data['subjects'].append(
                {"title": sub, 'topics': []})

        for subject in data['subjects']:

            for ref in references:
                topic = ref['topic']['content']
                topic_titles = [topic['title'] for topic in subject['topics']]

                if topic not in topic_titles:
                    subject['topics'].append(
                        {"title": ref['topic']["content"], 'generating_topics': []})

            for topic in subject['topics']:

                for ref in references:
                    gen_topic = ref['topic']['generating_topic']['content']
                    gen_topics = [gen_topic['title']
                                  for gen_topic in topic['generating_topics']]

                    if gen_topic not in gen_topics:
                        topic['generating_topics'].append(
                            {"title": ref['topic']["generating_topic"]["content"], 'curriculum_references': []})

                for gen_topic in topic['generating_topics']:

                    for ref in references:
                        tpr = ref['content']
                        tpr_titles = [tpref['title']
                                      for tpref in gen_topic['curriculum_references']]

                        if tpr not in tpr_titles:
                            gen_topic['curriculum_references'].append(
                                {"title": ref['content']})

        return None if len(data['subjects']) == 0 else data


class LessonProgramSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = LessonProgram
        fields = '__all__'


class CourseSectionSerializer(serializers.ModelSerializer):
    class_journal = ClassJournalSerializer(many=True)
    schedule = ClassScheduleSerializer(many=True)
    next_lesson = LessonProgramSerializer()

    class Meta:
        model = CourseSection
        fields = (
            'id',
            'name',
            'class_journal',
            'schedule',
            'next_lesson'
        )

    def get_fields(self):
        fields = super().get_fields()
        excluded_fields = self.context.get('excluded_fields', [])

        for f in excluded_fields:
            if f in fields:
                del fields[f]

        return fields


class CourseSerializer(serializers.ModelSerializer):
    institution_level = serializers.CharField(
        source='institution_level.name', read_only=True)
    institution = InstitutionSerializer(
        source='institution_level.institution', read_only=True)
    program = serializers.CharField(source='program.name')
    lesson_count = serializers.IntegerField(source='program.n_lessons')
    lessons = serializers.DictField(child=LessonSerializer(
        many=True), source='program.getLessons')
    sections = CourseSectionSerializer(many=True)
    forum = ForumSerializer()
    next_lesson = LessonProgramSerializer()
    course_teachers = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, source='teachers')

    class Meta():
        model = Course
        fields = (
            'id',
            'institution',
            'institution_level',
            'program',
            'start_date',
            'end_date',
            'year',
            'status',
            'group_numbers',
            'trial',
            'teachers',
            'is_curricular',
            'lesson_count',
            'lessons',
            'sections',
            'course_teachers',
            'forum',
            'next_lesson'
        )

    def get_fields(self):
        fields = super().get_fields()

        excluded_fields = self.context.get('excluded_fields', [])
        for field in excluded_fields:
            if field in fields:
                fields.pop(field, default=None)

        return fields
