from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# class UserComment(models.Model):
#    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
#    user_comment = models.TextField()
#    user_image = models.FileField(
#        default='default.jpg', upload_to='comment_pics')

#    def __str__(self):
#        return self.user_name
