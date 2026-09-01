from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apps.core.response import APIResponse

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    A viewset for performing CRUD operations on task instances.
    """

    serializer_class = TaskSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["status", "priority", "due_date"]
    search_fields = ["name", "description"]
    ordering_fields = [
        "name",
        "status",
        "priority",
        "due_date",
        "created_at",
    ]

    def get_queryset(self):
        """
        Return tasks belonging to the authenticated user.
        """
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Save the task instance with the authenticated user.
        """
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        paginated_response = self.get_paginated_response(serializer.data).data

        return APIResponse.success(
            data=paginated_response, message="Tasks retrieved successfully"
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return APIResponse.success(
            data=serializer.data,
            message="Task created successfully",
            status_code=201,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return APIResponse.success(
            data=serializer.data, message="Task retrieved successfully", status_code=200
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return APIResponse.success(
            data=serializer.data, message="Task updated successfully", status_code=200
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return APIResponse.success(message="Task deleted successfully", status_code=204)
