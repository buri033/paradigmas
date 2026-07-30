import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'duckbank.settings')
django.setup()

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user_a(db):
    """Create test user A (Ana)."""
    user = User.objects.create_user(
        username='ana@duckbank.cl',
        email='ana@duckbank.cl',
        password='ana12345',
        first_name='Ana',
        last_name='Pérez',
    )
    user.profile.rut = '11111111-1'
    user.profile.phone = '+573001111111'
    user.profile.save()
    # Signal creates Profile + Account with $4,850,900 COP
    return user


@pytest.fixture
def user_b(db):
    """Create test user B (Bob)."""
    user = User.objects.create_user(
        username='bob@duckbank.cl',
        email='bob@duckbank.cl',
        password='bob12345',
        first_name='Bob',
        last_name='Gómez',
    )
    user.profile.rut = '22222222-2'
    user.profile.phone = '+573002222222'
    user.profile.save()
    # Signal creates Profile + Account with $4,850,900 COP
    return user


@pytest.fixture
def client_a(user_a):
    """Authenticated API client for user A."""
    client = APIClient()
    refresh = RefreshToken.for_user(user_a)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def client_b(user_b):
    """Authenticated API client for user B."""
    client = APIClient()
    refresh = RefreshToken.for_user(user_b)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def account_a(user_a):
    """Get user A's default account."""
    return user_a.profile.accounts.first()


@pytest.fixture
def account_b(user_b):
    """Get user B's default account."""
    return user_b.profile.accounts.first()