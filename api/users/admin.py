from django.contrib import admin
from api.users.models import User, Employee, Teacher
from django.contrib.auth.admin import UserAdmin
from api.users.forms import UserCreationForm, UserChangeForm

@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ('id', 'username','first_name','last_name', 'email', 'last_login','date_joined','is_active','is_staff','is_superuser', 'teacher_profile', 'employee_profile', 'role')

    list_filter = ('is_active','first_name','last_name', 'is_superuser','is_staff', 'created_by')

    readonly_fields = ['last_login','date_joined','created_at', 'updated_at', 'created_by']

    search_fields = ('id', 'username', 'email')

    ordering = ('id', "username", "last_login")

    fieldsets = (
        ('User', {'fields': ('username',"first_name","last_name", 'email', 'password', 'created_by', 'teacher_profile', 'employee_profile', 'role', 'groups')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        ('Dates', {'fields': ('created_at', 'updated_at', 'last_login',)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2"),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Employee, admin.ModelAdmin)
admin.site.register(Teacher, admin.ModelAdmin)
