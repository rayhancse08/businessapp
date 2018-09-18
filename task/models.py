from django.db import models
from employee.models import Employee,Group

# Create your models here.

class Task(models.Model):
    status_choice=(('Initial','Initial'),
                   ('Half Done','Half Done'),
                   ('Done','Done'))
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=2000,null=True)
    assign_by=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='tasks_assign_by')
    assign_to=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='tasks_assign_to')
    assign_time=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,choices=status_choice,default='Initial')
    complete_time=models.DateField()
    group_task=models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    title=models.CharField(max_length=100)
    description = models.TextField(max_length=2000, null=True)
    announced_by=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='announced_by')
    announced_to=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='announced_to')
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



