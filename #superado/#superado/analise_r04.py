import numpy as np
from tramos_r11 import Tramos, calculo_semi_rigido
from numpy import arange, linspace
from scipy.integrate import odeint, nquad
import matplotlib.pyplot as plt
from scipy.misc import derivative

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
    for vao in lista_vaos:
        vaoTotal += vao
        
    y0 = [0,1]
    x = arange(0, vaoTotal, 1)
    xi = linspace(0, vaoTotal, 100)
    ##    yp = np.empty((vaoTotal/.1),float)
    def dv(x):        
        v = 0
        v -= x * q
        xt = 0
        v += reacoes[0]
        for i in range(len(lista_vaos)):
            xt += lista_vaos[i]            
            if x >= xt:
                v += reacoes[i+1]
        return v

    x = 0
    xn = vaoTotal
    y = -2
    h = 0.1
    n = int((xn-x)/h)

    xp = np.linspace( x, xn, n+1)
    yp = np.empty( n+1, float)
    yp[0] = y
    for i in range(len(xp)):
        yp[i] = dv(xp[i])
        

    #  Plotar funções
    plt.plot( xp, yp, 'ro')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(['Rk4'])
    plt.title('Runge-Kutta 4 X Analitico')
    plt.grid()
    plt.show()

####    print(y)
##    def ddy(y,x):
##        y,u = y
##        dydx = [u, q * x - y]                
##        return dydx
##
##    sol = odeint(ddy, y0, x)
##    print(sol, x)
##    y = odeint(funcaoCortante, x)    

    #################################################################
    ## Plotagem dos Diagramas de Momento    
    ## xi = ponto inicial da plotagem do diagrama
    ## xf = ponto final da plotagem do diagrama
##    xi = xf = 0.0
##    plt.subplot(211)
##    plt.ylabel('Momento (kN.m)')
##    plt.xlabel('vao (m)')
##    plt.grid()
##    for i in range(0, len(lista_vaos)):
##        # função de diagrama para o vão em questão
##        f = funcoes[i] 
##        # valor coordenada x final
##        xf += lista_vaos[i]
##        # valor da coordenada y final
##        yf = f(xf) 
##        # valor da coordenada y inicial
##        yi = f(xi) 
##        # cria uma sequencia de pontos na coordenada x
##        x = np.arange(xi, xf, 0.001)
##        # a partir de f, cria os pontos y para cada coordenada x
##        y = f(x)
##        ## plotar valores dos momentos nos extremos e meio do vao
##        plt.text(xi, yi, '%.2f kN.m' % yi, fontsize=8)
##        plt.text(xf, yf, '%.2f kN.m' % yf, fontsize=8)
##        #plotar representacao da viga
##        plt.plot([xi,xf],[0., 0.],'k')
##        plt.plot(x, y, 'b')
##        xi = xf # para a proxima iteração, o ponto inicial sera o final desta

##    ## Plotagem dos Diagramas de Cortante - Derivadas de f(x)
##    ## xi = ponto inicial da plotagem do diagrama
##    ## xf = ponto final da plotagem do diagrama
##    xf = xi = 0
##    plt.subplot(212)
##    plt.ylabel('Cortante (kN)')
##    plt.xlabel('vao (m)')
##    plt.grid()
##    for i in range(0, len(lista_vaos)):
##        # função de diagrama para o vão em questão
##        f = funcoes[i]
##        h = 0.001 # valor de 'erro' para a derivação
##        # valor da coordenada y inicial
##        yi = derivative(f, xi, h, 1)
##        # valor coordenada x final
##        xf += lista_vaos[i]
##        # valor da coordenada y final
##        yf = derivative(f, xf, h, 1)
##        # cria uma sequencia de pontos na coordenada x
##        x = np.linspace(xi, xf, 1000)        
##        # a partir da derivada de f, cria os pontos y para cada coordenada x
##        y = derivative(f, x, h, 1)
##        ## plotar valores dos cortantes nos extremos e meio do vao
##        plt.text(xi, yi, '%.2f kN' % yi, fontsize=8)
##        plt.text(xf, yf, '%.2f kN' % yf, fontsize=8)
##        #grafica
##        #plotar representacao da viga
##        plt.plot([xi,xf],[0., 0.],'k')
##        #desnivel entre cortantes
##        plt.plot([xi,xi], [0.0, yi], 'b')
##        plt.plot([xf, xf], [yf, 0.0], 'b')
##        plt.plot(x, y, 'b')
##        xi = xf
##
##    ## Calculo dos momentos nos apoios, sem diagramas - RETIRAR
##    vao = 0
##    reac = 0
##    momentos = []
##    momentos.append(0.0)
##    for i in range(1, len(reacoes)-1):
##        vao += lista_vaos[i-1]
##        reac = 0
##        for j in range(i):
##            for k in range(j+1):
##                reac += reacoes[k] * lista_vaos[j]
##        mq = q * vao **2 / 2.0
##        momentos.append(reac - q * vao **2 / 2.0)

    print("reaçoes semi rigidas")
    print(reacoes)
    plt.show()

    sair = str(input("Sair (q/s/y):  "))








