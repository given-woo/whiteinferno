from django.urls import path

from . import views

urlpatterns = [
    #Leave as empty string for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('all/', views.all, name="all"),
    path('process_order/', views.processOrder, name="process_order"),
    path('product/<int:id>/', views.product_view, name='product_view'),
    path('collection/<str:name>/<str:type>', views.collection_view, name='collection_view'),
    path('login/', views.login_view, name='login'),
    path('process_login/', views.processLogin, name='process_login'),
    path('process_logout/', views.processLogout, name='process_logout'),
    path('register/', views.register_view, name='register'),
    path('process_register/', views.register, name='process_register'),
]
