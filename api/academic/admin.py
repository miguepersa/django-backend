from django.contrib import admin
from api.academic.models import *
from api.academic.forms import LessonForm

# Register your models here.
admin.site.register(Resource, admin.ModelAdmin)
admin.site.register(CourseSection, admin.ModelAdmin)
admin.site.register(AcademicYear, admin.ModelAdmin)
admin.site.register(License, admin.ModelAdmin)
admin.site.register(AchievementIndicator, admin.ModelAdmin)
admin.site.register(Goal, admin.ModelAdmin)
admin.site.register(LearningOutcome, admin.ModelAdmin)
admin.site.register(PreschoolGoal, admin.ModelAdmin)
admin.site.register(CurricularContent, admin.ModelAdmin)
admin.site.register(LearningTopic, admin.ModelAdmin)
admin.site.register(TPReference, admin.ModelAdmin)
admin.site.register(Topic, admin.ModelAdmin)
admin.site.register(GeneratingTopic, admin.ModelAdmin)
admin.site.register(LearningSubject, admin.ModelAdmin)
admin.site.register(ClassSchedule, admin.ModelAdmin)
admin.site.register(ClassMaterial, admin.ModelAdmin)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'licenss',
                    'version', 'language', 'description')
    list_filter = ('licenss', 'version', 'language')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'licens', 'title',)
    filter_horizontal = ('resources', )
    form = LessonForm


@admin.register(LessonProgram)
class LessonProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'program', 'term', 'lesson_number')
    list_filter = ('lesson', 'program', 'term', 'lesson_number')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'program', 'institution_level',
                    'start_date', 'end_date', 'status')
    list_filter = ('program', 'institution_level', 'status')
    filter_horizontal = ('teachers', )
