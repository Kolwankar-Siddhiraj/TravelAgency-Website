# Generated by Django 3.1.5 on 2021-02-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Database_users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_Name', models.CharField(max_length=30)),
                ('User_Email', models.EmailField(max_length=50)),
                ('User_password', models.CharField(max_length=100)),
                ('User_otp', models.CharField(default=None, max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_name', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('offer', models.BooleanField(default=False)),
                ('destination_image', models.ImageField(upload_to='images')),
                ('discription', models.TextField()),
            ],
        ),
    ]
