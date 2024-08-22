from rest_framework import serializers
from .models import Materials, MaterialTypes, Categories
from django.db.models import Sum

class MaterialTypesSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)

    class Meta:
        model = MaterialTypes
        fields = ['category_name', 'category', 'type_name']
        read_only_fields = ['type_id']

    def to_representation(self, instance):
        """Добавляем dict_name в начало вывода."""
        representation = super().to_representation(instance)
        dict_name = "Автомобильные запчасти"
        return {
            "dict_name": dict_name,
            **representation
        }


class MaterialSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.type_name', read_only=True)
    category_name = serializers.CharField(source='type.category.category_name', read_only=True)

    class Meta:
        model = Materials
        fields = ['category_name', 'type_name', 'type', 'material_name', 'material_price']
        read_only_fields = ['material_id']

    def to_representation(self, instance):
        """Добавляем dict_name в начало вывода."""
        representation = super().to_representation(instance)
        dict_name = "Автомобильные запчасти"
        return {
            "dict_name": dict_name,
            **representation
        }

    def validate_material_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ensure material_price >= 0")
        return value


class TreeMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = ['material_id', 'material_name', 'material_price']


class TreeMaterialTypesSerializer(serializers.ModelSerializer):
    materials = TreeMaterialSerializer(many=True, read_only=True)
    type_price = serializers.SerializerMethodField()

    class Meta:
        model = MaterialTypes
        fields = ['type_name', 'materials', 'type_price']

    def get_type_price(self, obj):
        # Используем метод aggregate для подсчета общей стоимости
        return obj.materials.aggregate(type_price=Sum('material_price'))['type_price'] or 0

class TreeCategoriesSerializer(serializers.ModelSerializer):
    types = TreeMaterialTypesSerializer(many=True, read_only=True)
    category_price = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = ['category_name', 'types', 'category_price']

    def get_category_price(self, obj):
        # Считаем сумму всех материалов во всех типах, связанных с категорией
        return obj.types.aggregate(category_price=Sum('materials__material_price'))['category_price'] or 0




