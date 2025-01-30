from django.urls  import path
from . import views

urlpatterns = [
    path('blog/', views.blog, name='blog'), 
    path('blog/update/<int:pk>/', views.updatePost, name='update_post'),
    path('blog/delete/<int:pk>/', views.deletePost, name='delete_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]