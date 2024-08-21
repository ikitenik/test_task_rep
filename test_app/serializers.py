from rest_framework import serializers
from .models import Materials


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = ['type', 'material_name', 'material_price']  # Не включайте `material_id`
        read_only_fields = ['material_id']

    def validate_material_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ensure material_price >= 0")
        return value
