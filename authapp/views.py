from django.shortcuts import render, HttpResponseRedirect, redirect

from django.http import HttpResponse

from django.template.loader import render_to_string

from django.views.generic import *

from .forms import *

from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth import authenticate, login

from django.contrib import messages

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_activation_token

from django.core.mail import EmailMessage

from .models import User
from .apis import send_verfication_code, verify_sent_code

from django.views.decorators.csrf import csrf_exempt

import re
import json

# Create your views here.

@csrf_exempt
def user_login(request):
	login_form = LoginForm(request.POST or None)
	errors = {}
	if request.method == 'POST':
		if login_form.is_valid():
			password = request.POST.get('password')
			phone_or_email = request.POST.get('phone_or_email')
			user = authenticate(phone_or_email=phone_or_email, password=password)
			if user is not None:
				login(request, user, backend='django.contrib.auth.backends.ModelBackend')
				messages.success(request, f"You are now logged in as {user.first_name} {user.last_name}")
				return redirect('account')
			else:
				errors['Invalid data.'] = 'Invalid data.'
		else:
			errors['invalid_data'] = 'Invalid data.'
	return render(request, 'registration/sign-in.html', {'form':login_form, 'errors':errors})

@csrf_exempt
def sign_up(request):
	template_name = 'registration/sign-up.html'
	user_form = UserForm()
	if request.method == "POST":
		user_form = UserForm(request.POST)
		if user_form.is_valid() and request.POST.get('name') != 'activate-phone' :
			user = user_form.save(commit=False)
			if re.match(r'^[+]{1}[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', user_form.cleaned_data.get('phone_or_email')):
				try:
					user.phone = user_form.cleaned_data.get('phone_or_email')
					user.email = None
					user.save()
					user = authenticate(phone_or_email=user_form.cleaned_data.get('phone_or_email'), password=user_form.clean_password1())
					try:
						response = send_verfication_code(user)
					except:
						return render(request, template_name, {'error': 'verification code not sent.\n Please re-register.', 'user_form':user_form})
					data = json.loads(response.text)
					print(response.status_code, response.reason)
					print(response.text)
					print(data['success'])
					if data['success'] == False:
						return render(request, template_name, {'error': data['message'], 'user_form':user_form})
					else:
						kwargs = {'user': user}
						request.method = 'GET'
						return phone_verification(request, **kwargs)
				except:
					return render(request, template_name, {'error': 'Phone already exists', 'user_form':user_form})

			elif re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', user_form.cleaned_data.get('phone_or_email')):
				try:
					user.is_active = False
					user.email=user_form.cleaned_data.get('phone_or_email')
					user.phone = None
					user.save()
					current_site = get_current_site(request)
					mail_subject = 'Activate your blog account.'
					message = render_to_string('registration/activate-message.html', {
						'user': user,
						'domain': current_site.domain,
						'uid':urlsafe_base64_encode(force_bytes(user.pk)),
						'token':account_activation_token.make_token(user),
					})
					to_email = user_form.cleaned_data.get('phone_or_email')
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
					return redirect('activate_page')
				except:
					return render(request, template_name, {'error': 'Email already exists', 'user_form':user_form})
			else:
				return render(request, template_name, {'user_form':user_form})
	return render(request, template_name, {'user_form':user_form})



def phone_verification(request, **kwargs):
	template_name = 'registration/activate-phone-page.html'
	form = PhoneVerificationForm()

	if request.method == 'POST':
		id = request.POST['user']
		user = User.objects.get(pk=id)
		form = PhoneVerificationForm(request.POST)
		if form.is_valid():
			verification_code = request.POST['one_time_password']
			response = verify_sent_code(verification_code, user)
			print(response.text)
			data = json.loads(response.text)

			if data['success'] == True:
				login(request, user, backend='django.contrib.auth.backends.ModelBackend')
				if user.phone_number_verified is False:
					user.phone_number_verified = True
					user.save()
				return redirect('account')
			else:
				return render(request, template_name, {'form':form,'user':user, 'error': data['message']})
		else:
			return render(request, template_name, {'form':form,'user':user})
	elif request.method == 'GET':
		try:
			user = kwargs['user']
			return render(request, template_name, {'form':form, 'user':user})
		except:
			return HttpResponse("Not Allowed")
			

def activate_page(request):
	return render(request, 'registration/activate_page.html')


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user, backend='django.contrib.auth.backends.ModelBackend')
		messages.success(request, 'Your account has been created!')
		return redirect('account')
	else:
		return HttpResponse('Activation link is invalid!')
