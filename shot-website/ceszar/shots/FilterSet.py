import django_filters
from .models import Shot

class ShotFilter(django_filters.FilterSet):
    current = django_filters.NumberFilter()
    current__gt = django_filters.NumberFilter(field_name='current', lookup_expr='gt')
    current__lt = django_filters.NumberFilter(field_name='current', lookup_expr='lt')

    current_time__gt = django_filters.NumberFilter(field_name='current_time', lookup_expr='gt')
    current_time__lt = django_filters.NumberFilter(field_name='current_time', lookup_expr='lt')

    gasConfig__target__gas = django_filters.CharFilter(lookup_expr='icontains')
    gasConfig__inner__gas = django_filters.CharFilter(lookup_expr='icontains')
    gasConfig__outer__gas = django_filters.CharFilter(lookup_expr='icontains')

    time__gt = django_filters.TimeFilter(field_name='time',lookup_expr='gt')
    time__lt = django_filters.TimeFilter(field_name='time',lookup_expr='lt')
    date__gt = django_filters.DateFilter(field_name='date',lookup_expr='gt')
    date__lt = django_filters.DateFilter(field_name='date',lookup_expr='lt')

    xrayDetector__peak_time__gt = django_filters.NumberFilter(field_name='xrayDetector__peak_time',lookup_expr='gt')
    xrayDetector__peak_time__lt = django_filters.NumberFilter(field_name='xrayDetector__peak_time', lookup_expr='lt')

    o = django_filters.OrderingFilter(
            fields=(
                ('num', 'num'),
                ('current', 'current'),
                # and any model field you want to sort based on
            )
        )

    class Meta:
        model = Shot
        fields = ['current','gasConfig','time','date','current_time']
