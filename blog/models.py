from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
#slugify
from django.utils.text import slugify
from django.contrib.auth.models import User
import re

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_tags(text):
    cleaned_text = re.sub(r'</.*?>', '. ', text)
    return remove_html_tags(cleaned_text)
# Create your models here.

STATUS_CHOICES = (
    ('Draft', 'Draft'),
    ('Pending', 'Pending'),
    ('Flagged', 'Flagged'),
    ('Rejected', 'Rejected'),
    ('Published', 'Published'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=80, unique=True, null=True, blank=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            if Category.objects.filter(slug=slug).exists():
                slug = slug + '-' + str(Category.objects.filter(slug=slug).count())
            self.slug = slug
        super(Category, self).save(*args, **kwargs)

    

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=80, unique=True, null=True, blank=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            if Tag.objects.filter(slug=slug).exists():
                slug = slug + '-' + str(Tag.objects.filter(slug=slug).count())
            self.slug = slug
        super(Tag, self).save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey(User, related_name='post', null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=70)
    image = models.ImageField(upload_to='blog/%Y/%m/%d', blank=True)
    slug = models.SlugField(max_length=80, unique=True, null=True, blank=True)
    body = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Draft')
    admin_comment = models.TextField(blank=True, null=True)
    flag_comment = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.excerpt = remove_tags(self.body)[:200] + '...'
        if not self.slug:
            slug = slugify(self.title)
            if Post.objects.filter(slug=slug).exists():
                slug = slug + '-' + str(Post.objects.filter(slug=slug).count())
            self.slug = slug
        check = self.flag_check()
        if len(check) > 0:
            self.status = 'Flagged'
            self.flag_comment = ", ".join(check)
        elif self.status == 'Flagged':
            self.status = 'Pending'
            self.flag_comment = ''
        self.updated_at = timezone.now()
        super(Post, self).save(*args, **kwargs)

    def flag_check(self):
        word_list = ['offensive']
        flagged = []
        for word in word_list:
            if word in self.body:
                flagged.append(word)
        return flagged

    def get_author(self):
        if self.author:
            return f'{self.author.first_name} {self.author.last_name}'
        return 'Anonymous'

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.post.title + '@' + str(self.date)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.post.title + '@' + str(self.date)
    
