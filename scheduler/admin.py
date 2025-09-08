from django.contrib import admin
from .models import Subject, Faculty

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "theory_hours", "practical_hours")

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "subjects_taught")
