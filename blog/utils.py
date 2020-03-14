# Módulo com funções para gerar certificados digitais e chaves assimétricas
#from .models import Certificados_emitidos, Contador
from OpenSSL import crypto

def gerar_chave(bit_length):
    bit_length = int(bit_length)
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, bit_length)                
    pubkey = crypto.dump_publickey(crypto.FILETYPE_PEM, key).decode()
    privkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode()
    return key, pubkey, privkey

def gerar_cert(cn,c,st,l,o,ou,req_key,ac_key,issuer,autoassinado):
    #serial = Contador.objects.all().count()
    cert = crypto.X509() # Instanciando certificado
    
    # Campo subject:
    cert.get_subject().CN = cn
    cert.get_subject().C = c
    cert.get_subject().ST = st
    cert.get_subject().L = l
    cert.get_subject().O = o
    cert.get_subject().OU = ou
    # Serial:
    cert.set_serial_number(1000) # Identificação
    # Validade: 
    cert.gmtime_adj_notBefore(0) # Certificado começa a ser válido em 0 segundos
    cert.gmtime_adj_notAfter(31536000) # Certificado perde a validade após 365 dias
    
    #serial = Certificados_emitidos.objects.all().count()
    
    if autoassinado == True:
        # Neste caso como é um certificado da própria CA, ele será igual ao subject)
        issuer = cert.get_subject()
    
    lista_componentes = issuer.get_components()
    dict_nomes = {}

    for name in lista_componentes:
        dict_nomes[name[0].decode()] = name[1].decode()
    
    print()
    print(dict_nomes)
    #print(serial)
    print()

    # Issuer (CA emissora)
    cert.set_issuer(issuer)

    # Definindo a chave pública 
    cert.set_pubkey(req_key)
    # Assinatura (key é um objeto, e dependendo da função de crypto.X509() que passamos, ele acessará a chave privada ou local
    # por isso utilizei key na assinatura, e na definição da chave pública)
    cert.sign(ac_key, "sha256") # Produz hash, e assina hash com a chave privada

    #contar = Contador()
    #contar.save()

    return cert, dict_nomes, 1000
