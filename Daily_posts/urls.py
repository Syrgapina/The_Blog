from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name='home'),
    path('hello/', views.hello, name='hello'),
    path('add_post/', views.add_post),
    path('post_page/<int:post_id>/', views.post_page, name='post_page'),
    path('remove_post/<int:post_id>/', views.remove_post),
    path('edit_post/<int:post_id>/', views.edit_post),
    path('remove_comment/<int:post_id>/<int:comment_id>/', views.remove_comment),
    path('edit_comment/<int:post_id>/<int:comment_id>/', views.edit_comment)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
