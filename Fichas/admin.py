from django.contrib import admin
from .models import Ficha, Review, Assignment, ComplementaryImage, Keywords
from django.utils.html import format_html


class FichaAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "linked_assignment_id",  # 'id' is added to the list_display to show the id of the ficha
        "status",
        "student",
        "assignment",
        "created_at",
        "updated_at",
    )
    list_filter = ("status",)
    search_fields = ["title", "description"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("teacher", "ficha", "created_at", "updated_at")
    search_fields = ["review", "ficha__title"]


class FichaInline(admin.TabularInline):  # or admin.StackedInline
    model = Ficha
    fields = (
        "id",
        "link_to_ficha",
        "student",
        "assignment",
        "status",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "id",
        "link_to_ficha",
        "student",
        "assignment",
        "status",
        "main_image",
        "get_short_description",
        "get_short_analysis",
        "references",
        "keywords",
        "misc",
        "created_at",
        "updated_at",
    )
    can_delete = False
    max_num = 0

    def get_short_analysis(self, obj):
        return obj.analysis[:50] + "..." if len(obj.analysis) > 50 else obj.analysis

    get_short_analysis.short_description = "Analysis"

    def get_short_description(self, obj):
        return (
            obj.description[:50] + "..."
            if len(obj.description) > 50
            else obj.description
        )

    get_short_description.short_description = "Description"

    def link_to_ficha(self, instance):
        link = '<a href="/fichas/{}/">{}</a>'.format(instance.id, instance.title)
        return format_html(link)

    link_to_ficha.short_description = "Titulo"


class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "id",  # 'id' is added to the list_display to show the id of the assignment
        "description",
        "formatted_status",
        "time_window_start",
        "time_window_end",
        "ficha_count",
    )
    readonly_fields = ["status", "id"]
    inlines = [FichaInline]

    def formatted_status(self, obj):
        color = "green" if obj.is_open() else "red"
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.status,
        )

    formatted_status.short_description = "Status"

    def ficha_count(self, obj):
        return obj.fichas.count()

    ficha_count.short_description = "Fichas Llenadas"


class ComplementaryImageAdmin(admin.ModelAdmin):
    list_display = ("ficha", "images")


class KeywordsAdmin(admin.ModelAdmin):
    list_display = ("name",)


# Register your models here
admin.site.site_header = "Administración de las Fichas"
admin.site.register(Ficha, FichaAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(ComplementaryImage, ComplementaryImageAdmin)
admin.site.register(Keywords, KeywordsAdmin)
