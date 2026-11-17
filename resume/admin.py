from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter

from .models import Resume


@admin.register(Resume)
class ResumeAdmin(ModelAdmin):
    list_display = ('photo', 'full_name', 'speciality', 'city', 'email', 'email_verified', 'user', 'created_at')
    list_display_links = ('photo', 'full_name')
    list_filter = ('email_verified', 'speciality', 'city', ('created_at', RangeDateFilter))
    list_filter_submit = True
    search_fields = ('name', 'surname', 'father_name', 'email', 'user__username')
    autocomplete_fields = ('user',)
    date_hierarchy = 'created_at'
    readonly_fields = ('photo_preview', 'created_at')
    list_per_page = 25
    fieldsets = (
        ('Person', {'fields': ('name', 'surname', 'father_name', 'email', 'email_verified', 'user')}),
        ('Profile', {'fields': ('speciality', 'city', 'education', 'experience')}),
        ('Photo', {'fields': ('image', 'photo_preview')}),
        ('Meta', {'fields': ('created_at',)}),
    )

    @admin.display(description='')
    def photo(self, obj):
        if not obj.image:
            return '—'
        return format_html('<img src="{}" alt="" style="width:36px;height:36px;object-fit:cover;border-radius:6px">', obj.image.url)

    @admin.display(description='Preview')
    def photo_preview(self, obj):
        if not obj.image:
            return 'No photo'
        return format_html('<img src="{}" alt="" style="max-width:220px;border-radius:8px">', obj.image.url)

    @admin.display(description='Name', ordering='surname')
    def full_name(self, obj):
        return f'{obj.name} {obj.surname} {obj.father_name}'.strip()
