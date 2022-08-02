
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from location.gerarPdf import gerarObj
from location.models import Contract, Location

from company.models import Company

from .forms import CompanyForm, CompanyUserChangeForm

# Create your views here.


def login_view(request):

    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':

        cnpj = request.POST.get('cnpjValue')
        print("O CNPJ: ", cnpj)
        password = request.POST.get('password')
        print("PASSWORD: ", password)
        user = authenticate(username=cnpj, password=password)

        if user is not None:
            login(request, user)
            print("USUARIO", user)
            return redirect(reverse('vehicle:indexVehicle'))
            # Redirecione para uma página de sucesso.
        else:
            messages.error(
                request, "Senha ou email Invalidos, tente novamente !")
        return redirect('company:login')


@login_required(login_url='company:login', redirect_field_name='next')
def logout_view(request):

    if not request.POST:
        return redirect(reverse('company:login'))

    logout(request)
    return redirect(reverse('company:login'))


@login_required(login_url='company:login', redirect_field_name='next')
def profile(request):

    form = CompanyForm(instance=request.user)

    if request.POST:
        form = CompanyForm(request.POST, instance=request.user)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.save()
            messages.success(request, "Dados da empresa Alterados")

            # atualizando os contrato de locacoes em andamento
            try:
                for i in Location.objects.filter(id_company=edit, status=True):
                    if Contract.objects.filter(id_location=i).exists():
                        gerarObj(i)
            except:
                pass

        else:
            print('NAO E VALIDOOOO')
    return render(request, 'perfil.html', {'form': form, 'company': request.user})
