from django.db import models
#from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.conf import settings
from datetime import date
# Create your models here.

def uploadLocation(instance, filename):
    #returns a string path for where to save uploaded files. 
    #
    
    loc = "{}/{}".format(instance.id, filename)
    return loc
    
class BPostManager(models.Manager):
    
    def active(self, *args, **kwargs):
        #BPost.objects.all() = super(BPostManager, self).all()
        return super(BPostManager, self).filter(is_draft=False).filter(publish_date__lte=date.today())  
    
    
    
    

class BPost(models.Model):
    #a class for our blog posts.
    title = models.CharField(max_length=120)
    
    #an image: optional field
    image = models.ImageField(upload_to=uploadLocation,
                             null=True, 
                             blank=True, 
                             height_field = 'height_field', 
                             width_field = 'width_field')

    #height & width_field will be auto-populated when image uploaded!
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    
    content = models.TextField() #allows much more chars than CharField
    #field for time of last update --> thats why auto_now=True
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    #field for time post was initially created --> thats why auto_now_add=True
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    #field for the admin user who created theb] blog post. Default = superuser.
    user_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    #boolean var for posts. If true, then we want to hide blog post from public
    is_draft = models.BooleanField(default=False)
    #date that we want blog post to be readable to public. 
    #default means it cant be null or blank.
    publish_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)
    
    objects = BPostManager()
    

    #method that will return a posts title as its representation
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #calls reverse() to reverse lookup.
        #will look at urlpatterns in urls.py, and look up url with name='detail'
        #will find 'detail/(?P<postId>\d+)/$'. It will include url part that leads from project to app
        #Then it takes object's self.id, and places it into (?P<postId>\d+/S).
        #Ex: if the objects id = 14, The string created & returned = 'posts/detail/14' .
        #if multiple apps have url's named "detail", it will cause conflict.
        #fix = give your project --> app url a namespace variable, ex: 'postsApp'.
        #Thats why its 'postsApp:detail' in reverse(). the Url returned is same with/without 'postsApp:''
        aSlug = self.getSlug()        
        absUrl = reverse("postsApp:detail", kwargs={'postId': self.id, 'slug': aSlug})
        return absUrl

    def getSlug(self):
        return slugify(self.title)








#def pre_save_bpost_receiver(sender, instance, *args, **kwargs):
#
#    #function that is called before saving a new BPost object
#    #will try to set slug = title. But if multiple blog posts with same title,
#    #there would be conflict bc slug must be unique.
#    #so ad a number to title to make slug unque. So keep iterating x until
#    #slug = title-x is unique.
#    #can't append 'instance.title - instance.id' because id field is only given to
#    #an object AFTER it is saved(). This is pre save, so no access to any id.
#    aSlug = slugify(instance.title)
#    #ex: 'Tesla item 14' --> 'tesla-item-14'
#    #x = iterator
#    x = 1
#    #if title was already used as slug:
#    alreadyExists = BPost.objects.filter(slug=aSlug).exists()
#    #append -x to title, find value of x that has not been used yet
#    while alreadyExists:
#        newSlug = "{}-{}".format(aSlug, x)
#        alreadyExists = BPost.objects.filter(slug=newSlug).exists()
#        x = x + 1
#    #if slug has not existed:
#    if x == 1:
#        #keep slug = title
#        instance.slug = aSlug
#    else:
#        #otherwise have slug = title - x
#        instance.slug = newSlug
#    
#    
#    
#
##call pre_save_bpost_receiver() to set a unique instance.slug before saving new object
#pre_save.connect(pre_save_bpost_receiver, sender=BPost)











