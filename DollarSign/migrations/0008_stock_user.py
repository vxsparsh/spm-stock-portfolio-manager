# Generated by Django 4.2.1 on 2023-09-06 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DollarSign', '0007_remove_stock_ytdchange_stock_current_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]