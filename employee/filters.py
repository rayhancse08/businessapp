from .models import Employee
import django_filters

class EmployeeFilter(django_filters.FilterSet):
    name=django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model=Employee
        fields=['name']