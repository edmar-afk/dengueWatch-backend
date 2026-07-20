from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import ResidentsSerializer
from .models import Residents
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["userData"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "is_staff": self.user.is_staff,
            "is_superuser": self.user.is_superuser,
        }

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        first_name = request.data.get("first_name")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Phone Number already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create User
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            password=password,
        )

        # Create Resident profile
        Residents.objects.create(
            user=user,
            full_name=first_name,
            phone_number=username,
        )

        return Response(
            {"message": "Account created successfully."},
            status=status.HTTP_201_CREATED,
        )


# GET ALL RESIDENTS
class ResidentsListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        residents = Residents.objects.select_related("user").filter(
            user__is_superuser=False,
            user__is_staff=False
        )

        serializer = ResidentsSerializer(
            residents,
            many=True,
            context={"request": request}
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

# GET SINGLE RESIDENT
class ResidentDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        try:
            resident = Residents.objects.select_related("user").get(
                user_id=user_id
            )
        except Residents.DoesNotExist:
            return Response(
                {"detail": "Resident not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResidentsSerializer(
            resident,
            context={"request": request}
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# UPDATE RESIDENT
class ResidentUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, pk):
        try:
            resident = Residents.objects.select_related("user").get(pk=pk)
        except Residents.DoesNotExist:
            return Response(
                {"detail": "Resident not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = resident.user

        new_phone_number = request.data.get("phone_number")
        new_full_name = request.data.get("full_name")

        # Check if phone number already belongs to another user
        if new_phone_number:
            phone_exists = User.objects.filter(
                username=new_phone_number
            ).exclude(
                id=user.id
            ).exists()

            if phone_exists:
                return Response(
                    {"error": "Phone Number already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = ResidentsSerializer(
            resident,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_resident = serializer.save()

            # Synchronize full_name with User.first_name
            if new_full_name is not None:
                user.first_name = new_full_name

            # Synchronize phone_number with User.username
            if new_phone_number is not None:
                user.username = new_phone_number

            user.save()

            return Response(
                ResidentsSerializer(updated_resident).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# DELETE RESIDENT
class ResidentDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        try:
            resident = Residents.objects.get(pk=pk)
        except Residents.DoesNotExist:
            return Response(
                {"detail": "Resident not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        resident.delete()

        return Response(
            {"detail": "Resident deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
        
        


class ResidentAccountUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, pk):
        try:
            resident = Residents.objects.select_related("user").get(pk=pk)
        except Residents.DoesNotExist:
            return Response(
                {"detail": "Resident not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = resident.user

        new_first_name = request.data.get("first_name")
        new_username = request.data.get("username")

        # Update first_name and full_name
        if new_first_name is not None:
            user.first_name = new_first_name
            resident.full_name = new_first_name

        # Update username and phone_number
        if new_username is not None:
            user.username = new_username
            resident.phone_number = new_username

        # Save both models
        user.save()
        resident.save()

        return Response(
            {
                "id": resident.id,

                # User fields
                "user_id": user.id,
                "first_name": user.first_name,
                "username": user.username,

                # Resident fields
                "full_name": resident.full_name,
                "dengue_status": resident.dengue_status,
                "phone_number": resident.phone_number,
                "location": resident.location,
                "address": resident.address,

                "profile_picture": (
                    request.build_absolute_uri(
                        resident.profile_picture.url
                    )
                    if resident.profile_picture
                    else None
                ),
            },
            status=status.HTTP_200_OK,
        )