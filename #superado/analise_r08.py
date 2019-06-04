import numpy as np
from numpy.linalg import inv
from tramos_r14 import Tramos
from scipy.integrate import nquad
from scipy.optimize import newton
import dimensionamento_R04 as dim
import plotar_R01 as plot
from propriedades_perfil_i import wx, i_x

# k1 = ke = vinculo semi-rigido do lado esquerdo do tramo
# k2 = kd = vinculo semi-rigido do lado direito do tramo
# vao = valor do vao do tramo
# q = carga distribuida
# i = Inercia do perfil

# TODO acrescentar condições para pre-cura e pos-cura
# TODO criar condicionantes para carregamentos diferentes
# TODO calcular flechas
# TODO vincular com rotina de plotagem
# TODO criar função/metodo de analise

um = 2

bInfl = 3.75  # m

cp = 2.5  # kN/m2
cpsd = 2.8  # kN/m2
sc = 5.  # kN/m2
scm = 1.00  # kN/m2
# combinações
qd = (1.2*(cp + cpsd + .40) + 1.6*sc) * bInfl

ql =  (1.*sc + cp) * bInfl
qglinha = 1*(cpsd + .40) * bInfl

qdlinha = 1.2 * qglinha * 1.6 * 1 * bInfl

qd = (1.2*(cpsd + .40 + cp) + 1.6* sc) * bInfl

#combinações raras
qlong =  1.* cp * bInfl
qsc =  1.*sc * bInfl

nvaos = 9
lista_vaos = [12.5] * nvaos

# Armaduras do negativo
nbarras = 4
bitola = 1.6 # cm
Asl = 3.14 * (bitola/2) ** 2 * nbarras

n_list = []
lista_tramos = []
lista_sub = []
e = 2.0 * (10 ** 8)  # kN/m2 ##E = 200000 # MPa

# (Es, E,   fys, ha, d, bf, tw, tf, hdeck, vao, vaoad, largInfluencia, interna)
dictVal = dict()
dictVal['es'] =  es = 2.1 * (10 ** 8)  # kN/m2
dictVal['fy'] =  fy =       34.5       # kN/cm2
dictVal['fck'] = fck =      2.         # kN/cm2
dictVal['fys'] = fys =      50         # kN/cm2
dictVal['ha'] =  ha =       25.        # cm
dictVal['Asl'] = Asl # cm2   = 3.14 * (bitola/2) ** 2 * nbarras

dictVal['hdeck'] = hdeck = 150.    # mm    
dictVal['d'] = d =          68.    # cm
dictVal['bfs'] = bfs =      15.    # cm
dictVal['bfi'] = bfi =      15.    # cm
dictVal['tw'] = tw =         0.8   # cm
dictVal['tfs'] = tfs =       0.8   # cm
dictVal['tfi'] = tfi =       0.8   # cm
dictVal['bInfl'] = bInfl


ponta_esq = "ponta_esquerda"  # "ponta_direita"#
ponta_dir = "ponta_direita"
intermediario = "intermediario"

#Condição de analise
listaCondicao = ['curta','longa']
condicao = 'longa'#'pos-cura'

listaMomentosMestre = []
listaMomentosPosMestre = []
listaCortantesMestre = []

listaQ = [[qd, 'D'], [qglinha, 'G\''],[qdlinha, 'D\''], [ql, 'L'], [qsc, 'Curta'], [qlong,'Longa']]

for j in range(nvaos):  # range(n_vaos):
    if j == 0:
        tramo = Tramos(j, lista_vaos[j], e, ponta_esq, d, bfs, bfi, tw, tfs, tfi)
        for sub in tramo.create_subs(condicao, [0, lista_vaos[j+1]],
                                     bInfl, 0,
                                     hdeck, Asl,
                                     fck, fy, e):
            lista_sub.append(sub)
        
    elif j == nvaos - 1 and j != 0:
        tramo = Tramos(j, lista_vaos[j], e, ponta_dir, d, bfs, bfi, tw, tfs, tfi)
        for sub in tramo.create_subs(condicao, [lista_vaos[j-1],0],
                                     bInfl, 0,
                                     hdeck, Asl,
                                     fck, fy, e):
            lista_sub.append(sub)
    else:
        tramo = Tramos(j, lista_vaos[j], e, intermediario, d, bfs, bfi, tw, tfs, tfi)
        for sub in tramo.create_subs(condicao, [lista_vaos[j-1], lista_vaos[j+1]],
                                     bInfl, 1,
                                     hdeck, Asl,
                                     fck, fy, e):
            lista_sub.append(sub)
##for condicao in listaCondicao:
##    print(condicao)
for q, text in listaQ:
    n = len(lista_sub)

    napoios = nvaos + 1
    nef = napoios + (napoios - 2) * 4

    kij  = np.zeros((nef, nef))
    f_ep = np.zeros((nef, 1))

    for j in range(n):
        tramo = lista_sub[j]
        vao = tramo.vao
        vaoc = lista_vaos[tramo.n]
        vaoad1 = vaoad2 = 0

        if tramo.momento == 'neg':
            if tramo.idSub == 1:
                vaoad1 = lista_vaos[tramo.n-1]
                vaoad2 = 0
            elif tramo.idSub == 3:
                vaoad1 = 0 
                vaoad2 = lista_vaos[tramo.n+1]
        # momento positivo de analise
        i = 0
        if tramo.momento == 'neg':
            i = tramo.iefNeg # 7500*100**-4#
        elif tramo.momento == 'pos':
            if text == 'Curta':
                i = tramo.iefPosCurta #10000*100**-4#
            elif text == 'Longa':
                i = tramo.iefPosLonga  # 10000*100**-4#
            else:
                i = tramo.iefPosLonga  # 10000*100**-4#
        inercia = i
        ei = tramo.e * inercia
        eng = (10 ** 9) * ei / vao  # extremidade rigida, 'k' aproxima-se de valores de 10^9 x EI / L
        
        C1, tetau1, ylnp1, mrd_neg1 = dim.calculo_C(es, e,
                                 Asl, fck, fys, ha,
                                 d, bfs, bfi, tw, tfs, tfi, hdeck,
                                 vaoc, vaoad1, bInfl)
        C1 *= 1 / 100.
        
        C2, tetau2, ylnp2, mrd_neg2 = dim.calculo_C(es, e,
                                 Asl, fck, fys, ha,
                                 d, bfs, bfi, tw, tfs, tfi, hdeck,
                                 vaoc, vaoad2, bInfl)
        C2 *= 1 / 100.
        
        tramo.mrdNeg = min(mrd_neg1, mrd_neg2)
    ##    print(tramo.n, tramo.idSub,tramo.iefNeg*100**4,tramo.iefPosLonga*100**4,C1, C2)

        kk1 = C1  # 12000. kN.m/rad
        kk2 = C2  # 12000. kN.m/rad
##        if tramo.n < 2:
##            if q == qult:
##                print('Tramo %d  %s - Inercia = %.2f cm4\t C = %.2f kNm/rad' %(tramo.n, tramo.momento, inercia*100**4, C1), C2)
    ##    print(' EI/C = %.2f \t C/ei = %.2f' %(inercia*e / C1, C1 / inercia*e))
        
        # Utilizando a dissertação de André Christoforo
        # pagina 40(pdf)
        e1 = lambda z: 1 + z * er1
        e2 = lambda z: 1 + z * er2

        if tramo.n == 0:
            if tramo.idSub == 1:
                k1 = eng  # ke
                k2 = eng  # ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                e2 = lambda z: 1 + z * er2

                tramo.me_0 = q * vao ** 2 * e2(6) / (12 * e2(4))  # M2
                tramo.ve_0 = q * vao * e2(5) / (2 * e2(4))  # R2
                tramo.md_0 = - q * vao ** 2 / (12 * e2(4))  # M1
                tramo.vd_0 = q * vao * e2(3) / (2 * e2(4))  # R1

                tramo.rigidez(k1, k2, inercia)

                f_ep[j] += tramo.me_0
                f_ep[j + 1] += tramo.md_0
                f_ep[j + 2] += tramo.vd_0

                kij[j, j]     += tramo.me_1
                kij[j, j + 1] += tramo.md_1
                kij[j, j + 2] += tramo.vd_1

                kij[j + 1, j]     += tramo.me_2
                kij[j + 1, j + 1] += tramo.md_2
                kij[j + 1, j + 2] += tramo.vd_2

                kij[j + 2, j]     += tramo.me_4
                kij[j + 2, j + 1] += tramo.md_4
                kij[j + 2, j + 2] += tramo.vd_4

            else:
                k1 = eng  # ke
                k2 = kk2  # eng#ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                e2 = lambda z, er: 1 + z * er

                tramo.me_0 =   q * vao ** 2 * e2(6, er2) / (12 * e2(4, er2))  # M2
                tramo.ve_0 =   q * vao * e2(5, er2) / (2 * e2(4, er2))  # R2
                tramo.md_0 = - q * vao ** 2 / (12 * e2(4, er2))  # M1
                tramo.vd_0 =   q * vao * e2(3, er2) / (2 * e2(4, er2))  # R1

                tramo.rigidez(k1, k2, inercia)

                f_ep[j]     += tramo.me_0
                f_ep[j + 1] += tramo.ve_0
                f_ep[j + 2] += tramo.md_0

                kij[j, j]     += tramo.me_1
                kij[j, j + 1] += tramo.ve_1
                kij[j, j + 2] += tramo.md_1

                kij[j + 1, j]     += tramo.me_3
                kij[j + 1, j + 1] += tramo.ve_3
                kij[j + 1, j + 2] += tramo.md_3

                kij[j + 2, j]     += tramo.me_2
                kij[j + 2, j + 1] += tramo.ve_2
                kij[j + 2, j + 2] += tramo.md_2

        elif tramo.n == (nvaos - 1): # ponta direita
            if tramo.idSub == 2: #segundo sub tramo
                k1 = eng  # ke
                k2 = eng  # ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                e2 = lambda z: 1 + z * er2

                tramo.me_0 = q * vao ** 2 * e2(6) / (12 * e2(4))  # M2
                tramo.ve_0 = q * vao * e2(5) / (2 * e2(4))  # R2
                tramo.md_0 = - q * vao ** 2 / (12 * e2(4))  # M1
                tramo.vd_0 = q * vao * e2(3) / (2 * e2(4))  # R1

                tramo.rigidez(k1, k2, inercia)

                f_ep[nef - 1 - 2] += tramo.me_0
                f_ep[nef - 1 - 1] += tramo.ve_0
                f_ep[nef - 1]     += tramo.md_0

                kij[nef - 1 - 2, nef - 1 - 2] += tramo.me_1
                kij[nef - 1 - 2, nef - 1 - 1] += tramo.ve_1
                kij[nef - 1 - 2, nef - 1]     += tramo.md_1

                kij[nef - 1 - 1, nef - 1 - 2] += tramo.me_3
                kij[nef - 1 - 1, nef - 1 - 1] += tramo.ve_3
                kij[nef - 1 - 1, nef - 1]     += tramo.md_3

                kij[nef - 1, nef - 2 - 1] += tramo.me_2
                kij[nef - 1, nef - 1 - 1] += tramo.ve_2
                kij[nef - 1, nef - 1]     += tramo.md_2

            else: # primeiro sub tramo, no apoio
                k1 = kk1  # eng#ke
                k2 = eng  # ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                e2 = lambda z, er: 1 + z * er

                tramo.md_0 = - q * vao ** 2 * e2(6, er1) / (12 * e2(4, er1))  # M2
                tramo.vd_0 = q * vao * e2(5, er1) / (2 * e2(4, er1))  # R2
                tramo.me_0 = q * vao ** 2 / (12 * e2(4, er1))  # M1
                tramo.ve_0 = q * vao * e2(3, er1) / (2 * e2(4, er1))  # R1

                tramo.rigidez(k1, k2, inercia)

                f_ep[nef - 3 - 1] += tramo.me_0
                f_ep[nef - 2 - 1] += tramo.md_0
                f_ep[nef - 1 - 1] += tramo.vd_0

                kij[nef - 3 - 1, nef - 3 - 1] += tramo.me_1
                kij[nef - 3 - 1, nef - 2 - 1] += tramo.md_1
                kij[nef - 3 - 1, nef - 1 - 1] += tramo.vd_1

                kij[nef - 2 - 1, nef - 3 - 1] += tramo.me_2
                kij[nef - 2 - 1, nef - 2 - 1] += tramo.md_2
                kij[nef - 2 - 1, nef - 1 - 1] += tramo.vd_2

                kij[nef - 1 - 1, nef - 3 - 1] += tramo.me_4
                kij[nef - 1 - 1, nef - 2 - 1] += tramo.md_4
                kij[nef - 1 - 1, nef - 1 - 1] += tramo.vd_4

        else:
            if tramo.idSub == 1:
                k1 = kk1  # eng#ke
                k2 = eng  # ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                e2 = lambda z, er: 1 + z * er

                tramo.md_0 = - q * vao ** 2 * e2(6, er1) / (12 * e2(4, er1))  # M2
                tramo.vd_0 = q * vao * e2(5, er1) / (2 * e2(4, er1))  # R2
                tramo.me_0 = q * vao ** 2 / (12 * e2(4, er1))  # M1
                tramo.ve_0 = q * vao * e2(3, er1) / (2 * e2(4, er1))  # R1

                tramo.rigidez(k1, k2, inercia)
                k = (tramo.n * 6) - (tramo.n - 1) + 3 - 1

                f_ep[k - 5] += tramo.me_0
                f_ep[k - 4] += tramo.md_0
                f_ep[k - 3] += tramo.vd_0

                kij[k - 5, k - 5] += tramo.me_1
                kij[k - 5, k - 4] += tramo.md_1
                kij[k - 5, k - 3] += tramo.vd_1

                kij[k - 4, k - 5] += tramo.me_2
                kij[k - 4, k - 4] += tramo.md_2
                kij[k - 4, k - 3] += tramo.vd_2

                kij[k - 3, k - 5] += tramo.me_4
                kij[k - 3, k - 4] += tramo.md_4
                kij[k - 3, k - 3] += tramo.vd_4

            elif tramo.idSub == 2:
                k1 = kk1
                k2 = kk2
                a = (2 * ei / vao) * 1 / k1
                b = (2 * ei / vao) * 1 / k2
                ##
                tramo.me_0 = + ((3 * b + 1) * q * vao ** 2) / (12 * (3 * b * a + 2 * b + 2 * a + 1))
                tramo.md_0 = - ((3 * a + 1) * q * vao ** 2) / (12 * (3 * b * a + 2 * b + 2 * a + 1))
                tramo.ve_0 = (tramo.md_0 + tramo.me_0 + q * vao ** 2 / 2.0) / vao
                tramo.vd_0 = q * vao - tramo.ve_0

                tramo.rigidez(k1, k2, inercia)
                k = (tramo.n * 6) - (tramo.n - 1) + 3 - 1

                f_ep[k - 4] += tramo.me_0
                f_ep[k - 3] += tramo.ve_0
                f_ep[k - 2] += tramo.md_0
                f_ep[k - 1] += tramo.vd_0

                kij[k - 4, k - 4] += tramo.me_1
                kij[k - 4, k - 3] += tramo.ve_1
                kij[k - 4, k - 2] += tramo.md_1
                kij[k - 4, k - 1] += tramo.vd_1

                kij[k - 3, k - 4] += tramo.me_3
                kij[k - 3, k - 3] += tramo.ve_3
                kij[k - 3, k - 2] += tramo.md_3
                kij[k - 3, k - 1] += tramo.vd_3

                kij[k - 2, k - 4] += tramo.me_2
                kij[k - 2, k - 3] += tramo.ve_2
                kij[k - 2, k - 2] += tramo.md_2
                kij[k - 2, k - 1] += tramo.vd_2

                kij[k - 1, k - 4] += tramo.me_4
                kij[k - 1, k - 3] += tramo.ve_4
                kij[k - 1, k - 2] += tramo.md_4
                kij[k - 1, k - 1] += tramo.vd_4

            elif tramo.idSub == 3:
                k1 = eng  # ke
                k2 = kk2  # eng#ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                e2 = lambda z, er: 1 + z * er

                tramo.me_0 = q * vao ** 2 * e2(6, er2) / (12 * e2(4, er2))  # M2
                tramo.ve_0 = q * vao * e2(5, er2) / (2 * e2(4, er2))  # R2
                tramo.md_0 = - q * vao ** 2 / (12 * e2(4, er2))  # M1
                tramo.vd_0 = q * vao * e2(3, er2) / (2 * e2(4, er2))  # R1

                tramo.rigidez(k1, k2, inercia)
                k = (tramo.n * 6) - (tramo.n - 1) + 3 - 1

                f_ep[k - 2] += tramo.me_0
                f_ep[k - 1] += tramo.ve_0
                f_ep[k] += tramo.md_0

                kij[k - 2, k - 2] += tramo.me_1
                kij[k - 2, k - 1] += tramo.ve_1
                kij[k - 2, k] += tramo.md_1

                kij[k - 1, k - 2] += tramo.me_3
                kij[k - 1, k - 1] += tramo.ve_3
                kij[k - 1, k] += tramo.md_3

                kij[k, k - 2] += tramo.me_2
                kij[k, k - 1] += tramo.ve_2
                kij[k, k] += tramo.md_2

    ##print(kij)
    ##print(f_ep)
    kij_inv = inv(kij)
    dij = kij_inv.dot(-f_ep)

    # determinacao das reaçoes
    reacoes = [0] * (nvaos + 1)
    tramo = lista_sub[0]
    tramoult = lista_sub[-1]

    soma = 0
    reacoes[0] += tramo.ve_0 + dij[0] * tramo.ve_1 + dij[1] * tramo.ve_2 + dij[2] * tramo.ve_4
    soma += reacoes[0]

    reacoes[-1] += tramoult.vd_0 + dij[-3] * tramoult.vd_1 + dij[-2] * tramoult.vd_3 + dij[-1] * tramoult.vd_2
    soma += reacoes[-1]

    j = 0
    for p in range(1, len(lista_vaos)):
        n = (p + 1) * 3 - 2 - 2
        tramoi = lista_sub[n - 1]
        tramoj = lista_sub[n]
        k = (tramoj.n * 6) - (tramoj.n - 1) + 3 - 1
        reacoes[p] += tramoi.vd_0 + dij[k - 7] * tramoi.vd_1 + dij[k - 6] * tramoi.vd_3 + dij[k - 5] * tramoi.vd_2
        reacoes[p] += tramoj.ve_0 + dij[k - 5] * tramoj.ve_1 + dij[k - 4] * tramoj.ve_2 + dij[k - 3] * tramoj.ve_4

        soma += reacoes[p]

    vaoTotal = 0
    listaDx = [0]
    listaReacoes = []
    listaReacoes.append([0.0, reacoes[0]])
    listaRaizes = []
    # cria uma lista com os valores de x, contanto da origem até o proximo apoio
    # cria um dicionario com o valor de x e o valor de reação do apoio
    for i in range(0, len(lista_vaos)):
        vaoTotal += lista_vaos[i]
        listaDx.append(vaoTotal)
        listaReacoes.append([vaoTotal, reacoes[i+1]])
        
    #  Função cortante, escrita como derivada da função Momento
    def dy(x):
        v = 0
        vr = 0
        v -= x * q  # valor proveniente da carga distribuida
        for value in listaReacoes:
            if x > value[0]:
                vr += value[1]
        v += vr
        return v


    def dm(x):
        m = 0
        mr = 0
        m -= q * x**2 / 2.  # valor proveniente da carga distribuida
        for value in listaReacoes:
            if x >= value[0]:
                mr += value[1] * (x - value[0])
        m += mr
        return m

    # Valores de 'x' em que o cortante é zero = momento positivo é maximo
    for j in range(len(listaDx)):
        try:
            root = newton(dy, listaDx[j])
            if root not in listaRaizes:
                listaRaizes.append(root)
        except:
            raiz = 0
        try:
            root = newton(dy, listaDx[j]*.5)
            if root not in listaRaizes:
                listaRaizes.append(root)
        except:
            raiz = 0

            # listaRaizes.add(newton(dy, listaDx[i]))

    listaMomentos = []
    listaMomentosPos = []
    listaCortantes = []

    # # Inicio da montagem dos diagramas
    # # Diagrama cortante
    x = 0  # valor inicial de x
    y = 0  # valor inicial de y
    xn = vaoTotal  # valor final de x
    h = 0.5  # valor 'step' para cada iteração
    n = int((xn - x) / h)  # numero de iterações

    xp = np.linspace(x, xn, n + 1)  # coordenadas de x
    ypv = np.empty(n + 1, float)  # coordenadas de y
    ypv[0] = y
    for j in range(len(xp)):
        ypv[j] = dy(xp[j])

    for j in listaDx:
        xi = j
        listaCortantes.append([xi, dy(j)])
        yi = dy(xi)
        if xi < vaoTotal:
            yi = dy(j + h)
            xi = j
            listaCortantes.append([xi, yi])

    # Diagrama de Momento
    ypm = np.empty(n + 1, float)
    ypmi = 0
    ypm[0] = 0
    for i in range(len(xp)):
        ypm[i] = dm(xp[i])


    for k in range(1, n):
        for j in range(len(listaDx)):
            if (x + k * h) == (listaDx[j]):
                xi = (x + k * h)
                yi = ypm[k]
                listaMomentos.append([xi, ypm[k]])

    for root in listaRaizes:
        yi = dm(root)
        listaMomentosPos.append([root, yi])

    ##listaCortantesMestre.append(listaCortantes)
    ##listaMomentosPosMestre.append(listaMomentosPos)
    ##listaMomentosMestre.append(listaMomentos)
    ##print("\nreaçoes semi rigidas")
    ##print(reacoes)
##    print("\nMOMENTOS - semi rigidas")
##    for valor in listaMomentos:
##        print(valor[0], valor[1])
##
##    print("\nMOMENTOS + semi rigidas")
##    for valor in listaMomentosPos:
##        print(valor[0], valor[1])

    ##        plot.plotar_diagramas(x, xn, xp, ypv, ypm, listaCortantes, listaMomentos, listaMomentosPos)

    for j in range(4):#len(lista_sub)):
        tramo = lista_sub[j]
        if q == qd and 1==um: #tramo.momento == 'neg'and q == qult:
            if tramo.idSub == 1:
                print('\ntramo n: %d - sub: %s \t\t k1/ke = %.2f kN.m/rad' % (tramo.n, tramo.momento,C1))
                print('Tetau1: %.2f mrad  \t\t ylnp1: %.2f mm' % (tetau1, ylnp1))
                print('Mrd(+): %.2f kN.cm  \t Mrd(-): %.2f kN.cm ' % (tramo.mrdPos, tramo.mrdNeg))
                print('Ief(-): %.2f cm4' % (tramo.iefNeg*100**4))
    ##                print('WefCurta: %.2f cm3 \t WefLonga: %.2f cm3 ' % (tramo.wefCurta, tramo.wefLonga))
            elif tramo.idSub == 3:
                print('\ntramo n: %d - sub: %s \t\t k2/kd = %.2f kN.m/rad' % (tramo.n, tramo.momento, C2))
                print('Tetau2: %.2f mrad  \t\t ylnp2: %.2f mm  ' % (tetau2, ylnp2))
                print('Mrd(+): %.2f kN.cm  \t Mrd(-): %.2f kN.cm ' % (tramo.mrdPos, tramo.mrdNeg))
                print('Ief(-): %.2f cm4' % (tramo.iefNeg*100**4))
    ##                print('WefCurta: %.2f cm3 \t WefLonga: %.2f cm3 ' % (tramo.wefCurta, tramo.wefLonga))
            elif tramo.idSub == 2:
                print('\ntramo n: %d - sub: %s \t\t k2/kd = %.2f kN.m/rad' % (tramo.n, tramo.momento, C2))
                print('Tetau2: %.2f mrad  \t\t ylnp2: %.2f mm  ' % (tetau2, ylnp2))
                print('Mrd(+): %.2f kN.cm  \t Mrd(-): %.2f kN.cm' % (tramo.mrdPos, tramo.mrdNeg))
                print('Ief(-): %.2f cm4' % (tramo.iefNeg*100**4))
            print('IefCurta(+): %.2f cm4 \t\tIefLonga(+): %.2f cm4 \t' % (tramo.iefPosCurta*100**4, tramo.iefPosLonga*100**4))
            print('WefCurta: %.2f cm3 \t\tWefLonga: %.2f cm3 ' % (tramo.wefCurta * 100**3, tramo.wefLonga* 100**3))

##    plot.plotar_diagramas(x, xn, xp, ypv, ypm, listaCortantes, listaMomentos, listaMomentosPos)
##    for i in range(len(listaCondicao)):
    print('\n%s - %.2f kN/m'% (text,q))
    if q == qd and 1 == um:
        print('VMAX: %.2f  \t\tVMIN: %.2f  \t\t\t [kN]' %(min(ypv),max(ypv)))
    print('M(-)MAX: %.2f \tM1(-): %.2f \tM2(-): %.2f\t [kN.m]' %(min(ypm),listaMomentos[0][1], listaMomentos[2][1]))
    print('M(+)MAX: %.2f \tM1(+): %.2f \tM2(+): %.2f\t [kN.m]' %(max(ypm),listaMomentosPos[0][1], listaMomentosPos[2][1]))
    if text == 'Curta':
        mlCurta = max(ypm)
        mlNegCurta = min(ypm)
        
    if text == 'Longa':
        mlLonga = max(ypm)
        mlNegLonga = min(ypm)
    if text == 'D':
        md = max(ypm)
        vd = max(max(ypv),abs(min(ypv)))

    wPosCurta = tramo.wefCurta
    wPosLonga = tramo.wefLonga
    mrdPos = tramo.mrdPos * .85 /100
    mrdNeg = tramo.mrdNeg /100
    vrd = tramo.vrd

mg = qglinha * lista_vaos[0] ** 2 / 8.  # max(ypm)

mlNeg = mlNegCurta + mlNegLonga  # min(ypm)
yyy = (d*10*tw*10 + bfs*10*tfs*10+bfi*10*tfi*10 )/1000**2 * 7850
ia = round(i_x(d, tw, bfs, tfs, bfi, tfi), 2)
wa = round(wx(ia,d))
t1 = round((mg*100 / wa + mlCurta*100/(wPosCurta*100**3)+ mlLonga*100/(wPosLonga*100**3)),2)
ftc = round(abs(mlNeg*100) / (d + 7.5 + 3.5),2)
t2 = round(ftc / Asl,2)
t3 = round(ftc / ((bfs * tfs)/1.1),2)
pasl = Asl/100**2*4.35*7850
print('\nMg = %.2f kN.m' % mg)
print('WefCurta = %.2f cm3 \tWefCurta = %.2f cm3 ' % (wPosCurta*100**3, wPosLonga*100**3))

print('\nY = %.2f kg/m  %.1fx%.1fx%.1fx%.2fx%.2fx%.2f'%(yyy, d,bfs,bfi,tw,tfs,tfi))
print('Força T/C: %.2f' % ftc)

print('\nTensão M(+): %.2f kN/cm2 - %.2f - %.2f + %.2f + %.2f'%(t1, t1/fy, mg*100 / wa,mlCurta*100/(wPosCurta*100**3),mlLonga*100/(wPosLonga*100**3)))
print('Tensão Asl:  %.2f kN/cm2 - %.2f '%(t2, t2/fys))
print('Tensão BFS:  %.2f kN/cm2 - %.2f '%(t3, t3/fy))

print('\nAsl = %.2f cm2\t L = 4.35m\t Peso Armaduras = %.2f kg' %(Asl, pasl))
print('Peso linear Perfil + Armaduras = %.2f kg/m (sem cantoneiras)' % (yyy+pasl / 12.5))

print('\n3º Verificação: %.2f / %.2f = %.2f' %((md-mrdNeg), mrdPos,((md-mrdNeg)/mrdPos)))
print('4º Verificação: %.2f / %.2f = %.2f' %(vd, vrd,(vd/vrd)))






