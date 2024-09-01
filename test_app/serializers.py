from rest_framework import serializers
from .models import Material, Category
from django.db.models import Sum
from mptt.forms import TreeNodeChoiceField
import logging
logger = logging.getLogger(__name__)


# Сериализатор для материалов
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['category', 'name', 'price']

    # Проверка корректности ввода цены
    def validate_material_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Стоимость материала не может быть отрицательной")
        return value


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = TreeCategorySerializer(value, context=self.context)
        return serializer.data


# Сериализатор для категорий в виде дерева
class TreeCategorySerializer(serializers.ModelSerializer):
    # Дочерние категории
    children = RecursiveField(many=True, read_only=True)

    # Материалы в категориях
    materials = MaterialSerializer(many=True, read_only=True)

    # Общая стоимость материалов
    price = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'price', 'children', 'materials')
        extra_kwargs = {
            'parent': {'write_only': True}
        }

    def get_price(self, obj):
        # Считаем стоимость материалов в текущей категории
        current_materials_price = obj.materials.aggregate(total=Sum('price'))['total'] or 0

        # Считаем стоимость материалов в дочерних категориях
        children_total_price = 0

        children = obj.children.all()
        for child in children:
            child_category = Category.objects.get(id=child.id)
            children_total_price += self.get_price(child_category)

        return current_materials_price + children_total_price


# Сериализатор для категорий в виде плоского списка
class FlatCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']
        extra_kwargs = {
            'parent': {'write_only': True}
        }


