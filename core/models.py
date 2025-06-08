from django.db import models

class StoredFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.description or f"File {self.id}"

