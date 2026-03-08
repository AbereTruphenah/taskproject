# IMPORT DJANGO'S DATABASE MODELS MODULE
from django.db import models

# CREATE A MODEL/TABLE NAMED TASK
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # CONTROL HOW OBJECT APPEARS IN ADMIN PANEL
    def __str__(self):
        return self.title
