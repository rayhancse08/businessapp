from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Department(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    designation_choice=(('Head of Department','Head of Department'),
                        ('Manager','Manger'),
                        ('Asst. Manager','Asst. Manager'),
                        ('Executive','Executive'),
                        ('Engineer','Engineer'),
                        ('Sr.Engineer','Sr.Engineer'),
                        ('Lead Engineer','Lead Engineer')
                        )
    name=models.CharField(max_length=100,null=True,default='')
    user=models.OneToOneField(User,on_delete=models.CASCADE,default='',related_name='employee')
    date_of_birth=models.DateField(null=True)
    phone=models.CharField(max_length=100,default='')
    email=models.EmailField(null=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='employees',null=True)
    designation=models.CharField(max_length=20,choices=designation_choice,default="Engineer")

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)                                                                           # synchornize user and profile model
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)
    instance.employee.save()





class Group(models.Model):
    title=models.CharField(max_length=200)
    member=models.ManyToManyField(Employee,related_name='groups_member')
    creator=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='groups',null=True)

    def __str__(self):
        return self.title