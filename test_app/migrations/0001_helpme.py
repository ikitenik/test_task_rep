from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        # Укажите зависимости, например, другие миграции, если есть
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                # Поскольку таблицы уже существуют, мы не добавляем операции создания таблиц.
            ],
            state_operations=[
                migrations.CreateModel(
                    name='Categories',
                    fields=[
                        ('category_id', models.AutoField(primary_key=True)),
                        ('category_name', models.TextField()),
                    ],
                    options={
                        'db_table': 'categories',
                        'managed': False,
                    },
                ),
                migrations.CreateModel(
                    name='MaterialTypes',
                    fields=[
                        ('type_id', models.AutoField(primary_key=True)),
                        ('category', models.ForeignKey(on_delete=models.DO_NOTHING, to='test_app.Categories')),
                        ('type_name', models.TextField()),
                    ],
                    options={
                        'db_table': 'material_types',
                        'managed': False,
                    },
                ),
                migrations.CreateModel(
                    name='Materials',
                    fields=[
                        ('material_id', models.AutoField(primary_key=True)),
                        ('type_id', models.ForeignKey(on_delete=models.DO_NOTHING, to='test_app.MaterialTypes')),
                        ('material_name', models.TextField()),
                        ('material_price', models.DecimalField(max_digits=12, decimal_places=3)),
                    ],
                    options={
                        'db_table': 'materials',
                        'managed': False,
                    },
                ),
            ]
        )
    ]
