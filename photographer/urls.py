from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
        #Leave as empty string for base url
    path('PackageAddPage', views.PackageAddPage, name='PackageAddPage'),
    path('add_package', views.add_package, name='add_package'),
    path('view_packages', views.view_packages, name='view_packages') , 
    path('view_profile', views.phototGrapherViewProfile, name='phototGrapherViewProfile') , 
    path('updatePhotographerProfile', views.updatePhotographerProfile, name='updatePhotographerProfile') , 
    path('delete_package/<int:pk>/', views.delete_package, name='delete_package'),
    path('edit_package/<int:pk>/', views.edit_package, name='edit_package'),
    path('received_jobs', views.received_jobs, name='received_jobs') , 
    path('approve_job/<int:details_id>/', views.approve_job, name='approve_job'),
    path('reject_job/<int:details_id>/', views.reject_job, name='reject_job'),
    path('completed_job/<int:details_id>/', views.completed_job, name='completed_job'),
    path('accounts_info', views.accounts_info, name='accounts_info') , 
    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)