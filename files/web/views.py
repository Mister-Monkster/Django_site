from django.shortcuts import render

import random

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, FormView
from django.db.models import Q

from .forms import *
from .utils import DataMixin
from Site import settings
from users.models import User

mainmenu = [{'title': 'Главная', 'urlname': '/main'},
            {'title': 'О сайте', 'urlname': '/about'},
            {'title': 'Контакты', 'urlname': '/contacts'}]

def generate_code():
    random.seed()
    code = str(random.randint(10000,99999))
    return code

def mail_for_admins(post, user):
    admins = User.objects.filter(is_superuser=True)
    mails = []
    for admin in admins:
        mails.append(admin.email)
    send_mail("На проверку поступила новая новость.", f'{user} отправил на проверку новую новость,'
                                                      f'ссылка на новость http://127.0.0.1:8000/main/post/{post.slug}',
              'on-news.nevazhno@yandex.ru', tuple(mails))

def valid_word(list, form):
    flag = True
    for i in list:
        print(i)
        if str(i).lower() in form.cleaned_data['text'].lower():
            flag = False
    return flag

def MainPage(request):
    return redirect('main', permanent=True)


def menu(request):
    context = {'menu': mainmenu
               }
    return render(request, 'web/base.html', context=context)

def email_verif(request):
    if not request.user.is_verificated and request.user.is_authenticated:
        mail = request.user.email
        try:
            code = Codes.objects.get(mail=mail)
        except:
            Codes.objects.filter(mail=mail).delete()
            code = Codes.objects.create(code=generate_code(), mail=mail)
        send_mail("Opushka news", f'Здравствуйте, Ваш код для регистрации:{code.code}.\nПисьмо отправлено автоматически не отвечайте на него и никому не сообщайте код.', 'on-news.nevazhno@yandex.ru', (mail,))
    return redirect('verification')


class Main(DataMixin, ListView):
    model = Posts
    template_name = 'web/MainPage.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Posts.objects.all().order_by('-date')
        else:
            return (Posts.objects.filter(is_published=True).order_by('-date'))


class not_published(DataMixin, ListView):
    model = Posts
    template_name = 'web/MainPage.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Не опубликовано',
                                      cat_selected=3)

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
                return Posts.objects.filter(is_published=False).order_by('-date')


class categoryshow(DataMixin, ListView):
    model = Posts
    template_name = 'web/MainPage.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if len(context['posts']) != 0:
            c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].category),
                                            cat_selected=context['posts'][0].category_id)
        else:
            c_def = self.get_user_context(title='В данной категории нет ни одной новости')

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Posts.objects.filter(category__slug=self.kwargs['category_slug']).order_by('-date')
        else:
            posts = (Posts.objects.filter((Q(category__slug=self.kwargs['category_slug']) & Q(is_published=True))))
            if len(posts) == 0:
                redirect('main')
                return posts
            else:
                return posts



def get(request, post_slug):
    global status
    ban_list = Ban_words.objects.all()
    post = get_object_or_404(Posts, slug=post_slug)
    comms = Comments.objects.filter(post_id=post.pk).order_by('-date')
    if request.user.is_authenticated:
        status = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = AddComments(request.POST)
        if form.is_valid():
            try:
                if request.user.is_authenticated:
                    if status.is_superuser:
                        form.cleaned_data['author'] = '👑' + request.user.username
                    else:
                        form.cleaned_data['author'] = request.user.username
                Comments.objects.create(**form.cleaned_data, post_id=post.pk, is_published=valid_word(ban_list, form))
                return redirect(request.path)
            except:
                form.add_error(None, 'Ошибка')
    else:
        form = AddComments()
    if request.user.is_authenticated:
        context = {'form': form,
               'title': post.title,
               'menu': mainmenu,
               'post': post,
               'comments': comms,
               'status': status
               }
    else:
        context = {'form': form,
               'title': post.title,
               'menu': mainmenu,
               'post': post,
               'comments': comms
               }
    return render(request, 'web/PostPage.html', context=context)

class registration(DataMixin, CreateView):
    form_class = Registration
    template_name = 'web/registration.html'
    success_url = reverse_lazy('/verification')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('send_message')

class Login(DataMixin, LoginView):
    form_class = Login
    template_name = 'web/login.html'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

def verification(request):
    form = email_verification(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            mail = request.user.email
            user_code = form.cleaned_data.get('code')
            code = Codes.objects.get(mail=mail)
            if str(user_code) == str(code.code):
                user = User.objects.get(email=mail)
                user.is_verificated = True
                user.save()
                code.delete()
                return redirect('/main')
            else:
                return redirect('send_message')
    context ={'form': form,
              'title': 'Верификация'}
    return render(request, 'web/email-verification.html', context=context)

def logout_user(request):
    logout(request)
    return redirect('main')

def redirecter(request):
    return redirect('main')


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    form_class = Recovery
    template_name = 'web/recovery.html'
    success_url = reverse_lazy('main')
    from_email = 'on-news.nevazhno@yandex.ru'
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'web/password_subject_reset_mail.txt'
    email_template_name = 'web/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = UserSetNewPasswordForm
    template_name = 'web/user_password_set_new.html'
    success_url = reverse_lazy('main')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context

class User_Change(DataMixin, UpdateView):
    template_name = 'web/user_profile.html'
    form_class = account
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Изменить данные")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return self.request.path

class Password_change(DataMixin, PasswordChangeView):
    template_name = 'web/change_password.html'
    form_class = password

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Изменить данные")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        user = self.request.user.pk
        return f'/main/user/{user}'


class Post_edit(DataMixin, UpdateView):
    template_name = 'web/Post_edit.html'
    form_class = post_edit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Изменить данные")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        slug = self.request.path.split('/')[-2]
        post = Posts.objects.filter(slug=slug)
        return post

    def get_success_url(self):
        return '/main/'


class AddPost(DataMixin, CreateView):
    form_class = add_post
    template_name = 'web/Post_edit.html'
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        user = self.request.user.username
        post = Posts.objects.create(title=data['title'].capitalize(), text=data['text'], image=data['image'], image2=data['image2'],
                             image3=data['image3'], category=data['category'], author=user)
        post.save()
        mail_for_admins(post, user)
        return redirect('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить запись")
        return dict(list(context.items()) + list(c_def.items()))


class moderation(DataMixin, ListView):
    template_name = 'web/moderation.html'
    model = Comments
    context_object_name = 'comments'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Модерация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        comments = Comments.objects.filter(is_published=False).order_by('-date')
        return comments

def del_com(request, pk):
    if request.user.is_staff or request.user.is_superuser:
        comment = Comments.objects.get(pk=pk)
        comment.delete()
        return redirect('moderation')
    else:
        return redirect('main')


def confirm_com(request, pk):
    if request.user.is_staff or request.user.is_superuser:
        comment = Comments.objects.get(pk=pk)
        comment.is_published = True
        comment.save()
        return redirect('moderation')
    else:
        return redirect('main')


def publish(request, pk):
    if request.user.is_staff or request.user.is_superuser:
        post = Posts.objects.get(pk=pk)
        post.is_published = True
        post.save()
        return redirect('not_pub')
    else:
        return redirect('main')


def contact(request):
    context = {'title': 'Контакты',
               'menu': mainmenu}
    return render(request, 'web/Contacts.html', context=context)


def about(request):
    context= {'title': 'О нас',
              'menu': mainmenu}
    return render(request, 'web/About.html', context=context)


class fedd_mail(DataMixin, FormView):
    form_class = feedback
    template_name = 'web/Post_edit.html'
    success_url = '/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        text = form.cleaned_data['text']
        name = form.cleaned_data['name']
        send_mail(f"Feedback from {name}.",
                  text + f'\n Электронная почта для ответа: {email}',
                  'on-news.nevazhno@yandex.ru', ('on-news.nevazhno@yandex.ru',))
        return redirect(self.success_url)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

