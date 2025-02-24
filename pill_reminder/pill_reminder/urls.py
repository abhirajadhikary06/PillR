from django.urls import path
from reminder.views import dashboard, register, login, logout, set_reminder, share_prescription, view_prescription

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('set_reminder/', set_reminder, name='set_reminder'),
    path('share/<int:prescription_id>/', share_prescription, name='share_prescription'),
    path('view-prescription/<int:prescription_id>/', view_prescription, name='view_prescription'),
]