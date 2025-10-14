from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from consultas.models import Consulta
from consultas.forms import ConsultaForm


def consulta_lista(request):
    consultas = Consulta.objects.all().order_by("-data")
    form = ConsultaForm()
    return render(request, "paciente/consulta/crud.html", {
        "consultas": consultas,
        "form": form
    })


def consulta_criar(request):
    consultas = Consulta.objects.all().order_by("-data")

    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save()
            messages.success(request, f"Consulta ID {consulta.id} criada com sucesso!")
            return redirect("consultas-lista")
    else:
        form = ConsultaForm()

    return render(request, "paciente/consulta/crud.html", {
        "form": form,
        "consultas": consultas
    })


def consulta_editar(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    consultas = Consulta.objects.all().order_by("-data")

    if request.method == "POST":
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, f"Consulta ID {consulta.id} atualizada com sucesso!")
            return redirect("consultas-lista")
    else:
        form = ConsultaForm(instance=consulta)

    return render(request, "paciente/consulta/crud.html", {
        "form": form,
        "consultas": consultas,
        "consulta": consulta,
        "consulta_editando": True
    })


def consulta_excluir(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    consulta.delete()
    messages.success(request, f"Consulta ID {consulta_id} excluída com sucesso!")
    return redirect("consultas-lista")
