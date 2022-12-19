from django.http import HttpResponse
# import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import *
from datetime import datetime

# import local data
from .serializers import BancoSerializer, DivisasSerializer
from .models import Banco, Divisas, Client, Petition

# create a viewset
class BancoViewSet(APIView):


     # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Banco.objects.all()
        serializer = BancoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        bancos_creados = []

        nombres_bancos = prepare_data_divisas()
        cont = 10
        data_banco = {
                'bc_code': str(cont),
                'bc_name': 'Banco Central'
            }
        banco_central_existe  = Banco.objects.filter(bc_name = 'Banco Central')
        if len(banco_central_existe) == 0:
            bancos_creados.append(data_banco)    
                
        cont += 1
        for banco in nombres_bancos:

            # Si el banco existe, ya no lo crea
            banco_existe  = Banco.objects.filter(bc_name = banco)
            if len(banco_existe) > 0:
                continue

            data = {
                'bc_code': str(cont),
                'bc_name': banco
            }
            bancos_creados.append(data)
            cont += 1
        
        for banco_creado in bancos_creados:    
            serializer = BancoSerializer(data=banco_creado)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'Resultado': 'OK', 'bancos_creados': bancos_creados}, status=status.HTTP_201_CREATED)
            

class DivisasViewSet(APIView):

     # 1. List all
    def get(self, request, *args, **kwargs):
        param_banco_id = request.GET.get('banco_id', None)
        param_fecha = request.GET.get('fecha', None)
        param_user = request.GET.get('user', None)
        format_datetime = '%Y-%m-%d'
        
        if len(param_user) == 0:
            return Response({'Error': 'El usuario ingresado no es correcto'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cliente = Client.objects.get(user_cl = str(param_user))
        except Client.DoesNotExist:
            return Response({'Error': 'El usuario ingresado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            banco_id = int(param_banco_id)
        except:
            return Response({'Error': 'Formato no admitido para codigo de banco'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            banco = Banco.objects.get(bc_code = str(banco_id))
        except Banco.DoesNotExist:
            return Response({'Error': 'Banco con el codigo ingresado no existe'}, status=status.HTTP_400_BAD_REQUEST)

        if cliente.num_allowed == 0:
             return Response({'Error': 'El usuario se encuentra inactivo, por favor comuniquese con el proveedor para más información'}, status=status.HTTP_400_BAD_REQUEST)
        
        if cliente.num_allowed != -1 and cliente.num_peticiones >= cliente.num_allowed:
            return Response({'Error': 'El usuario ingresado no tiene créditos para obtener información, es necesario revor su suscripción'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            fecha = datetime.strptime(param_fecha, format_datetime)
        except:
            return Response({'Error': 'Formato no admitido para fecha de consultas, formato admitido: YYYY-M-D'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_ip = get_ip_address(request)
        petition = Petition(id=None, client = cliente, fecha_peticion=fecha.date(), 
                           banco=banco, ip_address=str(user_ip))
        petition.save()
        
        cliente.num_peticiones += 1
        cliente.save()
        
        divisas = Divisas.objects.filter(banco_id = banco.id, fecha_consulta=fecha.date()) 
        serializer = DivisasSerializer(divisas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        