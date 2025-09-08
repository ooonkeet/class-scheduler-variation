from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    theory_hours = models.IntegerField(default=0)
    practical_hours = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    subjects_taught = models.CharField(max_length=255, help_text="Comma-separated subjects")

    def __str__(self):
        return self.name
