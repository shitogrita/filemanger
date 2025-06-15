from django.db import models
from django.contrib.auth.models import User

class MLRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_data = models.JSONField()
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"MLRequest {self.id} by {self.user.username}"
