from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# from rest_framework.response import request
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .serializers import UserSerializer, UserCreateSerializer
import json

User = get_user_model()


# @csrf_exempt
# @permission_classes([permissions.AllowAny])
# class CustomAuthToken(ObtainAuthToken):
#     # permission_classes = [permissions.AllowAny]
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'username': user.username,
#             'email': user.email,
#         })

# @api_view(['POST'])
# @method_decorator(csrf_exempt, name='dispatch')
# @api_view(['POST'])
# @api_view([''])
# @csrf_exempt
# def CustomAuthToken(request):
#     print(request)
#     # username = request.data.get('username')
#     # password = request.data.get('password')
#     username=str(request)
#     password=str(request)
#     print(f"username: {username}")

#     # if not username or not password:
#     #     return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

#     # user = authenticate(username=username, password=password)
#     # if user:
#     #     token, _ = Token.objects.get_or_create(user=user)
#     #     return Response({
#     #         'token': token.key,
#     #         'user_id': user.id,
#     #         'username': user.username,
#     #         'email': user.email
#     #     })
#     # else:
#     #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response({'token':""})

@csrf_exempt
def CustomAuthToken(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
    except Exception as e:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)

    # Authenticate user
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    # Get or create token
    token, _ = Token.objects.get_or_create(user=user)

    return JsonResponse({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
    }, status=200)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow or unfollow a user based on POST request
    """
    target_user = get_object_or_404(User, pk=user_id)
    current_user = request.user
    
    # Don't allow users to follow themselves
    if target_user == current_user:
        return Response(
            {'error': 'You cannot follow yourself.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if already following and toggle
    if current_user in target_user.followers.all():
        target_user.followers.remove(current_user)
        action = 'unfollowed'
    else:
        target_user.followers.add(current_user)
        action = 'followed'
    
    return Response({
        'status': 'success',
        'action': action,
        'user': UserSerializer(target_user).data
    })

@api_view(['GET'])
def user_followers(request, user_id):
    """
    Get all followers of a specific user
    """
    user = get_object_or_404(User, pk=user_id)
    followers = user.followers.all()
    serializer = UserSerializer(followers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user_following(request, user_id):
    """
    Get all users that a specific user is following
    """
    user = get_object_or_404(User, pk=user_id)
    following = user.following.all()
    serializer = UserSerializer(following, many=True)
    return Response(serializer.data)