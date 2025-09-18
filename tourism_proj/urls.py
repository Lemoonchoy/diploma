from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from voyage.views import register_view
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('voyage.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register_view, name='register'),
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='voyage/registration/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
