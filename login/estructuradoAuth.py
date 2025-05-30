from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages  

def adminAuth(modelo_relacionado):
    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login_admin/')

            if not hasattr(request.user, modelo_relacionado):
                messages.error(request, "No tienes permisos para acceder a esta página.")
                return redirect('/') 

            return vista(request, *args, **kwargs)
        return envoltura
    return decorador

def clienteAuth(modelo_relacionado):
    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login/')
            if not hasattr(request.user, modelo_relacionado): 
                return redirect('/') 
            return vista(request, *args, **kwargs)
        return envoltura
    return decorador

def corredorAuth(modelo_relacionado):
    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login/')
            if not hasattr(request.user, modelo_relacionado):
                return redirect('/') 
            return vista(request, *args, **kwargs)
        return envoltura
    return decorador

def duenoAuth(modelo_relacionado):
    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login/')
            if not hasattr(request.user, modelo_relacionado):
                return redirect('/')
            return vista(request, *args, **kwargs)
        return envoltura
    return decorador
