from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("residents/", views.ResidentsListView.as_view(), name="residents-list"),
    path("residents/user/<int:user_id>/", views.ResidentDetailView.as_view(), name="resident-detail"),
    path("residents/<int:pk>/update/", views.ResidentUpdateView.as_view(), name="resident-update"),
    path("residents/<int:pk>/account-update/", views.ResidentAccountUpdateView.as_view(), name="resident-account-update",),
    path("residents/<int:pk>/location/", views.ResidentLocationUpdateView.as_view(), name="resident-location-update",),
    path("residents/<int:pk>/profile-picture/", views.ResidentProfilePictureUpdateView.as_view(), name="resident-profile-picture-update",),
    path("residents/<int:pk>/delete/", views.ResidentDeleteView.as_view(), name="resident-delete"),
    
    path("dengue-locations/", views.DengueLocationListView.as_view(), name="dengue-location-list"),
    path("dengue-locations/<int:pk>/", views.DengueLocationDetailView.as_view(), name="dengue-location-detail"),
    path("dengue-locations/<int:pk>/update/", views.DengueLocationUpdateView.as_view(), name="dengue-location-update"),
    path("dengue-locations/<int:pk>/delete/", views.DengueLocationDeleteView.as_view(), name="dengue-location-delete"),
]