from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Skill, SwapRequest, Feedback
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    SkillSerializer, SwapRequestSerializer, SwapRequestUpdateSerializer,
    FeedbackSerializer
)
from django.db import models


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message": "Error logging out"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = User.objects.filter(is_public=True).exclude(id=self.request.user.id)
        
        # Filter by skill if provided
        skill = self.request.query_params.get('skill', None)
        if skill:
            # Filter users who have offered or wanted skills containing the search term
            queryset = queryset.filter(
                Q(sent_requests__offered_skill__name__icontains=skill) | 
                Q(sent_requests__requested_skill__name__icontains=skill) |
                Q(received_requests__offered_skill__name__icontains=skill) |
                Q(received_requests__requested_skill__name__icontains=skill)
            ).distinct()
        
        return queryset


class SkillListView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class SwapRequestListView(generics.ListCreateAPIView):
    serializer_class = SwapRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SwapRequest.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class SwapRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SwapRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SwapRequest.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SwapRequestUpdateSerializer
        return SwapRequestSerializer


class SwapRequestActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk, action):
        try:
            swap_request = SwapRequest.objects.get(
                id=pk, 
                receiver=request.user,
                status='pending'
            )
            
            if action == 'accept':
                swap_request.status = 'accepted'
            elif action == 'reject':
                swap_request.status = 'rejected'
            else:
                return Response(
                    {"error": "Invalid action"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            swap_request.save()
            serializer = SwapRequestSerializer(swap_request)
            return Response(serializer.data)
            
        except SwapRequest.DoesNotExist:
            return Response(
                {"error": "Swap request not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class FeedbackListView(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Feedback.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        )
    
    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Feedback.objects.filter(from_user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Get user statistics"""
    user = request.user
    
    stats = {
        'total_sent_requests': SwapRequest.objects.filter(sender=user).count(),
        'total_received_requests': SwapRequest.objects.filter(receiver=user).count(),
        'accepted_requests': SwapRequest.objects.filter(
            Q(sender=user) | Q(receiver=user),
            status='accepted'
        ).count(),
        'pending_requests': SwapRequest.objects.filter(
            Q(sender=user) | Q(receiver=user),
            status='pending'
        ).count(),
        'average_rating': Feedback.objects.filter(to_user=user).aggregate(
            avg_rating=models.Avg('rating')
        )['avg_rating'] or 0,
        'total_feedbacks': Feedback.objects.filter(to_user=user).count(),
    }
    
    return Response(stats)
