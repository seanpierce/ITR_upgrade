import datetime
from django.contrib import admin
from django.utils.encoding import force_str


class ShowFilter(admin.SimpleListFilter):
    title = 'Upcoming'
    parameter_name = 'upcoming'
    default_value= 'Upcoming'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Upcoming', 'Upcoming'),
            ('Past', 'Past'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        # Compare the requested value (either 'Upcoming' or 'Past')
        # to decide how to filter the queryset.

        if self.value() == None:
            self.used_parameters[self.parameter_name] = 'Upcoming'

        if self.value() == 'Upcoming':
            return queryset.filter(
                date__gte = datetime.date.today()
            )

        if self.value() == 'Past':
            return queryset.filter(
                date__lte = datetime.date.today()
            ).order_by('-date', '-end_date_time')

    def choices(self, changelist):
        """
        Override to remove the 'All' option for this filter.
        """

        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string({}, [self.parameter_name]),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}, []),
                'display': title,
            }