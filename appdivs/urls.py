from django.conf.urls import url
from django.urls import path, include
from .views import *

# specify URL Path for rest_framework
urlpatterns = [
    path('api_banco', BancoViewSet.as_view()),
    path('api_divisas', DivisasViewSet.as_view()),
]