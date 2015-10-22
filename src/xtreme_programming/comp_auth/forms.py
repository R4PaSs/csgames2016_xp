from django.forms import Form, SlugField


class LoginForm(Form):
    team_token = SlugField()
    competition_token = SlugField()
