

from django.conf.urls import url

from django.contrib import admin
#from current directory (posts) import 'views' file
from . import views


urlpatterns = [

	#when url finds first matching pattern. It will send a HttpRequest object into
	#the view function to be called and calls it. Any groups, denoted by () in reg exp,
	#will be passed into function call as arguments. If group is not named, they're passed
	#in as positional args. If group is named, they're passed in as keyword args.
	url(r'^$', views.bposts_list, name="listing"),
	url(r'^create/$', views.bposts_create),
	#using reg exp 'named groups'. Will capture text b/w the (), will save text in a variable called "postId".
	#then it will send it as an argument parameter into bposts_detail function call.
	url(r'^detail/(?P<postId>\d+)/(?:(?P<slug>[\w-]+)/)?$', views.bposts_detail, name='detail'),
	url(r'^update/(?P<postId>\d+)/$', views.bposts_update, name='update'),
	url(r'^delete/(?P<postId>\d+)/$', views.bposts_delete),

]
