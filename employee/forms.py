from django import forms
from .models import Employee,Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,HttpResponse

class SignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    def clean(self):
        form_data=self.cleaned_data
        if User.objects.filter(username=form_data['username']).exists():
            forms.ValidationError("*** User already exists")

class EmployeeForm(forms.ModelForm):

    class Meta:
        model=Employee
        exclude=('user',)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class GroupForm(forms.ModelForm):

    class Meta:
        model=Group
        fields=['title','member']

    def __init__(self,*args,**kwargs):
        login_user=kwargs.pop('login_user')
        super(GroupForm,self).__init__(*args,**kwargs)
        self.fields['member'].queryset=Employee.objects.exclude(user=login_user)


    def save(self, commit=False):                                      ###override save method

        if commit:
            self.save()
            self.save_m2m()
        return super(GroupForm, self).save(commit=True)

class MemberForm(forms.ModelForm):

    buddy=forms.ModelMultipleChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        )

    class Meta:
        model=Group
        fields=['buddy',]

    def __init__(self,*args,**kwargs):
        group_id=kwargs.pop('group_id')
        super(MemberForm,self).__init__(*args,**kwargs)
        self.fields['buddy'].queryset=Employee.objects.exclude(pk__in=Group.objects.filter(pk=group_id).values('member__id'))


