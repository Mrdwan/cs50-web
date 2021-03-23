from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Follows(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
class Post(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    likedBy = models.ManyToManyField(User, default=None, blank=True, related_name="likes")


    @property
    def likesCount(self):
        return self.likedBy.all().count()