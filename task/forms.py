from django import forms
from .models import Task
from employee.models import Employee

class TaskCreatorForm(forms.ModelForm):
    class Meta:
        model=Task
        exclude=('group_task','assign_by')

    def __init__(self,*args,**kwargs):
        login_user=kwargs.pop('login_user')
        super(TaskCreatorForm,self).__init__(*args,**kwargs)
        self.fields['assign_to'].queryset=Employee.objects.exclude(user=login_user)

class UpdateTaskStatusForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['status']