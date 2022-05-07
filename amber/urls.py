from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

from amberapp import views
from botapp import views as bot_views
from products import views as products_views
from authapp import views as authapp_views
from orders import views as orders_views
from authapp import apis

from django.conf.urls.static import static
from django.conf import settings
from django import forms

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),


    ########################
    #     REGISTRATION     #
    ########################

    # Registartion and login/logout 
    path('sign-in/', authapp_views.user_login, name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(next_page='/'), name='sign-out'),
    path('sign-up/', authapp_views.sign_up, name='sign-up'),
    path('verify/', authapp_views.phone_verification, name='phone_verification'),
    path('activate/<uidb64>/<token>/', authapp_views.activate, name='activate'),
    path('activate/', authapp_views.activate_page, name='activate_page'),

    # Password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password-reset-form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password-reset-done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-confirm.html', success_url='/account/'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset-complete.html'), name='password_reset_complete'),
    


    ########################
    #        ACCOUNT       #
    ########################

    # Account page
    path('account/', views.account, name='account'),
    # Account management page
    path('account/actions', views.actions, name='actions'),
    # Account settings
    path('account/settings/', views.settings, name='settings'),
    # Change password
    path('account/settings/change-passwd/', auth_views.PasswordChangeView.as_view(template_name='account/settings/change-pswd.html', success_url='/account/'), name='change-passwd'),
    # Change user profile
    path('account/settings/update-profile/', views.update_profile, name='update-profile'),
    
    ########################
    #         CHAT         #
    ########################

    
    path('direct/', include('chatapp.urls')),

    ########################
    #     BOTAPP           #
    ########################

    # ADDing GROUPS
    path('account/group/add', bot_views.addNewGroup, name='add-group'),
    # ADDing GROUPS
    path('account/group/<id>/edit', bot_views.EditExistingGroup, name='edit-group'),
    # ADDing TOKENS
    path('account/<messenger>/add', bot_views.addNewToken, name='add-token'),

    # Process task
    path('account/task/<task>', bot_views.process_task, name='account'),




    # Change password
    path('account/settings/change-passwd/', auth_views.PasswordChangeView.as_view(template_name='account/settings/change-pswd.html', success_url='/account/'), name='change-passwd'),

    # Change user profile
    path('account/settings/update-profile/', views.update_profile, name='update-profile'),
    



    ########################
    #       PRODUCTS       #
    ########################

    # Add Product Page
    path('account/add/product/', products_views.user_add_product, name='create_product'),
    # Add Joint Product Page
    path('account/add/joint-product/', products_views.user_add_joint_product, name='create-joint-product'),
    # Take Part In Joint Product Page
    path('account/products/<product_id>/join/', products_views.join_joint_product, name='join-joint-product'),
    # Leave from Joint Product Page
    path('account/products/<product_id>/leave/', products_views.leave_joint_product, name='leave-joint-product'),
    # User Products
    path('account/user/products/', products_views.user_products, name='user-products'),
    # Product edit
    path('account/edit/product/<product_id>', products_views.user_edit_product, name='edit-product'),
    # Products page
    path('account/products/', products_views.products, name='products'),
    # Product info
    path('account/product/<product_id>', products_views.product_info, name='product-info'),
    # Search path
    path('search/', products_views.search_for_product, name='search-for-product'),
    # Get by category path
    path('account/products/get/category/', products_views.get_by_category, name='get-by-category'),
    
    
    ########################
    #       ORDERS         #
    ########################
    
    # Add new order path
    path('order/new/<owner>/<product>', orders_views.add_new_order),


    ########################
    #         APIS         #
    ########################
    
    # All products api 
    path('api/account/products/', apis.user_get_products, name='products-api'),
    # Product by id api
    path('api/account/product/<product_id>', apis.user_get_product, name='products-user-api'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
