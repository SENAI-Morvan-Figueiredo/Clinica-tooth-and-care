from django.views.generic import ListView
from .models import Medico
from .models import Especialidade
from .forms import MedicoForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

# ✅ Detalhar médico
def medico_detail(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    return render(request, 'medicos/medIndex.html', {'medico': medico})

# ✅ Editar médico
def medico_update(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    if request.method == "POST":
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('medico_detail', pk=medico.pk)
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'medicos/medIndex.html', {'form': form})


