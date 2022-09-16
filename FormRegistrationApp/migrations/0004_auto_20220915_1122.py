# Generated by Django 3.1.1 on 2022-09-15 11:22

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('FormRegistrationApp', '0003_auto_20220915_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationdata',
            name='lampiran_file_siswa',
            field=models.FileField(storage=gdstorage.storage.GoogleDriveStorage(permissions=(gdstorage.storage.GoogleDriveFilePermission(gdstorage.storage.GoogleDrivePermissionRole['READER'], gdstorage.storage.GoogleDrivePermissionType['USER'], 'mailing.torche@gmail.com'),)), upload_to='lampiran_siswa/%Y/%m/%d/'),
        ),
    ]
