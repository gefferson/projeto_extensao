#encoding: utf-8

from django.contrib import admin

from models import Servidor, Aluno, Projeto, Modalidade, Ediatal_ano
from core.forms import ServidorForm

#Remover sites
from django.contrib.sites.models import Site


class EditalAdmin(admin.ModelAdmin):
    list_display = ['edital','data_cadastro']
    search_fields = ['edital','data_cadastro']

admin.site.register(Ediatal_ano, EditalAdmin)


class ServidorAdmin(admin.ModelAdmin):

    list_display = ['first_name', 'last_name','titulacao','ramal','email','banco','agencia']
    search_fields = ['first_name', 'last_name','titulacao', 'ramal']
    form = ServidorForm

admin.site.register(Servidor, ServidorAdmin)

class AlunoAdmin(admin.ModelAdmin):

    list_display = ['first_name','curso','email','banco','agencia']
    search_fields = ['first_name', 'last_name']

admin.site.register(Aluno, AlunoAdmin)

class ProjetoAdmin(admin.ModelAdmin):

    filter_horizontal = ('bolsistas','professor_participante','aluno_participante')
    # raw_id_fields = ('bolsistas','professor_participante','aluno_participante')
    # filter_vertical = ('bolsistas','professor_participante','aluno_participante')

    # ,'data_inicio','data_fim'
    list_display = ['titulo','coordenador','edital_ano','ativo']
    search_fields = ['coordenador__first_name',
                     'coordenador__last_name',
                     'titulo',
                     'bolsistas__last_name',
                     'bolsistas__first_name',
                     'aluno_participante__last_name',
                     'aluno_participante__first_name']


admin.site.register(Projeto, ProjetoAdmin)

class ModalidadeAdmin(admin.ModelAdmin):

    list_display = ['modalidade']

admin.site.register(Modalidade, ModalidadeAdmin)

#Remover Sites
admin.site.unregister(Site)


