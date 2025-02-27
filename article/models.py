from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .constants import RATING_CHOICES

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Article(models.Model):
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=500)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publishing_time = models.DateTimeField(auto_now_add=True)
    total_rating = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to="article/media", null=True, blank=True)

    def avg_rating(self):
        if self.rating_count == 0:
            return -1
        return self.total_rating / self.rating_count
    
    def __str__(self):
        return self.headline[:100]
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    value = models.IntegerField(choices=RATING_CHOICES)
    time = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

@receiver(post_save, sender=Rating)
def post_rating_tasks(sender, instance, *args, **kwargs):
    instance.article.total_rating += instance.value
    instance.article.rating_count += 1
    instance.article.save()

    try:
        email = instance.article.editor.email
        headline = instance.article.headline
        reviewer = instance.user.first_name + " " + instance.user.last_name
        message = instance.body
        send_mail(
            subject="A new review on your article",
            from_email="imdashraful17@gmail.com",
            recipient_list=[email,],
            message='',
            html_message=f"""
                <h1>Review on your Article</h1>
                <p>A new review was made on your article {headline}</p>
                <b>Reviewer: </b>{reviewer}<br/>
                <b>Message: </b><p>{message}</p>
            """
        )
    except Exception as e:
        print(e)