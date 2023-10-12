from django.db import migrations


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunSQL(
            sql="CREATE SCHEMA IF NOT EXISTS content;",
            reverse_sql="DROP SCHEMA IF EXISTS content CASCADE;",
        )
    ]
