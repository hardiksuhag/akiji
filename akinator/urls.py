from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('game/', views.fastgame, name='fastgame'),
    path('find/', views.find, name='find'),
    path('submit/', views.submit, name='submit'),
]
