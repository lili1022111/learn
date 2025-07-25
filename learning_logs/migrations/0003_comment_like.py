# Generated by Django 5.2.3 on 2025-07-11 13:00

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0002_alter_like_unique_together_remove_like_entry_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='learning_logs.entry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='learning_logs.entry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('entry', 'user')},
            },
        ),
    ]
