# Generated by Django 3.0.8 on 2020-08-10 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200804_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.DeleteModel(
            name='Bids',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='comment',
        ),
        migrations.AddField(
            model_name='comments',
            name='text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='comments',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='comments',
            name='commented_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
