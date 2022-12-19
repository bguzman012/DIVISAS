from rest_framework import serializers

from .models import Banco, Divisas

# Create a model serializer
class BancoSerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    class Meta:
        model = Banco
        fields = ('bc_code', 'bc_name')
        
class DivisasSerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    class Meta:
        model = Divisas
        fields = ('venta', 'compra', 'fecha_consulta', 'banco_id')
