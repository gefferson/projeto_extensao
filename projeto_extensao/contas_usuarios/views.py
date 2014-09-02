from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.forms import Form
from django.contrib.auth.models import User
from django.shortcuts import (
    HttpResponseRedirect,
    render_to_response,
    Http404,
)

from contas_usuarios import legacy_db
import utils
from extencao import settings
from core.models import *


def registro(request):
    nextpage = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    if request.user.is_authenticated():
        return HttpResponseRedirect(nextpage)
    POST = request.POST
    auth_form = AuthenticationForm(data=POST or None)
    if auth_form.is_valid():
        utils.auth_and_login(request)
        return HttpResponseRedirect(nextpage)
    else:
        pessoadb = legacy_db.get_pessoafisica(POST.get('username'))
        if pessoadb is not None:
            salt = pessoadb.password[5:17]
            if pessoadb.password == utils.hashp(POST.get('password'), salt, 'sha1'):
                data = legacy_db.pessoa_from_legacy(pessoadb)
                modelform = utils.modelforms.get(pessoadb.tipo, Form)
                request.session['password'] = POST.get('password')
                form = modelform(data=data or None)
                return render_to_response(
                    "registro.html",
                    RequestContext(request, {'form': form})
                )
    return render_to_response(
        "login.html",
        RequestContext(request, {'next': nextpage, 'form': auth_form})
    )


def perfil(request):
    if request.user.is_authenticated():
        user = Pessoa.objects.get(id=request.user.id)
        form = utils.modelforms.get(user.tipo, None)
        model = form._meta.model if form is not None else None
        obj = None
        if model is not None:
            obj = model.objects.get(username=user.username)
        if model is Aluno:
            return render_to_response(
                'detalhe_aluno.html', RequestContext(request, {'aluno': obj})
            )
        else:
            return render_to_response(
                'detalhe_servidor.html', RequestContext(request, {'servidor': obj})
            )
    else:
        if request.method == "POST":
            tipo = request.POST.get('tipo')
            modelform = utils.modelforms.get(tipo, Form)
            form = modelform(data=request.POST or None)
            if form.is_valid():
                form.save()
                u = User.objects.get(username=request.POST.get('username'))
                utils.set_user_group(u, tipo)
                request.POST = request.POST.copy()
                request.POST['password'] = request.session['password']
                print request.POST
                utils.auth_and_login(request)
                return HttpResponseRedirect('/')
        else:
            print 'enter here'
            raise Http404()