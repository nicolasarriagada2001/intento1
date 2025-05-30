from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from dueno.models import Dueno
from dueno.forms import DuenoRegistroForm
from cliente.models import Cliente
from django.contrib import messages
from cliente.forms import ClienteForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if hasattr(user, 'adminuser'):
                return redirect('/administrador/index/')
            elif hasattr(user, 'dueno'):
                return redirect('/dueno/index/')
            elif hasattr(user, 'cliente'):
                return redirect('/cliente/index/')
            elif hasattr(user, 'corredor'):
                return redirect('/corredor/index/')
            else:
                messages.error(request, 'Usuario No Autenticado con Exito!')
                logout(request)
        else:
            messages.error(request, 'Credenciales No Validas!!')
    return render(request, 'login/login.html')
# ////////////////////////////////////////////////////////////

# Logout Terminado (No tocar)
def logout_view(request):
    logout(request)
    return redirect('/login/')
# ///////////////////////////////////////////////////////////

# Area de Registros permitidos!!
def registro_dueno(request):
    if request.method == 'POST':
        form = DuenoRegistroForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            dueno = form.save(commit=False)
            dueno.user = user
            dueno.save()
            return redirect('/login/')
        else:
            print(form.errors)
    else:
        form = DuenoRegistroForm()

    return render(request, 'login/registro_dueno.html', {'form': form})

    
# /////////////////////////////////////////////////////////////
def registro_cliente(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = ClienteForm(request.POST)

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está registrado. Elige otro.")
            return redirect('registro_cliente')

        if form.is_valid():
            email = form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                messages.error(request, "El correo electrónico ya está en uso.")
                return redirect('registro_cliente')

            # Crear usuario
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Asociar al cliente
            cliente = form.save(commit=False)
            cliente.user = user
            cliente.save()

            messages.success(request, "Cuenta creada exitosamente.")
            return redirect('login')
        else:
            messages.error(request, "Formulario inválido. Revisa los datos.")

    else:
        form = ClienteForm()

    return render(request, 'login/registro_cliente.html', {'form': form})