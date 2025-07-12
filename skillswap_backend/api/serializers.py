from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Skill, SwapRequest, Feedback


class UserSerializer(serializers.ModelSerializer):
    skills_offered = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Skill.objects.all(), 
        required=False
    )
    skills_wanted = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Skill.objects.all(), 
        required=False
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'location', 'profile_photo', 
                 'availability', 'is_public', 'skills_offered', 'skills_wanted']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return attrs


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class SwapRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    offered_skill = SkillSerializer(read_only=True)
    requested_skill = SkillSerializer(read_only=True)
    offered_skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), 
        source='offered_skill', 
        write_only=True
    )
    requested_skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), 
        source='requested_skill', 
        write_only=True
    )
    
    class Meta:
        model = SwapRequest
        fields = ['id', 'sender', 'receiver', 'offered_skill', 'requested_skill',
                 'offered_skill_id', 'requested_skill_id', 'status', 'timestamp']
        read_only_fields = ['id', 'sender', 'status', 'timestamp']
    
    def validate(self, attrs):
        if attrs['offered_skill'] == attrs['requested_skill']:
            raise serializers.ValidationError("Offered and requested skills cannot be the same")
        return attrs


class SwapRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwapRequest
        fields = ['status']
    
    def validate_status(self, value):
        if value not in ['accepted', 'rejected', 'cancelled']:
            raise serializers.ValidationError("Invalid status")
        return value


class FeedbackSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    
    class Meta:
        model = Feedback
        fields = ['id', 'swap_request', 'from_user', 'to_user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'from_user', 'created_at']
    
    def validate(self, attrs):
        swap_request = attrs['swap_request']
        if swap_request.status != 'accepted':
            raise serializers.ValidationError("Can only leave feedback for accepted swap requests")
        return attrs 