# Generated by Django 4.1 on 2022-10-05 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_alter_producto_pc_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='PC_FOTO',
            field=models.ImageField(default='default.jpg', upload_to='images'),
        ),
    ]
