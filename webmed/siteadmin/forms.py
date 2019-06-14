from django import forms

class LoginForm(forms.Form):
	user_name = forms.CharField(min_length=6, max_length=20)
	user_password = forms.CharField(min_length=6, max_length=20)
