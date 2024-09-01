from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .models import Material, Category
from .serializers import MaterialSerializer, TreeCategorySerializer, FlatCategorySerializer
import pandas as pd
from rest_framework.viewsets import ModelViewSet


class TreeCategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    # queryset для get-запросов
    def get_queryset(self):
        if self.request.method == 'GET':
            category_id = self.kwargs.get('pk')
            # Если необходимо вывести часть дерева
            if category_id is not None:
                return Category.objects.get(id=category_id).get_family()
            # Если необходимо вывести все дерево
            return Category.objects.filter(parent__isnull=True)

    serializer_class = TreeCategorySerializer


class FlatCategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = FlatCategorySerializer


class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


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
        count = 1
        for _, row in excel_file.iterrows():
            data = {
                'category': row.get('category'),
                'name': row.get('name'),
                'price': row.get('price')
            }

            serializer = MaterialSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                created_objects.append(serializer.data)
            else:
                errors.append(serializer.errors)
                errors.insert(count, {'Данные' : data})
                count += 2

        if errors:
            return Response({'Часть данных добавлена. Недобавленные данные, содержащие ошибки': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Добавленные материалы': created_objects}, status=status.HTTP_201_CREATED)


