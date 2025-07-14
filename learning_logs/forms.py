from django import forms
from .models import Topic, Entry, Comment

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text', 'image', 'video']  # 新增video字段
        labels = {
            'text': '',
            'image': '上传图片（可选）',
            'video': '上传视频（可选）'  # 视频字段标签
        }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 6}),
        }

class CommentForm(forms.ModelForm):
    """评论提交表单"""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '添加评论...',
                'class': 'form-control'
            }),
        }
        labels = {'text': ''}