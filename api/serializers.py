"""File with application serializers."""

from rest_framework import serializers

from .models import Company, Task, CustomUser

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""

    class Meta:
        model = Task
        exclude = ('company', )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users (without companies).

    Only for CompanyFullSerializer.
    """

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class CompanyFullSerializer(serializers.ModelSerializer):
    """Serializer for company (full data presentation with staff)."""

    staff = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'staff')


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for companies (without staff).

    Only for UserFullSerializer.
    """

    class Meta:
        model = Company
        fields = ('id', 'name')


class UserFullSerializer(serializers.ModelSerializer):
    """Serializer for user (full data presentation with companies)."""

    companies = CompanySerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'companies', 'active_company')
