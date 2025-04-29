
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from .models import Productos
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q  # Import para consultas OR


def es_admin(user):
    return user.is_authenticated and user.is_staff

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
    # Verificar si el usuario es administrador
    if request.user.is_staff:
        # Obtener todos los productos
        productos = Productos.objects.all()
        context = {
            'productos': productos
        }
        
        if request.method == 'POST':
            id = request.POST.get('producto_id')
            producto = Productos.objects.get(id=id)
            producto.Estado = 0
            producto.save()
            
        return render(request, 'index.html', context)
    else:
        # Si no es administrador, mostrar una vista básica
        return render(request, 'index.html')
    

@user_passes_test(es_admin, login_url='index')
def agregar_productos(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        valor_venta = request.POST.get('valor_venta')
        descripcion = request.POST.get('descripcion')
        
        if nombre and cantidad and valor_venta and descripcion:
            producto = Productos(
                Nombre=nombre,
                Cantidad=cantidad,
                ValorVenta=valor_venta,
                Descripcion=descripcion,
                Estado=1
            )
            producto.save()
            messages.success(request, 'Producto agregado exitosamente')
            return redirect('index')
        else:
            messages.error(request, 'Todos los campos son obligatorios')
    
    return render(request, 'agregar_productos.html')   


@user_passes_test(es_admin, login_url='index')
def eliminar(request, idProducto):
    producto = get_object_or_404(Productos, id=idProducto)
    producto.delete()
    return redirect('index')

@user_passes_test(es_admin, login_url='index')
def actualizar_producto(request, idProducto):
    producto = get_object_or_404(Productos, id=idProducto)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        valor_venta = request.POST.get('valor_venta')
        descripcion = request.POST.get('descripcion')
        Estado = request.POST.get('Estado')
        
        if nombre and cantidad and valor_venta and descripcion and Estado:
            producto.Nombre = nombre
            producto.Cantidad = cantidad
            producto.ValorVenta = valor_venta
            producto.Descripcion = descripcion
            producto.Estado = Estado
            producto.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('index')
        else:
            messages.error(request, 'Todos los campos son obligatorios')
    
    context = {
        'producto': producto
    }
    return render(request, 'actualizar_producto.html', context)

