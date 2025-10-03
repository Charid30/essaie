from rest_framework import serializers
from .models import User, Profile, UserContact
from skills.serializers import UserSkillSerializer, CVSerializer  # Import du serializer CV
from django.contrib.auth import authenticate
from skills.models import UserSkill

class SimpleProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'skills']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return UserSkill.objects.filter(profile=user.profile) # Renvoie queryset vide si pas connecté
        return UserSkill.objects.filter(profile=user.profile)

class UserContactSerializer(serializers.ModelSerializer):
    user_profile = SimpleProfileSerializer(many=True, read_only=True)  

    class Meta:
        model = UserContact
        fields = ['id', 'contact_type', 'value', 'label', 'created_at', 'updated_at', 'user_profile']
        read_only_fields = ['created_at', 'updated_at', 'user_profile']
class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request=self.context.get('request'),
                            username=email, password=password)
        if not user:
            raise serializers.ValidationError("Email ou mot de passe incorrect")
        data['user'] = user
        return data






class ProfileSerializer(serializers.ModelSerializer):
    cvs = CVSerializer(many=True, read_only=True)  # Ajout du champ CV ici

    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'photo', 'geographic_zone', 
            'bio', 'availability', 'subscription_status', 'verified_badge',
            'last_updated', 'cvs'  # Ne pas oublier d'ajouter ici
        ]
        read_only_fields = ['last_updated']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    contacts = UserContactSerializer(many=True, required=False)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    skills = UserSkillSerializer(many=True, source='profile.skills', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'is_active', 'is_staff', 'role', 'profile', 'contacts', 'skills']
        read_only_fields = ['is_active', 'is_staff', 'id']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        contacts_data = validated_data.pop('contacts', [])
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        for contact_data in contacts_data:
            UserContact.objects.create(user=user, **contact_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        contacts_data = validated_data.pop('contacts', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()

        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        if contacts_data is not None:
            instance.contacts.all().delete()
            for contact_data in contacts_data:
                UserContact.objects.create(user=instance, **contact_data)

        return instance

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        try:
            uid = urlsafe_base64_decode(data['uidb64']).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Token invalide')
        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError('Token invalide ou expiré')
        data['user'] = user
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
