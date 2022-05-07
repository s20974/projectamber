from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from botapp.tasks import telegramRegister
from botapp.forms import *

# Add new telegram token form
@login_required(login_url='/sign-in/')
def addNewToken(request, messenger):
	if messenger=="telegram":
		if request.method == 'POST':
			token_form = AddNewTelegramTokenForm(request.POST)

			if token_form.is_valid():
				element = TelegramToken.objects.create(data=request.POST["token"], owner = request.user, name = request.POST["name"])
				element.save()
			# redirect to a new URL:
			return HttpResponseRedirect('/account/')

		return render(request, 'account/body/addtoken.html', {'addTokenForm' : AddNewTelegramTokenForm})
	elif messenger == "viber":
		if request.method == 'POST':
			token_form = AddNewViberTokenForm(request.POST)

			if token_form.is_valid():
				element = ViberToken.objects.create(data=request.POST["token"], owner = request.user, name = request.POST["name"])
				element.save()
			# redirect to a new URL:
			return HttpResponseRedirect('/account/')

		return render(request, 'account/body/addtoken.html', {'addTokenForm' : AddNewViberTokenForm})
	else:
		return render(request, '404.html')


@login_required(login_url='/sign-in/')
def addNewGroup(request):
	if request.method == 'POST':
		groupForm = AddNewGroupForm(request.POST)

		group = Group.objects.create(name = request.POST.get('name'), owner = request.user)
		group.save()

		for token in request.POST.getlist('telegram_tokens'):
			group.telegram_tokens.add(TelegramToken.objects.get(id = token))
		for token in request.POST.getlist('viber_tokens'):
			group.viber_tokens.add(ViberToken.objects.get(id = token))

		return HttpResponseRedirect('/account')
	else:
		groupForm = AddNewGroupForm()
		groupForm.fields['telegram_tokens'].choices = [(l.id,l.name) for l in TelegramToken.objects.all().filter(owner=request.user)]
		groupForm.fields['viber_tokens'].choices = [(l.id,l.name) for l in ViberToken.objects.all().filter(owner=request.user)]
		groups = Group.objects.all().filter(owner = request.user)
		return render(request, 'account/body/addNewGroup.html', {"addNewGroupForm" : groupForm, 'groups' : groups})


@login_required(login_url='/sign-in/')
def EditExistingGroup(request, id):
	if request.method == 'POST':
		groupForm = AddNewGroupForm(request.POST)
		
		group = Group.objects.create(name = request.POST.get('name'), owner = request.user)
		group.save()

		for token in request.POST.getlist('telegram_tokens'):
			group.telegram_tokens.add(TelegramToken.objects.get(id = token))

		return HttpResponseRedirect('/account')
	else:
		try:
			data = Group.objects.get(id = id)
			if data.owner != request.user:
				return HttpResponseRedirect('/account/')
			groupForm = AddNewGroupForm(initial = {'name' : data.name})
			groupForm.fields['telegram_tokens'].choices = [(l.id,l.name) for l in TelegramToken.objects.all().filter(owner=request.user)]
			groupForm.fields['viber_tokens'].choices = [(l.id,l.name) for l in ViberToken.objects.all().filter(owner=request.user)]
			return render(request, 'account/body/addNewGroup.html', {"addNewGroupForm" : groupForm})
		except Exception:
			return HttpResponseRedirect('/account/')
			

@login_required(login_url='/sign-in/')
def process_task(request, task):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# tt = ''
		for token in request.POST['telegram_tokens']:
			telegramRegister.delay(TelegramToken.objects.get(id = token).data)
		if request.POST.get('groups') is not None:
			for group in request.POST.get('groups'):
				group = Group.objects.get(id = group)
				for token in group.telegram_tokens.values():
					telegramRegister.delay(token['data'])
		return HttpResponseRedirect('/account/')
	# if a GET (or any other method) we'll create a blank form
	else:

		fields = {
			'task_name' : forms.CharField(max_length = 100, required=True),
			'telegram_tokens' : forms.MultipleChoiceField(required = False),
			'viber_tokens' : forms.MultipleChoiceField(required = False),
			'groups' : forms.MultipleChoiceField(required = False),
		}

		fields['telegram_tokens'].choices = [(l.id,l.name) for l in TelegramToken.objects.all().filter(owner=request.user)]
		fields['viber_tokens'].choices = [(l.id,l.name) for l in ViberToken.objects.all().filter(owner=request.user)]
		fields['groups'].choices = [(l.id,l.name) for l in Group.objects.all().filter(owner=request.user)]

		if task == 'write-message':
			fields['message'] =  forms.CharField(widget=forms.Textarea, max_length=5000, required=True)
			fields['telegram_id'] =  forms.CharField(max_length=50)

		task_form = type('TaskForm',  # form name is irrelevant
			(forms.BaseForm,),
			{'base_fields': fields})
		return render(request, 'account/body/tasks/write-message.html', {'task_form': task_form})
