from django.urls import path
from .views import SignupView, LoginView, SearchUsersView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', SearchUsersView.as_view(), name='search-users'),
]
