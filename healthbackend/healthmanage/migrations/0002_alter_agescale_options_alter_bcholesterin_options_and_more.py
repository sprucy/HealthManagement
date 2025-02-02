# Generated by Django 5.1.5 on 2025-01-29 05:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("healthmanage", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="agescale",
            options={
                "ordering": ["sex", "maxv"],
                "verbose_name": "ICVD Age Criteria",
                "verbose_name_plural": "ICVD Age Criteria",
            },
        ),
        migrations.AlterModelOptions(
            name="bcholesterin",
            options={
                "ordering": ["user", "-measuretime"],
                "verbose_name": "Blood Lipid Info",
                "verbose_name_plural": "Blood Lipid Info",
            },
        ),
        migrations.AlterModelOptions(
            name="bloodpressure",
            options={
                "ordering": ["user", "-measuretime"],
                "verbose_name": "Blood Pressure Info",
                "verbose_name_plural": "Blood Pressure Info",
            },
        ),
        migrations.AlterModelOptions(
            name="bloodpressurescale",
            options={
                "ordering": ["sex", "maxv"],
                "verbose_name": "ICVD Blood Pressure Criteria",
                "verbose_name_plural": "ICVD Blood Pressure Criteria",
            },
        ),
        migrations.AlterModelOptions(
            name="bmiscale",
            options={
                "ordering": ["bmi", "wtype"],
                "verbose_name": "BMI Criteria",
                "verbose_name_plural": "BMI Criteria",
            },
        ),
        migrations.AlterModelOptions(
            name="bodyinfo",
            options={
                "ordering": ["user", "-measuretime"],
                "verbose_name": "Height&Weight Info",
                "verbose_name_plural": "Height&Weight Info",
            },
        ),
        migrations.AlterModelOptions(
            name="commonriskscale",
            options={
                "ordering": ["sex", "age"],
                "verbose_name": "ICVD 10-Year Standard Criteria",
                "verbose_name_plural": "ICVD 10-Year Standard Criteria",
            },
        ),
        migrations.AlterModelOptions(
            name="diabetesscale",
            options={
                "ordering": ["sex", "diabetes"],
                "verbose_name": "ICVD Diabetes Criteria",
                "verbose_name_plural": "ICVD Diabetes Criteria",
            },
        ),
        migrations.AlterModelOptions(
            name="healthintervent",
            options={
                "verbose_name": "Intervene Suggestions",
                "verbose_name_plural": "Intervene Suggestions",
            },
        ),
        migrations.AlterModelOptions(
            name="indicator",
            options={
                "ordering": ["parent_id", "name"],
                "verbose_name": "Health Indicators",
                "verbose_name_plural": "Health Indicators",
            },
        ),
        migrations.AlterModelOptions(
            name="riskanalyse",
            options={
                "verbose_name": "Health Risk Analysis",
                "verbose_name_plural": "Health Risk Analysis",
            },
        ),
        migrations.AlterModelOptions(
            name="riskevaluatscale",
            options={
                "ordering": ["sex", "score"],
                "verbose_name": "ICVD 10-Year Criteria",
                "verbose_name_plural": "ICVD 10-Year Criteria",
            },
        ),
        migrations.AlterModelOptions(
            name="singleassess",
            options={
                "ordering": ["assesstype", "assessname", "minv"],
                "verbose_name": "Single Indicator Criteria",
                "verbose_name_plural": "Single Indicator Criteria",
            },
        ),
        migrations.AlterModelOptions(
            name="smokediabetesinfo",
            options={
                "verbose_name": "Drinking&Diabetes Info",
                "verbose_name_plural": "Drinking&Diabetes Info",
            },
        ),
        migrations.AlterModelOptions(
            name="smokescale",
            options={
                "ordering": ["sex", "smoke"],
                "verbose_name": "ICVD Smoke Criteria",
                "verbose_name_plural": "ICVD Smoke Criteria",
            },
        ),
        migrations.AlterModelOptions(
            name="tcscale",
            options={
                "ordering": ["sex", "maxv"],
                "verbose_name": "ICVD Blood Lipid Criteria",
                "verbose_name_plural": "ICVD Blood Lipid Criteria",
            },
        ),
        migrations.AlterModelOptions(
            name="userinfo",
            options={"verbose_name": "Basic Info", "verbose_name_plural": "Basic Info"},
        ),
        migrations.AlterModelOptions(
            name="weightscale",
            options={
                "ordering": ["sex", "maxv"],
                "verbose_name": "ICVD Weight Criteria",
                "verbose_name_plural": "ICVD Weight Criteria",
            },
        ),
        migrations.AlterField(
            model_name="agescale",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="agescale",
            name="maxv",
            field=models.SmallIntegerField(verbose_name="Max Age"),
        ),
        migrations.AlterField(
            model_name="agescale",
            name="score",
            field=models.SmallIntegerField(verbose_name="Score"),
        ),
        migrations.AlterField(
            model_name="agescale",
            name="sex",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")],
                default="M",
                max_length=1,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="bcholesterin",
            name="HDL",
            field=models.DecimalField(
                decimal_places=2, max_digits=4, verbose_name="HDL(mmol/L)"
            ),
        ),
        migrations.AlterField(
            model_name="bcholesterin",
            name="LDL",
            field=models.DecimalField(
                decimal_places=2, max_digits=4, verbose_name="LDL(mmol/L)"
            ),
        ),
        migrations.AlterField(
            model_name="bcholesterin",
            name="TC",
            field=models.DecimalField(
                decimal_places=2, max_digits=4, verbose_name="TC(mmol/L)"
            ),
        ),
        migrations.AlterField(
            model_name="bcholesterin",
            name="TG",
            field=models.DecimalField(
                decimal_places=2, max_digits=4, verbose_name="TG(mmol/L)"
            ),
        ),
        migrations.AlterField(
            model_name="bcholesterin",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="bcholesterin",
            name="measuretime",
            field=models.DateTimeField(unique=True, verbose_name="Measure Time"),
        ),
        migrations.AlterField(
            model_name="bcholesterin",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="bloodpressure",
            name="DBP",
            field=models.SmallIntegerField(verbose_name="DBP(mmHg)"),
        ),
        migrations.AlterField(
            model_name="bloodpressure",
            name="HR",
            field=models.SmallIntegerField(verbose_name="Heart Rate"),
        ),
        migrations.AlterField(
            model_name="bloodpressure",
            name="SBP",
            field=models.SmallIntegerField(verbose_name="SBP(mmHg)"),
        ),
        migrations.AlterField(
            model_name="bloodpressure",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="bloodpressure",
            name="measuretime",
            field=models.DateTimeField(unique=True, verbose_name="Measure Time"),
        ),
        migrations.AlterField(
            model_name="bloodpressure",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="bloodpressurescale",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="bloodpressurescale",
            name="maxv",
            field=models.SmallIntegerField(verbose_name="SBP Max Value"),
        ),
        migrations.AlterField(
            model_name="bloodpressurescale",
            name="score",
            field=models.SmallIntegerField(verbose_name="Score"),
        ),
        migrations.AlterField(
            model_name="bloodpressurescale",
            name="sex",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")],
                default="M",
                max_length=1,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="bmiscale",
            name="bmi",
            field=models.DecimalField(
                decimal_places=2, max_digits=4, verbose_name="BMI Value"
            ),
        ),
        migrations.AlterField(
            model_name="bmiscale",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="bmiscale",
            name="wtype",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="healthmanage.indicator",
                verbose_name="Weight Classification",
            ),
        ),
        migrations.AlterField(
            model_name="bodyinfo",
            name="height",
            field=models.DecimalField(
                decimal_places=2, max_digits=5, verbose_name="Height(cm)"
            ),
        ),
        migrations.AlterField(
            model_name="bodyinfo",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="bodyinfo",
            name="measuretime",
            field=models.DateTimeField(unique=True, verbose_name="Measure Time"),
        ),
        migrations.AlterField(
            model_name="bodyinfo",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="bodyinfo",
            name="waist",
            field=models.DecimalField(
                decimal_places=2, max_digits=4, verbose_name="Waist(cm)"
            ),
        ),
        migrations.AlterField(
            model_name="bodyinfo",
            name="weight",
            field=models.DecimalField(
                decimal_places=2, max_digits=5, verbose_name="Weight(kg)"
            ),
        ),
        migrations.AlterField(
            model_name="commonriskscale",
            name="age",
            field=models.SmallIntegerField(verbose_name="Age"),
        ),
        migrations.AlterField(
            model_name="commonriskscale",
            name="avgrisk",
            field=models.DecimalField(
                decimal_places=1, max_digits=3, verbose_name="Average Risk%"
            ),
        ),
        migrations.AlterField(
            model_name="commonriskscale",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="commonriskscale",
            name="minrisk",
            field=models.DecimalField(
                decimal_places=1, max_digits=3, verbose_name="Min Risk%"
            ),
        ),
        migrations.AlterField(
            model_name="commonriskscale",
            name="sex",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")],
                default="M",
                max_length=1,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="diabetesscale",
            name="diabetes",
            field=models.BooleanField(verbose_name="Whether Diabetes"),
        ),
        migrations.AlterField(
            model_name="diabetesscale",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="diabetesscale",
            name="score",
            field=models.SmallIntegerField(verbose_name="Score"),
        ),
        migrations.AlterField(
            model_name="diabetesscale",
            name="sex",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")],
                default="M",
                max_length=1,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="healthintervent",
            name="hmtype",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="healthmanage.indicator",
                verbose_name="Risk Types",
            ),
        ),
        migrations.AlterField(
            model_name="healthintervent",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="healthintervent",
            name="intervent",
            field=models.CharField(
                max_length=254, verbose_name="Intervene Suggestions"
            ),
        ),
        migrations.AlterField(
            model_name="indicator",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="indicator",
            name="name",
            field=models.CharField(
                max_length=30, unique=True, verbose_name="Indicator Name"
            ),
        ),
        migrations.AlterField(
            model_name="indicator",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="parents",
                to="healthmanage.indicator",
                verbose_name="Upper Class",
            ),
        ),
        migrations.AlterField(
            model_name="riskanalyse",
            name="hmtype",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="healthmanage.indicator",
                verbose_name="Risk Types",
            ),
        ),
        migrations.AlterField(
            model_name="riskanalyse",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="riskanalyse",
            name="risk",
            field=models.CharField(max_length=254, verbose_name="Risk"),
        ),
        migrations.AlterField(
            model_name="riskevaluatscale",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="riskevaluatscale",
            name="risk",
            field=models.DecimalField(
                decimal_places=1, max_digits=3, verbose_name="Rsik Value%"
            ),
        ),
        migrations.AlterField(
            model_name="riskevaluatscale",
            name="score",
            field=models.SmallIntegerField(verbose_name="Score"),
        ),
        migrations.AlterField(
            model_name="riskevaluatscale",
            name="sex",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")],
                default="M",
                max_length=1,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="singleassess",
            name="assessname",
            field=models.CharField(max_length=30, verbose_name="Indicator Criteria"),
        ),
        migrations.AlterField(
            model_name="singleassess",
            name="assesstype",
            field=models.CharField(max_length=30, verbose_name="Indicator Type"),
        ),
        migrations.AlterField(
            model_name="singleassess",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="singleassess",
            name="maxv",
            field=models.FloatField(verbose_name="Max Indicator Criteria"),
        ),
        migrations.AlterField(
            model_name="singleassess",
            name="minv",
            field=models.FloatField(verbose_name="Min Indicator Criteria"),
        ),
        migrations.AlterField(
            model_name="smokediabetesinfo",
            name="diabetes",
            field=models.BooleanField(
                db_index=True, default=False, verbose_name="Diabetes"
            ),
        ),
        migrations.AlterField(
            model_name="smokediabetesinfo",
            name="diabetesstart",
            field=models.DateField(
                blank=True, default=None, null=True, verbose_name="Diabetes Startime"
            ),
        ),
        migrations.AlterField(
            model_name="smokediabetesinfo",
            name="drink",
            field=models.BooleanField(
                db_index=True, default=False, verbose_name="Drinking"
            ),
        ),
        migrations.AlterField(
            model_name="smokediabetesinfo",
            name="drinkstart",
            field=models.DateField(
                blank=True, default=None, null=True, verbose_name="Drinking Startime"
            ),
        ),
        migrations.AlterField(
            model_name="smokediabetesinfo",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="smokediabetesinfo",
            name="smoke",
            field=models.BooleanField(
                db_index=True, default=False, verbose_name="Smoke"
            ),
        ),
        migrations.AlterField(
            model_name="smokediabetesinfo",
            name="smokestart",
            field=models.DateField(
                blank=True, default=None, null=True, verbose_name="Smoke Startime"
            ),
        ),
        migrations.AlterField(
            model_name="smokediabetesinfo",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Usename",
            ),
        ),
        migrations.AlterField(
            model_name="smokescale",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="smokescale",
            name="score",
            field=models.SmallIntegerField(verbose_name="Score"),
        ),
        migrations.AlterField(
            model_name="smokescale",
            name="sex",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")],
                default="M",
                max_length=1,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="smokescale",
            name="smoke",
            field=models.BooleanField(verbose_name="Whether Smoke"),
        ),
        migrations.AlterField(
            model_name="tcscale",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="tcscale",
            name="maxv",
            field=models.DecimalField(
                decimal_places=2, max_digits=4, verbose_name="Max cholesterol"
            ),
        ),
        migrations.AlterField(
            model_name="tcscale",
            name="score",
            field=models.SmallIntegerField(verbose_name="Score"),
        ),
        migrations.AlterField(
            model_name="tcscale",
            name="sex",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")],
                default="M",
                max_length=1,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="address",
            field=models.CharField(
                default=None, max_length=60, null=True, verbose_name="Address"
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="birthday",
            field=models.DateField(verbose_name="BirthDay"),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="city",
            field=models.CharField(
                default="Shenyang", max_length=16, verbose_name="City"
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="job",
            field=models.CharField(
                default="Engineer", max_length=20, verbose_name="Position"
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="org",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=30,
                null=True,
                verbose_name="Company",
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="phone",
            field=models.CharField(max_length=11, verbose_name="Phone"),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="photo",
            field=models.ImageField(
                blank=True, default=None, upload_to="", verbose_name="Photo"
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="province",
            field=models.CharField(
                db_index=True,
                default="Liaoning",
                max_length=16,
                verbose_name="Province",
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="sex",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")],
                db_index=True,
                default="M",
                max_length=1,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="ssn",
            field=models.CharField(max_length=18, null=True, verbose_name="ID Number"),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Username",
            ),
        ),
        migrations.AlterField(
            model_name="weightscale",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="weightscale",
            name="maxv",
            field=models.SmallIntegerField(verbose_name="BMI Max Value"),
        ),
        migrations.AlterField(
            model_name="weightscale",
            name="score",
            field=models.SmallIntegerField(verbose_name="Score"),
        ),
        migrations.AlterField(
            model_name="weightscale",
            name="sex",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")],
                default="M",
                max_length=1,
                verbose_name="Gender",
            ),
        ),
    ]
