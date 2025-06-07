from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import StoredFile
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from .forms import EmailForm

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

def file_list(request):
    files = StoredFile.objects.all().order_by('-uploaded_at')
    return render(request, 'list.html', {'files': files})

def replace_file(request, file_id):
    stored_file = get_object_or_404(StoredFile, id=file_id)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, instance=stored_file)
        if form.is_valid():
            # Удаляем старый файл с диска, если пришёл новый
            if 'file' in request.FILES:
                old_file_path = stored_file.file.path
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            form.save()
            return redirect('file_list')
    else:
        form = FileUploadForm(instance=stored_file)

    return render(request, 'replace.html', {'form': form, 'stored_file': stored_file})

def send_report(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
            return redirect('file_list')
    else:
        form = EmailForm()

    return render(request, 'email_form.html', {'form': form})
