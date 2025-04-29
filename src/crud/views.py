from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q  # Import para consultas OR

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        print(f"Datos recibidos: username={username}, email={email}, password={password}, password_confirm={password_confirm}")

        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'sign-up.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            print(f"Usuario creado: {user}")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '¡Registro exitoso!', extra_tags='new_user')
                return redirect('index')
            else:
                print("Error al autenticar al usuario después del registro.")
                
        except Exception as e:
            print(f"Error al registrar usuario: {str(e)}")
            messages.error(request, f'Error al registrar: {str(e)}')
            return render(request, 'sign-up.html')

    return render(request, 'sign-up.html')

def sign_in(request):
    if request.method == 'GET':
        return render(request, 'sign-in.html')
    else:
        identifier = request.POST.get('username')  # Cambiado de 'email' a 'username'
        password = request.POST.get('password')

        print(f"Intentando iniciar sesión con: identifier={identifier}, password={password}")

        try:
            user = User.objects.get(Q(username=identifier) | Q(email=identifier))
            print(f"Usuario encontrado: {user}")
        except User.DoesNotExist:
            user = None
            print("Usuario no encontrado.")

        if user is not None:
            user = authenticate(request, username=user.username, password=password)
            if user is None:
                print("Error al autenticar al usuario.")
        else:
            print("No se encontró un usuario con el identificador proporcionado.")

        if user is None:
            messages.error(request, '¡Usuario y/o Contraseña Incorrectos!')
            return render(request, 'sign-in.html')

        else:
            login(request, user)
            print(f"Usuario autenticado y logueado: {user}")
            if 'recuerdame' in request.POST:
                request.session.set_expiry(1209600)  # 2 semanas
            else:
                request.session.set_expiry(0)  # Cerrar sesión al cerrar navegador

            return redirect('index')

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('sign_in')

def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, '¡Sesión cerrada exitosamente!')
    else:
        messages.error(request, 'No hay ninguna sesión activa.')

    return redirect('sign_in')