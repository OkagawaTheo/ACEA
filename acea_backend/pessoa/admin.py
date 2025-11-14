from django.contrib import admin
from .models import Aluno,Professor,Administrador,Presidente,Doador

admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Administrador)
admin.site.register(Presidente)
admin.site.register(Doador)