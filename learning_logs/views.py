from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import Topic, Entry, Like, Comment
from .forms import TopicForm, EntryForm, CommentForm

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Show a single topic (支持公开访问校验)"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    # 权限校验逻辑
    if topic.owner != request.user:
        if not topic.is_public:
            raise Http404("该主题未公开或已被删除")
        
        if topic.share_expire_at and topic.share_expire_at < timezone.now():
            return HttpResponseBadRequest("该分享链接已过期")
        
        if topic.share_password:
            input_password = request.GET.get('password')
            if not input_password or input_password != topic.share_password:
                return render(request, 'learning_logs/public_topic_password.html', {'topic': topic})
    
    # 搜索逻辑
    search_query = request.GET.get('q', '')
    entries = topic.entries.all().order_by('-date_added')
    for entry in entries:
        entry.user_liked = entry.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
        entry.comment_count = entry.comments.count()
    
    if search_query:
        entries = entries.filter(Q(text__icontains=search_query))
    
    return render(request, 'learning_logs/topic.html', {
        'topic': topic,
        'entries': entries,
        'comment_form': CommentForm(),
        'search_query': search_query
    })

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry with image and video upload."""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        # 支持文件上传（图片+视频）
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry with image and video update."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        # 支持更新视频文件
        form = EntryForm(instance=entry, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    """删除指定条目（验证权限后执行）"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic': topic}
    return render(request, 'learning_logs/delete_entry.html', context)

@login_required
def delete_topic(request, topic_id):
    """删除指定主题及关联条目"""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')
    
    context = {'topic': topic}
    return render(request, 'learning_logs/delete_topic.html', context)

@login_required
def toggle_public_topic(request, topic_id):
    """切换主题公开状态及设置分享参数"""
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    
    if request.method == 'POST':
        topic.is_public = not topic.is_public
        topic.share_password = request.POST.get('share_password', '').strip() or None
        
        expire_str = request.POST.get('share_expire_at')
        if expire_str:
            naive_datetime = parse_datetime(expire_str)
            if naive_datetime:
                topic.share_expire_at = timezone.make_aware(naive_datetime)
            else:
                topic.share_expire_at = None
        else:
            topic.share_expire_at = None
        
        topic.save()
        return redirect('learning_logs:topics')
    
    context = {
        'topic': topic,
        'share_link': request.build_absolute_uri(f'/topics/{topic.id}/')
    }
    return render(request, 'learning_logs/toggle_public.html', context)

@login_required
def like_entry(request, entry_id):
    """处理点赞"""
    entry = get_object_or_404(Entry, id=entry_id)
    like, created = Like.objects.get_or_create(entry=entry, user=request.user)
    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True
    
    return JsonResponse({
        'like_count': entry.likes.count(),
        'is_liked': is_liked
    })

@login_required
def add_comment(request, entry_id):
    """处理评论"""
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.entry = entry
            comment.user = request.user
            comment.save()
    return redirect('learning_logs:topic', topic_id=entry.topic.id)