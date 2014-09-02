#encoding: utf-8

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from datetimewidget.widgets import DateTimeWidget
from django_localflavor_br.forms import BRCPFField, BRPhoneNumberField
from input_mask.contrib.localflavor.br.widgets import BRPhoneNumberInput, BRCPFInput
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from core.models import Servidor, Projeto, Aluno, Ediatal_ano, Modalidade, Pessoa


class PessoaForm(ModelForm):

    cpf = BRCPFField(label='CPF', widget=BRCPFInput)
    telefone = BRPhoneNumberField(widget=BRPhoneNumberInput)
    nome = forms.TextInput()

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()
        self.fields['password'].widget = forms.HiddenInput()
        self.fields['tipo'].widget = forms.HiddenInput()

    class Meta(UserCreationForm.Meta):
        model = Pessoa

        fields = ['first_name', 'last_name', 'email', 'banco', 'agencia', 'conta',
                  'cpf', 'username', 'password', 'telefone', 'tipo']


class ServidorForm(PessoaForm):


    class Meta(PessoaForm.Meta):
        model = Servidor
        verbose_name = 'Servidor'

        fields =  PessoaForm.Meta.fields  + ['ramal', 'titulacao']


class EditalFom(ModelForm):

    class Meta:
        model = Ediatal_ano

        dateTimeOptions = {
        'format': 'dd/mm/yyyy',
        'autoclose': 'true',
        'showMeridian' : 'false',
        'minView': '4',
        'todayBtn' : 'true',
        }

        widgets = {
            'data_cadastro': DateTimeWidget(attrs={'id':"id_data_cadastro   "}, options=dateTimeOptions),
        }

class ModalidadeForm(ModelForm):

    class Meta:
        model = Modalidade

        dateTimeOptions = {
        'format': 'dd/mm/yyyy',
        'autoclose': 'true',
        'showMeridian' : 'false',
        'minView': '4',
        'todayBtn' : 'true',
        }


class AlunoForm(PessoaForm):

    class Meta(PessoaForm.Meta):
        model = Aluno
        verbose_name = 'Aluno'

        fields = PessoaForm.Meta.fields + ['curso',]


class ContatoForm(forms.Form):

    nome = forms.CharField(label=u'Nome', max_length=100)

    email = forms.EmailField(label=u'Email')

    mensagem = forms.CharField(label=u'Mensagem', widget=forms.Textarea)

    def send_mail(self):
        subject = u'E-mail de contato de %s' % self.cleaned_data['nome']
        mensagem = u'E-mail: %s\nMensagem: %s' % (self.cleaned_data['email'], self.cleaned_data['mensagem'])
        send_mail(subject, mensagem, 'no-reply', ['geffersonvivan@gmail.com'])


class ProjetoForm(forms.ModelForm):

    professor_participante = forms.ModelMultipleChoiceField(queryset=Servidor.objects.all(),
                                          label='Professor Participante',
                                          required=False,
                                          widget=FilteredSelectMultiple("Professores Participantes", False))

    bolsistas = forms.ModelMultipleChoiceField(queryset=Aluno.objects.all(),
                                          label='Bolsistas',
                                          required=False,
                                          widget=FilteredSelectMultiple("Bolsistas", False))

    aluno_participante = forms.ModelMultipleChoiceField(queryset=Aluno.objects.all(),
                                          label='Aluno Participante',
                                          required=False,
                                          widget=FilteredSelectMultiple("Participantes", False))


    class Meta:
        model = Projeto
        filter_horizontal = ("bolsistas",)

        dateTimeOptions = {
        'format': 'dd/mm/yyyy',
        'autoclose': 'true',
        'showMeridian' : 'false',
        'minView': '4',
        'todayBtn' : 'true',
        }

        widgets = {
            'data_inicio': DateTimeWidget(attrs={'id':"id_data_inicio"}, options=dateTimeOptions),
            'data_fim': DateTimeWidget(attrs={'id':"id_data_fim"}, options=dateTimeOptions),
            # 'edital_ano': YearWidget(attrs={'id':'edital_ano'}, years=xrange(2000, 2090)),
        }









