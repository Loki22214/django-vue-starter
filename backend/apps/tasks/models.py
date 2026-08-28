from django.db import models


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN PROGRESS", "In Progress"
        DONE = "DONE", "Done"

    class PriorityChoices(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.TODO
    )
    priority = models.CharField(
        max_length=20, choices=PriorityChoices.choices, default=PriorityChoices.MEDIUM
    )
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
