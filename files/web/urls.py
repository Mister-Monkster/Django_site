from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from Site import settings


urlpatterns = [

    path('', redirecter),
    path('main/', Main.as_view(), name='main'),
    path('add-post/', AddPost.as_view(), name='add_post'),
    path('contacts/', contact, name='contact'),
    path('feedback/', fedd_mail.as_view(), name='feedback'),
    path('about/', about, name='about'),
    path('moderation/', moderation.as_view(), name='moderation'),
    path('publish/<int:pk>', publish , name='publish_post'),
    path('com-del/<int:pk>', del_com, name='del_com'),
    path('con-allowed/<int:pk>', confirm_com, name='con-allowed'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('verification/', verification, name='verification'),
    path('email-verification/', email_verif, name='send_message'),
    path('registration/', registration.as_view(), name='registration'),
    path('recovery/', UserForgotPasswordView.as_view(), name='recovery'),
    path('password-recovery/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('main/user/<int:pk>/', User_Change.as_view(), name='profile'),
    path('main/user/<int:pk>/password/', Password_change.as_view(), name='password'),
    path('main/all', redirecter, name='all'),
    path('main/not-published', not_published.as_view(), name='not_pub'),
    path('main/post/<slug:post_slug>', get, name='post_page'),
    path('main/post/<slug:slug>/edit', Post_edit.as_view(), name='post_edit'),
    path('main/<slug:category_slug>', categoryshow.as_view(), name='sport'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

