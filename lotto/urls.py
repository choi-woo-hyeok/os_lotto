from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auto/', views.auto_lotto, name='auto_lotto'),
    path('manual/', views.manual_lotto, name='manual_lotto'),
    path('draw/', views.draw_lotto, name='draw_lotto'),
    path('winnings/', views.winnings_list, name='winnings_list'),
]

