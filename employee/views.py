from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from .models import Employee,Department,Group
from django.views.generic import CreateView,TemplateView,DetailView,View,ListView,DeleteView
from .forms import EmployeeForm,SignupForm,GroupForm,MemberForm
from django.urls import reverse_lazy
from .models import Employee
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('profile_home')
    return render(request,'home.html')


class EmployeeSignup(CreateView):
    form_class = SignupForm
    model = User
    template_name = 'registration/signup_form.html'
    #success_url =reverse_lazy('create_profile')

    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return redirect('create_profile')


@method_decorator(login_required,name='dispatch')
class EmployeeProfile(CreateView):
    form_class = EmployeeForm
    model = Employee
    template_name = 'employee/create_profile.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        profile=get_object_or_404(Employee,user=self.request.user)
        profile.name=form.cleaned_data['name']
        profile.date_of_birth=form.cleaned_data['date_of_birth']
        profile.phone=form.cleaned_data['phone']
        profile.email=form.cleaned_data['email']
        profile.department=form.cleaned_data['department']
        profile.designation=form.cleaned_data['designation']
        profile.save()
        return redirect('home')

@method_decorator(login_required,name='dispatch')
class EmployeeListView(ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'employee/employee_list.html'

    def get_queryset(self):
        return Employee.objects.exclude(user=self.request.user)

@method_decorator(login_required,name='dispatch')
class HomeView(TemplateView):
    template_name = 'employee/profile_home.html'


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['profile']=get_object_or_404(Employee,user=self.request.user)
        context['buddy_list']=Employee.objects.exclude(user=self.request.user)
        context['groups']=context['profile'].groups_member.all()
        context['creating_tasks']=context['profile'].tasks_assign_by.all()
        context['assigning_task']=context['profile'].tasks_assign_to.all()
        context['announcement']=context['profile'].announced_to.order_by('-time')[:2]
        context['trainings']=context['profile'].schedule_to.all()
        context['meetings'] = context['profile'].arranged_for.all()
        return context


@method_decorator(login_required,name='dispatch')
class CreateGroupView(CreateView):
    form_class = GroupForm
    model = Group
    template_name = 'employee/create_group.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self,**kwargs):
        kwargs=super(CreateGroupView,self).get_form_kwargs(**kwargs)
        kwargs['login_user']=self.request.user
        return kwargs


    def form_valid(self, form):
        user = get_object_or_404(Employee, user=self.request.user)
        #member=form.cleaned_data['buddy']
        #print(member)
        group=form.save(commit=False)
        group.creator = user
        group.member.add(user.pk)
        group.save()
        return redirect('home')


@method_decorator(login_required,name='dispatch')
class GroupListView(ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'employee/group_list.html'

    def get_queryset(self):
        return Group.objects.filter(member__user=self.request.user)



@method_decorator(login_required,name='dispatch')
class GroupDetailView(DetailView):
    model = Group
    template_name = 'employee/group_info.html'
    context_object_name = 'group_info'
    pk_url_kwarg = 'group_id'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['login_user']=self.request.user
        return context


@method_decorator(login_required,name='dispatch')
class GroupDeleteView(DeleteView):
    model = Group
    context_object_name = 'group'
    pk_url_kwarg = 'group_id'
    template_name = 'employee/group_delete_confirm.html'
    success_url = reverse_lazy('group_list')





@method_decorator(login_required,name='dispatch')
class GroupMemberDeleteView(View):

    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,pk=self.kwargs['group_id'])

        for item in group.member.all():
           print(item.user)
           print(self.request.user)
           if group.creator.user == self.request.user or self.request.user == item.user :
                group.member.remove(self.kwargs['member_id'])
                return redirect('group_info',group_id = group.pk)

        raise PermissionError("You are not owner on this group")

@method_decorator(login_required,name='dispatch')
class GroupMemberAddView(CreateView):
    form_class = MemberForm
    template_name ='employee/add_member.html'
    model = Group

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['group_id']=self.kwargs['group_id']
        return context

    def get_form_kwargs(self,**kwargs):
        kwargs=super(GroupMemberAddView,self).get_form_kwargs(**kwargs)
        kwargs['group_id']=self.kwargs['group_id']
        return kwargs


    def form_valid(self, form):
        group=get_object_or_404(Group,pk=self.kwargs['group_id'])
        if group.creator.user.username == self.request.user.username:
            for item in form.cleaned_data['buddy']:
                group.member.add(item.pk)
            group.save()
            return redirect('group_info', group_id=group.pk)






