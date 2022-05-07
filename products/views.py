from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from products.decorators import user_has_product
from products.models import *
from products.forms import *


@login_required(login_url='/sign-in/')
def user_add_product(request):
	form = ProductForm()
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			product = form.save(commit=False)
			product.user = request.user
			product.save()
			return redirect('account')


	return render(request, 'account/body/products/add-product.html', {'product': form})


@login_required(login_url='/sign-in/')
def user_add_joint_product(request):
	form = JointProductForm()
	if request.method == 'POST':
		form = JointProductForm(request.POST, request.FILES)
		if form.is_valid():
			product = form.save(commit=False)
			product.user = request.user
			product.save()
			return redirect('account')


	return render(request, 'account/body/products/add-product.html', {'product': form})


@login_required(login_url='/sign-in/')
def user_products(request):
	products = Product.objects.filter(user=request.user).order_by("-id")
	return render(request, 'account/body/products/user-products.html', {'products': products})


@login_required(login_url='/sign-in/')
@user_has_product
def user_edit_product(request, product_id):
	form = ProductForm(instance = Product.objects.get(id = product_id))
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES, instance = Product.objects.get(id = product_id))

		if form.is_valid():
			form.save()
			return redirect('account')

	return render(request, 'account/body/products/edit-product.html', {'product': form})

@login_required(login_url='/sign-in/')
def products(request):
	products = Product.objects.all().order_by("-id")
	mainCategories = MainProductsCategorie.objects.all()
	subCategories  = ProductsSubCategorie.objects.all()
	jointProducts = JointProduct.objects.all()

	return render(request, 'account/body/products/products-page.html', {'products': products, 'mainCategories' : mainCategories, 'subCategories' : subCategories, 'joint' : jointProducts})

@login_required(login_url='/sign-in/')
def product_info(request, product_id):
	product = Product.objects.get(id=product_id)
	jp = JointProduct.objects.all().filter(id = product_id)
	return render(request, 'account/body/products/product-info.html', {'product': product, 'jp' : jp[0] if jp else jp})
	

@login_required(login_url='/sign-in/')
def search_for_product(request):
	if request.is_ajax and request.method == 'POST':
		form = SearchForm(request.POST)
		products = list(Product.objects.filter(name__icontains = request.POST["query"]).values())
		return JsonResponse({"instance": products}, status=200)
	return JsonResponse({"error": ""}, status=400)


@login_required(login_url='/sign-in/')
def get_by_category(request):
	if request.is_ajax and request.method == 'POST':
		products = list(Product.objects.filter(category = ProductsSubCategorie.objects.get(name=request.POST["data"])).values())
		return JsonResponse({"products": products}, status=200)
	return JsonResponse({"error": ""}, status=400)


@login_required(login_url='/sign-in/')
def join_joint_product(request, product_id):
	joint = JointProduct.objects.get(id = product_id)
	if request.user in joint.joined.all():
		pass
	else:
		joint.joined.add(request.user)
	return redirect('account')


@login_required(login_url='/sign-in/')
def leave_joint_product(request, product_id):
	joint = JointProduct.objects.get(id = product_id)
	if request.user in joint.joined.all():
		joint.joined.remove(request.user)
	else:
		pass
	return redirect('account')
