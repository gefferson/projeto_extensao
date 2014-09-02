from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
import hashlib

from core.forms import *

modelforms = {
    'A': AlunoForm,
    'P': ServidorForm,
}

groups = {
    'A': 'Alunos',
    'P': 'Professores',
}

def clean_number(number_field):
    number = ''
    if number_field is not None:
        for elem in number_field:
            if elem in '0123456789':
                number += elem
    return number

def auth_and_login(request, uname=None, passwd=None):
    user = authenticate(
        username=request.POST.get('username') if uname is None else uname,
        password=request.POST.get('password') if passwd is None else passwd,
    )
    login(request, user)
    return user

def hashp(passwd, salt, alg):
    """Returns the passwd + salt encrypted (with alg) using the same
    syntax which Django uses to store the user's passwords.
    """
    return "%s$%s$%s" % \
        (alg, salt, getattr(hashlib, alg)(salt + passwd).hexdigest(),)


def set_user_group(user, tipo):
    g = Group.objects.get(name=groups[tipo])
    g.user_set.add(user)