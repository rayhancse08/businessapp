from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import DetailView,UpdateView,CreateView,DeleteView,ListView,TemplateView
from .models import Task,Announcement,Training,Meeting
from .forms import TaskCreatorForm,UpdateTaskStatusForm,AnnouncementForm,TrainingForm,MeetingForm
from django.urls import reverse_lazy
from employee.models import Employee
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

@method_decorator(login_required,name='dispatch')
class CreateTaskView(CreateView):
    model = Task
    form_class = TaskCreatorForm
    success_url = reverse_lazy('home')
    template_name = 'task/create_task.html'

    def get_form_kwargs(self,**kwargs):
        kwargs=super(CreateTaskView,self).get_form_kwargs(**kwargs)
        kwargs['login_user']=self.request.user
        return kwargs


    def form_valid(self, form):
        user = get_object_or_404(Employee, user=self.request.user)
        #member=form.cleaned_data['buddy']
        #print(member)
        task=form.save(commit=False)
        task.assign_by = user

        task.save()
        return redirect('home')


@method_decorator(login_required,name='dispatch')
class TaskView(TemplateView):
    template_name = 'task/task.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Employee, user=self.request.user)
        context['creating_task']=context['profile'].tasks_assign_by.all()
        context['assigning_task'] = context['profile'].tasks_assign_to.all()
        return context



@method_decorator(login_required,name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'task/task_detail.html'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['login_user']=self.request.user
        return context


@method_decorator(login_required,name='dispatch')
class TaskCreatorEditView(UpdateView):
    model = Task
    form_class = TaskCreatorForm
    pk_url_kwarg = 'task_id'
    template_name = 'task/edit_task.html'
    #success_url = reverse_lazy('home')

    def get_form_kwargs(self,**kwargs):
        kwargs=super(TaskCreatorEditView,self).get_form_kwargs(**kwargs)
        kwargs['login_user']=self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('task_detail',kwargs={'task_id':self.kwargs['task_id']})

@method_decorator(login_required,name='dispatch')
class UpdateTaskStatusView(UpdateView):
    model = Task
    form_class = UpdateTaskStatusForm
    pk_url_kwarg = 'task_id'
    template_name = 'task/edit_task.html'



    def get_success_url(self):
        return reverse_lazy('task_detail',kwargs={'task_id':self.kwargs['task_id']})

@method_decorator(login_required,name='dispatch')
class DeleteTaskView(DeleteView):
    model = Task
    pk_url_kwarg = 'task_id'
    template_name = 'task/delete_task_confirm.html'
    context_object_name = 'task'

    def get_success_url(self):
        return reverse_lazy('task_detail',kwargs={'task_id':self.kwargs['task_id']})


@method_decorator(login_required,name='dispatch')
class CreateAnnouncementView(CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'task/create_announcement.html'



    def get_form_kwargs(self,**kwargs):
        kwargs=super(CreateAnnouncementView,self).get_form_kwargs(**kwargs)
        kwargs['login_user']=self.request.user
        return kwargs

    def form_valid(self, form):
        user = get_object_or_404(Employee, user=self.request.user)
        announcement=form.save(commit=False)
        announcement.announced_by=user
        announcement.save()
        return redirect('announcements')




@method_decorator(login_required,name='dispatch')
class AnnouncementView(TemplateView):
    template_name = 'task/announcements.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Employee, user=self.request.user)
        context['sent_announcements'] = context['profile'].announced_by.all()
        context['received_announcements'] = context['profile'].announced_to.all()
        return context



@method_decorator(login_required,name='dispatch')
class AnnouncementDetailView(DetailView):
    model = Announcement
    context_object_name = 'announcement'
    pk_url_kwarg = 'announcement_id'
    template_name = 'task/announcement_detail.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['login_user']=self.request.user
        return context


@method_decorator(login_required,name='dispatch')
class DeleteAnnouncementView(DeleteView):
    model = Announcement
    template_name = 'task/delete_announcement_confirm.html'
    context_object_name = 'announcement'
    pk_url_kwarg = 'announcement_id'
    success_url = reverse_lazy('announcements')

    def delete(self, request, *args, **kwargs):
        announcement=get_object_or_404(Announcement,pk=self.kwargs['announcement_id'])
        if self.request.user==announcement.announced_by.user:
            return super().delete(request,*args,**kwargs)
        else:
            raise PermissionError("You are not permitted this action")



@method_decorator(login_required,name='dispatch')
class EditAnnouncementView(UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'task/update_announcement.html'
    context_object_name = 'announcement'
    pk_url_kwarg = 'announcement_id'
    success_url = reverse_lazy('announcements')

    def get_form_kwargs(self,**kwargs):
        kwargs=super(EditAnnouncementView,self).get_form_kwargs(**kwargs)
        kwargs['login_user']=self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        announcement = get_object_or_404(Announcement, pk=self.kwargs['announcement_id'])
        if self.request.user == announcement.announced_by.user:
            return super().post(request,*args,**kwargs)
        else:
            raise PermissionError("You are not permitted this action")





@method_decorator(login_required,name='dispatch')
class TrainingView(TemplateView):
    template_name = 'task/trainings.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Employee, user=self.request.user)
        context['training_arrangements'] = context['profile'].schedule_by.all()
        context['training_participates'] = context['profile'].schedule_to.all()
        return context


@method_decorator(login_required,name='dispatch')
class TrainingDetailView(DetailView):
    model = Training
    context_object_name = 'training'
    pk_url_kwarg = 'training_id'
    template_name = 'task/training_detail.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['login_user']=self.request.user
        return context


@method_decorator(login_required,name='dispatch')
class CreateTrainingView(CreateView):
    model = Training
    template_name = 'task/create_training.html'
    form_class =TrainingForm


    def get_form_kwargs(self,**kwargs):
        kwargs=super(CreateTrainingView,self).get_form_kwargs(**kwargs)
        kwargs['login_user']=self.request.user
        return kwargs

    def form_valid(self, form):
        user = get_object_or_404(Employee, user=self.request.user)
        training=form.save(commit=False)
        training.schedule_by=user
        training.save()
        return redirect('trainings')

@method_decorator(login_required,name='dispatch')
class DeleteTrainingView(DeleteView):
    model = Training
    template_name = 'task/delete_training_confirm.html'
    context_object_name = 'training'
    pk_url_kwarg = 'training_id'
    success_url = reverse_lazy('trainings')

    def delete(self, request, *args, **kwargs):
        training=get_object_or_404(Training,pk=self.kwargs['training_id'])
        if self.request.user==training.schedule_by.user:
            return super().delete(request,*args,**kwargs)
        else:
            raise PermissionError("You are not permitted this action")

@method_decorator(login_required,name='dispatch')
class EditTrainingView(UpdateView):
    model = Training
    form_class = TrainingForm
    template_name = 'task/update_training.html'
    context_object_name = 'training'
    pk_url_kwarg = 'training_id'
    #success_url = reverse_lazy('trainings')

    def get_form_kwargs(self,**kwargs):
        kwargs=super(EditTrainingView,self).get_form_kwargs(**kwargs)
        kwargs['login_user']=self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        training = get_object_or_404(Training, pk=self.kwargs['training_id'])
        if self.request.user == training.schedule_by.user:
            return super().post(request,*args,**kwargs)
        else:
            raise PermissionError("You are not permitted this action")

    def get_success_url(self):
        return reverse_lazy('trainings')



@method_decorator(login_required,name='dispatch')
class MeetingView(TemplateView):
    template_name = 'task/meetings.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Employee, user=self.request.user)
        context['meeting_arrangements'] = context['profile'].arranged_by.all()
        context['meeting_participates'] = context['profile'].arranged_for.all()
        return context


@method_decorator(login_required,name='dispatch')
class MeetingDetailView(DetailView):
    model = Meeting
    context_object_name = 'meeting'
    pk_url_kwarg = 'meeting_id'
    template_name = 'task/meeting_detail.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['login_user']=self.request.user
        return context


@method_decorator(login_required,name='dispatch')
class CreateMeetingView(CreateView):
    model = Meeting
    template_name = 'task/create_meeting.html'
    form_class =MeetingForm


    def get_form_kwargs(self,**kwargs):
        kwargs=super(CreateMeetingView,self).get_form_kwargs(**kwargs)
        kwargs['login_user']=self.request.user
        return kwargs

    def form_valid(self, form):
        user = get_object_or_404(Employee, user=self.request.user)
        meeting=form.save(commit=False)
        meeting.arranged_by=user
        meeting.save()
        return redirect('meetings')


@method_decorator(login_required,name='dispatch')
class DeleteMeetingView(DeleteView):
    model = Meeting
    template_name = 'task/delete_meeting_confirm.html'
    context_object_name = 'meeting'
    pk_url_kwarg = 'meeting_id'
    success_url = reverse_lazy('meetings')

    def delete(self, request, *args, **kwargs):
        meeting=get_object_or_404(Meeting,pk=self.kwargs['meeting_id'])
        if self.request.user==meeting.arranged_by.user:
            return super().delete(request,*args,**kwargs)
        else:
            raise PermissionError("You are not permitted this action")



@method_decorator(login_required,name='dispatch')
class EditMeetingView(UpdateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'task/update_meeting.html'
    context_object_name = 'meeting'
    pk_url_kwarg = 'meeting_id'
    success_url = reverse_lazy('meetings')

    def get_form_kwargs(self,**kwargs):
        kwargs=super(EditMeetingView,self).get_form_kwargs(**kwargs)
        kwargs['login_user']=self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        meeting = get_object_or_404(Meeting, pk=self.kwargs['meeting_id'])
        if self.request.user == meeting.arranged_by.user:
            return super().post(request,*args,**kwargs)
        else:
            raise PermissionError("You are not permitted this action")

