from django import forms
from .models import Profile

class AvatarUploadForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ["avatar"]

	avatar = forms.ImageField()
