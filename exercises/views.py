from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from datetime import datetime, timedelta
from exercises.models import Exercises,Prerequisites,Videos,RelatedVideos,CommonCoreMap,CommonCore,Units,Missions,MissionMap

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


def matrix_view(request):
    missions = Missions.objects.order_by('sequenceid')
    print(missions)
    context_dict = {'matrix_view':True,'missions':missions}
    template_name = 'exercises/matrix_view.html'
    
    return render(request,template_name,context_dict)
    
def mission(request,mission):
    mission_record = Missions.objects.get(slug=mission)
    print(mission_record.slug)
    units = Units.objects.filter(mission=mission_record).order_by('sequenceid')
    exercises = []
    for unit in units:
        exercises+=MissionMap.objects.filter(unit=unit)
    context_dict = {'matrix_view':True,'exercises':[],'missions':units,'mission':mission_record}
    for exercise in exercises:
        prerequisites = Prerequisites.objects.filter(requiredfor=exercise.exercise.name)
        videos = RelatedVideos.objects.filter(exercise=exercise.exercise.name)
        try:
            context_dict['exercises'].append({
                'cc':CommonCoreMap.objects.filter(exercise=exercise.exercise),
                'exercise':exercise.exercise,
                'prerequisites':prerequisites,
                'videos':videos,
                'unit':exercise.unit
                })            
        except CommonCoreMap.DoesNotExist:
            context_dict['exercises'].append({
                'cc':None,
                'exercise':exercise.exercise,
                'prerequisites':prerequisites,
                'videos':videos,
                'unit':exercise.unit
                })
    template_name = 'exercises/mission.html'
    
    return render(request,template_name,context_dict)
    
def exercise(request,exercise_name_url):
    exercise_list = get_exercise_list()
    template_name = 'exercises/exercise.html'
    context_dict = {'skill_view':True,'exercise_list':exercise_list,}
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
        commoncore = CommonCoreMap.objects.filter(exercise=exercise)
        
        #videos = [i[1:-1] for i in exercise.related_videos[1:-1].split(',')]
        context_dict['prerequisites'] = prerequisites
        context_dict['videos']=videos
        context_dict['commoncore']=commoncore
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
    
