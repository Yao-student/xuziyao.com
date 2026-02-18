from django.db import models

# Phigros Fanmade Charts
class PhigrosFanmadeChart(models.Model):
    title = models.CharField(max_length=80)
    difficulty = models.CharField(max_length=10)
    date = models.DateField()
    composer = models.CharField(max_length=80)
    illustrator = models.CharField(max_length=80)
    charter = models.CharField(max_length=80)
    bpm = models.FloatField()
    offset = models.FloatField()
    notenum = models.IntegerField()
    bilibili_bv = models.CharField(max_length=10, blank=True)
    phira_id = models.IntegerField(blank=True, null=True)
    phizone_id = models.CharField(max_length=36, blank=True)

    def __str__(self):
        return f'{self.title} [{self.difficulty}]'

# Posts
class Post(models.Model):
    title = models.CharField(max_length=80)
    date = models.DateField()
    tags = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title
