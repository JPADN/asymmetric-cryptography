from django.contrib import admin
from .models import Post
from .models import Ac_certificado, Certificados_emitidos, Contador


admin.site.register(Post)
admin.site.register(Ac_certificado)
admin.site.register(Certificados_emitidos)
admin.site.register(Contador)
