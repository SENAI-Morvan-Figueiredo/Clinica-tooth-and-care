from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from consultas.models import Consulta
from consultas.forms import ConsultaForm
from pacientes.models import Paciente

# ======================================================
# 🔹 AGENDAR CONSULTA (PACIENTE)
# ======================================================
#@login_required
def agendar_consulta(request):
    """
    Permite ao paciente agendar uma nova consulta.
    """
    # Obter o paciente associado ao usuário logado
    try:
        paciente = Paciente.objects.get(user=request.user)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('pagina-inicial')

    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente  # 🔹 ASSOCIA AO PACIENTE LOGADO
            consulta.save()
            
            messages.success(request, f"Consulta agendada com sucesso para {consulta.data}!")
            return redirect("consultas-lista")
        else:
            messages.error(request, "Erro ao agendar consulta. Verifique os dados.")
    else:
        form = ConsultaForm()

    # Consultas futuras do paciente
    consultas_futuras = Consulta.objects.filter(
        paciente=paciente, 
        data__gte=timezone.now().date()
    ).order_by("data", "horario")

    contexto = {
        "form": form,
        "consultas": consultas_futuras,
        "paciente": paciente,
        "nome_usuario": paciente.nome,
    }
    return render(request, "paciente/consulta/crud.html", contexto)

# ======================================================
# 🔹 LISTA DE CONSULTAS DO PACIENTE
# ======================================================
#@login_required
def consulta_lista(request):
    """
    Lista todas as consultas do paciente logado.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('pagina-inicial')

    consultas = Consulta.objects.filter(paciente=paciente).order_by("-data", "-horario")
    form = ConsultaForm()
    
    contexto = {
        "consultas": consultas,
        "form": form,
        "paciente": paciente,
        "nome_usuario": paciente.nome,
    }
    return render(request, "paciente/consulta/crud.html", contexto)

# ======================================================
# 🔹 CRIAR CONSULTA (ATUALIZADA)
# ======================================================
#@login_required
def consulta_criar(request):
    """
    Cria uma nova consulta para o paciente logado.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('pagina-inicial')

    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente  # 🔹 ASSOCIA AO PACIENTE
            consulta.save()
            
            messages.success(request, f"Consulta agendada com sucesso para {consulta.data}!")
            return redirect("consultas-lista")
        else:
            messages.error(request, "Erro ao agendar consulta. Verifique os dados.")
    else:
        form = ConsultaForm()

    consultas = Consulta.objects.filter(paciente=paciente).order_by("-data", "-horario")
    
    return render(request, "paciente/consulta/crud.html", {
        "form": form,
        "consultas": consultas,
        "paciente": paciente,
        "nome_usuario": paciente.nome,
    })

# ======================================================
# 🔹 EDITAR CONSULTA (ATUALIZADA)
# ======================================================
#@login_required
def consulta_editar(request, consulta_id):
    """
    Edita uma consulta existente do paciente logado.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
        consulta = get_object_or_404(Consulta, id=consulta_id, paciente=paciente)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('pagina-inicial')

    if request.method == "POST":
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, f"Consulta atualizada com sucesso!")
            return redirect("consultas-lista")
    else:
        form = ConsultaForm(instance=consulta)

    consultas = Consulta.objects.filter(paciente=paciente).order_by("-data", "-horario")

    return render(request, "paciente/consulta/crud.html", {
        "form": form,
        "consultas": consultas,
        "consulta": consulta,
        "consulta_editando": True,
        "paciente": paciente,
        "nome_usuario": paciente.nome,
    })

# ======================================================
# 🔹 EXCLUIR CONSULTA (ATUALIZADA)
# ======================================================
#@login_required
def consulta_excluir(request, consulta_id):
    """
    Exclui uma consulta do paciente logado.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
        consulta = get_object_or_404(Consulta, id=consulta_id, paciente=paciente)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('pagina-inicial')

    consulta.delete()
    messages.success(request, "Consulta excluída com sucesso!")
    return redirect("consultas-lista")
