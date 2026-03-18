from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_resume/', views.create_resume, name='create_resume'),
    path('create_resume_category/', views.create_resume_category, name='create_resume_category'),
    path('resume_detail/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('edit_resume/<int:pk>/', views.edit_resume, name='edit_resume'),
    path('delete_resume/<int:pk>/', views.delete_resume, name='delete_resume'),
]
