from django.shortcuts import render

from .forms import LoginForm


def index(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
	return render(request, 'siteadmin/index.html', {
			'loginform': LoginForm()
		})
