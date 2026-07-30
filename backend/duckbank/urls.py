from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('users.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('transactions.urls')),
    path('api/', include('savings.urls')),
    path('api/', include('loans.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('money_requests.urls')),
]