from django import forms
from django.utils.translation import gettext_lazy as _

from django_select2.forms import ModelSelect2MultipleWidget
from material import Fieldset, Layout

from aleksis.core.forms import AnnouncementForm

from .models import AutomaticPlan, LessonSubstitution


class LessonSubstitutionForm(forms.ModelForm):
    """Form to manage substitutions."""

    class Meta:
        model = LessonSubstitution
        fields = ["week", "lesson_period", "subject", "teachers", "room", "cancelled"]
        widgets = {
            "teachers": ModelSelect2MultipleWidget(
                search_fields=[
                    "first_name__icontains",
                    "last_name__icontains",
                    "short_name__icontains",
                ]
            )
        }


AnnouncementForm.add_node_to_layout(Fieldset(_("Options for timetables"), "show_in_timetables"))


class AutomaticPlanForm(forms.ModelForm):
    layout = Layout("slug", "name", "number_of_days", "show_header_box")

    class Meta:
        model = AutomaticPlan
        fields = ["slug", "name", "number_of_days", "show_header_box"]
