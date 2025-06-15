from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include

from filemanager.views import upload_file, file_list, replace_file, delete_file, send_report, profile, status_view

# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='filemanager API')
from rest_framework.routers import DefaultRouter
from .views import FileViewSet


router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')
router = DefaultRouter()
router.register(r'api/files', FileViewSet, basename='file')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload_file, name='upload_file'),
    path('', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'),
    path('replace/<int:file_id>/', replace_file, name='replace_file'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
    path('send-report/', send_report, name='send_report'),
    # path('docs', schema_view, name='swagger'),
    path('accounts/', include('allauth.urls')),
    path('profile/', profile, name='profile'),
    path('status/', status_view, name='status'),
    path('api/ml/', include('ml_api.urls')),

]

urlpatterns += router.urls





from django.conf import settings
from django.urls import include, path

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
