# Generated by Django 5.2.3 on 2025-06-24 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proteintf',
            name='AF3',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proteintf',
            name='ENSEMBL',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proteintf',
            name='PDB',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proteintf',
            name='UNIPROT',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proteintf',
            name='proteinatlas',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
    ]
