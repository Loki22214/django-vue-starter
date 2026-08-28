from django.utils import timezone
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["user"]

    def validate_due_date(self, value):
        if value is not None and value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
