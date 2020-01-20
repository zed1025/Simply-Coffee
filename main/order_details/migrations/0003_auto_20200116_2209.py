# Generated by Django 3.0.1 on 2020-01-16 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_details', '0002_auto_20200101_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='customer',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='order_date_time',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='phone',
            field=models.ForeignKey(default='0000000000', on_delete=django.db.models.deletion.CASCADE, to='order_details.Customer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=200),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='order',
            field=models.CharField(max_length=500),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]