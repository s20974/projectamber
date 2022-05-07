from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from django.template.loader import render_to_string

from django.views.generic import *

from django.urls import reverse

from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db import transaction
from django.db.models.query_utils import Q

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.core.exceptions import FieldError

from django.conf import settings

from django.core.mail import EmailMessage

from django import forms
import requests

from .models import *

from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse

import re
import json

#tasks
from botapp.tasks import *

from botapp.models import Action, Task

from .forms import *

def home(request):
	return render(request, 'home.html', {})








########################
#    	 ACCOUNT       #
########################


@login_required(login_url='/sign-in/')
def account(request):
	tasks = Task.objects.all()
	return render(request, 'account/body/account-page.html', {'tasks':tasks})


@login_required(login_url='/sign-in/')
def settings(request):
	return render(request, 'account/settings/settings.html')


@login_required(login_url='/sign-in/')
def actions(request):
	Actions = Action.objects.all()
	return render(request, 'account/actions.html', {'actions': Actions})

@login_required(login_url='/sign-in/')
@transaction.atomic
def update_profile(request):
	if request.method == 'POST':
		user_form = ChangeUserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, ('Your profile was successfully updated!'))
			return redirect('account')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		user_form = ChangeUserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
	return render(request, 'account/settings/change-userinfo.html', {
	'user_form': user_form,
	'profile_form': profile_form
	})



