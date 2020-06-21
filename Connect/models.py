from django.db import models
from django.contrib.auth.models import User

class UserDataBase(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    user_title = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    experience = models.CharField(max_length=150, null=True, blank=True)
    company = models.CharField(max_length=150, null=True, blank=True)
    degree = models.CharField(max_length=150, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    facebook_ac = models.CharField(max_length=100, null=True, blank=True)
    whatshapp_ac = models.CharField(max_length=100, null=True, blank=True)
    google_ac = models.CharField(max_length=100, null=True, blank=True)
    instagram_ac = models.CharField(max_length=100, null=True, blank=True)
    linkedin_ac = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "UserData"
        verbose_name_plural = "UserDataBase"


class Connections(models.Model):
    sender = models.ForeignKey(UserDataBase, related_name="sender", on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(UserDataBase, related_name="receiver", on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=30, null=True, blank=True, default="Sent")
    date = models.DateField(auto_now_add=True, null=True)


    def __str__(self):
        return "{} send the request to {} with current status {}".format(self.sender, self.receiver, self.status)

    class Meta:
        verbose_name = "Connection"
        verbose_name_plural = "Connections"


class Company_Model(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=150, default="Information Technology", null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    number = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    map = models.TextField(null=True, blank=True)
    company_title = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    start_date = models.DateField(auto_now=True, blank=False,null=False)
    linkedin_ac = models.CharField(max_length=100, null=True, blank=True)
    facebook_ac = models.CharField(max_length=100, null=True, blank=True)
    twitter_ac = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.CharField(max_length=10, default="False", null=True, blank=True,
                                   choices=(("True", "True"), ("False", "False")))


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

class Blogs_Model(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    blog = models.TextField(null=True, blank=True)
    youtube_video = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BlogLikes(models.Model):
    usr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    blog = models.ForeignKey(Blogs_Model, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Like of Blog - {}".format(self.blog.title)

    class Meta:
        verbose_name = "BlogLike"
        verbose_name_plural = "BlogLikes"

class User_Follow(models.Model):
    following = models.ForeignKey(UserDataBase, related_name="following", on_delete=models.CASCADE, null=True, blank=True)
    followers = models.ForeignKey(UserDataBase, related_name="follower", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "User {} follows user {}".format(self.following.name, self.followers.name)


class Follow_Company(models.Model):
    user = models.ForeignKey(UserDataBase, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company_Model, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return "User {} follows company {}".format(self.user.name, self.company.name)


class Queries(models.Model):
    email = models.EmailField(max_length=40, null=False, blank=False)
    first_name = models.CharField(max_length=60, null=False, blank=False)
    last_name = models.CharField(max_length=60, null=True, blank=True)
    query = models.TextField(max_length=500, null=False, blank=False)


    def __str__(self):
        return "New Query from {}".format(self.first_name)



class Company_Queries(models.Model):
    comp = models.ForeignKey(Company_Model, on_delete=models.CASCADE, null=False, blank=False)
    email = models.EmailField(max_length=40, null=False, blank=False)
    first_name = models.CharField(max_length=60, null=False, blank=False)
    last_name = models.CharField(max_length=60, null=True, blank=True)
    query = models.TextField(max_length=500, null=False, blank=False)
    country = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return "New Query from {}".format(self.first_name)
