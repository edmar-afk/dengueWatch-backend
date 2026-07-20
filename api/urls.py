from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("residents/", views.ResidentsListView.as_view(), name="residents-list"),
    path("residents/user/<int:user_id>/", views.ResidentDetailView.as_view(), name="resident-detail"),
    path("residents/<int:pk>/update/", views.ResidentUpdateView.as_view(), name="resident-update"),
    path("residents/<int:pk>/account-update/", views.ResidentAccountUpdateView.as_view(), name="resident-account-update",),
    path("residents/<int:pk>/delete/", views.ResidentDeleteView.as_view(), name="resident-delete"),
]