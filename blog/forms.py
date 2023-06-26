from django import forms
from .models import FilesAdmin

class EmailForm(forms.Form):
    recipient_email = forms.EmailField(label='Recipient Email')


class UploadForm(forms.ModelForm):
    
    class Meta:
        model= FilesAdmin
        fields = ('title','description','adminupload',)