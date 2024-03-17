from django.urls import path
from . import views  


urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users_page, name='users_page'),
    path('users-details/<int:pk>', views.user_details_page, name='user_details_page'),
    path('update-user/<int:pk>', views.update_user, name='update_user'),
    path('delete_user/<int:pk>', views.delete_user, name='delete_user'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('meeting_home/', views.meeting_home, name='meeting_home'),
    path('meeting-details/<int:pk>', views.meeting_details, name='meeting_details'),
    path('upcoming-meetings/', views.upcoming_meetings, name='upcoming_meetings'),
    path('past-meetings/', views.past_meetings, name='past_meetings'),
    path('create_meeting/', views.schedule_meeting, name='create_meeting'),
    path('delete_meeting/<int:pk>', views.delete_meeting, name='delete_meeting'),
    path('create_user/', views.create_user, name='create_user'),
    path('zoom/callback/', views.zoom_callback, name='zoom-callback'),
]