from django import forms
from django.core.urlresolvers import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Submission


class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = ['challenge', 'time', 'file', 'comment', 'team']
        exclude = ('challenge', 'time', 'team')
        help_texts = {
            "file": "*.zip",
        }
        labels = {
            "comment": "README"
        }

    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args)
        self.helper = FormHelper()
        if 'cid' in kwargs.keys():
            self.helper.form_action = reverse_lazy('submit',
                                                   args=[kwargs['cid']])
        self.helper.form_method = "POST"
        self.helper.form_id = "submission_form"
        self.helper.add_input(Submit('submit', 'Submit'))
