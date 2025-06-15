from django.urls import path
from ml_api.views import MLPredictView

urlpatterns = [
    path('predict/', MLPredictView.as_view(), name='ml_predict'),
]
