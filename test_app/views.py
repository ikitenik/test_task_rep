from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .models import Materials, MaterialTypes, Categories
from .serializers import MaterialSerializer, MaterialTypesSerializer, CategoriesSerializer
import pandas as pd


class CategoriesAPIView(APIView):
    def get_object(self, pk):
        try:
            return Categories.objects.get(pk=pk)
        except Categories.DoesNotExist:
            raise Http404

    def get(self, request, param=None, pk=None):
        # Вывод плоским списком
        if param == "list":
            categories = Materials.objects.all()
            categories_serializer = MaterialSerializer(categories, many=True, context={'condition': "list"})
            return Response(categories_serializer.data, status=status.HTTP_200_OK)

        # Вывод деревом
        elif param == "tree":
            categories = Categories.objects.prefetch_related('types__materials').all()
            categories_serializer = CategoriesSerializer(categories, many=True, context={'condition': "tree"})
            data = {
                'car_dict': {
                    'name': 'Автомобильные запчасти',
                    'categories': categories_serializer.data
                }
            }
            return Response(data, status=status.HTTP_200_OK)

        # Вывод только категорий
        elif not param:
            if pk:
                category = self.get_object(pk)
                serializer = CategoriesSerializer(category)
            else:
                categories = Categories.objects.all()
                serializer = CategoriesSerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Категория успешно добавлена', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    def put(self, request, pk=None):
        category = self.get_object(pk)
        serializer = CategoriesSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Категория успешно обновлена', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        type = self.get_object(pk)
        type.delete()
        return Response({'message': 'Категория успешно удалена'})


class MaterialTypesAPIView(APIView):
    def get_object(self, pk):
        try:
            return MaterialTypes.objects.get(pk=pk)
        except MaterialTypes.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            material_types = self.get_object(pk)
            serializer = MaterialTypesSerializer(material_types)
        else:
            material_types = MaterialTypes.objects.all()
            serializer = MaterialTypesSerializer(material_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MaterialTypesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Тип материала успешно создан', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    def put(self, request, pk=None):
        material_types = self.get_object(pk)
        serializer = MaterialTypesSerializer(material_types, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Тип материала успешно обновлен', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        material_types = self.get_object(pk)
        material_types.delete()
        return Response({'message': 'Тип материала успешно удалён'})


class MaterialAPIView(APIView):
    def get_object(self, pk):
        try:
            return Materials.objects.get(pk=pk)
        except Materials.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            material = self.get_object(pk)
            serializer = MaterialSerializer(material)
        else:
            materials = Materials.objects.all()
            serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Материал успешно добавлен в справочник', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        material = self.get_object(pk)
        serializer = MaterialSerializer(material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Данные материала успешно обновлены', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        material = self.get_object(pk)
        material.delete()
        return Response({'message': 'Материал успешно удалён из справочника'})


class UploadExcelAPIView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Файл не загружен'}, status=400)
        # Чтение Excel с помощью pandas
        excel_file = pd.read_excel(file)
        # Список для хранения сериализованных данных
        created_objects = []
        # Список для хранения ошибок сериализации
        errors = []
        for _, row in excel_file.iterrows():
            data = {
                'type': row.get('type_id'),
                'material_name': row.get('material_name'),
                'material_price': row.get('material_price')
            }

            serializer = MaterialSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                created_objects.append(serializer.data)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({'Ошибки': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Добавленные материалы': created_objects}, status=status.HTTP_201_CREATED)
