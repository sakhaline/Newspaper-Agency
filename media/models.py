from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=True)

    class Meta:
        verbose_name = "redactor"
        ordering = ('username',)

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"


class Topic(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self) -> str:
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=55)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="newspapers"
    )

    def __str__(self) -> str:
        return self.title
