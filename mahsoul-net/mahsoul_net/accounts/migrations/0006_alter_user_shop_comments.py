# Generated by Django 4.2.4 on 2023-11-01 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_delete_comments'),
        ('accounts', '0005_user_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='shop',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller', to='products.shops', verbose_name='فروشگاه'),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_message', models.TextField(verbose_name='متن نظر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='products.products', verbose_name='محصول')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
    ]
