from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import DetailView,UpdateView,CreateView,DeleteView
from .models import Task
from .forms import TaskCreatorForm,UpdateTaskStatusForm
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
