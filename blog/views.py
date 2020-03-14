from django.shortcuts import render
from OpenSSL import crypto
from .models import Certificados_emitidos, Post, Ac_certificado, Contador
from .utils import gerar_cert, gerar_chave
import rsa
import json

message = {}
message = {'restart': True}
ac = Ac_certificado
ac.objects.all().delete()
# ------------------------------------- - ------------------------------------ #

def home(request):
    context = {
        #'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

# ------------------------------------- - ------------------------------------ #

def gera_chave(request):
    keys = {'pubkey': 0, 'privkey': 0}
    
    if request.method == 'POST':

        bit_length = request.POST.get('length','')
        if bit_length != '': 
            key, pubkey, privkey = gerar_chave(bit_length)
                
            # Implementar download
            #with open('./chaves/chave-priv.key', 'wb+') as f:
            #    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
            #with open('./chaves/chave-pub.key', 'wb+') as d:
            #    d.write(crypto.dump_publickey(crypto.FILETYPE_PEM, key))

            
            keys = {'pubkey': pubkey, 'privkey': privkey}
        
    return render(request,'blog/gera_chaves.html',keys)

# ------------------------------------- - ------------------------------------ #

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
            resumo['text'] = ' Entrada de dados inválida!'
    return render(request, 'blog/resumo_cripto.html', resumo)

# ------------------------------------- - ------------------------------------ #

def certificado_digital(request):
    message['warning'] = False

    if request.method == 'POST':
        
        if 'gerar_chaves' in request.POST:
            bit_length = request.POST.get('length','')
            if bit_length != '': 
                key, pubkey, privkey = gerar_chave(bit_length)
                
                display_keys = {'pubkey': pubkey, 'privkey': privkey}
                message['display_keys'] = display_keys
                message['app_keys'] = key
                message['restart'] = False

        elif 'criar_ac' in request.POST:
            cn = request.POST.get('cn','')
            c = request.POST.get('c','')
            st = request.POST.get('st','')
            l = request.POST.get('l','')
            o = request.POST.get('o','')
            ou = request.POST.get('ou','')
            # Checar validade do input
            
            key = crypto.PKey()
            key.generate_key(crypto.TYPE_RSA, 1024)
            message['ac_keys'] = key
            # N PERMITIR INPUT VAZIO
            if len(c) != 2:
                message['warning'] = True
            else:
                certificado_ac, var_inutilizada, serial = gerar_cert(cn,c,st,l,o,ou,key,key,None,True)
                issuer = certificado_ac.get_issuer()
                message['issuer'] = issuer

                #with open('./arquivo_certificados/ac_certificado.crt', 'wb+') as f:
                #    a = crypto.dump_certificate(crypto.FILETYPE_PEM, certificado_ac)
                #    f.write(a)
                
                ac = Ac_certificado(cert_autoassinado = crypto.dump_certificate(crypto.FILETYPE_PEM, certificado_ac))
                ac.save()
            
                # download do certificado...

        elif 'criar_cert' in request.POST:
            cn = request.POST.get('cn','')
            c = request.POST.get('c','')
            st = request.POST.get('st','')
            l = request.POST.get('l','')
            o = request.POST.get('o','')
            ou = request.POST.get('ou','')
            
            print()
            print(message['app_keys'])        
            print(message['ac_keys'])
            print(message['issuer'])
            print()

            #ac = Ac_certificado.objects.first()
            #issuer1 = pickle.loads(ac.issuer)
            #print(issuer1)
             
            if len(c) != 2:
                message['warning'] = True
            else:
                certificado, issuer_dict, serial = gerar_cert(cn,c,st,l,o,ou,message['app_keys'],message['ac_keys'],message['issuer'],False)
                certificado_dumped = crypto.dump_certificate(crypto.FILETYPE_PEM, certificado)
                issuer_json = json.dumps(issuer_dict)
                banco_de_dados = Certificados_emitidos(certificado = certificado_dumped,serial=serial, issuer=issuer_json)
                banco_de_dados.save()
                message['restart'] = True


    ac = Ac_certificado.objects.first()
    message['ac'] = ac    

    return render(request, 'blog/certificado_digital.html', message)

# ------------------------------------- - ------------------------------------ #

def listar_cert(request):
    
    
    return render(request,'blog/listar_cert.html')