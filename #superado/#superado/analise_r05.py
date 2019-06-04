import numpy as np
from numpy.linalg import inv
from tramos_r12 import Tramos
from scipy.integrate import nquad
from scipy.optimize import newton
import dimensionamento_R02 as dim
import plotar_R01 as plot

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

sair = ""

while sair != 'q' or sair != 'S' or sair != 's' or sair != 'y'or sair != 'Y':
    #    n_vaos = int(input("Inserir quantidade de vaos:  "))
    nvaos = 4

    n_list = []
    lista_tramos = []
    lista_sub = []

    ponta_esq = "ponta_esquerda"  # "ponta_direita"#
    ponta_dir = "ponta_direita"
    intermediario = "intermediario"

    e = 2.0 * (10 ** 8)  # kN/m2 ##E = 200000 # MPa

    # (Es, E,   fys, ha, d, bf, tw, tf, hdeck, vao, vaoad, largInfluencia, interna)
    dictVal = dict()
    dictVal['Asl'] = Asl = 4.91
    dictVal['fck'] = fck = 2.
    dictVal['fys'] = fys = 50
    dictVal['hdeck'] = hdeck = 140.  # mm
    dictVal['es'] = es = 2.1 * (10 ** 8)
    dictVal['fy'] = fy = 35.
    dictVal['ha'] = ha = 25.
    dictVal['d'] = d = 30.  # cm
    dictVal['bf'] = bf = 14.  # cm
    dictVal['tf'] = tf = 0.475  # cm
    dictVal['tw'] = tw = 0.8  # cm
    dictVal['bInfl'] = bInfl = 2.50  # m

    # bInfl = 3.75# largura de influencia da viga

    q = 5.  # kN/m

    # ei = e * i  #  30508 # kN.m2
    lista_vaos = [7.5] * nvaos

    condicao = 'pos-cura'

    # k1 = ke = vinculo semi-rigido do lado esquerdo do tramo
    # k2 = kd = vinculo semi-rigido do lado direito do tramo
    # vao = valor do vao do tramo
    for j in range(nvaos):  # range(n_vaos):
        if j == 0:
            tramo = Tramos(j, lista_vaos[j], e, ponta_esq, d, bf, tw, tf)
            for sub in tramo.create_subs(condicao, [0, lista_vaos[j+1]],
                                         bInfl, 0,
                                         hdeck, Asl,
                                         fck, fy, e):
                lista_sub.append(sub)
            
        elif j == nvaos - 1 and j != 0:
            tramo = Tramos(j, lista_vaos[j], e, ponta_dir, d, bf, tw, tf)
            for sub in tramo.create_subs(condicao, [lista_vaos[j-1],0],
                                         bInfl, 0,
                                         hdeck, Asl,
                                         fck, fy, e):
                lista_sub.append(sub)
        else:
            tramo = Tramos(j, lista_vaos[j], e, intermediario, d, bf, tw, tf)
            for sub in tramo.create_subs(condicao, [lista_vaos[j-1], lista_vaos[j+1]],
                                         bInfl, 1,
                                         hdeck, Asl,
                                         fck, fy, e):
                lista_sub.append(sub)

    # reacoes = calculo_semi_rigido(lista_sub, q, lista_vaos)

    n = len(lista_sub)
    nvaos = int((n - 4) / 3 + 2)

    napoios = nvaos + 1
    nef = napoios + (napoios - 2) * 4

    kij = np.zeros((nef, nef))
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
                vaoad1 = 0  # lista_sub[j-1].vao
                vaoad2 = lista_vaos[tramo.n+1]

        ei = tramo.e * tramo.i

        eng = (10 ** 9) * ei / vao  # extremidade rigida, 'k' aproxima-se de valores de 10^9 x EI / L
        # print('tramo ', tramo.momento)
        C1, _, _ = dim.calculo_C(es, e,
                                 Asl, fck, fys, ha,
                                 d, bf, tw, tf, hdeck,
                                 vaoc, vaoad1, bInfl)
        C1 *= 1 / 100.
        C2, _, _ = dim.calculo_C(es, e,
                                 Asl, fck, fys, ha,
                                 d, bf, tw, tf, hdeck,
                                 vaoc, vaoad2, bInfl)
        C2 *= 1 / 100.
        if tramo.momento == 'neg':
            print('tramo n %d \t  sub %d \tk1/ke = %.2f kN.m/rad\t k2/kd = %.2f kN.m/rad' % (tramo.n, tramo.idSub,C1, C2))

        kk1 = C1  # 12000. kN.m/rad
        kk2 = C2  # 12000. kN.m/rad

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

                tramo.me_0 = q * vao ** 2 * e2(6) / (12 * e2(4))  # M2
                tramo.ve_0 = q * vao * e2(5) / (2 * e2(4))  # R2
                tramo.md_0 = - q * vao ** 2 / (12 * e2(4))  # M1
                tramo.vd_0 = q * vao * e2(3) / (2 * e2(4))  # R1

                tramo.rigidez(k1, k2)

                f_ep[j] += tramo.me_0
                f_ep[j + 1] += tramo.md_0
                f_ep[j + 2] += tramo.vd_0

                kij[j, j] += tramo.me_1
                kij[j, j + 1] += tramo.md_1
                kij[j, j + 2] += tramo.vd_1

                kij[j + 1, j] += tramo.me_2
                kij[j + 1, j + 1] += tramo.md_2
                kij[j + 1, j + 2] += tramo.vd_2

                kij[j + 2, j] += tramo.me_4
                kij[j + 2, j + 1] += tramo.md_4
                kij[j + 2, j + 2] += tramo.vd_4

            else:
                k1 = eng  # ke
                k2 = kk2  # eng#ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                e2 = lambda z, er: 1 + z * er

                tramo.me_0 = q * vao ** 2 * e2(6, er2) / (12 * e2(4, er2))  # M2
                tramo.ve_0 = q * vao * e2(5, er2) / (2 * e2(4, er2))  # R2
                tramo.md_0 = - q * vao ** 2 / (12 * e2(4, er2))  # M1
                tramo.vd_0 = q * vao * e2(3, er2) / (2 * e2(4, er2))  # R1

                tramo.rigidez(k1, k2)

                f_ep[j] += tramo.me_0
                f_ep[j + 1] += tramo.ve_0
                f_ep[j + 2] += tramo.md_0

                kij[j, j] += tramo.me_1
                kij[j, j + 1] += tramo.ve_1
                kij[j, j + 2] += tramo.md_1

                kij[j + 1, j] += tramo.me_3
                kij[j + 1, j + 1] += tramo.ve_3
                kij[j + 1, j + 2] += tramo.md_3

                kij[j + 2, j] += tramo.me_2
                kij[j + 2, j + 1] += tramo.ve_2
                kij[j + 2, j + 2] += tramo.md_2

        elif tramo.n == (nvaos - 1):
            if tramo.idSub == 2:
                k1 = eng  # ke
                k2 = eng  # ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)

                tramo.me_0 = q * vao ** 2 * e2(6) / (12 * e2(4))  # M2
                tramo.ve_0 = q * vao * e2(5) / (2 * e2(4))  # R2
                tramo.md_0 = - q * vao ** 2 / (12 * e2(4))  # M1
                tramo.vd_0 = q * vao * e2(3) / (2 * e2(4))  # R1

                tramo.rigidez(k1, k2)

                f_ep[nef - 1 - 2] += tramo.me_0
                f_ep[nef - 1 - 1] += tramo.ve_0
                f_ep[nef - 1] += tramo.md_0

                kij[nef - 1 - 2, nef - 1 - 2] += tramo.me_1
                kij[nef - 1 - 2, nef - 1 - 1] += tramo.ve_1
                kij[nef - 1 - 2, nef - 1] += tramo.md_1

                kij[nef - 1 - 1, nef - 1 - 2] += tramo.me_3
                kij[nef - 1 - 1, nef - 1 - 1] += tramo.ve_3
                kij[nef - 1 - 1, nef - 1] += tramo.md_3

                kij[nef - 1, nef - 2 - 1] += tramo.me_2
                kij[nef - 1, nef - 1 - 1] += tramo.ve_2
                kij[nef - 1, nef - 1] += tramo.md_2

            else:
                k1 = kk1  # eng#ke
                k2 = eng  # ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                e2 = lambda z, er: 1 + z * er

                tramo.md_0 = - q * vao ** 2 * e2(6, er1) / (12 * e2(4, er1))  # M2
                tramo.vd_0 = q * vao * e2(5, er1) / (2 * e2(4, er1))  # R2
                tramo.me_0 = q * vao ** 2 / (12 * e2(4, er1))  # M1
                tramo.ve_0 = q * vao * e2(3, er1) / (2 * e2(4, er1))  # R1

                tramo.rigidez(k1, k2)

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

                tramo.rigidez(k1, k2)
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

                tramo.rigidez(k1, k2)
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

                tramo.rigidez(k1, k2)
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
    soma += reacoes[4]

    #    print('soma das reações: %.2f' % soma)
    j = 0
    for i in range(1, len(lista_vaos)):
        n = (i + 1) * 3 - 2 - 2
        tramoi = lista_sub[n - 1]
        tramoj = lista_sub[n]
        k = (tramoj.n * 6) - (tramoj.n - 1) + 3 - 1
        reacoes[i] += tramoi.vd_0 + dij[k - 7] * tramoi.vd_1 + dij[k - 6] * tramoi.vd_3 + dij[k - 5] * tramoi.vd_2
        reacoes[i] += tramoj.ve_0 + dij[k - 5] * tramoj.ve_1 + dij[k - 4] * tramoj.ve_2 + dij[k - 3] * tramoj.ve_4

        soma += reacoes[i]

    vaoTotal = 0
    listaDx = [0]
    dicReacoes = dict()
    dicReacoes[0] = reacoes[0]
    listaRaizes = []
    # cria uma lista com os valores de x, contanto da origem até o proximo apoio
    # cria um dicionario com o valor de x e o valor de reação do apoio
    for i in range(0, len(lista_vaos)):
        vaoTotal += lista_vaos[i]
        listaDx.append(vaoTotal)
        dicReacoes[vaoTotal] = reacoes[i + 1]

    #  Função cortante, escrita como derivada da função Momento
    def dy(x):
        v = 0
        vr = 0
        v -= x * q  # valor proveniente da carga distribuida
        for key, value in dicReacoes.items():
            if x > key:
                vr += value
        v += vr
        return v

    # Valores de 'x' em que o cortante é zero = momento positivo é maximo
    for i in range(len(listaDx)):
        try:
            root = newton(dy, listaDx[i])
            if root not in listaRaizes:
                listaRaizes.append(root)
        except:
            print('x = %.2f nao deu raiz' % listaDx[i])
        try:
            root = newton(dy, listaDx[i]*.5)
            if root not in listaRaizes:
                listaRaizes.append(root)
        except:
            print('x = %.2f nao deu raiz' % listaDx[i]*.5)

            # listaRaizes.add(newton(dy, listaDx[i]))

    listaMomentos = []
    listaMomentosPos = []
    dictMomentosPos = dict()
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
    for i in range(len(xp)):
        ypv[i] = dy(xp[i])

    for i in listaDx:
        xi = i
        listaCortantes.append([xi, dy(i)])
        yi = dy(xi)
        if xi < vaoTotal:
            yi = dy(i + h)
            xi = i
            listaCortantes.append([xi, yi])

    # Diagrama de Momento
    ypm = np.empty(n + 1, float)
    ypmi = 0
    ypm[0] = 0
    for i in range(0, n + 1):
        ypm[i], _ = nquad(dy, [[0, xp[i]]])  # integral da função Cortante 'dy'

    for root in listaRaizes:
        # if xp[i] == root:
        yi,_ = nquad(dy, [[0, root]])
        # dictMomentosPos[root] = yi
        listaMomentosPos.append([root, yi])

    # impressão dos valores de momentos negativos nos apoios
    for i in range(1, n):
        for j in range(len(listaDx)):
            if (x + i * h) == (listaDx[j]):
                xi = (x + i * h)
                yi = ypm[i]
                listaMomentos.append([xi, ypm[i]])

    # # impressao dos valores de momentos maximos positivos
    # for xi in listaRaizes:
    #     yi,_ = nquad(dy, [[0, xi]])

    print("reaçoes semi rigidas")
    print(reacoes)
    # print('Momentos POsitivos')
    # for arr in listaMomentosPos:
    #     print('x = %.2f \t M+ = %.2f kN.m' % (arr[0], arr[1]))
    #
    # print('\n Momentos Negativos')
    # for arr in listaMomentos:
    #     print('x = %.2f \t M- = %.2f kN.m' % (arr[0], arr[1]))
    #
    # print('\n Cortantes')
    # for arr in listaCortantes:
    #     print('x = %.2f \t V = %.2f  kN' % (arr[0], arr[1]))

    plot.plotar_diagramas(x, xn, xp, ypv, ypm, listaCortantes, listaMomentos, listaMomentosPos)

    q = input('sair???  q/quit/s/S/y/Y')









