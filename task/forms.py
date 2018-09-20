from django import forms
from .models import Task,Announcement,Training,Meeting
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

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model=Announcement
        fields=['title','description','announced_to']

    def __init__(self,*args,**kwargs):
        login_user=kwargs.pop('login_user')
        super(AnnouncementForm,self).__init__(*args,**kwargs)
        self.fields['announced_to'].queryset=Employee.objects.exclude(user=login_user)



class TrainingForm(forms.ModelForm):
    class Meta:
        model=Training
        fields=['title','topic','schedule_to','schedule_time']
        widgets = {
            'schedule_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'topic': forms.Textarea(attrs={'rows':5,'placeholder':'Training Topic'})
        }

    def __init__(self, *args, **kwargs):
        login_user = kwargs.pop('login_user')
        super(TrainingForm,self).__init__(*args, **kwargs)
        self.fields['schedule_to'].queryset = Employee.objects.exclude(user=login_user)


class MeetingForm(forms.ModelForm):

    class Meta:
        model=Meeting
        fields=['title','description','arranged_for','meeting_time']
        widgets = {
            'meeting_time': forms.DateTimeInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows':5,'placeholder':'Meeting Topic'})
        }

    def __init__(self, *args, **kwargs):
        login_user = kwargs.pop('login_user')
        super(MeetingForm,self).__init__(*args, **kwargs)
        self.fields['arranged_for'].queryset = Employee.objects.exclude(user=login_user)

