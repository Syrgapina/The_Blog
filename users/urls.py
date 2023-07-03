from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile_settings/', views.profile_settings, name='profile_settings'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_profile/<int:profile_id>/', views.edit_profile, name='edit_profile'),
    path('remove_profile_image/<int:profile_id>/', views.remove_profile_image),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)