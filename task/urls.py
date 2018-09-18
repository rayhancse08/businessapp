from django.urls import path
from task import views
urlpatterns=[
    path('create/',views.CreateTaskView.as_view(),name='create_task'),
    path('<int:task_id>/',views.TaskDetailView.as_view(),name='task_detail'),
    path('<int:task_id>/edit/',views.TaskCreatorEditView.as_view(),name='edit_task'),
    path('<int:task_id>/edit_status/',views.UpdateTaskStatusView.as_view(),name='update_task_status'),
    path('<int:task_id>/delete/',views.DeleteTaskView.as_view(),name='delete_task'),


]