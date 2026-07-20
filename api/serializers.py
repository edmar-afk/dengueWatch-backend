from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Residents



class ResidentsSerializer(serializers.ModelSerializer):
    # User information
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Residents
        fields = [
            "id",

            # User fields
            "user_id",
            "first_name",
            "username",

            # Resident fields
            "full_name",
            "dengue_status",
            "phone_number",
            "location",
            "address",
            "profile_picture",
        ]