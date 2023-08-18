from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .models import StudentProfile, TeacherProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    fk_name = "userprofile"


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    fk_name = "userprofile"


class CustomUserAdmin(UserAdmin):
    exclude = ("username", "last_login", "date_joined")
    USERNAME_FIELD = "email"

    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    add_form_template = "admin/auth/user/add_form.html"

    fieldsets = (
        (None, {"fields": ("email", "password", "avatar")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions",   {"fields": ('is_active', 'is_staff','is_superuser', 'role'),
                           'classes': ('collapse',),}),
    )

    def get_fieldsets(self, request, obj=None):
        if obj:
            return super().get_fieldsets(request, obj)
        return [(None, {'classes': ('wide',),
                        'fields': ('email', 'password1', 'password2'),
                        })]
    def get_inline_instances(self, request, obj=None):
        if obj:
            if hasattr(obj, "studentprofile"):
                self.inlines = [StudentProfileInline]
            elif hasattr(obj, "teacherprofile"):
                self.inlines = [TeacherProfileInline]
            else:
                self.inlines = []
        return super().get_inline_instances(request, obj)

    ordering = ("email",)
    list_filter = ("is_staff", "is_superuser",'is_active', 'role')

    inlines = [StudentProfileInline, TeacherProfileInline]

    list_display = (
        "email",
        "first_name",
        "last_name",
        "date_joined",
        "last_login",
        'is_student',
        'is_teacher',
    )

    def is_student(self, obj):
        return hasattr(obj, "studentprofile")
    is_student.boolean = True  # This will give a nice green/red display

    def is_teacher(self, obj):
        return hasattr(obj, "teacherprofile")
    is_teacher.boolean = True  # This will give a nice green/red display


admin.site.register(CustomUser, CustomUserAdmin)
