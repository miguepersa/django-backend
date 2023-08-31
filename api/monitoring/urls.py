from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api.monitoring.views import *


router = DefaultRouter()
router.register(r'announcement', AnnouncementViewSet)
router.register(r'announcement_user', AnnouncementUserViewSet)
router.register(r'form_template', FormTemplateViewSet)
router.register(r'user_form', UserFormViewSet)
router.register(r'form_question', FormQuestionViewSet)
router.register(r'form_template_question', FormTemplateQuestionViewSet)
router.register(r'form_question_options', FormQuestionOptionsViewSet)
router.register(r'user_form_answer', UserFormAnswerViewSet)
router.register(r'class_journal', ClassJournalViewSet)
router.register(r'monitoring_form', MonitoringFormViewSet)
router.register(r'monitoring_form_answer', MonitoringFormAnswerViewSet)
router.register(r'monitoring_form_question', MonitoringFormQuestionViewSet)
router.register(r'training', TrainingViewSet)
router.register(r'training_task', TrainingTaskViewSet)
router.register(r'monitoring_pictures', MonitoringPictureViewSet)