# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'categories'


class MaterialTypes(models.Model):
    type_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='types')
    type_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'material_types'


class Materials(models.Model):
    material_id = models.AutoField(primary_key=True)
    type = models.ForeignKey(MaterialTypes, on_delete=models.CASCADE, related_name='materials')
    material_name = models.TextField()
    material_price = models.DecimalField(max_digits=11, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'materials'
