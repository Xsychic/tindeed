from . import views
from django.urls import path

urlpatterns = [
    path('vacancy/', views.getIndex),
    path('vacancy/apply/', views.postApplication),
    path('vacancy/reject/', views.postReject),
    path('vacancy/fav/', views.postFavourite),
    path('applications/', views.getApplications),
    path('applications/stats/', views.getApplicationStats),
    path('applications/<int:applicationId>/', views.getApplicationDetails)
]