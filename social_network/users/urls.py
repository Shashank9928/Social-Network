from django.urls import path
from .views import (
    SignupView, 
    LoginView, 
    SearchUsersView,
    SearchUsersView,
    SendFriendRequestView,
    RespondToFriendRequestView,
    ListFriendsView,
    ListPendingFriendRequestsView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', SearchUsersView.as_view(), name='search-users'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/respond/', RespondToFriendRequestView.as_view(), name='respond-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('friend-requests/pending/', ListPendingFriendRequestsView.as_view(), name='list-pending-friend-requests'),
]
