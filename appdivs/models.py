from django.db import models
from django.contrib import admin 

# Create your models here.
class Client(models.Model):
    user_cl = models.CharField(max_length=200, unique = True)
    num_peticiones =  models.IntegerField(default=0)
    num_allowed =  models.IntegerField(default=0)

    # Muestra este valor en el campo de llave foranea
    def __str__(self):
        return "%s" % (self.user_cl)

class ClientsAdmin(admin.ModelAdmin):
    search_fields = ['user_cl']
    list_display = ('user_cl', 'num_peticiones', 'num_allowed')

class Banco(models.Model):
    bc_code = models.CharField(max_length=20, unique = True)
    bc_name = models.CharField(max_length=400, unique = True)

    # Muestra este valor en el campo de llave foranea
    def __str__(self):
        return "%s %s" % (self.bc_code, self.bc_name)

class BancoAdmin(admin.ModelAdmin):
    search_fields = ['bc_code', 'bc_name']
    list_display = ('bc_code', 'bc_name')


class Petition(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    fecha_peticion = models.DateField()
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=20, default='')
    
class PetitionAdmin(admin.ModelAdmin):
    search_fields = ['client__user_cl', 'fecha_peticion', 'banco__bc_code']
    list_display = ('client', 'fecha_peticion', 'banco', 'ip_address')
    
    
class Divisas(models.Model):
    fecha_consulta = models.DateField()
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    compra =  models.FloatField()
    venta =  models.FloatField()

    
class DivisasAdmin(admin.ModelAdmin):
    search_fields = ['banco__bc_code', 'banco__bc_name', 'fecha_consulta']
    list_display = ('banco', 'fecha_consulta', 'compra', 'venta')