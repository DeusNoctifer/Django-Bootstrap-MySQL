from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def sign_in(request):
    
    if request.method == 'GET':
        return render(request, 'sign_in.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is None:
            messages.error(request, '¡Correo y/o Contraseña Incorrectos!')
            return render(request, 'sign_in.html')

        else:
            login(request, user)
            if 'recuerdame' in request.POST:
                print("Recuerdame: Sí")
                request.session.set_expiry(1209600)
            else:
                print("Recuerdame: No")
                request.session.set_expiry(0)

            return redirect('index')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        if not username or not email or not password:
            messages.error(request, 'Usuario, email y contraseña son obligatorios')
            return render(request, 'sign_up.html')
            
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'sign_up.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nombre de usuario ya está registrado')
            return render(request, 'sign_up.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email ya está registrado')
            return render(request, 'sign_up.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '¡Registro exitoso!', extra_tags='new_user')
                return redirect('index')
                
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
            return render(request, 'sign_up.html')

    return render(request, 'sign_up.html')