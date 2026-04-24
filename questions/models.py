from django.db import models

class Question(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50)
    test_input = models.TextField(default='')
    test_output = models.TextField(default='')
    def __str__(self):
        return self.title