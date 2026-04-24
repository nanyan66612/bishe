from django.db import models
from users.models import User
from questions.models import Question

class Submit(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    code = models.TextField()
    result = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

class WrongQuestion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user','question')