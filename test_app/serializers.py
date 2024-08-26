from rest_framework import serializers
from .models import Materials, MaterialTypes, Categories
from django.db.models import Sum
import logging
logger = logging.getLogger(__name__)


# Выводим материалы в виде дерева с подсчетом сумм
class MaterialSerializer(serializers.ModelSerializer):
    # Определяем начальные поля сериализатора модели Materials
    class Meta:
        model = Materials
        fields = ['material_id', 'type', 'material_name', 'material_price']
        read_only_fields = ['material_id']

    # Проверка корректности ввода цены
    def validate_material_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Стоимость материала не может быть отрицательной")
        return value
    
    # Переопределение инициализации сериализатора для вывода плоского списка
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        condition = context.get('condition')
        super(MaterialSerializer, self).__init__(*args, **kwargs)
        # Если надо вывести плоский список
        if condition == 'list':
            # Берём данные по внешнему ключу
            self.fields["category_info"] = serializers.SerializerMethodField()
            #self.fields["type_name"] = serializers.CharField(source='type.type_name', read_only=True)
            self.fields["type_info"] = serializers.SerializerMethodField()
            # Добавляем перед выводом название справочника
            self.fields["dict_name"] = serializers.SerializerMethodField()
            self.fields = {
                'dict_name': self.fields['dict_name'],
                'category_info': self.fields['category_info'],
                'type_info': self.fields['type_info'],
                'material_id': self.fields['material_id'],
                'material_name': self.fields['material_name'],
                'material_price': self.fields['material_price']
            }

    def get_dict_name(self, obj):
        return "Автомобильные запчасти"

    def get_type_info(self, obj):
        serializer = MaterialTypesSerializer(obj.type)
        return {
            'type_id': serializer.data.get('type_id'),
            'type_name': serializer.data.get('type_name')
        }

    def get_category_info(self, obj):
        serializer = CategoriesSerializer(obj.type.category)
        return serializer.data

# Сериализатор для типов материалов
class MaterialTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialTypes
        fields = ['type_id', 'category', 'type_name']
        read_only_fields = ['type_id']

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        condition = context.get('condition')
        super(MaterialTypesSerializer, self).__init__(*args, **kwargs)
        if condition == 'tree':
            self.Meta.fields = ['type_id', 'type_name']
            self.fields['type_price'] = serializers.SerializerMethodField()
            self.fields['materials'] = MaterialSerializer(many=True)

    def get_type_price(self, obj):
        # Используем метод aggregate для подсчета общей стоимости
        return obj.materials.aggregate(type_price=Sum('material_price'))['type_price'] or 0


# Сериализатор для категорий
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category_id', 'category_name']
        read_only_fields = ['category_id']

# Для вывода в виде дерева
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        condition = context.get('condition')
        super(CategoriesSerializer, self).__init__(*args, **kwargs)
        if condition == 'tree':
            self.fields['category_price'] = serializers.SerializerMethodField()
            self.fields['types'] = serializers.SerializerMethodField()

    def get_category_price(self, obj):
        # Считаем сумму всех материалов во всех типах, связанных с категорией
        return obj.types.aggregate(category_price=Sum('materials__material_price'))['category_price'] or 0

    def get_types(self, obj):
        serializer = MaterialTypesSerializer(obj.types.all(), many=True, context={'condition': "tree"})
        return serializer.data


