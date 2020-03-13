Certificado Digital:
O cenário inicial que havia projetado para esta rota era o seguinte:
- O usuário provê um arquivo.key contendo sua chave pública
- A AC teria seu model no banco de dados com os seguintes campos: issuer, cert_autoassinado, privkey
- O algoritmo então le a chave e atribui a mesma na função crypto.X509.set_pubkey()
- Para informar o emissor do certificado, consulta-se o campo issuer da class Ac_certificado no models.py, e para assinar o certificado consulta-se o campo privkey

Por que não funcionou:

No módulo crypto da biblioteca OpenSSL, a classe de geração de certificado X.509 aceita apenas objetos de crypto.X509() em suas funções set_issuer(), set_pubkey(), sign().
Tentei então guardar os objetos no banco de dados utilizando a biblioteca pickle para serializar o objeto e assim poder guardar ele no banco de dados. Todavia os objetos de crypto.X509() e crypto.PKey() não são compativeis com o pickle, retornando o seguinte erro: 
can't pickle _cffi_backend.CDataGCP objects

Tentei outra biblioteca para geração de certificado X.509, cryptography.
Esta também aceitava apenas objetos nos inputs de chave privada e publica para geração de certificado digital. E ao tentar serializar estes com pickle, retornou o seguinte erro:
can't pickle CompiledFFI objects

Como implementei:





