from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from authapp.models import User
from products.models import Product
from .models import *
from .forms import *

# Create your views here.

@login_required(login_url='/sign-in/')
def add_new_order(request, owner, product):
	if request.POST:
		seller = User.objects.get(id = owner)
		item = Product.objects.get(id = product)
		order = Order.objects.create(customer = request.user, seller = seller, details = request.POST["details"], product = item)
		order.save()
		return HttpResponseRedirect('/account/products/')
	return render(request, 'account/body/orders/add-order.html', {'order' : OrderForm})
