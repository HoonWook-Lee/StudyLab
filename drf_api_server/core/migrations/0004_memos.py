# Generated by Django 4.2.2 on 2023-06-14 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_users_token_users_token_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Memos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('like', models.BigIntegerField(default=0)),
                ('img', models.FileField(blank=True, null=True, upload_to='')),
                ('keywords', models.ManyToManyField(blank=True, related_name='memos', to='core.keywords')),
                ('writer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
