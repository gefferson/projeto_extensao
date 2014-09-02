from django.db import models

from contas_usuarios.utils import clean_number


def get_user(login):
    legacy_user = LegacyUser.objects.filter(pk=login)
    return legacy_user[0] if len(legacy_user) > 0 else None


class LegacyUser(models.Model):
    matricula = models.CharField(max_length=135, primary_key=True)
    password = models.CharField(max_length=58)
    email = models.CharField(max_length=150, blank=True)
    tipo = models.CharField(max_length=9, blank=True)

    class Meta:
        db_table = 'usuario_academico'


def get_pessoafisica(login):
    leg_pf = LegacyPessoaFisica.objects.filter(matricula=login)
    return leg_pf[0] if len(leg_pf) > 0 else None


def pessoa_from_legacy(pessoadb):
    """Cria tanto aluno como professor para a base local, com base
    nos dados da base do sistema da secretaria."""
    p = LegacyPessoaFisica.objects.get(pk=pessoadb.matricula)
    data = {field.attname: getattr(p, field.attname) for field in p._meta.fields}
    data['username'] = pessoadb.matricula
    data['cpf'] = clean_number(data['cpf'])
    data['cep'] = clean_number(data['cep'])
    if pessoadb.tipo == 'P':
        del data['curso']
    return data


class LegacyPessoaFisica(models.Model):
    matricula = models.CharField(max_length=135, primary_key=True)
    email = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=58, blank=True)
    tipo = models.CharField(max_length=9)
    cpf = models.CharField(max_length=42, blank=True)
    rg = models.CharField(max_length=45, blank=True)
    orgao_expedidor = models.CharField(max_length=135, blank=True)
    nacionalidade = models.CharField(max_length=90, blank=True)
    first_name = models.CharField(max_length=165, blank=True)
    last_name = models.CharField(max_length=165, blank=True)
    telefone = models.CharField(max_length=135, blank=True)
    curso = models.CharField(max_length=600, blank=True)
    rua = models.CharField(max_length=135, blank=True)
    numero = models.CharField(max_length=24, blank=True)
    complemento = models.CharField(max_length=60, blank=True)
    bairro = models.CharField(max_length=135, blank=True)
    cep = models.CharField(max_length=27, blank=True)
    municipio = models.CharField(max_length=135, blank=True)

    class Meta:
        db_table = 'pessoa_fisica_academico'