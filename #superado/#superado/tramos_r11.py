## ve = reaçao do lado esquerdo
## vd = reaçao do lado direito
## me = momento do lado esquerdo
## md = momento do lado direito
## vao = distancia entre apoios da viga
## i =  inercia do tramo
## Livro:  semi-Rigid Connections in Steel Frames
## matriz de rigidez a partir da pagina 78
from numpy.linalg import inv
import numpy as np

ponta_esq = "ponta_esquerda"
ponta_dir = "ponta_direita"
intermediario = "intermediario"

def calculo_semi_rigido(lista_tramos, q, lista_vaos):
    n = len(lista_tramos)
    
    nvaos = int((n-4)/3 + 2)    
    napoios = nvaos + 1
    nef = napoios + (napoios - 2) * 4
    
    kij = np.zeros((nef,nef))
    f_ep = np.zeros((nef,1))    

    for j in range(n):
        tramo = lista_tramos[j]        
        vao = tramo.vao
        ei = tramo.e * tramo.i

        eng = (10**9) * ei/vao # extremidade rigida, 'k' aproxima-se de valores de 10^9 x EI / L
        kk1 = 12000.
        kk2 = 12000.
        
        ## Utilizando a dissertação de André Christoforo
        ## pagina 40(pdf)
        e1 = lambda x: 1 + x*er1
        e2 = lambda x: 1 + x*er2

        if tramo.n == 0:
            if tramo.idSub == 1:
                k1 = eng#ke
                k2 = eng#ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                
                tramo.me_0 =   q * vao ** 2 * e2(6) / (12 * e2(4)) # M2                
                tramo.ve_0 =   q * vao * e2(5)/ ( 2 *e2(4))        # R2
                tramo.md_0 = - q * vao ** 2 / ( 12 * e2(4))        # M1                
                tramo.vd_0 =   q * vao * e2(3) / (2*e2(4))         # R1

                tramo.rigidez(k1, k2)

                f_ep[j] += tramo.me_0
                f_ep[j+1] += tramo.md_0
                f_ep[j+2] += tramo.vd_0

                kij[j,j]   += tramo.me_1
                kij[j,j+1] += tramo.md_1
                kij[j,j+2] += tramo.vd_1

                kij[j+1,j]   += tramo.me_2
                kij[j+1,j+1] += tramo.md_2
                kij[j+1,j+2] += tramo.vd_2

                kij[j+2,j]   += tramo.me_4
                kij[j+2,j+1] += tramo.md_4
                kij[j+2,j+2] += tramo.vd_4

                
            else:
                k1 = eng#ke
                k2 = kk2# eng#ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                e2 = lambda x,er: 1 + x*er
                
                tramo.me_0 =   q * vao ** 2 * e2(6,er2) / (12 * e2(4,er2)) # M2
                tramo.ve_0 =   q * vao * e2(5,er2)/ ( 2 *e2(4,er2))        # R2
                tramo.md_0 = - q * vao ** 2 / ( 12 * e2(4,er2))            # M1
                tramo.vd_0 =   q * vao * e2(3,er2) / (2*e2(4,er2))         # R1
                
                tramo.rigidez(k1, k2)

                f_ep[j] += tramo.me_0
                f_ep[j+1] += tramo.ve_0
                f_ep[j+2] += tramo.md_0

                kij[j,j]   += tramo.me_1
                kij[j,j+1] += tramo.ve_1
                kij[j,j+2] += tramo.md_1

                kij[j+1,j]   += tramo.me_3
                kij[j+1,j+1] += tramo.ve_3
                kij[j+1,j+2] += tramo.md_3

                kij[j+2,j]   += tramo.me_2
                kij[j+2,j+1] += tramo.ve_2
                kij[j+2,j+2] += tramo.md_2

        elif tramo.n == (nvaos - 1):
            if tramo.idSub == 2:
                k1 = eng#ke
                k2 = eng#ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                
                tramo.me_0 =   q * vao ** 2 * e2(6) / (12 * e2(4)) # M2
                tramo.ve_0 =   q * vao * e2(5)/ ( 2 *e2(4))        # R2
                tramo.md_0 = - q * vao ** 2 / ( 12 * e2(4))        # M1
                tramo.vd_0 =   q * vao * e2(3) / (2*e2(4))         # R1

                tramo.rigidez(k1, k2)

                f_ep[nef-1-2] += tramo.me_0
                f_ep[nef-1-1] += tramo.ve_0
                f_ep[nef-1] += tramo.md_0

                kij[nef-1-2,nef-1-2] += tramo.me_1
                kij[nef-1-2,nef-1-1] += tramo.ve_1
                kij[nef-1-2,nef-1]   += tramo.md_1

                kij[nef-1-1,nef-1-2] += tramo.me_3
                kij[nef-1-1,nef-1-1] += tramo.ve_3
                kij[nef-1-1,nef-1]   += tramo.md_3

                kij[nef-1,nef-2-1]   += tramo.me_2
                kij[nef-1,nef-1-1]   += tramo.ve_2
                kij[nef-1,nef-1]     += tramo.md_2
                
            else:
                k1 = kk1#eng#ke
                k2 = eng#ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)
                e2 = lambda x, er: 1 + x*er
                
                tramo.md_0 = - q * vao ** 2 * e2(6,er1) / (12 * e2(4,er1)) # M2
                tramo.vd_0 =   q * vao * e2(5,er1) / ( 2 *e2(4,er1))       # R2
                tramo.me_0 =   q * vao ** 2 / ( 12 * e2(4,er1))            # M1
                tramo.ve_0 =   q * vao * e2(3,er1) / (2*e2(4,er1))         # R1
                
                tramo.rigidez(k1, k2)

                f_ep[nef-3-1] += tramo.me_0
                f_ep[nef-2-1] += tramo.md_0                
                f_ep[nef-1-1] += tramo.vd_0

                kij[nef-3-1,nef-3-1] += tramo.me_1
                kij[nef-3-1,nef-2-1] += tramo.md_1
                kij[nef-3-1,nef-1-1] += tramo.vd_1

                kij[nef-2-1,nef-3-1] += tramo.me_2
                kij[nef-2-1,nef-2-1] += tramo.md_2
                kij[nef-2-1,nef-1-1] += tramo.vd_2

                kij[nef-1-1,nef-3-1] += tramo.me_4
                kij[nef-1-1,nef-2-1] += tramo.md_4
                kij[nef-1-1,nef-1-1] += tramo.vd_4

        else:
            if tramo.idSub == 1:
                k1 = kk1#eng#ke
                k2 = eng#ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)

                e2 = lambda x, er: 1 + x*er
                
                tramo.md_0 = - q * vao ** 2 * e2(6,er1) / (12 * e2(4,er1)) # M2
                tramo.vd_0 =   q * vao * e2(5,er1) / ( 2 *e2(4,er1))    # R2
                tramo.me_0 =   q * vao ** 2 / ( 12 * e2(4,er1))        # M1
                tramo.ve_0 =   q * vao * e2(3,er1) / (2*e2(4,er1))         # R1

                tramo.rigidez(k1, k2)
                k = (tramo.n * 6) - (tramo.n -1) + 3 -1

                f_ep[k-5] += tramo.me_0
                f_ep[k-4] += tramo.md_0
                f_ep[k-3] += tramo.vd_0

                kij[k-5,k-5] += tramo.me_1
                kij[k-5,k-4] += tramo.md_1
                kij[k-5,k-3] += tramo.vd_1

                kij[k-4,k-5] += tramo.me_2
                kij[k-4,k-4] += tramo.md_2
                kij[k-4,k-3] += tramo.vd_2

                kij[k-3,k-5] += tramo.me_4
                kij[k-3,k-4] += tramo.md_4
                kij[k-3,k-3] += tramo.vd_4
                
            elif tramo.idSub == 2:                
                k1 = kk1
                k2 = kk2
                a = (2*ei/vao)*1/k1
                b = (2*ei/vao)*1/k2
                ##
                tramo.me_0 = + ((3*b + 1) * q * vao ** 2) / (12 *( 3*b*a + 2*b + 2*a + 1))
                tramo.md_0 = - ((3*a + 1) * q * vao ** 2) / (12 *( 3*b*a + 2*b + 2*a + 1))            
                tramo.ve_0 = (tramo.md_0 + tramo.me_0 + q * vao ** 2 / 2.0) / vao
                tramo.vd_0 = q*vao - tramo.ve_0
                
                tramo.rigidez(k1, k2)
                k = (tramo.n * 6) - (tramo.n -1) + 3 -1

                f_ep[k-4] += tramo.me_0
                f_ep[k-3] += tramo.ve_0
                f_ep[k-2] += tramo.md_0
                f_ep[k-1] += tramo.vd_0
                
                kij[k-4,k-4] += tramo.me_1
                kij[k-4,k-3] += tramo.ve_1
                kij[k-4,k-2] += tramo.md_1
                kij[k-4,k-1] += tramo.vd_1

                kij[k-3,k-4] += tramo.me_3
                kij[k-3,k-3] += tramo.ve_3
                kij[k-3,k-2] += tramo.md_3
                kij[k-3,k-1] += tramo.vd_3

                kij[k-2,k-4] += tramo.me_2
                kij[k-2,k-3] += tramo.ve_2
                kij[k-2,k-2] += tramo.md_2
                kij[k-2,k-1] += tramo.vd_2
                
                kij[k-1,k-4] += tramo.me_4
                kij[k-1,k-3] += tramo.ve_4
                kij[k-1,k-2] += tramo.md_4
                kij[k-1,k-1] += tramo.vd_4
                
            elif tramo.idSub == 3:
                k1 = eng#ke
                k2 = kk2# eng#ke
                er1 = ei / (vao * k1)
                er2 = ei / (vao * k2)                
                e2 = lambda x,er: 1 + x*er
                
                tramo.me_0 =   q * vao ** 2 * e2(6,er2) / (12 * e2(4,er2)) # M2
                tramo.ve_0 =   q * vao * e2(5,er2)/ ( 2 *e2(4,er2))        # R2
                tramo.md_0 = - q * vao ** 2 / ( 12 * e2(4,er2))            # M1
                tramo.vd_0 =   q * vao * e2(3,er2) / (2*e2(4,er2))         # R1                
                
                tramo.rigidez(k1, k2)
                k = (tramo.n * 6) - (tramo.n -1) + 3 -1

                f_ep[k-2] += tramo.me_0
                f_ep[k-1] += tramo.ve_0
                f_ep[k] += tramo.md_0

                kij[k-2,k-2] += tramo.me_1
                kij[k-2,k-1] += tramo.ve_1
                kij[k-2,k]   += tramo.md_1

                kij[k-1,k-2] += tramo.me_3
                kij[k-1,k-1] += tramo.ve_3
                kij[k-1,k]   += tramo.md_3

                kij[k,k-2] += tramo.me_2
                kij[k,k-1] += tramo.ve_2
                kij[k,k]   += tramo.md_2
            

##    print(kij)
##    print(f_ep)

    kij_inv = inv(kij)
    dij = kij_inv.dot(-f_ep)

    # determinacao das reaçoes
    reacoes = [0] * (nvaos+1)
    tramo = lista_tramos[0]

    tramoult = lista_tramos[-1]

    soma = 0
    reacoes[0] += tramo.ve_0 + dij[0]*tramo.ve_1 + dij[1]*tramo.ve_2 + dij[2]*tramo.ve_4
    soma += reacoes[0]
    
    reacoes[-1] += tramoult.vd_0 + dij[-3]*tramoult.vd_1 + dij[-2]*tramoult.vd_3 + dij[-1]*tramoult.vd_2
    soma += reacoes[4]

##    print('soma das reações: %.2f' % soma)
    j = 0
    for i in range(1,len(lista_vaos)):
        n = (i + 1)* 3 - 2 - 2
        tramoi = lista_tramos[n-1]
        tramoj = lista_tramos[n]
        k = (tramoj.n * 6) - (tramoj.n -1) + 3 -1
        reacoes[i] += tramoi.vd_0 + dij[k-7]*tramoi.vd_1 + dij[k-6]*tramoi.vd_3 + dij[k-5]*tramoi.vd_2
        reacoes[i] += tramoj.ve_0 + dij[k-5]*tramoj.ve_1 + dij[k-4]*tramoj.ve_2 + dij[k-3]*tramoj.ve_4

        soma += reacoes[i]

    return(reacoes)


class Tramos(object):
    def __init__(self, n, vao, i, e, situacao):
        # o tramo é considerado como engastado - engastado
        self.vao = vao
        self.n = n
        self.i = i
        self.e = e
        self.situacao = situacao  
        
        
    def create_subs(self):
        listaSubs = []
        if self.situacao == "ponta_esquerda":
            vao1 = self.vao*.85
            vao2 = self.vao*.15

            i1 = self.i
            i2 = self.i * .75

            sub1 = SubTramos(self.n, 1, 'pos', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'neg', vao2, i2, self.e)

            return sub1, sub2
        elif self.situacao == "ponta_direita":
            vao1 = self.vao*.15
            vao2 = self.vao*.85

            i1 = self.i * .75
            i2 = self.i 

            sub1 = SubTramos(self.n, 1, 'neg', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'pos', vao2, i2, self.e)

            listaSubs.append(sub1)
            return sub1, sub2
        elif self.situacao == "intermediario":

            vao1 = self.vao*.15
            vao2 = self.vao*.70
            vao3 = self.vao*.15

            i1 = self.i * .75
            i2 = self.i
            i3 = self.i * .75

            sub1 = SubTramos(self.n, 1, 'neg', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'pos', vao2, i2, self.e)
            sub3 = SubTramos(self.n, 3, 'neg', vao3, i3, self.e)

            return sub1, sub2, sub3

##        return listaSubs


class SubTramos(Tramos):
    def __init__(self, tramoN, idSub, momento, vao, i, e):
        self.vao = vao
        self.n = tramoN
        self.i = i
        self.e = e
        self.idSub = idSub
        self.momento = momento
        self.ve_0 = 0
        self.vd_0 = 0
        self.me_0 = 0
        self.md_0 = 0

        self.ve_1 = 0
        self.vd_1 = 0
        self.me_1 = 0
        self.md_1 = 0

        self.ve_2 = 0
        self.vd_2 = 0
        self.me_2 = 0
        self.md_2 = 0

        self.ve_3 = 0
        self.vd_3 = 0
        self.me_3 = 0
        self.md_3 = 0

        self.ve_4 = 0
        self.vd_4 = 0
        self.me_4 = 0
        self.md_4 = 0


    def rigidez(self, k1, k2):
        ei = self.e*self.i
        vao = self.vao
        er1 = ei / (vao * k1)
        er2 = ei / (vao * k2)

        ## Utilizando a dissertação de André Christoforo
        # pagina 47(pdf)
        eri = ei / ( vao * k1) # equação 54.a
        erj = ei / ( vao * k2) # equação 54.b
        erij = 1 + eri + erj   # equação 54.c
        eri1 = 1 + eri         # equação 55.a
        erj1 = 1 + erj         # equação 55.b
        eri2 = 1 + eri * 2     # equação 55.c
        erj2 = 1 + erj * 2     # equação 55.d
        eri3 = 1 + eri * 3     # equação 55.e
        erj3 = 1 + erj * 3     # equação 55.f
        
        # pagina 48(pdf), equação 59.b
        C = 2 * ei / (vao**3 * (4 * erij + 3 *(4 * eri * erj - 1)))
        
        # pagina 51(pdf), equação 68
        self.ve_1 =   3 * C * vao * erj2
        self.me_1 =   2 * C * vao ** 2 * erj3
        self.vd_1 = - 3 * C * vao * erj2
        self.md_1 =       C * vao ** 2

        self.ve_2 =   3 * C * vao * eri2
        self.me_2 =       C * vao ** 2
        self.vd_2 = - 3 * C * vao * eri2
        self.md_2 =   2 * C * vao ** 2 * eri3

        self.ve_3 =   6 * C * erij
        self.me_3 =   3 * C * vao * erj2
        self.vd_3 = - 6 * C * erij
        self.md_3 =   3 * C * vao * eri2

        self.ve_4 = - 6 * C * erij
        self.me_4 = - 3 * C * vao * erj2
        self.vd_4 =   6 * C * erij
        self.md_4 = - 3 * C * vao * eri2
        
