from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tarea
from .forms import TareaForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def lista_tareas(request):
    print("Usuario:", request.user)

    tareas = Tarea.objects.filter(usuario=request.user)

    # Búsqueda
    buscar = request.GET.get('buscar')
    if buscar:
        tareas = tareas.filter(titulo__icontains=buscar)

    # Filtro por estado
    estado = request.GET.get('estado')
    if estado == 'pendientes':
        tareas = tareas.filter(completada=False)
    elif estado == 'completadas':
        tareas = tareas.filter(completada=True)

    # Ordenamiento por fecha
    orden = request.GET.get('orden')
    if orden == 'antiguas':
        tareas = tareas.order_by('creada')
    else:
        tareas = tareas.order_by('-creada')  # Por defecto: más recientes primero

    # Paginación
    paginator = Paginator(tareas, 5)
    pagina = request.GET.get('page')
    tareas_paginadas = paginator.get_page(pagina)

    return render(request, 'tareas/lista_tareas.html', {
        'tareas': tareas_paginadas,
        'estado_actual': estado,
        'buscar_actual': buscar,
        'orden_actual': orden,
    })



@login_required
def agregar_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = request.user  # Asocia la tarea al usuario logueado
            tarea.save()
            return redirect('lista_tareas')  # Redirige a la lista de tareas después de agregar
    else:
        form = TareaForm()
    
    return render(request, 'tareas/agregar_tarea.html', {'form': form})

@login_required
def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    tarea.completada = True
    tarea.save()
    return redirect('lista_tareas')

@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('lista_tareas')
    return render(request, 'tareas/confirmar_eliminar.html', {'tarea': tarea})

@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    
    if request.method == 'POST':
        tarea.titulo = request.POST['titulo']
        tarea.descripcion = request.POST['descripcion']
        tarea.save()
        return redirect('lista_tareas')

    return render(request, 'tareas/editar_tarea.html', {'tarea': tarea})