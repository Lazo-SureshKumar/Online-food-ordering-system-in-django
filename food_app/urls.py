from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('adminclick', views.adminclick_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('adminlogin', LoginView.as_view(template_name='adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('view-customer', views.view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('admin-items', views.admin_items_view,name='admin-items'),
    path('admin-add-item', views.admin_add_item_view,name='admin-add-item'),
    path('delete-item/<int:pk>', views.delete_item_view,name='delete-item'),
    path('update-item/<int:pk>', views.update_item_view,name='update-item'),
    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),
    path('logout', LogoutView.as_view(template_name='logout.html'),name='logout'),








    path('home',views.home,name='home'),
    path('add_view/home',views.index,name='add_view/home'),
    path('index',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('',views.home,name='home'),
    path('login/', views.login_view, name="login"),
    # path('logout', views.logout,name='logout'),
    path('aboutus', views.aboutus,name='aboutus'),
    path('add_view/<int:pk>', views.add_view,name='add_view'),
    path('full_view/<int:pk>',views.full_view,name='full_view'),
    path('cart',views.cart,name='cart'),
    path('remove_cart/<int:pk>',views.remove_cart,name='remove_cart'),
    path('place_order',views.place_order,name='place_order'),
    path('payment_success',views.payment_success,name="payment_success"),
    path('my_order',views.my_order,name="my_order"),
    path('cancel_order_view',views.cancel_order_view,name="cancel_order_view"),
    path('my_profile',views.my_profile,name="my_profile"),
    path('edit_profile',views.edit_profile_view,name="edit_profile"),
    path('search', views.search_view,name='search'),

    # path('cash_on_delivery',views.cash_on_delivery,name="cash_on_delivery"),
    # path('aboutus', views.aboutus_view),
    # path('contactus', views.contactus_view,name='contactus'),
    # path('search', views.search_view,name='search'),
    # path('send-feedback', views.send_feedback_view,name='send-feedback'),
    # path('view-feedback', views.view_feedback_view,name='view-feedback'),

    # path('adminclick', views.adminclick_view),
    # path('adminlogin', LoginView.as_view(template_name='ecom/adminlogin.html'),name='adminlogin'),
    # path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    # path('view-customer', views.view_customer_view,name='view-customer'),
    # path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    # path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),

    # path('admin-items', views.admin_items_view,name='admin-items'),
    # path('admin-add-item', vi,emname='admin-add-item'),
    # path('delete-item/<int:pk>', views.delete_product_view,name='delete-item'),
    # path('update-item/<int:pk>', views.update_product_view,name='update-item'),

    # path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    # path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    # path('update-order/<int:pk>', views.update_order_view,name='update-order'),

    # path('customer-home', views.customer_home_view,name='customer-home'),
    # path('my-order', views.my_order_view,name='my-order'),
    # # path('my-order', views.my_order_view2,name='my-order'),
    # path('my-profile', views.my_profile_view,name='my-profile'),
    # path('edit-profile', views.edit_profile_view,name='edit-profile'),


    # path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    # path('cart', views.cart_view,name='cart'),
    # path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    # path('customer-address', views.customer_address_view,name='customer-address'),
    # path('payment-success', views.payment_success_view,name='payment-success'),

]