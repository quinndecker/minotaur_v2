# Generated by Django 2.2 on 2020-09-12 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('m_a_n', '0007_auto_20200911_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_pic',
            field=models.ImageField(blank=True, null=True, upload_to='uploaded_files/'),
        ),
    ]