from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lista_tareas')  # Redirige luego del login
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

