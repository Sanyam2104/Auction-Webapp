# Generated by Django 3.0.8 on 2020-08-10 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bids'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='favorite',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.AuctionListings'),
        ),
    ]
