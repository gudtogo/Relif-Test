from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Client
from clients.serializers import *
from rest_framework.decorators import api_view, permission_classes
from utils import IsActiveModel
from django.http import JsonResponse
from django.views import View
import openai
import datetime
from dotenv import load_dotenv
import os

load_dotenv()


class ClientController(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Client.objects.all()
        serializer = ClientSerializer(queryset, many=True, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format="json", *args, **kwargs):
        data = request.data
        serializer = CreateClientSerializer(data=data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GenerateMessageView(View):
    def get(self, request, client_uuid, *args, **kwargs):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        try:
            client = Client.objects.get(uuid=client_uuid)
        except Client.DoesNotExist:
            return JsonResponse({'error': 'Client not found'}, status=404)

        prompt = (
            f"Genera un mensaje de venta de automóviles para {client.name}. "
            "Ofrecemos autos nuevos de las marcas Toyota, Ford y Honda. "
            "Nuestras sucursales están ubicadas en Santiago, Viña del Mar y Concepción. "
            "También ofrecemos financiamiento, pero solo para clientes sin deudas morosas. "
            "Asegúrate de que el mensaje suene humano y amable."
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo", 
                messages=[
                    {"role": "system", "content": "Eres un asistente de ventas."},
                    {"role": "user", "content": prompt}
                ]
            )

            generated_message = response.choices[0].message.content
            return JsonResponse({'generated_message': generated_message}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def get_client(request, client_uuid):
    
    queryset = Client.objects.filter(uuid=client_uuid)
    serializer = ClientSerializer(queryset, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_clients_to_follow_up(request):
    queryset = Client.objects.filter(messages__sentAt__lte=datetime.date.today() - datetime.timedelta(days=7))
    serializer = ClientSerializer(queryset, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)
   
@api_view(['POST'])
def post_message(request, client_uuid):
    try:
        client = Client.objects.get(uuid=client_uuid)
    except Client.DoesNotExist:
        return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    data['client'] = client

    serializer = MessageSerializer(data=data, context={"request": request})

    if serializer.is_valid():
        serializer.save(client=client)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)