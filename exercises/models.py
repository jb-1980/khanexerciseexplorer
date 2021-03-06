from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class Exercises(models.Model):
    ka_id = models.CharField(max_length=128,unique=True)
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

class Units(models.Model):
    name = models.CharField(max_length=128)
    mission = models.ForeignKey('Missions',to_field="name")
    slug = models.SlugField()
    sequenceid = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Units, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        unique_together = ('name', 'mission',)

class Missions(models.Model):
    name = models.CharField(max_length=128,unique=True)
    slug = models.SlugField(max_length=128)
    sequenceid = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name

class MissionMap(models.Model):
    unit = models.ForeignKey('Units')
    exercise = models.ForeignKey('Exercises',to_field="ka_id")
    sequenceid = models.IntegerField(default=0)
    

class CommonCore(models.Model):
    category = models.CharField(max_length=128)
    strand = models.CharField(max_length=128)
    standard = models.CharField(max_length=128,unique=True)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.standard

class CommonCoreMap(models.Model):
    standard = models.ForeignKey('CommonCore',to_field="standard")
    exercise = models.ForeignKey('Exercises',to_field="name")
    
    def __unicode__(self):
        return self.standard
    
