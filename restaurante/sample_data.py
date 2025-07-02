# sample_data.py - Ejecutar en Django shell (python manage.py shell)
from restaurante.models import Categoria, Producto
from decimal import Decimal

# Crear categorías
categorias_data = [
    {'nombre': 'Platos Principales', 'descripcion': 'Los mejores platos de la cocina colombiana'},
    {'nombre': 'Sopas', 'descripcion': 'Sopas tradicionales y caldos nutritivos'},
    {'nombre': 'Bebidas', 'descripcion': 'Bebidas naturales y refrescantes'},
    {'nombre': 'Postres', 'descripcion': 'Dulces tradicionales colombianos'},
    {'nombre': 'Entradas', 'descripcion': 'Aperitivos y entradas para compartir'}
]

for cat_data in categorias_data:
    categoria, created = Categoria.objects.get_or_create(
        nombre=cat_data['nombre'],
        defaults={'descripcion': cat_data['descripcion']}
    )
    if created:
        print(f"Categoría creada: {categoria.nombre}")

# Obtener categorías para asignar productos
platos_principales = Categoria.objects.get(nombre='Platos Principales')
sopas = Categoria.objects.get(nombre='Sopas')
bebidas = Categoria.objects.get(nombre='Bebidas')
postres = Categoria.objects.get(nombre='Postres')
entradas = Categoria.objects.get(nombre='Entradas')

# Crear productos de ejemplo
productos_data = [
    # Platos Principales
    {
        'nombre': 'Bandeja Paisa',
        'descripcion': 'El plato más tradicional de Antioquia con frijoles, arroz, chicharrón, chorizo, morcilla, carne molida, huevo frito, arepa y aguacate.',
        'precio': Decimal('25000'),
        'categoria': platos_principales
    },
    {
        'nombre': 'Sancocho Antioqueño',
        'descripcion': 'Sancocho tradicional con costilla de res, pollo, mazorca, yuca, plátano, papa y cilantro cimarrón.',
        'precio': Decimal('18000'),
        'categoria': platos_principales
    },
    {
        'nombre': 'Pescado a la Plancha',
        'descripcion': 'Filete de pescado fresco a la plancha acompañado de arroz con coco, patacones y ensalada.',
        'precio': Decimal('22000'),
        'categoria': platos_principales
    },
    
    # Sopas
    {
        'nombre': 'Ajiaco Santafereño',
        'descripcion': 'Sopa tradicional bogotana con pollo, papa criolla, papa sabanera, mazorca y guascas.',
        'precio': Decimal('15000'),
        'categoria': sopas
    },
    {
        'nombre': 'Sancocho de Gallina',
        'descripcion': 'Sancocho preparado con gallina criolla, ñame, yuca, plátano verde y condimentos naturales.',
        'precio': Decimal('16000'),
        'categoria': sopas
    },
    
    # Bebidas
    {
        'nombre': 'Jugo de Lulo',
        'descripcion': 'Refrescante jugo natural de lulo, una fruta exótica colombiana.',
        'precio': Decimal('5000'),
        'categoria': bebidas
    },
    {
        'nombre': 'Agua de Panela con Limón',
        'descripcion': 'Bebida tradicional colombiana preparada con panela y limón natural.',
        'precio': Decimal('4000'),
        'categoria': bebidas
    },
    {
        'nombre': 'Chicha Morada',
        'descripcion': 'Bebida refrescante de maíz morado con especias y frutas.',
        'precio': Decimal('6000'),
        'categoria': bebidas
    },
    
    # Postres
    {
        'nombre': 'Tres Leches',
        'descripcion': 'Delicioso postre de bizcocho empapado en tres tipos de leche y cubierto con merengue.',
        'precio': Decimal('8000'),
        'categoria': postres
    },
    {
        'nombre': 'Flan de Caramelo',
        'descripcion': 'Suave flan casero bañado en caramelo líquido.',
        'precio': Decimal('7000'),
        'categoria': postres
    },
    
    # Entradas
    {
        'nombre': 'Empanadas Antioqueñas',
        'descripcion': 'Empanadas tradicionales rellenas de carne y papa, acompañadas de ají.',
        'precio': Decimal('3000'),
        'categoria': entradas
    },
    {
        'nombre': 'Patacones con Guacamole',
        'descripción': 'Plátanos verdes fritos acompañados de guacamole casero.',
        'precio': Decimal('8000'),
        'categoria': entradas
    }
]

# Crear productos
for prod_data in productos_data:
    producto, created = Producto.objects.get_or_create(
        nombre=prod_data['nombre'],
        defaults={
            'descripcion': prod_data['descripcion'],
            'precio': prod_data['precio'],
            'categoria': prod_data['categoria'],
            'disponible': True
        }
    )
    if created:
        print(f"Producto creado: {producto.nombre} - ${producto.precio}")

print("\n¡Datos de prueba creados exitosamente!")
print("Puedes acceder al admin en: http://127.0.0.1:8000/admin/")
print("Y ver tu restaurante en: http://127.0.0.1:8000/")