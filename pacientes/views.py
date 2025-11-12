from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from consultas.models import Consulta
from consultas.forms import ConsultaForm
from pacientes.models import Paciente


# ===================== CONSULTAS =====================

@login_required
def consulta_lista(request):
    """
    Lista todas as consultas do paciente logado.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('/')

    consultas = Consulta.objects.filter(paciente=paciente).order_by("-data")
    form = ConsultaForm()

    contexto = {
        "consultas": consultas,
        "form": form,
        "paciente": paciente,
        "today": timezone.now().date(),
    }
    return render(request, "paciente/consulta/crud.html", contexto)


@login_required
def consulta_criar_ou_editar(request, consulta_id=None):
    """
    Cria ou edita uma consulta para o paciente logado.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('/')

    consulta = None
    if consulta_id:
        consulta = get_object_or_404(Consulta, id=consulta_id, paciente=paciente)

    if request.method == "POST":
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            consulta.save()
            messages.success(request, f"Consulta {'atualizada' if consulta_id else 'agendada'} com sucesso!")
            return redirect("paciente-consultas")
        else:
            messages.error(request, "Erro ao salvar consulta. Verifique os dados.")
    else:
        form = ConsultaForm(instance=consulta)

    consultas = Consulta.objects.filter(paciente=paciente).order_by("-data")

    return render(request, "paciente/consulta/crud.html", {
        "form": form,
        "consultas": consultas,
        "consulta": consulta,
        "consulta_editando": bool(consulta_id),
        "paciente": paciente,
        "today": timezone.now().date(),
    })


@login_required
def consulta_excluir(request, consulta_id):
    """
    Exclui uma consulta do paciente logado.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
        consulta = get_object_or_404(Consulta, id=consulta_id, paciente=paciente)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('/')

    consulta.delete()
    messages.success(request, "Consulta excluída com sucesso!")
    return redirect("paciente-consultas")


# ===================== INFORMAÇÕES PESSOAIS =====================

@login_required
def informacoes_pessoais(request):
    """
    Exibe/edita informações pessoais do paciente.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('/')

    editing = request.GET.get('edit', 'false').lower() == 'true'
    consultas = Consulta.objects.filter(paciente=paciente).order_by("-data")

    if request.method == "POST" and editing:
        # Atualiza os campos do paciente
        paciente.nome = request.POST.get('nome')
        paciente.data_nasc = request.POST.get('data_nascimento')
        paciente.genero = request.POST.get('sexo')
        paciente.cpf = request.POST.get('cpf')
        paciente.rg = request.POST.get('rg')
        paciente.endereco = request.POST.get('endereco')
        paciente.telefone = request.POST.get('telefone')
        paciente.user.email = request.POST.get('email')
        paciente.user.save()
        paciente.save()
        messages.success(request, "Informações atualizadas com sucesso!")
        return redirect('informacoes-pessoais')

    context = {
        "paciente": paciente,
        "editing": editing,
        "consultas": consultas,
    }
    return render(request, "paciente/consulta/historico_paciente.html", context)
