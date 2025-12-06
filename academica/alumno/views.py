from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import alumno

# Create your views here.
def holaMundo(request):
    return HttpResponse("hola mundo")

def miEdad(request, edad):
    return HttpResponse(f"Tengo {edad} años, esta edad es la mas genial")

def saludoNombre(request, nombre):
    return HttpResponse(f"Hola {nombre}, bienvenido a la UGB")

def index(request):
    return render(request, 'index.html')

def vistas(request, form):
    return render(request, f"{form}.html")

def consultar_alumnos(request):
    alumnos = list(alumno.objects.values())
    return JsonResponse(alumnos, safe=False)

@csrf_exempt
def guardar_alumnos(request):
    if request.method == "POST":
        data  = json.loads(request.body)
        if( data.get("accion")=="nuevo" ):
            editAlumno = alumno.objects.create(
                codigo = data.get("codigo"),
                nombre = data.get("nombre"),
                direccion = data.get("direccion"),
                telefono = data.get("telefono"),
                email = data.get("email")
            )
        elif( data.get("accion")=="modificar" ):
            editAlumno = alumno.objects.get(id=data.get("idAlumno"))
            editAlumno.codigo = data.get("codigo")
            editAlumno.nombre = data.get("nombre")
            editAlumno.direccion = data.get("direccion")
            editAlumno.telefono = data.get("telefono")
            editAlumno.email = data.get("email")
            editAlumno.save()

        elif( data.get("accion")=="eliminar" ):
            editAlumno = alumno.objects.get(id=data.get("idAlumno"))
            editAlumno.delete()

        return JsonResponse({'msg': 'ok', 'idAlumno': editAlumno.id})
    else:
        return JsonResponse({'msg': 'Metodo no permitido'})