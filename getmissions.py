from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from datetime import date,timedelta
import os

def get_mission_tasks(mission):
    b = webdriver.PhantomJS()
    b.set_window_size(1120, 550)
    url = 'https://www.khanacademy.org/mission/'+mission
    print(url)
    b.get(url)
    
    with open('credentials','r') as f:
        credentials = f.read().splitlines()
    
    b.find_element_by_name('identifier').send_keys(credentials[0])
    b.find_element_by_name('password').send_keys(credentials[1])
    b.find_element_by_link_text('Sign in').click()
    
    time.sleep(5)

    b.find_element_by_link_text('Show all skills').click()
    
    time.sleep(3)
    
    tasks = b.find_elements_by_class_name('progress-cell')
    
    
    task_ids=[]
    topics = []
    if mission=='math':
        topics=['math']
        for t in tasks:
            d = t.get_attribute('data-reactid').split('$')
            tid = d[3]
            task_ids.append(('math',tid))
    else:
        for t in tasks:
            d = t.get_attribute('data-reactid').split('$')
            tid = d[4]
            sect = d[3].split('.')[0]
            if sect not in topics:
                topics.append(sect)
            task_ids.append((sect,tid))
    
    b.quit()
    task_d = {}
    for t in task_ids:
        if t[0] in list(task_d.keys()):
            task_d[t[0]].append(t[1])
        else:
            task_d[t[0]] = [t[1]]

    return {'topics':topics,'tasks':task_d}
    
def check_cache(mission,expired):
    if not os.path.isfile(mission+'-cache2.json'):
        return False
    if date.today() - date.fromtimestamp(os.stat(mission+'-cache2.json').st_mtime) > timedelta(expired):
        return False
    return True

if __name__ == '__main__':
    from pprint import pprint
    t0 = time.time()
    pprint(get_mission_tasks('trigonometry'))
    print(time.time()-t0)
    

