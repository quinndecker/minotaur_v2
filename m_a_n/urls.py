from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('user_logger', views.user_logger),
    path('master_home', views.go_home_roger),
    path('new_shop', views.new_shop),
    path('create_shop', views.create_shop),
    path('shop/<int:id>', views.one_shop),
    path('new_product', views.new_product),
    path('create_product', views.create_product),
    path('product/<int:id>', views.one_product),
    path('delete/<int:id>', views.delete),
    path('my_shops/<int:id>', views.my_shops),
    path('purchase', views.purchase),
    path('checkout', views.checkout),

]