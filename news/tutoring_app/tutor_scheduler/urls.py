from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ta/<int:ta_id>/', views.ta_detail, name='ta_detail'),
    path('signup/', views.ta_signup, name='ta_signup'),
    path('login/', views.ta_login, name='ta_login'),
    path('logout/', views.ta_logout, name='ta_logout'),
    path('dashboard/', views.ta_dashboard, name='ta_dashboard'),
    path('add-hour/', views.add_tutoring_hour, name='add_tutoring_hour'),
    path('edit-hour/<int:hour_id>/', views.edit_tutoring_hour, name='edit_tutoring_hour'),
    path('delete-hour/<int:hour_id>/', views.delete_tutoring_hour, name='delete_tutoring_hour'),
]
