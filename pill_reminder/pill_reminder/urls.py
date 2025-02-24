from django.urls import path
from reminder import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('set_reminder/', views.set_reminder, name='set_reminder'),
    path('share/<int:prescription_id>/', views.share_prescription, name='share_prescription'),
    path('view-prescription/<int:prescription_id>/', views.view_prescription, name='view_prescription'),
    path('login/', views.login, name='login'),  # Serve the login page
    path('register/', views.register, name='register'),  # Serve the register page
]