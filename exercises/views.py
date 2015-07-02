from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from datetime import datetime, timedelta
from exercises.models import Exercises,Prerequisites,Videos,RelatedVideos,CommonCoreMap,CommonCore

# Create your views here.

def get_exercise_list(max_results=0,starts_with='',see=False):
    exercise_list = []
    if starts_with:
        exercise_list = Exercises.objects.filter(title__icontains=starts_with).order_by('-views')
    else:
        if see:
            exercise_list = Exercises.objects.order_by('title')
        else:
            exercise_list = Exercises.objects.order_by('-views')[:10]
    
    if max_results > 0:
        if len(exercise_list) > max_results:
            exercise_list = exercise_list[:max_results]
        
    return exercise_list

def exercise_table(request):
    exercises = Exercises.objects.order_by('title')
    context_dict = {'exercises':[]}
    for exercise in exercises:
        prerequisites = Prerequisites.objects.filter(requiredfor=exercise.name)
        videos = RelatedVideos.objects.filter(exercise=exercise)
        try:
            context_dict['exercises'].append({
                'cc':CommonCoreMap.objects.filter(exercise=exercise),
                'exercise':exercise,
                'prerequisites':prerequisites,
                'videos':videos,
                })            
        except CommonCoreMap.DoesNotExist:
            context_dict['exercises'].append({
                'cc':None,
                'exercise':exercise,
                'prerequisites':prerequisites,
                'videos':videos,
                })
    template_name = 'exercises/exercise_table.html'
    
    return render(request,template_name,context_dict)
    
def exercise(request,exercise_name_url):
    exercise_list = get_exercise_list()
    template_name = 'exercises/exercise.html'
    context_dict = {'exercise_list':exercise_list,}
    views = 0
    try:
        # Find the category with the given name.
        # Raises an exception if the category doesn't exist.
        # We also do a case insensitive match.
        exercise = Exercises.objects.get(name__iexact=exercise_name_url)
        views = exercise.views + 1
        exercise.views = views
        exercise.save()
        context_dict['exercise'] = exercise
        
        prerequisites = Prerequisites.objects.filter(requiredfor=exercise.name)
        videos = RelatedVideos.objects.filter(exercise=exercise)
        
        #videos = [i[1:-1] for i in exercise.related_videos[1:-1].split(',')]
        context_dict['prerequisites'] = prerequisites
        context_dict['videos']=videos
        #videos = json.loads(exercise.videos)
    except Exercises.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
     
    return render(request,template_name,context_dict)
    
def suggest_exercises(request):
    exercise_list = []
    starts_with=''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        
    exercise_list = get_exercise_list(10,starts_with)
    
    return render(request,'exercises/exercises_list.html',{'exercise_list':exercise_list})

def see_all(request):
    exercise_list = get_exercise_list(see=True)
    print ('this was activated')
    return render(request,'exercises/exercises_list.html',{'exercise_list':exercise_list})
    
