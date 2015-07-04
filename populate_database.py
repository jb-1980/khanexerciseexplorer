#!/usr/bin/env python3.4
import os,json
from getexercises import get_exercises
import getmissions
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

    exercise_dict = get_exercises(BASE_DIR+'/cachedskills.json',7)
    print(len(exercise_dict))
    for exercise in exercise_dict:

        #print exercise_dict[exercise]['description_html']
        if exercise_dict[exercise]['description_html'] == None:
            exercise_dict[exercise]['description_html'] = 'No description given.'
        ex = add_exercise(
            exercise_dict[exercise]['ka_id'],
            exercise,
            exercise_dict[exercise]['image_url_256'],
            exercise_dict[exercise]['ka_url'],
            exercise_dict[exercise]['title'],
            exercise_dict[exercise]['description_html']
        )
        print('{exercise} created'.format(exercise=exercise))
        if exercise_dict[exercise]['prerequisites']:
            for pre in exercise_dict[exercise]['prerequisites']:
                try:
                    pre_data = exercise_dict[pre]
                except KeyError:
                    continue
                if pre_data['description_html'] == None:
                    pre_data['description_html'] = 'No description given.'
                required = add_exercise(
                    pre_data['ka_id'],
                    pre,
                    pre_data['image_url_256'],
                    pre_data['ka_url'],
                    pre_data['title'],
                    pre_data['description_html']
                )
                add_prerequisite(exercise,required)
        
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
                
                add_related_video(rv,ex)

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

def populate_missions():
    khan_missions = {
      u'Early math (K-2)': [u'early-math',1],
      u'3rd grade (U.S.)': [u'cc-third-grade-math',2],
      u'4th grade (U.S.)': [u'cc-fourth-grade-math',3],
      u'5th grade (U.S.)': [u'cc-fifth-grade-math',4],
      #u'6th grade (Ontario)': [u'on-sixth-grade-math',5],
      u'6th grade (U.S.)': [u'cc-sixth-grade-math',6],
      u'7th grade (U.S.)': [u'cc-seventh-grade-math',7],
      u'8th grade (U.S.)': [u'cc-eighth-grade-math',8],
      u'Arithmetic': [u'arithmetic',9],
      u'Pre-algebra': [u'pre-algebra',10],
      u'Algebra basics': [u'algebra-basics',11],
      u'Algebra I': [u'algebra',12],
      #u'Basic geometry': [u'basic-geo',13],
      u'Geometry': [u'geometry',14],
      u'Algebra II': [u'algebra2',15],
      u'Trigonometry': [u'trigonometry',16],
      u'Probability and statistics': [u'probability',17],
      u'Precalculus': [u'precalculus',18],
      u'Differential calculus': [u'differential-calculus',19],
      u'Integral calculus': [u'integral-calculus',20],
      #u'Differential equations': [u'differential-equations',21],
      #u'Linear algebra': [u'linear-algebra',22],
      #u'Math contests': [u'competition-math',23],
      #u'Multivariable calculus': [u'multivariable-calculus',24],
      #u'Recreational math': [u'recreational-math',25],
      u'The World of Math':[u'math',26],
    }
    
    for mission in khan_missions:
        mission_sequence = khan_missions[mission][1]
        mission_slug = khan_missions[mission][0]
        mission_record = add_mission(mission,mission_slug,mission_sequence)
        print('retrieving all mission skills for {mission}'.format(mission=mission))
        if getmissions.check_cache(mission_slug,7):
            with open(khan_missions[mission][0]+'-cache2.json','r') as f:
                mission_tasks = json.loads(f.read())
        else:
            mission_tasks = getmissions.get_mission_tasks(mission_slug)
            with open(mission_slug+'-cache2.json','w') as f:
                f.write(json.dumps(mission_tasks))
        print('mission skills retrieved')
        for indx,unit in enumerate(mission_tasks['topics']):
            sequenceid = float('.'.join([str(mission_sequence),str(indx)]))
            unit_record = add_units(unit,mission_record,sequenceid)
            for sid,task in enumerate(mission_tasks['tasks'][unit]):
                try:
                    exercise_record = Exercises.objects.get(ka_id=task)
                except Exercises.DoesNotExist:
                    print('There is no record for exercise with ka_id {ka_id}'.format(ka_id=ka_id))
                    continue
                add_missionmap(unit_record,exercise_record,sid)

def add_exercise(ka_id,name,image_url_256,ka_url,title,description):
    fields = {
        'ka_id':ka_id,
        'name':name,
        'image_url_256':image_url_256,
        'ka_url':ka_url,
        'title':title,
        'description':description
    }
    return Exercises.objects.update_or_create(ka_id=ka_id,name=name,defaults=fields)[0]

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

def add_units(name,mission,sequenceid):
    fields = {
        'name':name,
        'mission':mission,
        'sequenceid':sequenceid,
    }
    return Units.objects.update_or_create(
        name=name,
        mission=mission,
        defaults=fields)[0]

def add_mission(name,slug,sequenceid):
    fields = {
        'name':name,
        'slug':slug,
        'sequenceid':sequenceid
    }
    return Missions.objects.update_or_create(
        name=name,
        slug=slug,
        defaults=fields)[0]

def add_missionmap(unit,exercise,sequenceid):
    fields = {
        'unit':unit,
        'exercise':exercise,
        'sequenceid':sequenceid,
    }
    return MissionMap.objects.update_or_create(
        unit=unit,
        exercise=exercise,
        sequenceid=sequenceid,
        defaults=fields)[0]
        

# Start execution here!
if __name__ == '__main__':
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khan_project.settings')
    import django
    django.setup()
    from exercises.models import *
    
    print("Starting population script...")
    populate()
    print("Starting commoncore population...")
    populate_cc()
    print("Starting mission population...")
    populate_missions()
