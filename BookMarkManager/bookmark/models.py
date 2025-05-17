from django.db import models
from django.contrib.auth.models import User

# Define category choices
CATEGORY_CHOICES = [
    ('work', 'Work'),
    ('personal', 'Personal'),
    ('study', 'Study'),
    ('entertainment', 'Entertainment')
]

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='work')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return str(self.id)
