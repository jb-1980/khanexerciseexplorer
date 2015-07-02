#!/usr/bin/env python3.4
import os
from getexercises import get_exercises
from django.db import IntegrityError
from makecommoncore import MakeCommonCore
from django.core.exceptions import ObjectDoesNotExist

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#def update_or_create(model, filter_kwargs, update_kwargs):
#    if not model.objects.filter(**filter_kwargs).update(**update_kwargs):
#        kwargs = filter_kwargs.copy()
#        kwargs.update(update_kwargs)
#        try:
#            model.objects.create(**kwargs)
#        except IntegrityError:
#            if not model.objects.filter(**filter_kwargs).update(**update_kwargs):
#                raise  # re-raise IntegrityError

def populate():

    exercise_dict = get_exercises(BASE_DIR+'/cachedskills.json')
    print(len(exercise_dict))
    for exercise in exercise_dict:

        #print exercise_dict[exercise]['description_html']
        if exercise_dict[exercise]['description_html'] == None:
            exercise_dict[exercise]['description_html'] = 'No description given.'
        ex = add_exercise(
            exercise,
            exercise_dict[exercise]['image_url_256'],
            exercise_dict[exercise]['ka_url'],
            exercise_dict[exercise]['title'],
            exercise_dict[exercise]['description_html']
        )
        print(exercise,ex)
        if exercise_dict[exercise]['prerequisites']:
            for pre in exercise_dict[exercise]['prerequisites']:
                try:
                    pre_data = exercise_dict[pre]
                except KeyError:
                    continue
                if pre_data['description_html'] == None:
                    pre_data['description_html'] = 'No description given.'
                required = add_exercise(
                    pre,
                    pre_data['image_url_256'],
                    pre_data['ka_url'],
                    pre_data['title'],
                    pre_data['description_html']
                )
                add_prerequisite(exercise,required[0])
        
        if exercise_dict[exercise]['related_videos']:
            for video in exercise_dict[exercise]['related_videos']:
                if video['description'] == None:
                    video['description'] = 'No description given.'
                rv = add_video(
                  videoid=video['videoid'],
                  title=video['title'],
                  description=video['description'],
                  url=video['url']
                )
                
                add_related_video(rv,ex[0])

    # TODO Print out what we have added to the console.

def populate_cc():
    cc = MakeCommonCore()
    cc_data = cc.quickly()
    for data in cc_data:
        category = data['category']
        strand = data['strand']
        standard = data['standard']
        description = 'None yet'
        cc_obj = add_commoncore(category,strand,standard,description)
        try:
            exercise = Exercises.objects.get(name=data['skill'])
        except ObjectDoesNotExist:
            continue
        add_commoncore_map(cc_obj,exercise)

def add_exercise(name,image_url_256,ka_url,title,description):
    fields = {
        'name':name,
        'image_url_256':image_url_256,
        'ka_url':ka_url,
        'title':title,
        'description':description
    }
    return Exercises.objects.update_or_create(name=name,defaults=fields)
    #return update_or_create(Exercises,filters,fields)

def add_prerequisite(name,exercise):
    fields = {
        'requiredfor':name,
        'exercise':exercise,
    }
    return Prerequisites.objects.update_or_create(
        requiredfor=name,
        exercise=exercise,
        defaults=fields)[0]

def add_video(videoid,title,description,url):
    fields = {
        'videoid':videoid,
        'title':title,
        'description':description,
        'ka_url':url,
    }
    return Videos.objects.update_or_create(videoid=videoid,defaults=fields)[0]

def add_related_video(videoid,exercise):
    fields = {
      'videoid':videoid,
      'exercise':exercise,
    }
    return RelatedVideos.objects.update_or_create(
        videoid=videoid,
        exercise=exercise,
        defaults=fields)[0]

def add_commoncore(category,strand,standard,description):
    fields = {
        'category':category,
        'strand':strand,
        'standard':standard,
        'description':description,
    }
    return CommonCore.objects.update_or_create(
        standard=standard,
        defaults=fields)[0]

def add_commoncore_map(commoncore,exercise):
    fields = {
        'standard':commoncore,
        'exercise':exercise,
    }
    return CommonCoreMap.objects.update_or_create(
        standard=commoncore,
        exercise=exercise,
        defaults=fields)[0]
       

# Start execution here!
if __name__ == '__main__':
    print("Starting population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khan_project.settings')
    import django
    django.setup()
    from exercises.models import *

    #populate()
    populate_cc()
