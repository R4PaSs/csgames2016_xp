from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Submission


class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = ['challenge', 'time', 'file', 'comment', 'team']

    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "/submit"
        self.helper.form_method = "POST"

        self.helper.add_input(Submit('submit', 'Submit'))
