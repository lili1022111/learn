from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('toggle_public/<int:topic_id>/', views.toggle_public_topic, name='toggle_public'),
    path('entries/<int:entry_id>/like/', views.like_entry, name='like_entry'),
    # 评论URL（同时支持顶级评论和回复）
    path('entries/<int:entry_id>/comment/', views.add_comment, name='add_comment'),
]