from django.db import models
from django.contrib.auth.models import User
import markdown
# Create your models here.
from django.utils.html import strip_tags
from django.urls import reverse


class Category(models.Model):
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
    
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ('-created_time',)
    
    title = models.CharField(max_length=80)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    abstract = models.CharField(max_length=150, blank=True)
    like = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        
        self.abstract = strip_tags(md.convert(self.body))[:100]
        
        super().save(*args, **kwargs)
    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def increase_like(self):
        self.like += 1
        self.save(update_fields=['like'])
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={'pk': self.pk})

