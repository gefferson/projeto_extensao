from django.db import models

# Create your models here.


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