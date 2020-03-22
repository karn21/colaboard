from django.contrib import admin
from django.urls import path, include
from accounts import urls as account_urls
from django.contrib.auth import views as auth_views
from boards import urls as board_urls
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('features/', views.features, name='features'),
    # password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<slug:uidb64>/<slug:token>',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),


    path('accounts/', include(account_urls, namespace='accounts')),
    path('boards/', include(board_urls, namespace='boards')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
