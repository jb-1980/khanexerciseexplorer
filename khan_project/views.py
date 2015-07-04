from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404 
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from exercises.models import Exercises

def get_exercise_list(max_results=0,starts_with='',see_all=False):
    exercise_list = []
    if starts_with:
        exercise_list = Exercises.objects.filter(name__istartswith=starts_with).order_by('-views')[:10]
    else:
        if see_all:
            exercise_list = Exercises.objects.order_by('title')
        else:
            exercise_list = Exercises.objects.order_by('-views')[:10]
    
    if max_results > 0:
        if len(exercise_list) > max_results:
            exercise_list = exercise_list[:max_results]    
    return exercise_list

def home(request):
    exercises = get_exercise_list()
    template_name = 'exercises/index.html'
    context_dict = {'skill_view':True,'exercise_list':exercises}
    
    print('home was activated')
    return render(request,template_name,context_dict)

    
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

def user_login(request):
       
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return render(request,'tlc_project/login.html',{'disabled_account':True,})
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return render(request,'tlc_project/login.html',{'bad_details':True,})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request,'tlc_project/login.html', {})   
