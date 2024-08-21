from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .models import Materials
from .serializers import MaterialSerializer
import pandas as pd

# Create your views here.
class MaterialAPIView(APIView):
    '''
    def get(self, request):
        # Получаем набор всех записей из таблицы Capital
        queryset = Materials.objects.all()
        print(f'{queryset=}')
        # Сериализуем извлечённый набор записей
        serializer_for_queryset = MaterialSerializer(
            instance=queryset, # Передаём набор записей
            many=True # Указываем, что на вход подаётся именно набор записей
        )
        return Response(serializer_for_queryset.data)
    '''

    def get_object(self, pk):
        try:
            return Materials.objects.get(pk=pk)
        except Materials.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk:
            material = self.get_object(pk)
            serializer = MaterialSerializer(material)
        else:
            materials = Materials.objects.all()
            serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Detail Created Successfully', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    def put(self, request, pk=None, format=None):
        material = self.get_object(pk)
        serializer = MaterialSerializer(material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Detail Updated Successfully', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        material = self.get_object(pk)
        material.delete()
        return Response({'message': 'Material deleted successfully'})


class UploadExcelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')  # Получаем загруженный файл

        if not file:
            return Response({'error': 'No file uploaded'}, status=400)

        # Чтение Excel-файла с помощью pandas
        excel_file = pd.read_excel(file)

        # Список для хранения сериализованных данных
        created_objects = []
        errors = []
        for _, row in excel_file.iterrows():
            data = {
                'type': row.get('type_id'),  # Замените на имя столбца из Excel
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
            return Response({'errors': errors}, status=400)

        return Response({'created_objects': created_objects}, status=201)
