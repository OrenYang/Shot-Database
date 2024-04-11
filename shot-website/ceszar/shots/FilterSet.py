import django_filters
from .models import Shot

class ShotFilter(django_filters.FilterSet):
    current = django_filters.NumberFilter()
    current__gt = django_filters.NumberFilter(field_name='current', lookup_expr='gt')
    current__lt = django_filters.NumberFilter(field_name='current', lookup_expr='lt')

    gasConfig__target__gas = django_filters.CharFilter(lookup_expr='icontains')
    gasConfig__inner__gas = django_filters.CharFilter(lookup_expr='icontains')
    gasConfig__outer__gas = django_filters.CharFilter(lookup_expr='icontains')

    o = django_filters.OrderingFilter(
            fields=(
                ('num', 'num'),
                ('current', 'current'),
                # and any model field you want to sort based on
            )
        )

    class Meta:
        model = Shot
        fields = ['current','gasConfig',]
