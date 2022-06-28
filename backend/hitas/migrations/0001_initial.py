# Generated by Django 3.2.13 on 2022-06-28 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import enumfields.fields
import hitas.models.codes
import hitas.models.housing_company
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=1024)),
                ('description', models.TextField(blank=True)),
                ('in_use', models.BooleanField(default=True)),
                ('order', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('legacy_code_number', models.CharField(help_text='Format: 000', max_length=3, unique=True, validators=[hitas.models.codes.validate_code_number])),
                ('legacy_start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('legacy_end_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Building type',
                'verbose_name_plural': 'Building types',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=1024)),
                ('description', models.TextField(blank=True)),
                ('in_use', models.BooleanField(default=True)),
                ('order', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('legacy_code_number', models.CharField(help_text='Format: 000', max_length=3, unique=True, validators=[hitas.models.codes.validate_code_number])),
                ('legacy_start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('legacy_end_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Developer',
                'verbose_name_plural': 'Developers',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FinancingMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=1024)),
                ('description', models.TextField(blank=True)),
                ('in_use', models.BooleanField(default=True)),
                ('order', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('legacy_code_number', models.CharField(help_text='Format: 000', max_length=3, unique=True, validators=[hitas.models.codes.validate_code_number])),
                ('legacy_start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('legacy_end_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Financing methods',
                'verbose_name_plural': 'Financing methods',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HousingCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('official_name', models.CharField(max_length=1024)),
                ('display_name', models.CharField(max_length=1024)),
                ('state', enumfields.fields.EnumIntegerField(default=0, enum=hitas.models.housing_company.HousingCompanyState)),
                ('business_id', models.CharField(help_text='Format: 1234567-8', max_length=9, validators=[hitas.models.housing_company.validate_business_id])),
                ('street_address', models.CharField(max_length=1024)),
                ('acquisition_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('realized_acquisition_price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('primary_loan', models.DecimalField(decimal_places=2, max_digits=15)),
                ('sales_price_catalogue_confirmation_date', models.DateField(blank=True, null=True)),
                ('notification_date', models.DateField(blank=True, null=True)),
                ('legacy_id', models.CharField(blank=True, max_length=10)),
                ('notes', models.TextField(blank=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('building_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hitas.buildingtype')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hitas.developer')),
                ('financing_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hitas.financingmethod')),
                ('last_modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Housing company',
                'verbose_name_plural': 'Housing companies',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PostalCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=1024)),
                ('description', models.TextField(blank=True)),
                ('in_use', models.BooleanField(default=True)),
                ('order', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('legacy_code_number', models.CharField(help_text='Format: 000', max_length=3, unique=True, validators=[hitas.models.codes.validate_code_number])),
                ('legacy_start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('legacy_end_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Postal code',
                'verbose_name_plural': 'Postal codes',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RealEstate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('property_identifier', models.CharField(help_text='Format: 1234-1234-1234-1234', max_length=19, validators=[hitas.models.housing_company.validate_property_id])),
                ('street_address', models.CharField(max_length=1024)),
                ('housing_company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hitas.housingcompany')),
                ('postal_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hitas.postalcode')),
            ],
            options={
                'verbose_name': 'Real estate',
                'verbose_name_plural': 'Real estates',
            },
        ),
        migrations.CreateModel(
            name='PropertyManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('email', models.EmailField(max_length=254)),
                ('street_address', models.CharField(max_length=1024)),
                ('postal_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hitas.postalcode')),
            ],
            options={
                'verbose_name': 'Property manager',
                'verbose_name_plural': 'Property managers',
            },
        ),
        migrations.AddField(
            model_name='housingcompany',
            name='postal_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hitas.postalcode'),
        ),
        migrations.AddField(
            model_name='housingcompany',
            name='property_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hitas.propertymanager'),
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('completion_date', models.DateField(null=True)),
                ('street_address', models.CharField(max_length=1024)),
                ('building_identifier', models.CharField(blank=True, help_text='Format: 100012345A or 91-17-16-1 S 001', max_length=25, validators=[hitas.models.housing_company.validate_building_id])),
                ('housing_company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hitas.housingcompany')),
                ('postal_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hitas.postalcode')),
                ('real_estate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hitas.realestate')),
            ],
            options={
                'verbose_name': 'Building',
                'verbose_name_plural': 'Buildings',
            },
        ),
        migrations.AddConstraint(
            model_name='housingcompany',
            constraint=models.CheckConstraint(check=models.Q(('acquisition_price__gte', 0)), name='acquisition_price_positive'),
        ),
        migrations.AddConstraint(
            model_name='housingcompany',
            constraint=models.CheckConstraint(check=models.Q(('realized_acquisition_price__gte', 0)), name='realized_acquisition_price_positive'),
        ),
    ]
