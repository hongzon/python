# Generated by Django 2.0.4 on 2018-09-02 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='subject',
            field=models.ForeignKey(db_column='sno', on_delete=django.db.models.deletion.PROTECT, to='demo.Subject', verbose_name='所属学科'),
        ),
    ]
