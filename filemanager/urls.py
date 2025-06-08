from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from filemanager.views import upload_file, file_list, replace_file, delete_file, send_report
# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='filemanager API')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'),
    path('replace/<int:file_id>/', replace_file, name='replace_file'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
    path('send-report/', send_report, name='send_report'),
    # path('docs', schema_view, name='swagger'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

