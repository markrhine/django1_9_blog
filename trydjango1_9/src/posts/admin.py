from django.contrib import admin
#import models
from posts.models import BPost

class BPostModelAdmin(admin.ModelAdmin):
    #will display these BPost fields
    list_display = ["title", "updated", "timestamp", "id", "user_created_by", "is_draft", "publish_date"]
    #will have text be a link for the updated field
    list_display_links = ["updated"]
    #will let admin user edit the title of post by clicking it in list
    list_editable = ["title"]
    #will have filter options for these 2 fields
    list_filter = ["title", "content", "is_draft"]
    #search bar will search these 2 fields for all BPosts
    search_fields = ["title", "content"]
    class Meta:
        Model = BPost
        

# Register your models here. & Model admin. Tie ModelAdmin to its Model.
admin.site.register(BPost, BPostModelAdmin)
