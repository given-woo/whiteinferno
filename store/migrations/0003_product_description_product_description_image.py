# Generated by Django 4.2.7 on 2023-12-25 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
