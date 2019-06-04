import numpy as np
from numpy.linalg import inv
from tramos_r17 import Tramos
##from scipy.integrate import nquad, tplquad
##from scipy.optimize import newton
import dimensionamento_R10 as dim
##import plotar_R01 as plot
import metodos_numericos  as mn
from propriedades_perfil_i import wx, i_x, area
import time

import vm_db as datab
import vm_db_gerais as datab_gerais

db = r'vmsc.db'
dbg = r'vmsc_g.db'

# k1 = ke = vinculo semi-rigido do lado esquerdo do tramo
# k2 = kd = vinculo semi-rigido do lado direito do tramo
# vao = valor do vao do tramo
# q = carga distribuida
# i = Inercia do perfil

def calculo_sistema(nvaos, hdeck, cp, cpsd, sc, scm ):
    lista_vaos = []
    n_list = []
    lista_tramos = []
    lista_sub = []
    ppi = ppf = pp = 0
    diagrama_curta = diagrama_longa = []
    binfi = binff = bInfl = 0

    fy = float(datab_gerais.get_data(dbg, 'novo', 'fy'))
    fck = float(datab_gerais.get_data(dbg, 'novo', 'fck'))
    fys = float(datab_gerais.get_data(dbg, 'novo', 'fys'))
    ha = float(datab_gerais.get_data(dbg, 'novo', 'ha'))
    es = float(datab_gerais.get_data(dbg, 'novo', 'es'))
    e = float(datab_gerais.get_data(dbg, 'novo', 'e'))
    G = float(datab_gerais.get_data(dbg, 'novo', 'G'))

    for i in range(nvaos):
        ppf = ppi
        binff = binfi
        retorno = datab.get_data(db,'novo',i)
        vao = float(retorno[2])
        binfi = float(retorno[3])

        d = float(retorno[4])
        bfi = float(retorno[5])
        bfs = float(retorno[5])
        tw = float(retorno[6])
        tfs = float(retorno[7])
        tfi = float(retorno[8])

        nb = float(retorno[9])
        fi = float(retorno[10])

        lista_vaos.append(vao)            

        
        ppi = ((d-tfs-tfi)*1*tw*1 +
              bfs*1*tfs*1+bfi*1*tfi*1 )/10**6 * 7850 / 100.0
        
        pp = max(pp, ppi)
        bInfl = max(bInfl, binfi)

    # combinações
    # pp - peso proprio da viga
    # cp - carga permanente de divisorias e revestimento
    # cpsd - carga permanente do steel deck
    # scm -  sobrecarga de montagem
    # sc - sobrecarga de utilização
    # MG' antes da cura
    qglinha = 1 * (cpsd) * bInfl + pp
    # ML
    ql =  (1.*sc + cp) * bInfl
    # MD' antes da cura
    qdlinha = (1.2 * (cpsd ) + 1.6 * scm )* bInfl + 1.2 * pp
    # MD  depois da cura
    qd = (1.2 * (cp + cpsd) + 1.6 * sc) * bInfl + 1.2 * pp
    # Mvd
    qvd = (cpsd + cp + 0.7 * sc) * bInfl + pp

    #combinações raras
    qlong =  1.* cp * bInfl # Longa duração - Carga permanente depois da cura 
    qsc =    1.* sc * bInfl

    ##listaQ = [[qd, 'D'], [qglinha, 'G\''],[qdlinha, 'D\''], [ql, 'L'], [qsc, 'Curta'], [qlong,'Longa']]
    listaQ = [[qd, 'D'], [ql, 'L'], [qvd, 'Vd'], [qsc, 'Curta'], [qlong,'Longa']]
    listaQ = [[qd, 'D'], [qvd, 'Vd'], [qsc, 'Curta'], [qlong,'Longa']]

    # situação
    ponta_esq = "ponta_esquerda"  # "ponta_direita"#
    ponta_dir = "ponta_direita"
    intermediario = "intermediario"

    #Condição de analise
    listaCondicao = ['curta','longa']
    condicao = 'longa'#'pos-cura'

    listaMomentosMestre = []
    listaMomentosPosMestre = []
    listaCortantesMestre = []

    listaMDPos = []
    listaLongaPos = []
    listaCurtaPos = []

    listaMDNeg = []
    listaLongaNeg = []
    listaCurtaNeg = []

    listaCortantesVd = []

    lista_carregamentos = [['g\'', qglinha], ['d\'',qdlinha], ['l', ql], ['vd', qvd], ['d', qd], ['Longa', qlong], ['Curta', qsc] ]

    for j in range(nvaos):  # range(n_vaos):
        retorno = datab.get_data(db,'novo',j)
        vao = retorno[2]
        binf = retorno[3]

        d = retorno[4] / 10.0
        bfi = retorno[5] / 10.0
        bfs = retorno[5] / 10.0
        tw = retorno[6] / 10.0
        tfs = retorno[7] / 10.0
        tfi = retorno[8] / 10.0

        nb = retorno[9]
        fi = retorno[10]

        Asl = 3.14 * (fi/2) ** 2 * nb
        if j == 0:
            tramo = Tramos(j, vao, [0, lista_vaos[j+1]], binf, hdeck, ha,
                           Asl, fi, fck, fy, fys, e, es,
                           ponta_esq, d, bfs, bfi, tw, tfs, tfi)
            lista_tramos.append(tramo)
            for sub in tramo.create_subs(0):
                lista_sub.append(sub)
            
        elif j == nvaos - 1 and j != 0:
            tramo = Tramos(j, lista_vaos[j], [lista_vaos[j-1],0], binf, hdeck, ha,
                           Asl, fi, fck, fy, fys, e, es,
                           ponta_dir, d, bfs, bfi, tw, tfs, tfi)
            lista_tramos.append(tramo)
            for sub in tramo.create_subs(0):
                lista_sub.append(sub)
        else:
            tramo = Tramos(j, lista_vaos[j], [lista_vaos[j-1], lista_vaos[j+1]], binf, hdeck, ha,
                           Asl, fi, fck, fy, fys, e, es,
                           intermediario, d, bfs, bfi, tw, tfs, tfi)
            lista_tramos.append(tramo)
            for sub in tramo.create_subs(1):
                lista_sub.append(sub)
                
    ##for condicao in listaCondicao:
    ##    print(condicao)
    for q, text in listaQ:
        n = len(lista_sub)

        napoios = nvaos + 1
        nef = napoios + (napoios - 2) * 4

        kij  = np.zeros((nef, nef))
        f_ep = np.zeros((nef, 1))

####        if text == 'Curta':
####            print('Curta_Duração {}'.format(q))
        vao_acumulado = 0
        for j in range(n):
            tramo = lista_sub[j]
            vao = tramo.vao
            vaoc = lista_vaos[tramo.n]

            # momento positivo de analise
            i = 0
            if tramo.momento == 'neg':
                i = tramo.iefNeg
            elif tramo.momento == 'pos':
                if text == 'Curta':
                    i = tramo.iefPosCurta
                elif text == 'Longa':
                    i = tramo.iefPosLonga
                else:
                    # Qual inercia usar nos demais casos?!?!?!?!
                    i = tramo.iefPosLonga
            
####            if text == 'Curta':
####                if tramo.momento == 'neg':
####                    vao_acumulado += tramo.vao
####                    print('tr {1}  vao {2:.2f} Ief_N {0:.2f}cm4 k1 {3} k2 {4}'.format(i*100**4, tramo.n, tramo.vao, tramo.k1, tramo.k2))
####                    print('        vao {:.2f}'.format(vao_acumulado))
####                elif tramo.momento == 'pos':
####                    vao_acumulado += tramo.vao
####                    print('tr {1}  vao {2:.2f} Ief_C {0:.2f}cm4 k1 {3} k2 {4}'.format(i*100**4, tramo.n, tramo.vao, tramo.k1, tramo.k2))
####                    print('        vao {:.2f}'.format(vao_acumulado))

            
            inercia = i
            ei = tramo.e * inercia
            eng = (10 ** 9) * ei / vao  # extremidade rigida, 'k' aproxima-se de valores de 10^9 x EI / L

            k1 = tramo.k1  # C1  # 12000. kN.m/rad
            k2 = tramo.k2  # C2  # 12000. kN.m/rad
           
            # Utilizando a dissertação de André Christoforo
            # pagina 40(pdf)
            e1 = lambda z: 1 + z * er1
            e2 = lambda z: 1 + z * er2

            # função que cria os valores para preencher a matriz de rigidez
            tramo.rigidez(inercia)

            if tramo.n == 0:
                if tramo.idSub == 1:
                    er1 = ei / (vao * k1)
                    er2 = ei / (vao * k2)
                    e2 = lambda z: 1 + z * er2

                    tramo.me_0 =   q * vao ** 2 * e2(6) / (12 * e2(4))  # M2
                    tramo.ve_0 =   q * vao * e2(5) / (2 * e2(4))  # R2
                    tramo.md_0 = - q * vao ** 2 / (12 * e2(4))  # M1
                    tramo.vd_0 =   q * vao * e2(3) / (2 * e2(4))  # R1

                    f_ep[j]     += tramo.me_0
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
                    er1 = ei / (vao * k1)
                    er2 = ei / (vao * k2)
                    e2 = lambda z, er: 1 + z * er

                    tramo.me_0 =   q * vao ** 2 * e2(6, er2) / (12 * e2(4, er2))  # M2
                    tramo.ve_0 =   q * vao * e2(5, er2) / (2 * e2(4, er2))  # R2
                    tramo.md_0 = - q * vao ** 2 / (12 * e2(4, er2))  # M1
                    tramo.vd_0 =   q * vao * e2(3, er2) / (2 * e2(4, er2))  # R1

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
                    er1 = ei / (vao * k1)
                    er2 = ei / (vao * k2)
                    e2 = lambda z: 1 + z * er2

                    tramo.me_0 = + q * vao ** 2 * e2(6) / (12 * e2(4))  # M2
                    tramo.ve_0 = + q * vao * e2(5) / (2 * e2(4))  # R2
                    tramo.md_0 = - q * vao ** 2 / (12 * e2(4))  # M1
                    tramo.vd_0 = + q * vao * e2(3) / (2 * e2(4))  # R1

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
                    er1 = ei / (vao * k1)
                    er2 = ei / (vao * k2)
                    e2 = lambda z, er: 1 + z * er

                    tramo.md_0 = - q * vao ** 2 * e2(6, er1) / (12 * e2(4, er1))  # M2
                    tramo.vd_0 = + q * vao * e2(5, er1) / (2 * e2(4, er1))  # R2
                    tramo.me_0 = + q * vao ** 2 / (12 * e2(4, er1))  # M1
                    tramo.ve_0 = + q * vao * e2(3, er1) / (2 * e2(4, er1))  # R1

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
                    er1 = ei / (vao * k1)
                    er2 = ei / (vao * k2)
                    e2 = lambda z, er: 1 + z * er

                    tramo.md_0 = - q * vao ** 2 * e2(6, er1) / (12 * e2(4, er1))  # M2
                    tramo.vd_0 = + q * vao * e2(5, er1) / (2 * e2(4, er1))  # R2
                    tramo.me_0 = + q * vao ** 2 / (12 * e2(4, er1))  # M1
                    tramo.ve_0 = + q * vao * e2(3, er1) / (2 * e2(4, er1))  # R1

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
                    a = (2 * ei / vao) * 1 / k1
                    b = (2 * ei / vao) * 1 / k2
                    ##
                    tramo.me_0 = + ((3 * b + 1) * q * vao ** 2) / (12 * (3 * b * a + 2 * b + 2 * a + 1))
                    tramo.md_0 = - ((3 * a + 1) * q * vao ** 2) / (12 * (3 * b * a + 2 * b + 2 * a + 1))
                    tramo.ve_0 = (tramo.md_0 + tramo.me_0 + q * vao ** 2 / 2.0) / vao
                    tramo.vd_0 = q * vao - tramo.ve_0

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
                    er1 = ei / (vao * k1)
                    er2 = ei / (vao * k2)
                    e2 = lambda z, er: 1 + z * er

                    tramo.me_0 = q * vao ** 2 * e2(6, er2) / (12 * e2(4, er2))  # M2
                    tramo.ve_0 = q * vao * e2(5, er2) / (2 * e2(4, er2))  # R2
                    tramo.md_0 = - q * vao ** 2 / (12 * e2(4, er2))  # M1
                    tramo.vd_0 = q * vao * e2(3, er2) / (2 * e2(4, er2))  # R1

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
        
        # Definição das Reações no0s apoios
        for p in range(1, len(lista_vaos)):
            n = (p + 1) * 3 - 2 - 2
            tramoi = lista_sub[n - 1]
            tramoj = lista_sub[n]
            k = (tramoj.n * 6) - (tramoj.n - 1) + 3 - 1
            reacoes[p] += tramoi.vd_0 + dij[k - 7] * tramoi.vd_1 + dij[k - 6] * tramoi.vd_3 + dij[k - 5] * tramoi.vd_2
            reacoes[p] += tramoj.ve_0 + dij[k - 5] * tramoj.ve_1 + dij[k - 4] * tramoj.ve_2 + dij[k - 3] * tramoj.ve_4

            soma += reacoes[p]


        vaoTotal = 0
        listaDx = [0]           # Lista com valores somados de cada vão
        listaReacoes = []       # Lista com os valores das reações
        listaMomentoZero = []   # Lista com posições de momento zero    
        listaRaizes = []        # Lista com posições dos valores de cortante zero
        listaMomentos = []      # lista com valores de momentos negativos
        listaMomentosPos = []   # lista com valores de momentos positivos
        listaCortantes = []     # lista com valores de Cortantes
        
        listaReacoes.append([0.0, reacoes[0]])
        # cria uma lista com os valores de x, contanto da origem até o proximo apoio
        # cria um dicionario com o valor de x e o valor de reação do apoio
        for i in range(0, len(lista_vaos)):
            vaoTotal += lista_vaos[i]
            listaDx.append(vaoTotal)
            listaReacoes.append([vaoTotal, reacoes[i+1]])
        ############################################################  
        # Função Cortante
        def dy(x):
            v = 0
            vr = 0
            v -= x * q  # valor proveniente da carga distribuida
            for value in listaReacoes:
                if x > value[0]:
                    vr += value[1]
            v += vr
            return v

        # Função Momento
        def dm(x):
            m = 0
            mr = 0
            m -= q * x**2 / 2.  # valor proveniente da carga distribuida
            for value in listaReacoes:
                if x >= value[0]:
    ##                mr += value[1] * (x - value[0])
                    mr += value[1] * x - value[1] * value[0]
            m += mr
            return m

        # Função Flecha
        def flecha(x, x1,x2,x3,f1,f2,f3):
            matriz_a  = np.zeros((3, 3))
            matriz_b  = np.zeros((3, 1))
            matriz_a[0,0] = x1**2
            matriz_a[0,1] = x1
            matriz_a[0,2] = 1

            matriz_a[1,0] = x2**2
            matriz_a[1,1] = x2
            matriz_a[1,2] = 1

            matriz_a[2,0] = x3**2
            matriz_a[2,1] = x3
            matriz_a[2,2] = 1


            matriz_b = np.zeros((3,1))
            matriz_b[0,0] = f1
            matriz_b[1,0] = f2
            matriz_b[2,0] = f3

            matriz_a_inv = inv(matriz_a)
            matriz_a_inv = matriz_a_inv.dot(-matriz_b)

            aa = matriz_a_inv[0,0]
            bb = matriz_a_inv[1,0]
            cc = matriz_a_inv[2,0]

            return aa*x**2 + bb*x + cc ## retorna o valor da flecha em x
        
        ############################################################

        ############################################################
        # Valores de 'x' em que o cortante é zero = momento positivo é maximo
        aux = []
        listaRaizes = []        
        for x in range(0,int(listaDx[-1]+1)):
            try:
                fl = lambda x: -q
                root3 = round(mn.newton(dy, fl, x)[0],2)
                
                if root3 not in listaRaizes:
                    listaRaizes.append(root3)
            except Exception as e:
                raiz = 0
                
        # Pega os valores de momentos positivos maximos para os valores de 'x'
        for root in listaRaizes:
            yi = dm(root)
            listaMomentosPos.append([root, yi])
            
        ############################################################
        # Valores de 'x' em que o Momento é zero = momento 0 (zero)
        aux2 = []
        for x in range(0,int(listaDx[-1]),2):
            try:
##                root = round(float(newton(dm, x)),2)
                root3 = round(mn.newton2(dm, dy, x,0.01,200)[0],2)

                if root3 < 0:
                    root3 = 0.0
                if root3 > vaoTotal:
                    root3 = vaoTotal

                if root3 not in listaMomentoZero:
                    listaMomentoZero.append(root3)
            except Exception as e:
##                print('Raizes da função momento', e)
                raiz = 0

        ############################################################
        # # Inicio da montagem dos diagramas
        # # Diagrama cortante
        x = 0  # valor inicial de x
        y = 0  # valor inicial de y
        xn = vaoTotal  # valor final de x
        h = step = 0.05  # valor 'step' para cada iteração
        n = int((xn - x) / h)  # numero de iterações

        xp = np.linspace(x, xn, n + 1)  # coordenadas de x
        ypv = np.empty(n + 1, float)  # coordenadas de y
        ypv[0] = y

        ###############################################
        # Diagrama de Cortantes - valores x e  y
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
                
        ###############################################
        # Diagrama de Momento - valores x e  y
        ypm = np.empty(n + 1, float)
        ypmi = 0
        ypm[0] = 0
        for i in range(len(xp)):
            ypm[i] = dm(xp[i])

        ###############################################
        # Momentos nas regiões dos apoios
        for j in range(len(listaDx)):
            xi = listaDx[j]
            yi = dm(xi) # ypm[k]
            listaMomentos.append([xi, yi])
        carr = 0
        

        ###############################################
        ###############################################
        # Calculo das rotações e flechas
        # Nos 'x' de cortante 0 (zero)/momento positivo maximo
        # listaRaizes = lista de valores de 'x' em que o cortante é 0 (zero)
        # lista_tramos = lista com os elementos tramos
        # lista_sub = lista com os elementos sub_tramos

        ypf = np.empty(n + 1, float)  # coordenadas de y
    
        ## Flecha no primeiro tramo
        tramo = lista_tramos[0]
        sub_tramo_i = lista_sub[0]
        sub_tramo_ii = lista_sub[1]

        vao_inicial = tramo.vao
        
        x1 = 0 # coordenada 'x' inicial
        craken = x2 = sub_tramo_i.vao # coordenada 'x' do ponto intermediario
        x3 = (sub_tramo_i.vao + sub_tramo_ii.vao) # coordenada 'x' do ponto final

        f1 = 0  # flecha da coordenada inicial
        f2 = dij[2]  # flecha da coordenada intermediaria
        f3 = 0  # flecha do ponto final
            
        for i in range(len(xp)):
            if xp[i] <= vao_inicial:
                ypf[i] = flecha(xp[i],
                                x1, x2, x3,
                                f1, f2, f3)            
            else:            
                break

        ## Flecha nos tramos intermediarios
        for i in range(1, len(lista_tramos)-1):
            tramo = lista_tramos[i]
            k = tramo.n * 6 - (tramo.n -1) + 3 -1
            x_inicial = listaDx[tramo.n]
            x_final = listaDx[tramo.n + 1]

            sub_tramo_i = lista_sub[tramo.n*3-1]
            sub_tramo_ii = lista_sub[tramo.n*3]
            
            x1 =  sub_tramo_i.vao  # coordenada de flecha nos 15% do vão
            x2 =  sub_tramo_i.vao + sub_tramo_ii.vao  # coordenada de flecha nos 85% do vão
            x3 =  tramo.vao  # coordenada x da flecha do apoio

            f1 = dij[k-3] # flecha primeiros 15% do vao
            f2 = dij[k-1] # flecha ultimos 15% do vao
            f3 = 0.0 # apoio

            for j in range(len(xp)):        
                if xp[j] >= x_inicial and xp[j] <= x_final:
                    ypf[j] = flecha(xp[j] - x_inicial,
                                    x1,x2,x3,
                                    f1,f2,f3)

        ## Flecha no ultimo tramo
        tramo = lista_tramos[-1]
        sub_tramo_i = lista_sub[-2]
        sub_tramo_ii = lista_sub[-1]

        x_inicial = listaDx[-2]
        
        x1 = 0 # coordenada 'x' inicial
        x2 = sub_tramo_i.vao # coordenada 'x' do ponto intermediario
        x3 = (sub_tramo_i.vao + sub_tramo_ii.vao) # coordenada 'x' do ponto final

        f1 = 0.0  # flecha da coordenada inicial
        f2 = dij[-2]  # flecha da coordenada intermediaria
        f3 = 0.0  # flecha do ponto final
            
        for i in range(len(xp)):
            if xp[i] >= x_inicial:
                ypf[i] = flecha(xp[i] - x_inicial,
                                x1, x2, x3,
                                f1, f2, f3)
            else:            
                continue

        listaFlechas = []
        
        for tramo in lista_tramos:
            x_inicial = listaDx[tramo.n]
            x_final = listaDx[tramo.n + 1]
            flecha_max = 0.0
            flecha_x = 0.0
            lista_flecha_y = []
            lista_flecha_x = []
            for j in range(len(xp)):
                if xp[j] >= x_inicial and xp[j] <= x_final:
                    lista_flecha_y.append(ypf[j])
                    lista_flecha_x.append(xp[j])

            flecha_max = max(lista_flecha_y)  # em [cm]
            flecha_x = lista_flecha_x[lista_flecha_y.index(flecha_max)] # em [m]
            flecha_max *= 100
            if text == 'Curta':
                tramo.flecha_curta = flecha_max

            if text == 'Longa':
                tramo.flecha_longa = flecha_max

            if text == 'D':
                tramo.flecha_md = flecha_max

            listaFlechas.append([flecha_x, flecha_max])


        ###############################################
        
        if text == 'Curta':
            listaCurtaPos = listaMomentosPos
            listaCurtaNeg = listaMomentos
            diagrama_curta = [xp, ypv, ypm, ypf, listaCortantes, listaMomentos, listaMomentosPos, listaFlechas]
                      
        if text == 'Longa':
            listaLongaPos = listaMomentosPos
            listaLongaNeg = listaMomentos
            diagrama_longa = [xp, ypv, ypm, ypf, listaCortantes, listaMomentos, listaMomentosPos, listaFlechas]
            
        if text == 'D':
            listaMDPos = listaMomentosPos
            listaMDNeg = listaMomentos
            diagrama_md = [xp, ypv, ypm, ypf, listaCortantes, listaMomentos, listaMomentosPos, listaFlechas]
##            print(listaMomentos, listaMomentosPos)
            
        if text == 'Vd':
            listaCortantesVd = listaCortantes

    return [lista_tramos, listaDx, lista_carregamentos,
                                   listaMDPos, listaMDNeg,
                                   listaCurtaPos, listaCurtaNeg,
                                   listaLongaPos, listaLongaNeg,
                                   listaCortantesVd, listaMomentoZero,
                                   nb, diagrama_longa, diagrama_curta, diagrama_md] 


def plotar_diagramas(nvaos, hdeck, cp, cpsd, sc, scm, carregamento):
    retorno_calculo = calculo_sistema(nvaos, hdeck, cp, cpsd, sc, scm)
    import plotar_R01 as plot
    
    if carregamento == 'curta':
        valores = retorno_calculo[-2] 
        plot.plotar_diagramas(0, valores[0][-1], valores[0], valores[1], valores[2], valores[3],
                              valores[4], valores[5], valores[6], valores[7])
    elif carregamento == 'longa':
        valores = retorno_calculo[-3]
        plot.plotar_diagramas(0, valores[0][-1], valores[0], valores[1], valores[2], valores[3],
                              valores[4], valores[5], valores[6], valores[7])
    elif carregamento == 'D':
        valores = retorno_calculo[-1]
        plot.plotar_diagramas(0, valores[0][-1], valores[0], valores[1], valores[2], valores[3],
                              valores[4], valores[5], valores[6], valores[7])




def analisar_sistema(nvaos, hdeck, cp, cpsd, sc, scm):

    retorno_calculo = calculo_sistema(nvaos, hdeck, cp, cpsd, sc, scm)
    
    save = False
    retorno = dim.verificar_tramos(retorno_calculo[0],
                                   retorno_calculo[1],
                                   retorno_calculo[2],
                                   retorno_calculo[3], retorno_calculo[4],
                                   retorno_calculo[5], retorno_calculo[6],
                                   retorno_calculo[7], retorno_calculo[8],
                                   retorno_calculo[9], retorno_calculo[10],
                                   retorno_calculo[11], save)


    return retorno

