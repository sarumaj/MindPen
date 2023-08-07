import django_filters
from .models import Journal

class JournalFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Journal
        fields = ["search", "journal_date"]
