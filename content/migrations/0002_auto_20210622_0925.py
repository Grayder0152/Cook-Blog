# Generated by Django 3.2.4 on 2021-06-22 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutpage',
            name='mini_img',
            field=models.ImageField(default='', upload_to='about/'),
        ),
        migrations.AlterField(
            model_name='aboutpage',
            name='name',
            field=models.CharField(help_text='Enter your name', max_length=50),
        ),
        migrations.AlterField(
            model_name='aboutpage',
            name='social_networks',
            field=models.ManyToManyField(help_text='Chose your social networks', to='content.SocialNetwork'),
        ),
    ]