#encoding: utf-8

from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import (
    User, UserManager
)

from core.utils import get_upload_path

class Pessoa(User):

    cpf = models.CharField(max_length=255, verbose_name=u'CPF')

    telefone = models.CharField(max_length=255, verbose_name=u'Telefone', blank=True)

    banco = models.CharField(max_length=255, verbose_name=u'Banco', blank=True)

    agencia = models.IntegerField(max_length=20, verbose_name=u'Agência', blank=True, null=True)

    conta = models.IntegerField(max_length=20, verbose_name=u'Conta Corrente', blank=True, null=True)

    tipo = models.CharField(max_length=1, verbose_name=u'Tipo')

    def _getSlug(self):
        return (self.first_name + '_' + self.last_name).replace(' ','_').lower()

    slug = AutoSlugField(populate_from = _getSlug, max_length=255, unique=True, blank=True, null=True, editable=False)


class Servidor(Pessoa):

    titulacao = models.CharField(max_length=20, verbose_name=u'Títulação')

    ramal = models.IntegerField(max_length=6, null=True, blank=True, verbose_name=u'Ramal')

    class Meta:
        verbose_name = u'Servidor'
        verbose_name_plural = u'Servidores'

    def __unicode__(self):
        return unicode(self.first_name + ' ' + self.last_name)

    def get_absolut_url(self):
        return '/detalhe_servidor/%s' % self.slug

    def save(self):
        super(Servidor, self).save()

class Aluno(Pessoa):

    curso = models.CharField(max_length=255, verbose_name=u'Curso')

    class Meta:
        verbose_name = u'Aluno'
        verbose_name_plural = u'Alunos'

    def __unicode__(self):
        return unicode(self.first_name + ' ' + self.last_name)

    def get_absolut_url(self):
        return '/detalhe_aluno/%s' % self.slug

    def save(self):
        super(Aluno, self).save()


class Modalidade(models.Model):

    modalidade = models.CharField(max_length=255, verbose_name=u'Modalidade')

    class Meta:
        verbose_name = u'Modalidade'
        verbose_name_plural = u'Modalidades'

    def __unicode__(self):
        return unicode(self.modalidade)

class Ediatal_ano(models.Model):

    edital = models.CharField(max_length=255, verbose_name='Edital Ano')

    data_cadastro = models.DateField(verbose_name='Data Cadastro    ', blank=True)

    class Meta:
        verbose_name = u'Edital'
        verbose_name_plural = u'Editais'

    def __unicode__(self):
        return unicode(self.edital)


class Projeto(models.Model):


    coordenador = models.ForeignKey(Servidor, related_name='coordenador',verbose_name=u'Coordenador')

    titulo = models.CharField(max_length=255, verbose_name=u'Título')

    data_inicio = models.DateField(verbose_name=u'Data início', blank=True, null=True)

    data_fim = models.DateField(verbose_name=u'Data fim', blank=True, null=True)

    edital_ano = models.ForeignKey(Ediatal_ano, related_name='edital_ano', verbose_name=u'Edital Ano', blank=True)

    bolsistas = models.ManyToManyField(Aluno, related_name='bolsistas', verbose_name=u'Bolsistas', blank=True)

    professor_participante = models.ManyToManyField(Servidor, related_name='professor_participante', verbose_name=u'Professores participante', blank=True)

    aluno_participante = models.ManyToManyField(Aluno, related_name='aluno_participante', verbose_name=u'Aluno participante', blank=True)

    modalidade = models.ForeignKey(Modalidade, verbose_name=u'Modalidade', blank=True)

    status = models.CharField(max_length=255, verbose_name=u'Status')

    pdf = models.FileField(upload_to=get_upload_path, verbose_name='PDF', null=True, blank=True)

    ativo = models.BooleanField(default=True, verbose_name=u'Projeto ativo?',
                                   help_text='O registro será tratado como ativo. Para bloquear o projeto, desmarque o campo.')

    slug = AutoSlugField(populate_from = 'titulo', max_length=255, unique=True, blank=True, null=True, editable=False)


    class Meta:
        verbose_name = u'Projeto'
        verbose_name_plural = u'Projetos'

    def __unicode__(self):
        return unicode(self.titulo)

    def get_absolut_url(self):
        return '/detalhe_projeto/%s' % self.slug

    def save(self):
        if not self.id:
            self.slug = self.titulo.replace(' ','_').lower()
            while Projeto.objects.filter(slug=self.slug):
                self.slug += '-1'
        super(Projeto, self).save()

# twopi, gvcolor, wc, ccomps, tred, sccmap, fdp, circo, neato, acyclic, nop, gvpr, dot, sfdp