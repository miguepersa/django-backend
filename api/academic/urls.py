from django.urls import path
from rest_framework.routers import DefaultRouter
from api.academic.views import *

router = DefaultRouter()
router.register(r'program', ProgramViewSet, basename="Programs")
router.register(r'course', CourseViewSet)
router.register(r'lesson', LessonViewSet)
router.register(r'resource', ResourceViewSet)
router.register(r'academic_year', AcademicYearViewSet)
router.register(r'course_section', CourseSectionViewSet)
router.register(r'lesson_program', LessonProgramViewSet)
router.register(r'license', LicenseViewSet)
router.register(r'achievement_indicator', AchievementIndicatorViewSet)
router.register(r'goal', GoalViewSet)
router.register(r'learning_outcome', LearningOutcomeViewSet)
router.register(r'preschool_objective', PreschoolGoalViewSet)
router.register(r'curricular_content', CurricularContentViewSet)
router.register(r'component', LearningTopicViewSet)
router.register(r'tp_reference', TPReferenceViewSet)
router.register(r'topic', TopicViewSet)
router.register(r'generating_topic', GeneratingTopicViewSet)
router.register(r'learning_area', LearningSubjectViewSet)
router.register(r'class_schedule', ClassScheduleViewSet)