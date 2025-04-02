from django.db import models

# Phigros Fanmade Charts
class PhigrosFanmadeChart(models.Model):
    illustration = models.CharField(max_length=10)
    title = models.CharField(max_length=80)
    difficulty = models.CharField(max_length=10)
    date = models.DateField()
    composer = models.CharField(max_length=80)
    illustrator = models.CharField(max_length=80)
    charter = models.CharField(max_length=80)
    bpm = models.FloatField()
    offset = models.FloatField()
    notenum = models.IntegerField()

    def __str__(self):
        return f'{self.title} [{self.difficulty}]'

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
