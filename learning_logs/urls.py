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
    # 新增：公开主题设置路由
    path('toggle_public/<int:topic_id>/', views.toggle_public_topic, name='toggle_public'),
    # 修改为与模板一致的路径（去掉 entries/ 前缀）
    path('<int:entry_id>/like/', views.like_entry, name='like_entry'),
    path('<int:entry_id>/comment/', views.add_comment, name='add_comment'),

]