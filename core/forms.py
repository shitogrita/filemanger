from django import forms
from .models import StoredFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = StoredFile
        fields = ['file', 'description']

class EmailForm(forms.Form):
    recipient = forms.EmailField(label="Кому")
    subject = forms.CharField(label="Тема", max_length=100)
    message = forms.CharField(label="Сообщение", widget=forms.Textarea)
