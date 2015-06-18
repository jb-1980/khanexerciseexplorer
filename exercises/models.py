from django.db import models

# Create your models here.

class Exercises(models.Model):
    name = models.CharField(max_length=512, unique=True)
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    image_url_256 = models.URLField(max_length=512)
    ka_url = models.URLField(max_length=512)
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class Prerequisites(models.Model):
    requiredfor = models.CharField(max_length=512)
    exercise = models.ForeignKey('Exercises',to_field="name")
    
    def __unicode__(self):
        return self.exercise.title

class Videos(models.Model):
    videoid = models.CharField(max_length=512, unique=True)
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    ka_url = models.URLField(max_length=512)
    
    def __unicode__(self):
        return self.title

class RelatedVideos(models.Model):
    videoid = models.ForeignKey('Videos',to_field="videoid")
    exercise = models.ForeignKey('Exercises',to_field="name")
    
    def __unicode__(self):
        return self.videoid.title
