from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
        #Leave as empty string for base url
    path('adminViewProfile', views.adminViewProfile, name='adminViewProfile'),
    path('updateProfile', views.updateProfile, name='updateProfile'),
    path('userList', views.userList, name='userList'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('photographerList', views.photographerList, name='photographerList'),  
    path('upload_category', views.upload_category, name='upload_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('see_package', views.see_package, name='see_package'),
    path('approved_package/<int:package_id>/', views.approved_package, name='approved_package'),
    path('decline_package/<int:package_id>/', views.decline_package, name='decline_package'),
    path('client/<int:client_id>/spend-history/', views.client_spend_history, name='client_spend_history'),
    path('photographer_info/<int:photographer_id>/info/', views.photographer_info, name='photographer_info'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)