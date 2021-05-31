import random
import time
import hashlib

_BASE = []

ArquivoBaseEntrada = ".\\base.txt"
ArquivoBaseSeguraSaida = ".\\baseSegura.txt"
Salt = "FEI"

# Método para leitura da base recebida em txt
def LerBase(ArquivoBase):
    with open(ArquivoBase) as arquivo:
        linhas = arquivo.readlines()

    return linhas

# Método para gerar a base segura e escrita dela em txt
def GerarBaseSegura(ArquivoBaseSeguraSaida, linhas, salt):
    arquivo = open(ArquivoBaseSeguraSaida, "w")

    for linha in linhas:
        # Separa as informações da base
        linhaSplit = linha.split('|')
        usuario = linhaSplit[1]
        senha = linhaSplit[2]
        string = f"{usuario}{senha}{salt}"
        # Criptografia hash
        hash = hashlib.sha256(string.encode('utf-8')).hexdigest()     
        arquivo.write(f"|{usuario}|{hash}|\n")
    arquivo.close()


def AutenticarUsuarioBase(linhasBase, usuario, senha):
    for x in linhasBase:
        usuarioBase = x.split('|')[1]
        senhaBase = x.split('|')[2]
        if usuarioBase == usuario and senhaBase == senha:
            return True

    return False


def GravarUsuario():
    usuario = input('Informe seu usuario: ')
    senha = input('Informe sua senha: ')
    salt = Salt
    string = f"{usuario}{senha}{salt}"
    hash = hashlib.sha256(string.encode('utf-8')).hexdigest()
    _BASE.append([usuario, hash])
    print("Usuario cadastrado com sucesso!")
    TestarAutenticacao()


def LogarUsuario():
    usuario = input('Informe seu usuario: ')
    senha = input('Informe sua senha: ')
    salt = Salt
    string = f"{usuario}{senha}{salt}"
    hash = hashlib.sha256(string.encode('utf-8')).hexdigest()

    valido = False

    for x in _BASE:
        if x[0] == usuario and x[1] == hash:
            valido = True
            break
    if valido:
        print("Usuário validado com sucesso!")
    else:
        print("Usuario ou senha incorretos.")
    TestarAutenticacao()


def AutenticarUsuarioBaseSegura(linhasBase, usuario, hash, salt):
    string = f"{usuario}{hash}{salt}"
    hash = hashlib.sha256(string.encode('utf-8')).hexdigest()

    for x in linhasBase:
        usuarioBase = x.split('|')[1]
        hashBase = x.split('|')[2]

        if usuarioBase == usuario and hashBase == hash:
            return True

    return False


def TestarAutenticacao():
    processo = input('Informe o processo que deseja realizar: \n 1 - Gravar \n 2 - Logar\n 3 - Sair\n')

    try:
        if int(processo) == 1:
            GravarUsuario()
        elif int(processo) == 2:
            LogarUsuario()
        elif int(processo) == 3:
            return
        else:
            print('Processo invalido.')
    except ValueError:
        print("Digite um número")
        TestarAutenticacao()


def main(ArquivoBaseEntrada,ArquivoBaseSeguraSaida,Salt):
    # Leitura dos arquivos de entrada
    linhasBase = LerBase(ArquivoBaseEntrada)
    tamanhoBase = len(linhasBase)
    
    # Geração da base segura
    ini = time.time()
    GerarBaseSegura(ArquivoBaseSeguraSaida, linhasBase, Salt)
    fim = time.time()
    print("Tempo para gerar base segura: ", fim - ini)
    
    # Seleção da quantidade utilizada 
    linhasBaseSegura = LerBase(ArquivoBaseSeguraSaida)
    aux = int(tamanhoBase / 100)
    print(f"Quantidade de usuários utilizados para validação: {aux}")
    
    # Validação por senha direta
    print("------------------ Teste com senha direta")
    ini = time.time()
    countBase = 0
    for i in range(0, aux):
        index = random.randint(0, tamanhoBase - 1)
        linha = linhasBase[index]
        linhaSplit = linha.split('|')
        usuario = linhaSplit[1]
        senha = linhaSplit[2]

        if AutenticarUsuarioBase(linhasBase, usuario, senha):
            countBase += 1
    fim = time.time()
    print("Tempo para execução da validação por senha: ", fim - ini)
    
    # Validação por senha segura
    print("------------------ Teste com senha segura")
    countBaseSegura = 0
    ini = time.time()
    for i in range(0, aux):
        index = random.randint(0, tamanhoBase - 1)
        linha = linhasBase[index]
        linhaSplit = linha.split('|')
        usuario = linhaSplit[1]
        hash = linhaSplit[2]

        if AutenticarUsuarioBaseSegura(linhasBaseSegura, usuario, hash, Salt):
            countBaseSegura += 1
    fim = time.time()
    print("Tempo para execução da validação por hash: ", fim - ini)
    print("--------------------------------------------------------------------------")
    
    TestarAutenticacao()

main(ArquivoBaseEntrada,ArquivoBaseSeguraSaida,Salt)