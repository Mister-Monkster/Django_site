from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from django.db.models import Q

from .models import *
from users.models import *



class AddComments(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Комментарий", 'required': True, "spellcheck": "false"}),
        max_length=1000, label='Комментарий')

class Registration(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', error_messages={'required': ''}, widget=forms.TextInput(attrs={'class': 'form_input', 'placeholder': ' '}))
    email = forms.CharField(label='Электронная почта', error_messages={'required': ''}, widget=forms.TextInput(attrs={'class': 'form_input', 'placeholder': ' '}))
    password1 = forms.CharField(label='Пароль', error_messages={'required': ''}, widget=forms.PasswordInput(attrs={'class': 'form_input', 'placeholder': ' '}))
    password2 = forms.CharField(label='Повтор пароля', error_messages={'required': ''}, widget=forms.PasswordInput(attrs={'class': 'form_input', 'placeholder': ' '}))
    captcha = CaptchaField(label='CAPTCHA')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_input', 'placeholder': ' '}),
            'email': forms.TextInput(attrs={'class': 'form_input', 'placeholder': ' '}),
            'password1': forms.PasswordInput(attrs={'class': 'form_input', 'placeholder': ' '}),
            'password2': forms.PasswordInput(attrs={'class': 'form_input', 'placeholder': ' '})
        }


class Login(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form_input', 'placeholder': ' '}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_input', 'placeholder': ' '}))


class email_verification(forms.Form):
    def get_invalid_code_error(self):
        if not Codes.objects.filter(code = self).exists():
            raise ValidationError('Неверный код. Пожалуйста, проверьтe правильность кода.')
        return self


    code = forms.CharField(label='Код', error_messages={'required': '', 'invalid_code' : 'Неверный код. Пожалуйста, проверьтe правильность кода.'}, validators=[get_invalid_code_error], widget=forms.TextInput(attrs={'class': 'form_input', 'placeholder': ' '}))

    error_messages ={ "invalid_code": ('Неверный код. Пожалуйста, проверьтe правильность кода')
                      }

class Recovery(PasswordResetForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form_input',
                'autocomplete': 'off',
                'placeholder': ' ',
            })


class UserSetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form_input',
                'autocomplete': 'off',
                'placeholder': ' '
            })


class account(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form_input', 'placeholder': ' '}))
    first_name = forms.CharField(label='Имя', required=False , widget=forms.TextInput(attrs={'class': 'form_input', 'placeholder': ' '}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(attrs={'class': 'form_input', 'placeholder': ' '}))
    email = forms.CharField(label='Адрес электронной почты', widget=forms.TextInput(attrs={'class': 'form_input', 'placeholder': ' '}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class password(PasswordChangeForm):

        old_password = forms.CharField(label='Старый пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form_input', 'placeholder': ' '}))
        new_password1 = forms.CharField(label='Новый пароль',
                                 widget=forms.PasswordInput(attrs={'class': 'form_input', 'placeholder': ' '}))
        new_password2 = forms.CharField(label='Новый пароль(еще раз)',
                                widget=forms.PasswordInput(attrs={'class': 'form_input', 'placeholder': ' '}))

        class Meta:
            model = User
            fields = ("old_password", "new_password1", "new_password2")



class post_edit(forms.ModelForm):
    title = forms.CharField( widget=forms.TextInput(attrs={'class': 'form_title_post', 'placeholder': 'Заголовок'}))
    text = forms.CharField( widget=forms.Textarea(attrs={'class': 'form_text_post', 'placeholder': 'Текст'}))
    image = forms.ImageField(label='Изображение', required=True, widget=forms.ClearableFileInput(attrs={'class': 'form_image_post'}))
    image2 = forms.ImageField(label='Изображение 2', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form_image_post'}))
    image3 = forms.ImageField(label='Изображение 3', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form_image_post'}))
    category = forms.ModelChoiceField( queryset=Category.objects.filter(~Q(category='Не опубликовано')))
    author = forms.CharField(label='Автор', widget=forms.TextInput(attrs={'class': 'form_input_author', 'placeholder': 'Автор'}))
    is_published = forms.BooleanField(label='Опубликовано', required=False)


    class Meta:
        model = Posts
        fields = ('title', 'text', 'image','image2', 'image3', 'category', 'author', 'is_published')

class add_post(forms.ModelForm):
    title = forms.CharField( widget=forms.TextInput(attrs={'class': 'form_title_post', 'placeholder': 'Заголовок'}))
    text = forms.CharField( widget=forms.Textarea(attrs={'class': 'form_text_post', 'placeholder': 'Текст'}))
    image = forms.ImageField(label='Изображение', required=True, widget=forms.ClearableFileInput(attrs={'class': 'form_image_post',}))
    image2 = forms.ImageField(label='Изображение 2',required=False, widget=forms.ClearableFileInput(attrs={'class': 'form_image_post'}))
    image3 = forms.ImageField(label='Изображение 3', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form_image_post'}))
    category = forms.ModelChoiceField( queryset=Category.objects.filter(~Q(category='Не опубликовано')))


    class Meta:
        model = Posts
        fields = ('title', 'text', 'image', 'image2', 'image3', 'category', )#'author'


class feedback(forms.Form):
    name = forms.CharField( required=True, widget=forms.TextInput(attrs={'class': 'form_title_post', 'placeholder': 'Имя'}))
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form_title_post', 'placeholder': 'Почта'}))
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form_text_post', 'placeholder': 'Текст'}))
    captcha = CaptchaField(label='CAPTCHA')