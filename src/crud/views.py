from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from .models import Productos



def es_admin(user):
    return user.is_authenticated and user.is_staff

# Create your views here.
def sign_in(request):
    
    if request.method == 'GET':
        return render(request, 'sign-in.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, '¡Correo y/o Contraseña Incorrectos!')
            return render(request, 'sign-in.html')

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
            return render(request, 'sign-up.html')
            
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'sign-up.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nombre de usuario ya está registrado')
            return render(request, 'sign_up.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email ya está registrado')
            return render(request, 'sign-up.html')
        
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
            return render(request, 'sign-up.html')

    return render(request, 'sign-up.html')

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

