from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions

from .models import Company
from .serializers import TaskSerializer, CompanyFullSerializer, UserFullSerializer


class TaskViewSet(generics.ListCreateAPIView):
    """Tasks list view."""

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Define the queryset by the current user."""

        return self.request.user.active_company.tasks.all().order_by('-last_active')


    def perform_create(self, serializer):
        """When creating a new record, attach it to the user's active company."""

        serializer.save(company=self.request.user.active_company)


class UpdateTaskView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating and destroying task."""

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Define the queryset by the current user."""

        return self.request.user.active_company.tasks.all().order_by('-last_active')


class CompanyView(APIView):
    """View for getting information about the user's active company."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Function returns information about the current user's company."""

        company = request.user.active_company
        serializer = CompanyFullSerializer(company)
        return Response(serializer.data)


class UserView(APIView):
    """View for getting information about user and company authorization."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Function returns information about the current user."""

        user = request.user
        serializer = UserFullSerializer(user)
        return Response(serializer.data)


    def post(self, request):
        """Function for authorization in one of the user's companies."""

        user = request.user

        # Get and check active_company id
        active_company_id = request.data.get('active_company')
        if not active_company_id:
            return Response(status=400)

        # Get active_company from the DB
        try:
            active_company = Company.objects.get(id=active_company_id)
        except Company.DoesNotExist:
            return Response(status=404)

        # Check if the user has access to this company
        user_companies = user.companies.all()
        if active_company not in user_companies:
            return Response(status=403)

        # If all is well, this company is assigned to the user as active_company
        user.active_company = active_company
        user.save()

        return Response(status=201)
