from django.core.urlresolvers import reverse_lazy
from django.forms import Form, SlugField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LoginForm(Form):
    team_token = SlugField()
    competition_token = SlugField()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse_lazy('login')
        self.helper.form_method = "POST"
        self.helper.add_input(Submit('submit', 'Login'))
