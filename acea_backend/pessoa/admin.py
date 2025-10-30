from django.contrib import admin
from .models import Aluno,Professor,Administrador,Presidente

admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Administrador)
admin.site.register(Presidente)
