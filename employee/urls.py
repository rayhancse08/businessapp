from django.urls import path,include
from employee import views

urlpatterns=[
    path('',views.home,name='home'),
    path('profile/',views.HomeView.as_view(),name='profile_home'),
    path('messages/',include('pinax.messages.urls')),
    path('signup/',views.EmployeeSignup.as_view(),name='signup'),
    path('create_profile/',views.EmployeeProfile.as_view(),name='create_profile'),
    path('employees/',views.EmployeeListView.as_view(),name='employee_list'),
    path('profile/groups/',views.GroupListView.as_view(),name='group_list'),
    path('create_group/',views.CreateGroupView.as_view(),name='create_group'),
    path('group/<int:group_id>/',views.GroupDetailView.as_view(),name='group_info'),
    path('group/<int:group_id>/delete',views.GroupDeleteView.as_view(),name='delete_group'),

    path('group/<int:group_id>/delete_member/<int:member_id>/',views.GroupMemberDeleteView.as_view(),name='delete_member'),
    path('group/<int:group_id>/add_member/',views.GroupMemberAddView.as_view(),name='add_member')
]