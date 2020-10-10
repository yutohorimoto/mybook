from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

label_choices = (
            (0, '小説'),
            (1, '漫画'),
            (2, 'ビジネス書'),
            (3, '学習書'),
            (4, '教養書'),
            (5, '自己啓発本'),
            (6, 'その他'),
        )

rate_choice =(
    (1,'1/5'),
    (2,'2/5'),
    (3,'3/5'),
    (4,'4/5'),
    (5,'5/5'),
)
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=50)
    book_author = models.CharField(max_length=20,blank=True, null=True)
    #book_label = models.CharField(max_length=20,blank=True, null=True)
    book_label = models.IntegerField(choices=label_choices,blank=True, null=True)
    book_int = models.CharField(max_length=200,blank=True, null=True)
    text = models.TextField()
    rate = models.IntegerField(choices = rate_choice ,blank=False, default=1)
    like_num = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.book_title
        return self.book_author


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return self.text
        