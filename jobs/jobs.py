from .utils import *
from appdivs.models import Banco, Divisas
from appdivs.serializers import DivisasSerializer
from datetime import date

def schedule_api():
    divisas = prepare_data_divisas()
   
    for divisa in divisas:
        try:
            banco = Banco.objects.get(bc_name = divisa['nombre_banco'])
        except Banco.DoesNotExist:
            continue
        
        divisas = Divisas(id=None, venta=divisa['val_venta'], compra=divisa['val_compra'], 
                    fecha_consulta= date.today(), banco=banco)
        
        divisas.save()
        
    