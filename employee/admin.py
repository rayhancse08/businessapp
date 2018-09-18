from django.contrib import admin
from .models import Employee,Department,Group
# Register your models here.

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Group)
