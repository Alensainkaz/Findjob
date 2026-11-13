from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register_view'),
    path('verify/', views.verify_code, name='verify_code'),
    path('verify/resend/', views.resend_code, name='resend_code'),
    path('api/check-availability/', views.check_availability, name='check_availability'),
]
