# models.py

from django.db import models

class RequestDataLog(models.Model):
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    body = models.TextField()
    user_agent = models.CharField(max_length=255)
    mobile = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.method} {self.path}'
