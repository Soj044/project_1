# Generated by Django 5.1 on 2025-02-04 23:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('forum', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dicuss', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='discussion',
            name='cat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='forum.category'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='tracks',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artist', to='forum.tracks'),
        ),
        migrations.AddIndex(
            model_name='discussion',
            index=models.Index(fields=['-pub_date'], name='forum_discu_pub_dat_860b0f_idx'),
        ),
    ]
