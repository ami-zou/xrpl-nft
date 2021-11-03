from django import forms
from .models import *

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ('title', 'description', 'file')