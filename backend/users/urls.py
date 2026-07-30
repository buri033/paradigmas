from django.urls import path
from .views import RegisterView, LogoutView, ProfileView, ToggleBalanceView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/toggle-balance/', ToggleBalanceView.as_view(), name='toggle-balance'),
]