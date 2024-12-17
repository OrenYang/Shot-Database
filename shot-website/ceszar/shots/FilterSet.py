import django_filters
from .models import Shot

class ShotFilter(django_filters.FilterSet):
    current = django_filters.NumberFilter()
    current__gt = django_filters.NumberFilter(field_name='current', lookup_expr='gt')
    current__lt = django_filters.NumberFilter(field_name='current', lookup_expr='lt')

    current_time__gt = django_filters.NumberFilter(field_name='current_time', lookup_expr='gt')
    current_time__lt = django_filters.NumberFilter(field_name='current_time', lookup_expr='lt')

    num = django_filters.NumberFilter()
    num__gt = django_filters.NumberFilter(field_name='num', lookup_expr='gt')
    num__lt = django_filters.NumberFilter(field_name='num', lookup_expr='lt')

    gasConfig__target__gas = django_filters.CharFilter(lookup_expr='icontains')
    gasConfig__inner__gas = django_filters.CharFilter(lookup_expr='icontains')
    gasConfig__outer__gas = django_filters.CharFilter(lookup_expr='icontains')

    target_press = django_filters.NumberFilter()
    target_press__gt = django_filters.NumberFilter(field_name='target_press', lookup_expr='gt')
    target_press__lt = django_filters.NumberFilter(field_name='target_press', lookup_expr='lt')

    inner_press = django_filters.NumberFilter()
    inner_press__gt = django_filters.NumberFilter(field_name='inner_press', lookup_expr='gt')
    inner_press__lt = django_filters.NumberFilter(field_name='inner_press', lookup_expr='lt')

    outer_press = django_filters.NumberFilter()
    outer_press__gt = django_filters.NumberFilter(field_name='outer_press', lookup_expr='gt')
    outer_press__lt = django_filters.NumberFilter(field_name='outer_press', lookup_expr='lt')

    target_timing = django_filters.NumberFilter()
    target_timing__gt = django_filters.NumberFilter(field_name='target_timing', lookup_expr='gt')
    target_timing__lt = django_filters.NumberFilter(field_name='target_timing', lookup_expr='lt')

    inner_timing = django_filters.NumberFilter()
    inner_timing__gt = django_filters.NumberFilter(field_name='inner_timing', lookup_expr='gt')
    inner_timing__lt = django_filters.NumberFilter(field_name='inner_timing', lookup_expr='lt')

    outer_timing = django_filters.NumberFilter()
    outer_timing__gt = django_filters.NumberFilter(field_name='outer_timing', lookup_expr='gt')
    outer_timing__lt = django_filters.NumberFilter(field_name='outer_timing', lookup_expr='lt')

    postNotes = django_filters.CharFilter(lookup_expr='icontains')
    preNotes = django_filters.CharFilter(lookup_expr='icontains')

    time__gt = django_filters.TimeFilter(field_name='time',lookup_expr='gt')
    time__lt = django_filters.TimeFilter(field_name='time',lookup_expr='lt')
    date__gt = django_filters.DateFilter(field_name='date',lookup_expr='gt')
    date__lt = django_filters.DateFilter(field_name='date',lookup_expr='lt')

    xrayDetector__peak_time__gt = django_filters.NumberFilter(field_name='xrayDetector__peak_time',lookup_expr='gt')
    xrayDetector__peak_time__lt = django_filters.NumberFilter(field_name='xrayDetector__peak_time', lookup_expr='lt')

    xuvImage__frame1__gt = django_filters.NumberFilter(field_name='xuvImage__frame1',lookup_expr='gt')
    xuvImage__frame1__lt = django_filters.NumberFilter(field_name='xuvImage__frame1', lookup_expr='lt')

    o = django_filters.OrderingFilter(
            fields=(
                ('num', 'num'),
                ('current', 'current'),
                # and any model field you want to sort based on
            ),
        )

    class Meta:
        model = Shot
        fields = ['num','current','gasConfig','time','date','current_time', 'preNotes', 'postNotes']
