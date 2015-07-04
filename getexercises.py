import io


import os
import json
from datetime import date,timedelta
from urllib.request import urlopen

def fetch_exercises():
    exercises_url = 'http://www.khanacademy.org/api/v1/exercises'
    response = json.loads(urlopen(exercises_url).read().decode('utf-8'))
    exer = {}
    for e in response:
        videos = []
        if e['curated_related_videos']:
          v = json.loads(urlopen('http://www.khanacademy.org/api/v1/exercises/'+e['name'].replace(' ','%20')+'/videos').read().decode('utf-8'))
          for vid in v:
              videos.append({
                  'videoid':vid['id'],
                  'title':vid['title'],
                  'description':vid['description_html'],
                  'url':vid['ka_url'],
              })
        exer[e['name']]={
            'ka_id':e['id'],
            'name':e['name'],
            'image_url_256':e['image_url_256'],
            'ka_url':e['ka_url'],
            'prerequisites':e['prerequisites'],
            'related_videos':videos,
            'title':e['title'],
            'description_html':e['description_html']
        }
    
    return exer


def get_exercises(cachedir,expired=7):
    if not os.path.isfile(cachedir):
        print('creating skill cache')
        exer = fetch_exercises()
        with open(cachedir,'w') as f:
            f.write(json.dumps(exer))
    elif date.today() - date.fromtimestamp(os.stat(cachedir).st_mtime) > timedelta(expired):
        print('updating skill cache')
        exer = fetch_exercises()
        with open(cachedir,'w') as f:
            f.write(json.dumps(exer))
    else:
        print('getting skill cache')
        with open(cachedir,'r') as f:
            exer = json.loads(f.read())

    return exer

if __name__ == '__main__':
    exercises = getExercises()
    for exercise in exercises:
        print (exercise)
        print (exercise['title'])

