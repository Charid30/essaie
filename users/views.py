from rest_framework import generics, viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser ,AllowAny
from rest_framework.views import APIView
from .models import User, Profile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .serializers import UserSerializer, ProfileSerializer ,CustomAuthTokenSerializer
User = get_user_model()

# Inscription
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# Connexion - Token
class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'role': user.role,
        })
# Déconnexion
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# Gestion profil utilisateur connecté
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Méthode non autorisée."}, status=405)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Méthode non autorisée."}, status=405)

# Administration complète utilisateurs
class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]



class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Email envoyé si compte existant'}, status=status.HTTP_200_OK)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        # Construire ici URL réinitialisation mot de passe à envoyer par email
        reset_url = f"http://votre-frontend/reset-password-confirm/{uid}/{token}/"
        send_mail(
            'Réinitialisation de votre mot de passe',
            f'Pour réinitialiser votre mot de passe, cliquez ici: {reset_url}',
            'no-reply@jobbooster.com',
            [email]
        )
        return Response({'detail': 'Email envoyé si compte existant'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Mot de passe réinitialisé avec succès'}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': 'Mot de passe actuel incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Mot de passe modifié avec succès'}, status=status.HTTP_200_OK)


from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import UserContact, User
from .serializers import UserContactSerializer

class UserContactViewSet(viewsets.ModelViewSet):
    serializer_class = UserContactSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Retourner uniquement les contacts de l'utilisateur connecté
        return UserContact.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Associer automatiquement le contact au user connecté
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'detail': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'detail': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)