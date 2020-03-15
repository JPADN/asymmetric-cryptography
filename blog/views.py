from django.shortcuts import render
from OpenSSL import crypto
from .models import Certificados_emitidos, Ac_certificado, Contador
from .utils import gerar_cert, gerar_chave
import rsa
import json

# --------------------- Neste arquivo definimos as rotas da aplicação -------------------- #

message = {'restart': True}

# A geração de certificados depende dos objetos de cypto.X509 e crypto.PKey
# Tendo em vista a impossibilidade de armazenar estes no banco de dados, como explicado na rota Home
# Torna-se necessário registrar uma nova AC cada vez que a aplicação reinicia, pois desta forma, posso armazenar
# os objetos dentro de dicionários.
ac = Ac_certificado
ac.objects.all().delete()

# ----------------------------------- Home ----------------------------------- #

def home(request):
    return render(request, 'blog/home.html')

# ---------------------- Gerador de Chaves Assimétricas ---------------------- #

def gera_chave(request):
    # Limpando o conteúdo dos arquivos
    with open('blog/static/blog/chave-priv.key','wb'): pass
    with open('blog/static/blog/chave-pub.key', 'wb'): pass

    # Dicionário que será passado ao HTML para exibir dos dados
    keys = {'pubkey': 0, 'privkey': 0}
    
    if request.method == 'POST':
        bit_length = request.POST.get('length','')
        if bit_length != '': 
            key, pubkey, privkey = gerar_chave(bit_length)
                
            # Escrevendo as chaves (em bytes) nos arquivos
            with open('blog/static/blog/chave-priv.key', 'wb') as f:
                f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
            with open('blog/static/blog/chave-pub.key', 'wb') as d:
                d.write(crypto.dump_publickey(crypto.FILETYPE_PEM, key))

            # Atualizando dicionário
            keys = {'pubkey': pubkey, 'privkey': privkey}
        
    return render(request,'blog/gera_chaves.html',keys)

# --------------------------- Resumo Criptográfico --------------------------- #

def resumo_cripto(request):
    resumo = {'text':''}
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['document']
            data = uploaded_file.read()
            m = rsa.compute_hash(data,'SHA-256')
            m = m.hex() 
            resumo['text'] = m
        except:
            # Caso o usuário tente gerar um resumo sem antes prover um documento
            resumo['text'] = ' Entrada de dados inválida!'
    return render(request, 'blog/resumo_cripto.html', resumo)

# ---------------------------- Certificado Digital --------------------------- #

def certificado_digital(request):
    message['warning'] = False

    if request.method == 'POST':
        
        # Dependendo da etapa em que estamos, uma condição diferente será executada
        # 1ª Etapa
        if 'gerar_chaves' in request.POST:
            bit_length = request.POST.get('length','')
            if bit_length != '': 
                key, pubkey, privkey = gerar_chave(bit_length)
                display_keys = {'pubkey': pubkey, 'privkey': privkey}
                # diplay_keys = dados para exibição no HTML
                message['display_keys'] = display_keys
                # app_keys = Applicant keys, chaves de que vai requerir um certificado digital
                message['app_keys'] = key
                message['restart'] = False
        
        # 2ª Etapa
        elif 'criar_ac' in request.POST:
            # Pegando o input que o usuário forneceu nos campos de texto
            cn = request.POST.get('cn','')
            c = request.POST.get('c','')
            st = request.POST.get('st','')
            l = request.POST.get('l','')
            o = request.POST.get('o','')
            ou = request.POST.get('ou','') 
            
            verificar = [cn,c,st,l,o,ou]

            # Verificação da validade do input
            if (len(c) != 2) or '' in verificar:
                message['warning'] = True
            
            else:
                # Gerando par de chaves da AC
                key = crypto.PKey()
                key.generate_key(crypto.TYPE_RSA, 1024)
                # Disponibilizando o objeto key para futuramente assinarmos um certificado emitido
                message['ac_keys'] = key
                # Gerando certificado autoassinado pela AC
                certificado_ac, issuer_json, serial, subject_json = gerar_cert(cn,c,st,l,o,ou,key,key,None,True)
                certificado_decoded = crypto.dump_certificate(crypto.FILETYPE_PEM, certificado_ac).decode()
                
                # Disponibilizando o objeto issuer para futuramente utilizarmos na emissão de certificados digitais
                issuer = certificado_ac.get_issuer()
                message['issuer'] = issuer 
                # Dados para exibir qual a AC atual, no HTML
                message['diplay_ac_subject'] = subject_json

                #with open('./arquivo_certificados/ac_certificado.crt', 'wb+') as f:
                    #a = crypto.dump_certificate(crypto.FILETYPE_PEM, certificado_ac)
                    #f.write(a)
                
                # Guardando no banco de dados
                ac = Ac_certificado(cert_autoassinado = certificado_decoded, serial = serial,
                issuer = issuer_json, subject = subject_json)
                ac.save()

        # 3ª Etapa  
        elif 'criar_cert' in request.POST:
            cn = request.POST.get('cn','')
            c = request.POST.get('c','')
            st = request.POST.get('st','')
            l = request.POST.get('l','')
            o = request.POST.get('o','')
            ou = request.POST.get('ou','')
            
            verificar = [cn,c,st,l,o,ou]
            print()
            #print(message['app_keys'])        
            #print(message['ac_keys'])
            #print(message['issuer'])
            print()
             
            if (len(c) != 2) or '' in verificar:
                message['warning'] = True
            else:
                certificado, issuer_json, serial, subject_json = gerar_cert(cn,c,st,l,o,ou,message['app_keys'],message['ac_keys'],message['issuer'],False)
                certificado_decoded = crypto.dump_certificate(crypto.FILETYPE_PEM, certificado).decode()
                banco_de_dados = Certificados_emitidos(certificado = certificado_decoded,serial = serial, issuer = issuer_json, subject = subject_json)
                banco_de_dados.save()
                message['restart'] = True

    # Obtendo o primeiro objeto da tabela de Autoridades Certificados
    ac = Ac_certificado.objects.first()
    # Será utilizado no HTML, caso ac seja nulo, o usuário terá de criar uma AC
    message['ac'] = ac    

    return render(request, 'blog/certificado_digital.html', message)

# ----------------------- Listar Certificados Emitidos ----------------------- #

def listar_cert(request):
    count = Certificados_emitidos.objects.all().count()
    # Caso count seja 0, não iremos listar os certificados, pois não há nenhum no banco de dados
    # Passando uma lista na key "certificados" que será percorrida no HTML
    listar = {'certificados': Certificados_emitidos.objects.all(), 'contagem': count}
    
    return render(request,'blog/listar_cert.html', listar)