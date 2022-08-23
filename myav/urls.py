from django.urls import path
from .views import index, WebAV
urlpatterns = [
    path('', index, name="homepage"),
    path('analyze', WebAV.as_view(), name="analyze")
]
