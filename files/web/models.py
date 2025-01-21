from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from autoslug import AutoSlugField



class Posts(models.Model):
    title = models.CharField('Заголовок',max_length=255)
    text = models.TextField('Текст', blank=False)
    image = models.ImageField('Изображение', upload_to='images/%Y/%m/%d', blank=True, )
    image2 = models.ImageField('Изображение', upload_to='images/%Y/%m/%d', blank=True, )
    image3 = models.ImageField('Изображение', upload_to='images/%Y/%m/%d', blank=True, )
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    date = models.DateTimeField('Дата публикации', auto_now_add=True)
    date_change = models.DateTimeField('Дата изменения', auto_now=True)
    author = models.CharField('Автор', max_length=100)
    slug = AutoSlugField(max_length=255, blank=True, unique=True, verbose_name="URL", populate_from='title')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано', help_text='Вы хотите опубликовать эту запись?')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        slugify(self.title)
        return super(Posts, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_page', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['date', 'title', 'is_published']


class Comments(models.Model):
    author = models.CharField(max_length=90, default='Гость')
    text = models.TextField(blank=False, max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Posts, verbose_name='Публикация', on_delete=models.CASCADE, null=True, blank=True)
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'

class Category(models.Model):
    category = models.CharField(max_length=30)
    slug = models.CharField(max_length=30, blank=False, unique=True, db_index=True, verbose_name="URL")
    image = models.ImageField('Изображение', upload_to='images/%Y/%m/%d', blank=True)
    selected_image = models.ImageField('Изображение', upload_to='images/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('sport', kwargs={'category_slug': self.slug})


    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

class Codes(models.Model):
    code = models.CharField(max_length=6, verbose_name='Код')
    mail = models.EmailField(blank=True, null=True, unique=True)

class Ban_words(models.Model):
    word = models.CharField(max_length=50, verbose_name='Слово')

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Фильтры слов'
        verbose_name_plural = 'Фильтры слов'
