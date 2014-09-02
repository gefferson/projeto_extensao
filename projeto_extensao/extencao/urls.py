from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',

    #Site
    url(r'^$', 'core.views.home', name='home'),
    url(r'^contato/$', 'core.views.contato', name='contato'),
    url(r'^curso/$','core.views.curso', name='curso'),
    url(r'^projeto/(?P<slug>[\-\d\w]+)/$', 'core.views.projeto', name='projeto'),
    url(r'^estatistica/$', 'core.views.estatistica', name='estatistica'),
    url(r'^edital/$', 'core.views.edital', name='edital'),
    url(r'^modalidade/$', 'core.views.modalidade', name='modalidade'),
    url(r'^perfil/$', 'contas_usuarios.views.perfil', name='perfil'),

    #Login
    url(r'^entrar/$', 'contas_usuarios.views.registro', name='login'),
    url(r'^sair/$', 'django.contrib.auth.views.logout', {'next_page':'/'}, name='logout'),

    #Casdastro Usuarios
    url(r'^contas/', 'contas_usuarios.views.registro', name='registro'),

    # Detalhes
    url(r'^lista_servidores/$', 'core.views.lista_servidores', name='lista_servidores'),
    url(r'^detalhe_servidor/(?P<slug>[\-\d\w]+)/$','core.views.detalhe_servidor', name = 'detalhe_servidor'),
    url(r'^lista_cursos/$', 'core.views.lista_cursos', name='lista_cursos'),
    url(r'^lista_projetos/$', 'core.views.lista_projetos', name='lista_projetos'),
    url(r'^detalhe_projeto/(?P<slug>[\-\d\w]+)/$','core.views.detalhe_projeto', name = 'detalhe_projeto'),
    url(r'^lista_alunos/$', 'core.views.lista_alunos', name='lista_alunos'),
    url(r'^detalhe_aluno/(?P<slug>[\-\d\w]+)/$','core.views.detalhe_aluno', name = 'detalhe_aluno'),


    # Admin
    url(r'^admin/', include(admin.site.urls)),

    #Media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

urlpatterns += staticfiles_urlpatterns()