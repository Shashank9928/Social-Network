from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import SocialUserSerializer, LoginSerializer, SocialUserSerializer, FriendRequestSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import SocialUser, FriendRequest
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle
from django.db.models import Q

class SignupView(APIView):
    def post(self, request):
        serializer = SocialUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SearchUsersView(generics.ListAPIView):
    serializer_class = SocialUserSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            if '@' in query:
                return SocialUser.objects.filter(email__iexact=query)
            else:
                return SocialUser.objects.filter(name__icontains=query)
        return SocialUser.objects.none()
    
    
class SendFriendRequestThrottle(UserRateThrottle):
    rate = '3/min'

class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [SendFriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        from_user = request.user
        to_user_email = request.data.get('email')
        try:
            to_user = SocialUser.objects.get(email=to_user_email)
        except SocialUser.DoesNotExist:
            raise ValidationError('User with this email does not exist.')

        if from_user == to_user:
            raise ValidationError('You cannot send a friend request to yourself.')

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise ValidationError('Friend request already sent.')

        FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return Response({'status': 'friend request sent'}, status=status.HTTP_201_CREATED)

class RespondToFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        friend_request_id = request.data.get('friend_request_id')
        action = request.data.get('action')

        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id)
        except FriendRequest.DoesNotExist:
            raise ValidationError('Friend request does not exist.')

        if friend_request.to_user != request.user:
            raise ValidationError('You are not authorized to respond to this friend request.')

        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({'status': 'friend request accepted'}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({'status': 'friend request rejected'}, status=status.HTTP_200_OK)
        else:
            raise ValidationError('Invalid action.')

class ListFriendsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(
            Q(from_user=user, status='accepted') |
            Q(to_user=user, status='accepted')
        )
        return friends

class ListPendingFriendRequestsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, status='pending')