from django.urls import path
from task import views
urlpatterns=[
    path('',views.TaskView.as_view(),name='tasks'),
    path('create/',views.CreateTaskView.as_view(),name='create_task'),
    path('<int:task_id>/',views.TaskDetailView.as_view(),name='task_detail'),
    path('<int:task_id>/edit/',views.TaskCreatorEditView.as_view(),name='edit_task'),
    path('<int:task_id>/edit_status/',views.UpdateTaskStatusView.as_view(),name='update_task_status'),
    path('<int:task_id>/delete/',views.DeleteTaskView.as_view(),name='delete_task'),
    path('announcements/',views.AnnouncementView.as_view(),name='announcements'),
    path('announcements/create/',views.CreateAnnouncementView.as_view(),name='create_announcement'),
    path('announcements/<int:announcement_id>/delete/',views.DeleteAnnouncementView.as_view(),name='delete_announcement'),
    path('announcements/<int:announcement_id>/edit/',views.EditAnnouncementView.as_view(),name='update_announcement'),
    path('trainings/',views.TrainingView.as_view(),name='trainings'),
    path('trainings/create/',views.CreateTrainingView.as_view(),name='create_training'),
    path('trainings/<int:training_id>/delete/',views.DeleteTrainingView.as_view(),name='delete_training'),
    path('trainings/<int:training_id>/edit/',views.EditTrainingView.as_view(),name='update_training'),
    path('meetings/',views.MeetingView.as_view(),name='meetings'),
    path('meetings/create/',views.CreateMeetingView.as_view(),name='create_meeting'),
    path('meetings/<int:meeting_id>/delete/',views.DeleteMeetingView.as_view(),name='delete_meeting'),
    path('meetings/<int:meeting_id>/edit/',views.EditMeetingView.as_view(),name='update_meeting'),






]