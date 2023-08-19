from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import CustomUser
from .models import StudentProfile, TeacherProfile


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile


class UserAdmin(DefaultUserAdmin):
    list_display = ("email", "first_name", "last_name", "role", "year")
    list_filter = ("role", "year", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("last_name", "first_name", "role", "year")
    filter_horizontal = ()
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "avatar")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Role & Year", {"fields": ("role", "year")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    inlines = [StudentProfileInline, TeacherProfileInline]

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if obj and obj.role == "A":
            return [
                inline for inline in inlines if isinstance(inline, StudentProfileInline)
            ]
        elif obj and obj.role == "P":
            return [
                inline for inline in inlines if isinstance(inline, TeacherProfileInline)
            ]
        else:
            return []


admin.site.register(CustomUser, UserAdmin)
