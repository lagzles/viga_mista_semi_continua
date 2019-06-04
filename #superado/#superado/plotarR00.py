import numpy as np
from tramos_r11 import Tramos, calculo_semi_rigido
from numpy import arange, linspace
from scipy.integrate import nquad
from scipy.optimize import newton
import matplotlib.pyplot as plt

## k1 = ke = vinculo semi-rigido do lado esquerdo do tramo
## k2 = kd = vinculo semi-rigido do lado direito do tramo
## vao = valor do vao do tramo
## q = carga distribuida
## i = Inercia do perfil

sair = ""

while sair != 'q' or sair != 'S' or sair != 's' or sair != 'y':
##    n_vaos = int(input("Inserir quantidade de vaos:  "))
    n_vaos = 4

    n_list = []
    lista_tramos = []
    lista_sub = []

    ponta_esq = "ponta_esquerda"#"ponta_direita"#
    ponta_dir = "ponta_direita"
    intermediario = "intermediario"

    i = 10000 * 100 ** -4  # m4 ## Ix = 15254 cm4 ## Iy = 513 cm4
    e = 2.0 * (10 ** 8) # kN/m2 ##E = 200000 # MPa

    q = 5. ## kN/m

    ei = e * i  #  30508 # kN.m2
    lista_vaos = [10.] * n_vaos

    ## k1 = ke = vinculo semi-rigido do lado esquerdo do tramo
    ## k2 = kd = vinculo semi-rigido do lado direito do tramo
    ## vao = valor do vao do tramo
    for j in range(n_vaos):#range(n_vaos):
##        vao = (float(input("Inserir valor do %.0f vao [m]:  " % (j + 1))))
        if j == 0:
            k1 = 100**10 #vinculo com valor de engaste
##            k2 = (float(input("Inserir valor k2/kd do %.0f vao [kN.m/rad]:  " % (j + 1))))
            tramo = Tramos( j, lista_vaos[j], i, e, ponta_esq)
##            lista_tramos.append([tramo, k1, k2])
##            lista_vaos.append(vao)
            for sub in tramo.create_subs():
                lista_sub.append(sub)
            
        elif j == n_vaos - 1 and j !=0:
##            k1 = (float(input("Inserir valor k1/ke do %.0f vao [kN.m/rad]:  " % (j + 1))))
            k2 = 100**10 #vinculo com valor de engaste
            tramo = Tramos( j, lista_vaos[j], i, e, ponta_dir)
##            lista_tramos.append([tramo, k1, k2])
##            lista_vaos.append(vao)
            for sub in tramo.create_subs():
                lista_sub.append(sub)
        else:
##            k1 = (float(input("Inserir valor k1/ke do %.0f vao [kN.m/rad]:  " % (j + 1))))
##            k2 = (float(input("Inserir valor k2/kd do %.0f vao [kN.m/rad]:  " % (j + 1))))
            tramo = Tramos( j, lista_vaos[j], i, e, intermediario)
##            lista_tramos.append([tramo, k1, k2])
##            lista_vaos.append(vao)
            for sub in tramo.create_subs():
                lista_sub.append(sub)

   
    reacoes = calculo_semi_rigido(lista_sub, q, lista_vaos)
##    reacoes2 = calculo_normal(lista_tramos, q)


    #################################################################
    ## Funções de diagramas de Momentos para cada Vão
    ## Orientação, esquerda para direita
    vaoTotal = 0
    listaDx = [0]
    dicReacoes = dict()
    dicReacoes[0] = reacoes[0]
    listaRaizes = []
    ## cria uma lista com os valores de x, contanto da origem até o proximo apoio
    ## cria um dicionario com o valor de x e o valor de reação do apoio
    for i in range(0,len(lista_vaos)):
        vaoTotal += lista_vaos[i]
        listaDx.append(vaoTotal)
        dicReacoes[vaoTotal] = reacoes[i+1]

        
    tolerancia = 0.000001
    ## Função cortante, escrita como derivada da função Momento
    def dy(x):
        v = 0       
        vr = 0
        v -= x * q # valor proveniente da carga distribuida
        xt = 0
        for key, value in dicReacoes.items():
            if x > key:
                vr += value
##        for i in range(int(x)+1):
##            if i in dicReacoes:                
##                vr += dicReacoes[i] # valor das reações, de acordo com a posição x
        v += vr
        return v
    #######################################3

    # Valores de 'x' em que o cortante é zero = momento positivo é maximo
    for i in range(len(listaDx)):
        listaRaizes.append(newton(dy,listaDx[i]))

    listaMomentos = []
    listaMomentosPos = []
    dictMomentosPos = dict()
    listaCortantes = []

    ## Inicio da montagem dos diagramas
    ## Diagrama cortante
    x = 0 # valor inicial de x
    y = 0 # valor inicial de y
    xn = vaoTotal  # valor final de x
    h = 0.5 # valor 'step' para cada iteração
    n = int((xn-x)/h) # numero de iterações
    
    xp = np.linspace( x, xn, n+1) # coordenadas de x
    ypv = np.empty( n+1, float)   # coordenadas de y
    ypv[0] = y
    for i in range(len(xp)):
        ypv[i] = dy(xp[i])

    plt.subplot(211)
    for i in listaDx:
        listaCortantes.append(dy(i))
        yi = dy(i)
        xi = i
        plt.text(xi, yi, '%.2f kN' % yi, fontsize=8)
        if xi < vaoTotal:
            yi = dy(i+h)
            xi = i
            listaCortantes.append(yi)
            plt.text(xi, yi, '%.2f kN' % yi, fontsize=8)
            

    # Plotagem do diagrama de Cortante
    
    plt.plot( xp, ypv, 'b')   
    plt.plot([x,xn],[0., 0.],'k')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(['V[x]'])
    plt.title('Cortante [kN] e Momento [kN.m]')
    plt.grid()

    # Diagrama de Momento
    ypm = np.empty(n+1,float)
    ypmi = 0
    ypm[0] = 0
    plt.subplot(212)
    for i in range(0, n+1):
        ypm[i],_ = nquad(dy, [[0, xp[i]]]) # integral da função Cortante 'dy'
        
    for i in range(0, n+1):
        for root in listaRaizes:
            if xp[i] == root:
                dictMomentosPos[xp[i]] = ypm[i]
                listaMomentosPos.append(ypm[i])
                
    # impressão dos valores de momentos negativos nos apoios
    for i in range(1,n):
        for j in range(len(listaDx)):
            if (x + i*h) == (listaDx[j]):
                xi = (x + i*h)
                yi = ypm[i]
                plt.text(xi, -yi, '%.2f kN.m' % yi, fontsize=8)
                listaMomentos.append(ypm[i])

    # impressao dos valores de momentos maximos positivos
    for xi in listaRaizes:
        yi,_ = nquad(dy, [[0, xi]])
        plt.text(xi, -yi*1.35, '%.2f kN.m' % yi, fontsize=8)
        
        
##       
    plt.plot( xp, -ypm, 'k')
    plt.plot([x,xn],[0., 0.],'b')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.ylim(min(ypm)*2, max(ypm)*1.5)
    plt.legend(['M[x]'], loc = 'upper left' )
##    plt.title('Momento')
    plt.grid()

    print("reaçoes semi rigidas")
    print(reacoes)
    print('Momentos POsitivos')
    print(listaMomentosPos)
    print('Momentos Negativos')
    print(listaMomentos)
    print('Cortantes')
    print(listaCortantes)
    plt.show()

    sair = str(input("Sair (q/s/y):  "))








