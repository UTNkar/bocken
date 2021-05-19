from django.utils.translation import gettext_lazy as _
from bocken.forms import ReportForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_object_actions import DjangoObjectActions
from django.contrib.admin import ModelAdmin
from bocken.models import Report, JournalEntry
from django.contrib import messages


class ReportAdmin(DjangoObjectActions, ModelAdmin):
    """Custom class for the admin pages for Report."""

    form = ReportForm
    add_form_template = 'admin/add_report_form.html'
    change_form_template = 'admin/change_report_form.html'
    change_list_template = 'admin/report_list.html'

    list_display = ("__str__", "created")
    ordering = ("-created", )

    changelist_actions = ('delete_latest_report', )
    # changelist_actions is added by django-object-actions.
    # https://pypi.org/project/django-object-actions/
    # It adds the button for deleting the latest report. Djangos default
    # actions require that the user selects a number of reports that
    # they want to perform the action on. However, we want to remove the
    # latest report which means that we don't want the user to select any
    # of the reports in the admin view. Therefore we use
    # django-object-actions instead.

    # Also:
    # django-object-actions also has the possibility to add similar buttons
    # to the view where you edit a specific report. You can use
    # change_actions in that case. More about this in the documentation for
    # django-object-actions
    # Ex. change_actions = ('name_of_func', )

    def delete_latest_report(self, request, queryset):
        """Redirect to the delete view for the latest report."""
        report = Report.get_latest_report()
        if not report:
            messages.error(request, _("There are no reports to delete"))
            return

        app_label = self.model._meta.app_label
        model_name = self.model.__name__.lower()

        # This url is a url that is defined in the django admin pages.
        # It is used since it asks if you really want to delete the latest
        # report
        # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls
        delete_url = reverse(
            'admin:{}_{}_delete'.format(
                app_label, model_name
            ),
            args=(report.id,)
        )

        return HttpResponseRedirect(delete_url)
    delete_latest_report.label = _("Delete latest report")
    delete_latest_report.short_description = _("Delete the latest report")
    delete_latest_report.attrs = {'style': 'background:red'}

    def get_actions(self, request):
        """Remove the default deleting action."""
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def add_view(self, request, form_url='', extra_context=None):
        """Django view for overriding the view where you add reports."""
        extra_context = extra_context or {}

        first, last, entries = Report.get_new_report_details()

        extra_context['no_entries'] = not JournalEntry.entries_exists()
        extra_context['entries'] = entries
        extra_context['first'] = first
        extra_context['last'] = last

        return super(ReportAdmin, self).add_view(
            request, form_url='', extra_context=extra_context
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Django view for overriding the editing view for reports.

        This is where the statistics is shown for a report.
        """
        extra_context = extra_context or {}

        report = Report.objects.get(pk=object_id)
        extra_context['statistics_for_groups'] = \
            report.get_statistics_for_groups()

        return super(ReportAdmin, self).change_view(
            request, object_id, form_url='', extra_context=extra_context
        )

    def changelist_view(self, request, extra_context=None):
        """Django view for the view that lists all reports."""
        extra_context = extra_context or {}
        extra_context['new_journal_entries'] = \
            JournalEntry.get_entries_since_last_report_amount()

        return super(ReportAdmin, self).changelist_view(
            request, extra_context=extra_context
        )
