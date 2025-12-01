from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Consulta, DisponibilidadeMedico
from django.shortcuts import get_object_or_404
from medicos.models import Medico 

