from django.contrib import admin

from .models import Client, ClientsAdmin, Petition, PetitionAdmin, Banco, BancoAdmin, Divisas, DivisasAdmin

admin.site.register(Client, ClientsAdmin)
admin.site.register(Petition, PetitionAdmin)
admin.site.register(Banco, BancoAdmin)
admin.site.register(Divisas, DivisasAdmin)


