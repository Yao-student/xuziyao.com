from django.db import models

# Dairies
class Diary(models.Model):
    title = models.CharField(max_length=80)
    date = models.DateField()

    class Meta:
        verbose_name_plural = "Diaries"

    def __str__(self):
        return self.title

# Programming
class Programming(models.Model):
    title = models.CharField(max_length=80)
    date = models.DateField()

    def __str__(self):
        return self.title