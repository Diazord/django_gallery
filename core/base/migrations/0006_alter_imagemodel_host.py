# Generated by Django 4.2.3 on 2023-08-10 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0005_remove_imagemodel_tags_delete_tag_imagemodel_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='host',
            field=models.ForeignKey(max_length=100, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]