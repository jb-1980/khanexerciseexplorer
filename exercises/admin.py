from django.contrib import admin
from exercises.models import *

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title','ka_url','views')
    
class VideosAdmin(admin.ModelAdmin):
    list_display = ('videoid','title','description','ka_url')
    
class RelatedVideosAdmin(admin.ModelAdmin):
    list_display = ('videoid','exercise')
    
class PrerequisitesAdmin(admin.ModelAdmin):
    list_display = ('requiredfor','exercise')
    
class CommonCoreAdmin(admin.ModelAdmin):
    list_display = ('category','strand','standard','description')
    
class CommonCoreMapAdmin(admin.ModelAdmin):
    list_display = ('standard','exercise')
    
admin.site.register(Exercises,ExerciseAdmin)
admin.site.register(Videos,VideosAdmin)
admin.site.register(RelatedVideos,RelatedVideosAdmin)
admin.site.register(Prerequisites,PrerequisitesAdmin)
admin.site.register(CommonCore,CommonCoreAdmin)
admin.site.register(CommonCoreMap,CommonCoreMapAdmin)


