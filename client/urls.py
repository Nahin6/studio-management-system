from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.home, name="dashboard"),
	path('photographerDashboard', views.photographerDashboard, name="photographerDashboard"),
	path('adminDashboard', views.adminDashboard, name="adminDashboard"),
	path('login', views.login, name="login"),
	path('signup', views.signup, name="signup"),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('client_login', views.client_login, name='client_login'),
    path('blocked', views.blocked, name='blocked'),
    path('view-profile', views.viewProfile, name='viewProfile'),
    path('update-profile', views.updateProfile, name='updateProfile'),
    path('order_success_page/<int:package_id>/', views.order_success_page, name='order_success_page'),
    path('hire_photographer_page/<int:package_id>/', views.hire_photographer_page, name='hire_photographer_page'),
    path('hiring_photographer/<int:package_id>/', views.hire_photographer, name='hire_photographer'),
    path('track_order', views.track_order, name='track_order'),
    path('details_page/<int:package_id>/', views.details_page, name='details_page'),
]