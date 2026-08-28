from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.response import APIResponse

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(APIView):
    """User registration endpoint."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return APIResponse.success(
                data=UserSerializer(user).data,
                message="User registered successfully",
                status_code=status.HTTP_201_CREATED,
            )
        else:
            return APIResponse.error(
                message="Registration failed",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    """User login and token generation endpoint."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        token = TokenObtainPairSerializer(data=request.data)

        token.is_valid(raise_exception=True)

        user = token.user

        refresh = token.validated_data["refresh"]
        access = token.validated_data["access"]

        payload = {
            "user": UserSerializer(user).data,
        }

        response = APIResponse.success(
            data=payload, message="Login successful", status_code=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=False,  # True in production
            samesite="Lax",
            max_age=5 * 60,
            path="/api/",
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
            path="/api/auth/",
        )

        return response


class RefreshView(APIView):
    """Refresh access token using refresh token from cookies."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return APIResponse.error(
                message="Refresh token not provided.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token

            response = APIResponse.success(
                data={"access": str(access)},
                message="Token refreshed successfully",
                status_code=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="access_token",
                value=str(access),
                httponly=True,
                secure=False,  # True in production with HTTPS
                samesite="Lax",
                max_age=5 * 60,
                path="/api/",
            )

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=False,  # True in production with HTTPS
                samesite="Lax",
                max_age=7 * 24 * 60 * 60,
                path="/api/auth/",
            )

            return response

        except Exception:
            return APIResponse.error(
                message="Invalid or expired refresh token.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    """Logout user and blacklist refresh token."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.COOKIES.get("refresh_token")

        if token:
            try:
                refresh = RefreshToken(token)
                refresh.blacklist()
            except Exception:
                pass

        response = APIResponse.success(message="Logout successful", status_code=status.HTTP_200_OK)

        response.delete_cookie(
            "refresh_token",
            path="/api/auth/",
        )

        response.delete_cookie(
            "access_token",
            path="/api/",
        )

        return response


class MeView(APIView):
    """Get authenticated user's information."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return APIResponse.success(data=serializer.data, message="User retrieved successfully")
