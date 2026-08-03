from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Residents, DengueLocation, DengueCase



class ResidentsSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    is_staff = serializers.BooleanField(source="user.is_staff", read_only=True)

    class Meta:
        model = Residents
        fields = [
            "id",
            "user_id",
            "first_name",
            "username",
            "is_staff",
            "full_name",
            "dengue_status",
            "phone_number",
            "location",
            "address",
            "profile_picture",
            "resident_idCard",   # add this
        ]
        
        
class DengueLocationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    resident_image_url = serializers.SerializerMethodField()

    class Meta:
        model = DengueLocation
        fields = [
            "id",
            "status",
            "location",
            "description",
            "image",
            "image_url",
            "resident_image_url",  # New field
            "posted_by",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")

        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url

        return None

    def get_resident_image_url(self, obj):
        request = self.context.get("request")

        try:
            resident = obj.posted_by.residents
        except Residents.DoesNotExist:
            return None

        if resident.profile_picture:
            if request:
                return request.build_absolute_uri(resident.profile_picture.url)
            return resident.profile_picture.url

        return None
    


class ResidentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Residents
        fields = [
            "id",
            "username",
            "first_name",
            "full_name",
            "phone_number",
            "profile_picture",
        ]
        
        
        
class DengueCaseSerializer(serializers.ModelSerializer):
    resident_name = serializers.CharField(
        source="resident.full_name",
        read_only=True
    )

    phone_number = serializers.CharField(
        source="resident.phone_number",
        read_only=True
    )

    address = serializers.CharField(
        source="resident.address",
        read_only=True
    )

    class Meta:
        model = DengueCase
        fields = [
            "id",
            "resident",
            "resident_name",
            "phone_number",
            "address",
            "status",
            "date_case",
        ]
        read_only_fields = ["date_case"]