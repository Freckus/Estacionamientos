from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

def get_media_root():
    return settings.MEDIA_ROOT

def pdf(template_src,context_dict={}):
    template=get_template(template_src)
    context_dict['get_media_root'] = get_media_root
    html=template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='App/reserva')
    return None

def calculadora(llegada,salida):

    diff=llegada-salida
    diff_hours=diff.total_seconds()/3600
    hours =f"cantidad de horas{diff_hours}"
    return diff_hours