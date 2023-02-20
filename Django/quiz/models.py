from django.db import models

# Create your models here.


class Question(models.Model):
    question = models.CharField(
        max_length=500, unique=True, default="", null=False)
    answer = models.CharField(max_length=100, default="", null=False)
    category = models.CharField(max_length=100, default="", null=False)
    level = models.CharField(max_length=100, default="", null=False)
    wrong_answers = models.JSONField(default=list, null=True)

