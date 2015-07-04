from django.conf.urls import patterns, url
from exercises import views

urlpatterns = patterns('',
##        url(r'^about/$',views.about,name='about'),
        url(r'^suggest_exercises/$',views.suggest_exercises,name='suggest_exercises'),
        url(r'matrix_view/$',views.matrix_view,name='matrix_view'),
        url(r'^matrix_view/(?P<mission>[a-zA-Z0-9_.-]+)/$',views.mission,name='mission'),
        url(r'^see_all/$',views.see_all,name='see_all'),
        url(r'^(?P<exercise_name_url>[a-zA-Z0-9_.-]+)/$', views.exercise, name='exercise'),
        
        
##        url(r'^add_category/$',views.add_category,name='add_category'),
##        url(r'^category/(?P<category_name_url>\w+)/add_page/$',views.add_page,name='add_page'),
##        url(r'^register/$',views.register,name='register'),
##        url(r'^login/$',views.user_login,name='login'),
##        url(r'^restricted/$',views.restricted,name='restricted'),
##        url(r'^logout/$',views.user_logout,name='logout'),
##        #url(r'^search/$',views.search,name='search'),
##        url(r'^profile/$',views.profile,name='profile'),
##        url(r'^goto/$',views.track_url,name='track_url'),
##        url(r'^like_category/$',views.like_category,name='like_category'),
##        url(r'^suggest_category/$',views.suggest_category,name='suggest_category'),
##        url(r'^auto_add_page/$',views.auto_add_page,name='auto_add_page'),
)
