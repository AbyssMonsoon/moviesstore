from django.db import models
from django.conf import settings

class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='petitions')
    created_at = models.DateTimeField(auto_now_add=True)
    yes_votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='petition_votes', blank=True)

    def yes_count(self):
        return self.yes_votes.count()

    def __str__(self):
        return self.title
