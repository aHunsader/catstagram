from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
	username = models.CharField(max_length=100)
	bio = models.TextField(blank=True)
	profile_pic = models.ImageField(blank=True)
	likes = models.TextField(default=" ", blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	default = models.BooleanField(default=True)


	def __str__(self):
		return self.username;

	def get_absolute_url(self):
		return reverse('member-detail', args=[str(self.id)])

	class Meta:
		ordering = ["username"]


class Picture(models.Model):

	image = models.ImageField()
	profile = models.ForeignKey(Profile)
	date = models.DateField(auto_now_add=True)
	caption = models.TextField(default="")
	upvote = models.IntegerField(default=0)
	downvote = models.IntegerField(default=0)

class Comment(models.Model):

	picture = models.ForeignKey(Picture)
	profile = models.ForeignKey(Profile)
	body = models.TextField()
	datetime = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-datetime"]