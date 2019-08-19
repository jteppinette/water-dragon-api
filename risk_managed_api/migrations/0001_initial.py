# Generated by Django 2.2.4 on 2019-08-18 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=160)),
                ('planner_name', models.CharField(max_length=80)),
                ('planner_mobile', models.CharField(max_length=80)),
                ('planner_email', models.EmailField(max_length=254)),
                ('president_email', models.EmailField(max_length=254)),
                ('sober_monitors', models.TextField()),
                ('expected_guest_count', models.IntegerField()),
                ('exclusivity', models.CharField(choices=[('Invitation Only', 'Invitation Only'), ('Open to the public', 'Open to the public'), ('Open to Faculty, Staff, Students', 'Open to Faculty, Staff, Students')], max_length=80)),
                ('alcohol_distribution', models.TextField(blank=True, null=True)),
                ('entry', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=80)),
                ('entry_description', models.CharField(max_length=160)),
                ('co_sponsored_description', models.TextField(blank=True, null=True)),
                ('transportation', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('acronym', models.CharField(max_length=80)),
                ('state', models.CharField(max_length=30)),
                ('longitude', models.CharField(blank=True, max_length=20, null=True)),
                ('latitude', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'Universities',
            },
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(choices=[('Interior Sweep', 'Interior Sweep'), ('Exterior Sweep', 'Exterior Sweep')], max_length=80)),
                ('completion_time', models.DateTimeField(blank=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='procedures', to='risk_managed_api.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Nationals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nationals', to='risk_managed_api.Organization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Nationals',
            },
        ),
        migrations.CreateModel(
            name='Invitee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=80)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitees', to='risk_managed_api.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=80)),
                ('dob', models.DateField()),
            ],
            options={
                'verbose_name': 'Identity',
                'verbose_name_plural': 'Identities',
                'unique_together': {('first_name', 'last_name', 'gender', 'dob')},
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=False)),
                ('administrator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hosts', to='risk_managed_api.Administrator')),
                ('nationals', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hosts', to='risk_managed_api.Nationals')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosts', to='risk_managed_api.Organization')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosts', to='risk_managed_api.University')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reach', models.CharField(choices=[('Nationals', 'Nationals'), ('Administrator', 'Administrator'), ('Host', 'Host')], max_length=80)),
                ('violation', models.CharField(choices=[('Underage Drinking', 'Underage Drinking'), ('Stealing', 'Stealing'), ('Vandalism', 'Vandalism'), ('Violence', 'Violence'), ('Probation', 'Probation'), ('Other', 'Other')], max_length=80)),
                ('other', models.CharField(blank=True, max_length=80, null=True)),
                ('administrator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flags', to='risk_managed_api.Administrator')),
                ('host', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flags', to='risk_managed_api.Host')),
                ('identity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flags', to='risk_managed_api.Identity')),
                ('nationals', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flags', to='risk_managed_api.Nationals')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='risk_managed_api.Host'),
        ),
        migrations.AddField(
            model_name='administrator',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='administrators', to='risk_managed_api.University'),
        ),
        migrations.AddField(
            model_name='administrator',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='GuestRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/guests')),
                ('date_time_taken', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='risk_managed_api.Event')),
                ('identity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='risk_managed_api.Identity')),
            ],
            options={
                'unique_together': {('identity', 'event')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('host', 'name', 'date')},
        ),
        migrations.CreateModel(
            name='CarbonCopyAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Carbon Copy Address',
                'verbose_name_plural': 'Carbon Copy Addresses',
                'unique_together': {('user', 'email')},
            },
        ),
    ]