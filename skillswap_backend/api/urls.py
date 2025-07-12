from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView, ProfileView, UserListView,
    SkillListView, SwapRequestListView, SwapRequestDetailView, SwapRequestActionView,
    FeedbackListView, FeedbackDetailView, user_stats
)

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User management
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('stats/', user_stats, name='user-stats'),
    
    # Skills
    path('skills/', SkillListView.as_view(), name='skill-list'),
    
    # Swap requests
    path('swap-requests/', SwapRequestListView.as_view(), name='swap-request-list'),
    path('swap-requests/<int:pk>/', SwapRequestDetailView.as_view(), name='swap-request-detail'),
    path('swap-requests/<int:pk>/<str:action>/', SwapRequestActionView.as_view(), name='swap-request-action'),
    
    # Feedback
    path('feedback/', FeedbackListView.as_view(), name='feedback-list'),
    path('feedback/<int:pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),
] 