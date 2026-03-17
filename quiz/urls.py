from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('results/', views.results_view, name='results'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
]
