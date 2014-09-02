#encoding: utf-8

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

from core.forms import ContatoForm, AlunoForm, ServidorForm, ProjetoForm, EditalFom, ModalidadeForm
from models import *
from admin import ProjetoAdmin, AlunoAdmin, ServidorAdmin

def in_stats_group(user):
    if user:
        return user.groups.filter(name='StatsGroup').count() == 1
    return False

def home(request):
    return render(request, 'home.html')

def contato(request):
    context = { }
    if request.method=='POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.send_mail()
            context['sucesso'] = True
    else:
        form = ContatoForm()
    context['form'] = form
    return render(request, 'contato.html', context)

@login_required()
def curso(request):
    if request.method=='POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            cadastro = form.save(commit=False)
            cadastro.save()
            print (form.cleaned_data['nome'])
            form = CursoForm()
    else:
        form = CursoForm
    context={}
    context['form'] = form
    context['curso'] = Curso.objects.all().order_by('-data_inicio') #mudar para ordem alfabetica
    return render(request, 'curso.html', context)

@login_required()
def aluno(request):
    if request.method=='POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            cadastro = form.save(commit=False)
            cadastro.save()
            form = AlunoForm()
    else:
        form = AlunoForm
    context={}
    context['form'] = form
    context['aluno'] = Aluno.objects.all()
    return render(request, 'aluno.html', context)

@login_required()
@user_passes_test(in_stats_group)
def edital(request):
    if request.method=='POST':
        form = EditalFom(request.POST)
        if form.is_valid():
            cadastro = form.save(commit=False)
            cadastro.save()
            form = EditalFom()
    else:
        form = EditalFom
    context={}
    context['form'] = form
    context['edital'] = Ediatal_ano.objects.all()
    return render(request, 'edital.html', context)

@login_required()
@user_passes_test(in_stats_group)
def modalidade(request):
    if request.method=='POST':
        form = ModalidadeForm(request.POST)
        if form.is_valid():
            cadastro = form.save(commit=False)
            cadastro.save()
            form = ModalidadeForm()
    else:
        form = ModalidadeForm
    context={}
    context['form'] = form
    context['modalidade'] = Modalidade.objects.all()
    return render(request, 'modalidade.html', context)

# @login_required()
# @user_passes_test(in_stats_group)
# def status(request):
#     if request.method=='POST':
#         form = StatusForm(request.POST)
#         if form.is_valid():
#             cadastro = form.save(commit=False)
#             cadastro.save()
#             form = StatusForm()
#     else:
#         form = StatusForm
#     context={}
#     context['form'] = form
#     context['status'] = Status.objects.all()
#     return render(request, 'status.html', context)

# @login_required()
# @user_passes_test(in_stats_group)
# def titulo(request):
#     if request.method=='POST':
#         form = TituloForm(request.POST)
#         if form.is_valid():
#             cadastro = form.save(commit=False)
#             cadastro.save()
#             form = TituloForm()
#     else:
#         form = TituloForm
#     context={}
#     context['form'] = form
#     context['titulo'] = Titulo.objects.all()
#     return render(request, 'titulo.html', context)

@login_required()
def servidor(request):
    if request.method=='POST':
        form = ServidorForm(request.POST)
        if form.is_valid():
            cadastro = form.save(commit=False)
            cadastro.save()
            form = ServidorForm()
    else:
        form = ServidorForm
    context={}
    context['form'] = form
    context['servidor'] = Servidor.objects.all()
    return render(request, 'servidor.html', context)


@login_required()
def projeto(request, slug = None):
    if request.method=='POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            cadastro = form.save()
            cadastro.save()
            form = ProjetoForm()
            #redirect(slug) rever para direcionar direcionar para projeto
    # else:
    #     if slug != None:
    #         form = ProjetoForm(instance=get_object_or_None(Projeto, slug=slug))
    # esta parte refere-se a editar o projeto cadastrado
    else:
        form = ProjetoForm
    context={}
    context['form'] = form
    return render(request, 'projeto.html', context)

@login_required()
# @user_passes_test(in_stats_group) desbloquear somente para admin
def estatistica(request):
    context={}
    context['contagem_projeto'] = len(Projeto.objects.all().order_by())
    context['contagem_alunos'] = len(Aluno.objects.all())
    context['contagem_servidores'] = len(Servidor.objects.all())
    return render(request, 'estastistica.html', context)

def lista_projetos(request):
    context={}
    if request.method == "POST":
        if request.POST['query'] != "":
            context['lista_projetos'] = search(Projeto, request.POST['query'], ProjetoAdmin.search_fields )
        else:
            context['lista_projetos'] = Projeto.objects.all()
    else:
        context['lista_projetos'] = Projeto.objects.all()
    return render(request, 'lista_projetos.html', context)

def detalhe_projeto(request, slug):
    projeto = get_object_or_404(Projeto, slug=slug)
    context={}
    context['projeto'] = projeto
    context['slug'] = slug
    context['coordenador'] = projeto.coordenador
    context['titulo'] = projeto.titulo
    context['ativo'] = projeto.ativo
    context['modalidade'] = projeto.modalidade
    context['data_inicio'] = projeto.data_inicio
    context['data_fim'] = projeto.data_fim
    context['status'] = projeto.status
    context['edital'] = projeto.edital_ano
    context['alunos_participantes'] = [aluno['nome']
        for aluno in projeto.aluno_participante.values('first_name')]
    context['professores_participantes'] = [professor['first_name']
        for professor in projeto.professor_participante.values('first_name')]
    context['bolsistas'] = [bolsista['bolsistas']
        for bolsista in projeto.bolsistas.values('bolsistas')]
    context['pdf'] = projeto.pdf
    return render(request, 'detalhe_projeto.html', context)


def lista_alunos(request):
    context={}
    if request.method == 'POST':
        if request.POST['query'] != "":
            alunos = search(Aluno, request.POST['query'], AlunoAdmin.search_fields)
        else:
            alunos = Aluno.objects.all()
    else:
        alunos = Aluno.objects.all()
    dados_aluno = []
    for aluno in alunos:
        nome = aluno.first_name + ' ' + aluno.last_name
        dados_aluno.append([aluno.get_absolut_url(),
                            nome,
                            aluno.curso,
                            aluno.email,
                            Projeto.objects.filter(bolsistas=aluno).count(),
                            Projeto.objects.filter(aluno_participante=aluno).count()])
    context['lista_alunos'] = dados_aluno
    return render(request, 'lista_alunos.html', context)

def detalhe_aluno(request, slug):
    aluno = get_object_or_404(Aluno, slug=slug)
    context={}
    context['aluno'] = aluno
    context['curso'] = aluno.curso
    context['email'] = aluno.email
    context['telefone'] = aluno.telefone
    context['banco'] = aluno.banco
    context['agencia'] = aluno.agencia
    context['conta'] = aluno.conta
    projetos_bolsista = []
    projetos_participante = []
    for projeto in aluno.bolsistas.all():
        projetos_bolsista.append([projeto.slug, projeto.titulo])
    for projeto in aluno.aluno_participante.all():
        projetos_participante.append([projeto.slug, projeto.titulo])
    context['projetos_bolsista'] = projetos_bolsista
    context['projetos_participante'] = projetos_participante
    return render(request, 'detalhe_aluno.html', context)


def lista_servidores(request):
    context={}
    if request.method == 'POST':
        if request.POST['query'] != "":
            servidores = search(Servidor, request.POST['query'], ServidorAdmin.search_fields)
        else:
            servidores = Servidor.objects.all()
    else:
        servidores = Servidor.objects.all()
    dados_servidor = []
    for servidor in servidores:
        nome = servidor.first_name + ' ' + servidor.last_name
        dados_servidor.append([servidor.get_absolut_url(),
                               nome,
                               servidor.titulacao,
                               servidor.ramal,
                               servidor.email,
                               Projeto.objects.filter(coordenador_id=servidor.id).count(),
                               Projeto.objects.filter(professor_participante=servidor).count()])
    context['lista_servidores'] = dados_servidor
    return render(request, 'lista_servidores.html', context)

def detalhe_servidor(request, slug):
    servidor = get_object_or_404(Servidor, slug=slug)
    context={}
    context['servidor'] = servidor
    context['titulo'] = servidor.titulacao
    context['ramal'] = servidor.ramal
    context['email'] = servidor.email
    context['telefone'] = servidor.telefone
    context['cpf'] = servidor.cpf
    context['banco'] = servidor.banco
    context['agencia'] = servidor.agencia
    context['conta'] = servidor.conta
    servidor_coordenador = []
    servidor_professor_participante = []
    for coordenador in servidor.coordenador.all():
        servidor_coordenador.append([coordenador.slug, coordenador.titulo])
    for professor_participante in servidor.professor_participante.all():
        servidor_professor_participante.append([professor_participante.slug, professor_participante.titulo])
    context['servidor_coordenador'] = servidor_coordenador
    context['servidor_professor_participante'] = servidor_professor_participante
    return render(request, 'detalhe_servidor.html', context)

def lista_cursos(request):
    context={}
    cursos = []
    if request.method == 'POST':
        if request.POST['query'] != "":
            cursos = search(Curso, request.POST['query'], CursoAdmin.search_fields)
        else:
            cursos = Curso.objects.all().order_by('data_inicio') # Alterar para ordem alfabética
    else:
        cursos = Curso.objects.all().order_by('data_inicio') # Alterar para ordem alfabética
    dados_cursos = []
    for curso in cursos:
        dados_cursos.append([curso.nome, curso.data_inicio, Aluno.objects.filter(curso__nome=curso.nome).count()])
    context['dados_cursos'] = dados_cursos
    return render(request, 'lista_cursos.html', context)

# Pesquisa
def search(model, keywords, search_fields):
    """Search according to fields defined in Admin's search_fields"""
    all_queries = None

    for keyword in keywords.split(' '):  #breaks query_string into 'Foo' and 'Bar'
        keyword_query = None

        for field in search_fields:
            each_query = Q(**{field+'__icontains':keyword})

            if not keyword_query:
                keyword_query = each_query
            else:
                keyword_query = keyword_query | each_query

        if not all_queries:
            all_queries = keyword_query
        else:
            all_queries = all_queries & keyword_query

    result_set = model.objects.filter(all_queries).distinct()

    return result_set


