# -*- coding: utf-8 -*-
import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR='l'



def printCores(texto, cor) :
  print(cor + texto + RESET)
  

def adicionar(descricao, extras):
  if descricao == '':
    print('Ocorreu um erro, o compromisso inserido não possui uma descrição válida.')
    print('Sugestão: coloque algo como no final da mesma, como um ponto final.')
    return False
  elif extras == ('', '', '', '', ''):
    novaAtividade = descricao
  else:
    texto =descricao.strip()  # +' '+ [' '.join([x for x in extras if x != ''])][0]
    if extras[0] != '':
      texto = extras[0] + ' '+ texto
    if extras[1] != '':
      texto = extras[1] + ' '+ texto
    if extras[2] != '':
      texto = extras[2] + ' '+ texto
    if extras[3] != '':
      texto = texto + ' '+ extras[3]
    if extras[4] != '':
      texto = texto + ' '+ extras[4]
    txtTupla = organizar(texto.strip())
    
    novaAtividade = txtTupla[0][1][0]+' ' + txtTupla[0][1][1]+' ' + txtTupla[0][0].strip()+' '+txtTupla[0][1][3]+' '+ txtTupla[0][1][4]
    novaAtividade = novaAtividade.strip()
  # Escreve no TODO_FILE. 
  try:
    
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False
  print('Atividade adicionada aos compromissos com sucesso!')
  return True


# Valida a prioridade.
def prioridadeValida(pri):
  if pri[0]== '(' and pri[2] == ')':
    if pri[1] >= 'A' and pri[1] <= 'Z':
      return True
  
  return False


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    if horaMin[:2] >= '00' and horaMin[:2] <= '23':
        if horaMin[2:] >= '00' and horaMin[2:] <= '59':
            return True
        else:
            return False
    else:
        return False

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
    if len(data) != 8 or not soDigitos(data) and diaMes(data[:4]):
        return False
    else:
        return True

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
    if  len(proj) >= 2 and proj[0] == '+':
        return True
    else:
        return False

def contextoValido(cont):
    if  len(cont) >= 2 and cont[0] == '@':
        return True
    else:
        return False
def prioridadeValida(priori):
    if len(priori) != 3 or priori[0] != '(' or priori[2] != ')':
        return False
    else:
        if priori[1] >= 'A' and priori[1] <= 'Z' or priori[1] >= 'a' and priori[1] <= 'z':
            return True
        else:
            return False
# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True

def diaMes(diames):
    trintaum = ['01','03','05','07','08','10']
    trinta = ['04','06','09','11']
    vinteoit = ['02']
    if len(diames) != 4:
        return False
    else:
        if diames[2:] == '02':
            if int(diames[0:2]) > 28:
                return False
        elif diames[0:2] == '31':
            if em(diames[2:3],trintaum) == True:
                return True
        elif diames[0:2] == '30':
            if em(diames[2:],trinta):
                return True
        return True
             
def em(oque,onde):
    for x in onde:
        if x == oque:
            return True
    return False
          
# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
    itens = []
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
    palavras = splits(linhas)
    for l in palavras:
        if dataValida(l) and l == palavras[0]:
            data = l
        elif horaValida(l) and l == palavras[1]:
            hora = l
        elif prioridadeValida(l):
            pri = l
        elif contextoValido(l) and l == palavras[len(palavras)-2]:
            contexto = l
        elif projetoValido(l) and l == palavras[len(palavras)-1]:
            projeto = l
        else: 
            desc += l + ' '

    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 
        
        

    itens.append((desc, (data, hora, pri, contexto, projeto)))

    return itens

def splits(frase):
    asPalavras = []
    palavra = ''
    for x in frase:
        if x == ' ':
            asPalavras.append(palavra)
            palavra = ''
        else:
            palavra += x
    asPalavras.append(palavra)
    return asPalavras

# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
  fp = open(TODO_FILE, 'r')
  linhas = fp.readlines()
  linhas = tiraQuebraDeLinhas(linhas)
  tuplas = []
  for x in linhas:
    tuplas += organizar(x)
  tuplasOrdenadas = ordenarPorPrioridade(tuplas)

  for x in tuplaParaLinhaFormatada(tuplasOrdenadas):
      print(x)
      	

  return


def tuplaParaLinha(tupla):
  linhasOrdenadas = []
  for x in tupla:
    c = 0
    linha= ''
    while c < 6:      
      if c == 0:
        if x[1][0] != '':
          linha+= x[1][0]
      if c == 1:
        if x[1][1] != '':
          linha+=' ' + x[1][1]
      if c== 2:
        if x[1][2] != '':
          linha+=' '+ x[1][2]
      if c == 3:
        linha +=' '+ x[0].strip()
      if c== 4:
        if x[1][3] != '':
          linha +=' '+ x[1][3]
      if c == 5:
        if x[1][4] != '':
          linha +=' '+ x[1][4]
      c+=1
    linhasOrdenadas.append(linha.strip())
  i=1  
  return linhasOrdenadas

def tuplaParaLinhaFormatada(tupla):
  linhasOrdenadas = []
  i = 1
  for x in tupla:
    c = 0
    linha= ''
    while c < 6:      
      if c == 0:
        if x[1][0] != '':
          linha+= x[1][0][:2] + '/'+x[1][0][2:4]+'/'+x[1][0][4:]
      if c == 1:
        if x[1][1] != '':
          linha+=' ' + x[1][1][:2]+'h'+x[1][1][2:]+'m'
      if c== 2:
        if x[1][2] != '':
          linha+=' '+x[1][2]
      if c == 3:
        linha +=' '+ x[0].strip()
      if c== 4:
        if x[1][3] != '':
          linha +=' '+ x[1][3]
      if c == 5:
        if x[1][4] != '':
          linha +=' '+ x[1][4]
      c+=1
    if x[1][2] == '(A)':
      linhasOrdenadas.append(BOLD+RED+str(i)+' '+linha.strip()+RESET)
    elif x[1][2] == '(B)':
      linhasOrdenadas.append(YELLOW+str(i)+' '+linha.strip()+RESET)
    elif x[1][2] == '(C)':
      linhasOrdenadas.append(CYAN+str(i)+' '+linha.strip()+RESET)
    elif x[1][2] == '(D)':
      linhasOrdenadas.append(GREEN+str(i)+' '+linha.strip()+RESET)
    else:
      linhasOrdenadas.append(str(i)+' '+linha.strip()+RESET)
    i+=1

  return linhasOrdenadas

def ordenarPorDataHora(itens):
  comData = []
  apenasHora = []
  semDataHora = []
  for x in itens:
    if x[1][0] != '':
      comData.append(x)
    elif x[1][1] != '':
      apenasHora.append(x)
    else:
      semDataHora.append(x)
  return quickSortPlus(comData,2) + quickSortPlus(apenasHora,3) + semDataHora
   
def ordenarPorPrioridade(itens):
  semPrioridade = []
  comPrioridade = []
  for x in itens:
    if x[1][2] == '':
      semPrioridade.append(x)
    else:
      comPrioridade.append(x)
  itens = quickSortPlus(comPrioridade,1)+ordenarPorDataHora(semPrioridade)  
  return itens

def fazer(num):
  fp = open(TODO_FILE, 'r')
  linhas = fp.readlines()
  linhas = tiraQuebraDeLinhas(linhas)
  tuplas = []
  for x in linhas:
    tuplas += organizar(x)
  tuplasOrdenadas = ordenarPorPrioridade(tuplas)
  compromissos = tuplaParaLinha(tuplasOrdenadas)
  if (num-1) > len(compromissos) or (num-1) < 0:
    print('Ocorreu um erro! A atividade a ser marcada como como feita não existe .')
    return 
  oque = organizar(compromissos[num-1])
  linhas2 = fp.readlines()
  linhas2 = tiraQuebraDeLinhas(linhas)
  tuplas = []
  for x in linhas2:
    if organizar(x)[0] != oque[0]:
      tuplas += organizar(x)
  fp.close()
  fp = open(TODO_FILE, 'w')
  for x in tuplaParaLinha(tuplas):
    fp.write(x+ '\n')
  fp.close()
  fp = open(ARCHIVE_FILE, 'a')
  fp.write(tuplaParaLinha(oque)[0]+ '\n')
  fp.close()
  print('Compromisso marcado como feito.')
  return 


def remover(ref):
  fp = open(TODO_FILE, 'r')
  linhas = fp.readlines()
  linhas = tiraQuebraDeLinhas(linhas)
  tuplas = []
  for x in linhas:
    tuplas += organizar(x)
  tuplasOrdenadas = ordenarPorPrioridade(tuplas)
  compromissos = tuplaParaLinha(tuplasOrdenadas)
  if (ref-1) > len(compromissos) or (ref-1) < 0:
    print('Ocorreu um erro! A atividade a ser removida não existe.')
    return 
  oque = organizar(compromissos[ref-1])
  linhas2 = fp.readlines()
  linhas2 = tiraQuebraDeLinhas(linhas)
  tuplas = []
  for x in linhas2:
    if organizar(x)[0] != oque[0]:
      tuplas += organizar(x)
  fp.close()
  fp = open(TODO_FILE, 'w')
  for x in tuplaParaLinha(tuplas):
    fp.write(x+ '\n')
  fp.close()
  return True
#este é um quicksort multiplo, o w deve ser substituído por um número: "1" para prioridade, "2" para data e hora
def quickSortPlus(lista,w):
  #1 - QS Prioridade
  if w ==1:
    if lista == []:
      return []
    else:
      pivot = lista.pop()
      maiores = [x for x in lista if x[1][2] > pivot[1][2] and x[1][2] != '']
      iguais = [x for x in lista if x[1][2] == pivot[1][2]]
      nulos = [x for x in lista if x[1][2] == '']
      menores = [x for x in lista if x[1][2] < pivot[1][2] and x[1][2] != '']
      return quickSortPlus(menores,1)+ordenarPorDataHora([pivot]+iguais)+quickSortPlus(maiores,1)

    
  #2 - QS Data
  elif w ==2:
    if lista == []:
      return []
    else:
      pivot = lista.pop(0)
      menores = [x for x in lista if x[1][0][4:]+x[1][0][2:4]+x[1][0][:2] <  pivot[1][0][4:]+pivot[1][0][2:4]+pivot[1][0][:2]]
      datasIguais = [x for x in lista if x[1][0][4:]+x[1][0][2:4]+x[1][0][:2] == pivot[1][0][4:]+pivot[1][0][2:4]+pivot[1][0][:2]] 
      maiores = [x for x in lista if x[1][0][4:]+x[1][0][2:4]+x[1][0][:2] > pivot[1][0][4:]+pivot[1][0][2:4]+pivot[1][0][:2]]
      
      return quickSortPlus(menores,2) +quickSortPlus([pivot]+datasIguais,3) + quickSortPlus(maiores,2)


  #3 - QS Hora
  elif w==3:
    if lista ==[]:
      return []
    else:
      pivot=lista.pop(0)
      menores = [x for x in lista if x[1][1] < pivot[1][1] and x[1][1] != '']
      #iguais = [x for x in lista if x[1][1] == pivot[1][1]]
      nulos = [x for x in lista if x[1][1] == '']
      maiores = [x for x in lista if x[1][1] >= pivot[1][1] and x[1][1] != '']
      return quickSortPlus(menores,3) +[pivot]+ quickSortPlus(maiores,3) + nulos
        
      
    
# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
#  if (num-1) > len(linhas) or (num-1) < 0:
#    print('Ocorreu um erro! O compromisso escolhido para priorizar não existe.')
#    return
  fp = open(TODO_FILE, 'r')
  linhas = fp.readlines()
  if (num) > len(linhas) or (num) <= 0:
    print('Ocorreu um erro! O compromisso escolhido para priorizar não existe.')
    return
  if not prioridadeValida('('+prioridade+')'):
    print('Ocorreu um erro! formato inválido da prioridade.')
    return 

  linhas = tiraQuebraDeLinhas(linhas)
  tuplas = []
  for x in linhas:
    tuplas += organizar(x)
  tuplasOrdenadas = ordenarPorPrioridade(tuplas)
  compromissos = tuplaParaLinha(tuplasOrdenadas)
  compromissoTupla = organizar(compromissos[num-1])
  
  compromissoTuplaPriori = []
  compromissoTuplaPriori.append((compromissoTupla[0][0],(compromissoTupla[0][1][0],compromissoTupla[0][1][1],'('+(prioridade.upper())+')',compromissoTupla[0][1][3],compromissoTupla[0][1][4],)))
  compromissoLinha = tuplaParaLinha(compromissoTuplaPriori)
  remover(num)
  fp.close()
  fp = open(TODO_FILE, 'a')
  fp.write(compromissoLinha[0] + "\n")
  fp.close()
  print('Prioridade efetuada com sucesso!')
  return True



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)][0])
    la = [' '.join(comandos)][0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))

    #print(itemParaAdicionar[0][0])
    #print(itemParaAdicionar[0][1])
    #return 
    adicionar(itemParaAdicionar[0][0], itemParaAdicionar[0][1]) # novos itens não têm prioridade
    ################ COMPLETAR

  elif comandos[1] == REMOVER:
    if remover(int(comandos[2])):
      print('Compromisso removido com sucesso!')
    return    

  elif comandos[1] == FAZER:
    fazer(int(comandos[2]))
    return    

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    if priorizar(int(comandos[2]),comandos[3]):
      return
  
  elif comandos[1] == LISTAR:
    return listar()
    
  else :
    print("Comando inválido.")

    
def tiraQuebraDeLinhas(lista):
    c=0
    for linhas in lista:
        palavra = ''
        for y in linhas:
            if y == '\n':
                continue
            else:
                palavra += y
        lista[c] = palavra
        c+=1
    return lista

# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
