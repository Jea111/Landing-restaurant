from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Categoria, Producto, Pedido, ItemPedido,Usuarios

@login_required
def landing_restaurante(request):
    """Vista principal del restaurante después del login"""
    categorias = Categoria.objects.all()
    productos_destacados = Producto.objects.filter(disponible=True)[:6]
    
    context = {
        'categorias': categorias,
        'productos_destacados': productos_destacados,
        'usuario': request.user
    }
    return render(request, 'restaurante/landing.html', context)

@login_required
def menu_completo(request):
    """Vista del menú completo por categorías"""
    categorias = Categoria.objects.prefetch_related('producto_set').all()
    
    context = {
        'categorias': categorias,
    }
    return render(request, 'restaurante/menu.html', context)

@login_required
def agregar_al_carrito(request):
    """Vista AJAX para agregar productos al carrito"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            cantidad = int(data.get('cantidad', 1))
            
            producto = get_object_or_404(Producto, id=producto_id, disponible=True)
            
            # Guardar en sesión (carrito temporal)
            carrito = request.session.get('carrito', {})
            
            if str(producto_id) in carrito:
                carrito[str(producto_id)]['cantidad'] += cantidad
            else:
                carrito[str(producto_id)] = {
                    'nombre': producto.nombre,
                    'precio': float(producto.precio),
                    'cantidad': cantidad
                }
            
            request.session['carrito'] = carrito
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'mensaje': f'{producto.nombre} agregado al carrito',
                'total_items': sum(item['cantidad'] for item in carrito.values())
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def ver_carrito(request):
    """Vista para mostrar el carrito de compras"""
    carrito = request.session.get('carrito', {})
    total = 0
    items = []
    
    for producto_id, item in carrito.items():
        subtotal = item['precio'] * item['cantidad']
        items.append({
            'id': producto_id,
            'nombre': item['nombre'],
            'precio': item['precio'],
            'cantidad': item['cantidad'],
            'subtotal': subtotal
        })
        total += subtotal
    
    context = {
        'items': items,
        'total': total
    }
    return render(request, 'restaurante/carrito.html', context)

@login_required
def confirmar_pedido(request):
    """Vista para confirmar y procesar el pedido"""
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        
        if not carrito:
            messages.error(request, 'Tu carrito está vacío')
            return redirect('ver_carrito')
        
        # Obtener datos del formulario
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        notas = request.POST.get('notas', '')
        
        if not direccion or not telefono:
            messages.error(request, 'Dirección y teléfono son obligatorios')
            return redirect('ver_carrito')
        
        try:
            # Crear el pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                direccion_entrega=direccion,
                telefono=telefono,
                notas=notas,
            )
            
            # Crear items del pedido
            total = 0
            for producto_id, item in carrito.items():
                producto = Producto.objects.get(id=producto_id)
                item_pedido = ItemPedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item['cantidad'],
                    precio_unitario=producto.precio,
                )
                total += item_pedido.subtotal()
            
            # Actualizar total del pedido
            pedido.total = total
            pedido.save()
            
            # Limpiar carrito
            request.session['carrito'] = {}
            request.session.modified = True
            
            messages.success(request, f'¡Pedido #{pedido.id} realizado exitosamente!')
            return redirect('mis_pedidos')
            
        except Exception as e:
            messages.error(request, f'Error al procesar el pedido: {str(e)}')
            return redirect('ver_carrito')
    
    return redirect('ver_carrito')

@login_required
def mis_pedidos(request):
    """Vista para mostrar los pedidos del usuario"""
    pedidos = Pedido.objects.filter(usuario=request.user).prefetch_related('items__producto')
    
    context = {
        'pedidos': pedidos
    }
    return render(request, 'restaurante/mis_pedidos.html', context)

@login_required
def detalle_pedido(request, pedido_id):
    """Vista para mostrar el detalle de un pedido específico"""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    
    context = {
        'pedido': pedido
    }
    return render(request, 'restaurante/detalle_pedido.html', context)



from django.http import HttpResponse

def usuarios(request):
    if request.method == 'POST':
        
        correo = request.POST['correo']
        password = request.POST['password']
                
        # Verificar si el usuario ya existe
        if not Usuarios.objects.filter(correo=correo).exists(): #Filtra los registros donde el campo 'correo' coincida exactamente con el valor de la variable 'correo'
            Usuarios.objects.create(correo=correo, password=password)
            return render(request,'restaurante/landing.html')
        else:
            return HttpResponse('El usuario ya existe')
    tittle = 'Formulario de Registro'
    return render(request,'restaurante/registro.html',{
            'tittle':tittle,
        })