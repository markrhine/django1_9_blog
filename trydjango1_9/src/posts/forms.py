

from django import forms
from .models import BPost

class BPostForm(forms.ModelForm):
	class Meta:
		#let form know we are using it to create BPost objects
		model = BPost
		#include BPost fields you want on form. (date modified & timestamp are auto-generates)
		fields = ["title", "content", "image", "is_draft", "publish_date"]
