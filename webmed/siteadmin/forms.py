from django import forms

class LoginForm(forms.Form):
	user_email = forms.EmailField(label='email')
	user_password = forms.CharField(max_length=20, min_length=6)
