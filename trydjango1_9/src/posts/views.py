from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import BPostForm
from posts.models import BPost
from datetime import date
from django.db.models import Q

# Create your views here.
#we want to do CRUD

#def bposts_create(request):
	#METHOD 1: one way you can create new object & save it.
	#just take in POST values from client & create a BPost object with the data
	#Requires custom validation ourself. Not recommended!

	# if request.method == "POST":
	# 	aTitle = request.POST.get("title")
	# 	aContent = request.POST.get("content")
	# 	BPost.objects.create(title=aTitle, content= aContent)
	# aForm = BPostForm()
	# context = {'bpostForm': aForm}
	# return render(request, "posts/bpost_form.html", context)

def bposts_create(request):
    #METHOD 2: the recommended way: use django forms, they have auto-validation.
    #if request is not sent by an admin staff:
    if not request.user.is_staff or not request.user.is_superuser:
        #throw 404  message to user. Don't let them add a post.
        raise Http404
    #if client is submitting a filled out form:
    if request.method == "POST":
        #create BPostForm with POST values that user entered in, including any uploaded image FILE.
        #User may not upload img, so accept None too.
        aForm = BPostForm(request.POST, request.FILES or None)
        #django will use its special form methods to validate data, if validated:
        if aForm.is_valid():
            #could get validated data if wanted:  title = aForm.cleaned_data.get("title")
            #turn form into a BPost instance. don't save it yet(commit=False)
            instance = aForm.save(commit=False)
            #do extra validation beyond django's auto-validation, if wish
            #save object to database
            instance.save()
            #redirect client to the new blog post's detailed page
            return HttpResponseRedirect(instance.get_absolute_url())
    #if client is requesting blank form, GET
    else:
        #form will have empty values
        aForm = BPostForm()
    #aForm will be empty if GET, but will have user input still filled in
    #if form was invalid.
    context = {'bpostForm': aForm}
    #render the form
    return render(request, "posts/bpost_form.html", context)


def bposts_detail(request, postId=None, slug=None):   #read/retreive
    #postId = Sent in from url reg expression named group ?P<postId>\d+
    #if no BPost object found with given id, returns 404 message to user
    aPostInstance = get_object_or_404(BPost, id=postId)
    #redirect user to proper detail url: will call bposts_detail again, but with right slug
    if slug != aPostInstance.getSlug():
        return HttpResponseRedirect(aPostInstance.get_absolute_url())

    #Hide the blog post from user, if hes not admin & the blogpost is still
    #a draft, or before its publish date.
    #if request is not sent by an admin staff:
    if not request.user.is_staff or not request.user.is_superuser:
        if aPostInstance.is_draft or aPostInstance.publish_date > date.today():
            #throw 404  message to user. Don't let them add a post.
            raise Http404
    
    #otherwise, show it:
    context = {'postInstance': aPostInstance}
    return render(request, "posts/bpost_detail.html", context)


def bposts_list(request):	#read/retrieve

    #this view implements a bootstrap paginator -> see django (not a typo) documentation 
    #copied from django docs. Made minor changes, especially var names
    #queryset_list = list of  BPost objects in database that we want users to see
    #if public user, only show them blog posts that are not drafts and published
    #we made custom model Manager, in models.py, contains active().
    queryset_list = BPost.objects.active().order_by('-updated')
    #if request is from an admin, show listing of all blog posts, even drafts & future publishes
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = BPost.objects.all().order_by('-updated')

    today = date.today()    #to be used in template
    
    #pull in search box parameter from listing page
    clientQuery = request.GET.get('q')
    #if user made a search:
    if clientQuery:
        #retreive only blog posts that find a match on title OR content
        #case insensitive
        queryset_list = queryset_list.filter(
            Q(title__icontains=clientQuery) | Q(content__icontains=clientQuery)
        
        )
    
    
    paginator = Paginator(queryset_list, 10) # Show 10 blog posts per page

    page_request_var = 'pageNum'     #can be any string you wish, put it in a var so its dynamic
    page = request.GET.get(page_request_var)
    
    #queryset = list of BPost objects that fit in one page
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
 
    context = {'title': 'Blog Listing', 'object_list': queryset,
               'page_request_var': page_request_var, 'today':today,
               'qCache': clientQuery}
    return render(request, "posts/index.html", context)
 
 
 
 

 


def bposts_update(request, postId=None):
    #if request is not sent by an admin staff:
    if not request.user.is_staff or not request.user.is_superuser:
        #throw 404  message to user. Don't let them edit a post.
        raise Http404
    #postId = Sent in from url reg expression named group ?P<postId>\d+
    #if no BPost object found with given id, returns 404 message to user
    aPostInstance = get_object_or_404(BPost, id=postId)
    #render form for user to enter new info. Since we're updating an existing object,
    #we will pass in the object instance as a parameter to BPostForm, so django
    #knows we are using form to edit this instance. Will also display old values
    #in display.:
    #if client is submitting a filled out form:
    if request.method == "POST":
        #create BPostForm that will edit an EXISTING object (blog post). 
        #will take in user's new POST values, including an uploaded image FILE, save it to a BPostForm.
        #Need to pass in an instance that you are editing. 
        aForm = BPostForm(request.POST, request.FILES or None, instance=aPostInstance)
        #user will have entered in new data in form
        #django will use its special form methods to validate data, if validated:
        if aForm.is_valid():
            #could get validated data if wanted:  title = aForm.cleaned_data.get("title")
            #save the revised BPost instance, call object whatever you like
            instance = aForm.save(commit=False)
            instance.save()
            messages.success(request, "Changes were successfully saved")
            #send user to the instance (blog post's) detail page.
            return HttpResponseRedirect(instance.get_absolute_url())


    #if client is requesting the form, via GET method
    else:
        #give client a form that will have the objecr's old values already filled in
        #not necessary, but nice thing for client to see.
        aForm = BPostForm(instance=aPostInstance)
    context = {'bpostForm': aForm}
    return render(request, "posts/bpost_form.html", context)


def bposts_delete(request, postId=None):
    #if request is not sent by an admin staff:
    if not request.user.is_staff or not request.user.is_superuser:
        #throw 404  message to user. Don't let them delete a post.
        raise Http404
    #postId = Sent in from url reg expression named group ?P<postId>\d+
    #if no BPost object found with given id, returns 404 message to user
    aPostInstance = get_object_or_404(BPost, id=postId)
    #delete the object (blog post) from database
    aPostInstance.delete()
    #create a message variable that will be sent to template
    messages.success(request, "Blog post was deleted successfully")
    #send client to url in urls.py with name="listing"
    return redirect("postsApp:listing")
