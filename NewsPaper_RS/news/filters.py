from django_filters import FilterSet, ModelChoiceFilter, DateFilter, DateRangeFilter
from .models import Post, Category
from django import forms


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='все категории',
    )

    date = DateFilter(
        field_name='post_date_time',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата',
        lookup_expr='date__gte',
    )

    date_range = DateRangeFilter(
        field_name='post_date_time',
        label='За период',
        empty_label='за весь период',
    )

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'author': ['exact'],
            'post_date_time': ['gt'],
            # 'postcategory__category': ['exact'],
        }
