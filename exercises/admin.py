from django.contrib import admin
from exercises.models import *

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title','ka_url','views')
    
admin.site.register(Exercises,ExerciseAdmin)

