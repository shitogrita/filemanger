from django.db.models.aggregates import Sum
from django.shortcuts import render, redirect
from core.forms import FileUploadForm
from core.models import StoredFile
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from core.forms import EmailForm

from django.shortcuts import render, redirect
from core.forms import FileUploadForm
from core.models import StoredFile
from django.conf import settings
import os
import glob

from django.shortcuts import render, redirect
from core.models import StoredFile
from core.forms import FileUploadForm
from django.conf import settings
from rest_framework.routers import DefaultRouter

from django.contrib.auth.decorators import login_required

import os

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            description = form.cleaned_data.get('description', '').strip()
            original_extension = os.path.splitext(uploaded_file.name)[1]

            if description:
                safe_name = "".join(c for c in description if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = safe_name + original_extension
            else:
                filename = uploaded_file.name

            upload_path = os.path.join('uploads', filename)
            full_path = os.path.join(settings.MEDIA_ROOT, upload_path)

            with open(full_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            StoredFile.objects.create(
                file=upload_path,
                description=description or os.path.splitext(filename)[0],
                user=request.user
            )

            return redirect('file_list')
    else:
        form = FileUploadForm()

    return render(request, 'upload.html', {'form': form})

@login_required
def file_list(request):
    files = StoredFile.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'list.html', {'files': files})


def replace_file(request, file_id):
    stored_file = get_object_or_404(StoredFile, id=file_id)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, instance=stored_file)
        if form.is_valid():
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

            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
            except Exception as e:
                actions_logger.error(f"Email sending error: {e}")
            return redirect('file_list')
    else:
        form = EmailForm()

    return render(request, 'email_form.html', {'form': form})


def delete_file(request, file_id: int):
    if request.method == 'GET':
        file_obj = get_object_or_404(StoredFile, pk=file_id)
        try:
            os.remove(file_obj.file.path)
        except:
            print("file is already deleted")
            StoredFile.objects.filter(id=file_id).delete()
            return redirect('file_list')
        file_obj.delete()
    return redirect('file_list')

@login_required
def profile(request):
    qs = StoredFile.objects.filter(user=request.user)
    context = {
        'count': qs.count(),
        'last': qs.order_by('-uploaded_at').first(),
    }
    return render(request, 'profile.html', context)


from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from core.models import StoredFile
from filemanager.serializer import FileSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = StoredFile.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


import logging

actions_logger = logging.getLogger('file_actions')

def delete_file_view(request, file_id):
    if request.method == 'GET':
        file_obj = get_object_or_404(StoredFile, pk=file_id)
        try:
            os.remove(file_obj.file.path)
        except:
            print("file is already deleted")
            StoredFile.objects.filter(id=file_id).delete()
            return redirect('file_list')
        file_obj.delete()
    actions_logger.info(f"User {request.user} deleted file {file_id}")

    return redirect('file_list')

from django.core.mail import send_mail
from django.core.mail import BadHeaderError



def replace_file_view(request, file_id):
    stored_file = get_object_or_404(StoredFile, id=file_id)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, instance=stored_file)
        if form.is_valid():
            if 'file' in request.FILES:
                old_file_path = stored_file.file.path
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            form.save()
            return redirect('file_list')
    else:
        form = FileUploadForm(instance=stored_file)

    actions_logger.info(f"User {request.user} replaced file {file_id}")
    return render(request, 'replace.html', {'form': form, 'stored_file': stored_file})


from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import get_connection
from django.db.models import Sum
from core.models import StoredFile

def status_view(request):
    user_count = User.objects.count()

    total_size = 0
    files = StoredFile.objects.all()
    for f in files:
        try:
            total_size += f.file.size
        except Exception:
            pass

    email_status = 'OK'
    try:
        connection = get_connection()
        connection.open()
        connection.close()
    except Exception as e:
        email_status = f'Error: {str(e)}'

    context = {
        'user_count': user_count,
        'total_files_size_bytes': total_size,
        'email_service_status': email_status,
    }
    return render(request, 'status.html', context)
