from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Topic(models.Model):
    """用户学习笔记中的主题（支持公开分享）"""
    text = models.CharField(
        _("主题名称"),
        max_length=200,
        help_text=_("主题名称最大长度为200个字符")
    )
    date_added = models.DateTimeField(
        _("创建时间"),
        auto_now_add=True,
        db_index=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("所属用户"),
        related_name="topics"
    )
    # 公开分享相关字段
    is_public = models.BooleanField(
        _("是否公开"),
        default=False,
        help_text=_("勾选后该主题可通过链接分享给他人")
    )
    share_password = models.CharField(
        _("访问密码"),
        max_length=50,
        blank=True,
        null=True,
        help_text=_("可选：设置访问密码，为空则无需密码")
    )
    share_expire_at = models.DateTimeField(
        _("过期时间"),
        blank=True,
        null=True,
        help_text=_("可选：设置分享过期时间，为空则永久有效")
    )
    
    def __str__(self):
        return self.text
    
    def save(self, *args, **kwargs):
        """保存时自动处理过期逻辑"""
        if self.share_expire_at and self.share_expire_at < timezone.now():
            self.is_public = False  # 已过期则自动设为不公开
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("主题")
        verbose_name_plural = _("主题")
        ordering = ["-date_added"]

class Entry(models.Model):
    """与主题相关的具体条目内容（支持图文、视频混排）"""
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name=_("关联主题"),
        related_name="entries"
    )
    text = models.TextField(
        _("条目内容"),
        help_text=_("存储条目详细内容的文本字段")
    )
    # 图片字段：支持上传图片
    image = models.ImageField(
        _("条目图片"),
        upload_to="entry_media/images/%Y/%m/%d/",  # 调整路径，与视频区分
        blank=True,
        null=True,
        help_text=_("可选：上传与条目相关的图片")
    )
    # 新增视频字段
    video = models.FileField(
        _("条目视频"),
        upload_to="entry_media/videos/%Y/%m/%d/",  # 视频单独存储目录
        blank=True,
        null=True,
        help_text=_("可选：上传与条目相关的视频（支持MP4、WebM格式）")
    )
    date_added = models.DateTimeField(
        _("创建时间"),
        auto_now_add=True,
        db_index=True
    )
    
    @property
    def like_count(self):
        return self.likes.count()
    
    def __str__(self):
        """返回条目简短描述"""
        return f"{self.text[:50]}..."
    
    class Meta:
        verbose_name = _("条目")
        verbose_name_plural = _("条目")
        ordering = ["-date_added"]

class Like(models.Model):
    """点赞模型：关联条目和用户"""
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entry_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('entry', 'user')  # 一个用户对一个条目只能点一次赞

class Comment(models.Model):
    """评论模型：关联条目和用户"""
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entry_comments')
    text = models.TextField(max_length=500)  # 限制评论长度
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']  # 最新评论在前