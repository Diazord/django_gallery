# Generated by Django 4.2.3 on 2023-08-29 12:42

import base.models
import base.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_imagemodel_is_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='image',
            field=models.ImageField(upload_to=base.models.user_directory_path, validators=[base.validators.FileValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'ico'], allowed_mimetypes=['image/jpeg', 'image/x-png', 'image/png', 'image/webp', 'image/x-icon'], max_size=10485760)]),
        ),
    ]