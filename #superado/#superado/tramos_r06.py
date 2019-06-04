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

ponta_esq = "ponta_esquerda"#"ponta_direita"#
ponta_dir = "ponta_direita"
intermediario = "intermediario"

kd = 15000.
ke = 12000.0
q = 2.
vao = 7.

ei = 2.*10**8 * 15254 *100**-4

##ve_0 = q *((vao**4 / (8*ei) + vao**3/(2*kd))/(vao**3/(3*ei) + vao**2/kd))
##vd_0 = q * vao - ve_0
##me_0 = 0.0
##md_0 = - q * vao**2 / 2. + ve_0 * vao 

a = (2*ei/vao)*1/ke
b = 0.0#(2*ei/vao)*1/kd
####
me_0 = ((3*b + 1) * q * vao ** 2) / (12 *( 3*b*a + 2*b + 2*a + 1))#*ei/vao
md_0 = 0.0#- ((3*a + 1) * q * vao ** 2) / (12 *( 3*b*a + 2*b + 2*a + 1))#*(ei/vao)
##      
ve_0 = (md_0 + me_0 + q*vao**2/2)/vao#q * vao / (2 + 3 *kd)
vd_0 = q*vao - ve_0# (q * vao / (2 + 3 *ke))

##v = ve_0+vd_0
##
##
##      
print("ve = ",ve_0)
print("vd = ",vd_0)
print("me = ",me_0)
print("md = ",md_0)
##print(v, q*vao)

def calculo_semi_rigido( lista_tramos, q, k1, k2):
    n = len(lista_tramos)
    kij = np.zeros((n+1,n+1))
    f_ep = np.zeros((n+1,1))

    for j in range(n):
        tramo = lista_tramos[j] 
        if tramo.situacao == "ponta_esquerda":
            tramo.calc_semi_rigido( q, 0.0, k1)
            # caso o o tramo seja o primeiro tramo, ou seja, o da extrema esquerda
            # momento na rotação unitaria do primeiro apoio
            kij[0][0] += tramo.me_1 # apoio da esquerda do 1 tramo
            kij[1][0] += tramo.md_1 # apoio da direita do 1 tramo

            # momento na rotação unitaria do segundo apoio
            kij[0][1] += tramo.me_2 # apoio da esquerda do 1 tramo
            kij[1][1] += tramo.md_2 # apoio da direita do 1 tramo

            #esforços de engaste perfeito nos apoios do primeiro tramo
            f_ep[0] += (tramo.me_0) # primeiro apoio do sistema
            f_ep[1] += (tramo.md_0) # segundo apoio do sistema
            
        elif tramo.situacao == "ponta_direita":
            tramo.calc_semi_rigido( q, k2, 0.0)#, k2)
            # caso o o tramo seja o ultimo tramo, ou seja, o da extrema direita
            # momento na rotação unitaria do penultimo apoio
            kij[n-1][n-1] += tramo.me_1 # apoio da esquerda
            kij[n][n-1] += tramo.md_1 # apoio da direita
            
            # momento na rotação unitaria do ultimo apoio 
            kij[n-1][n] += tramo.me_2 
            kij[n][n] += tramo.md_2

            # esforços de engaste perfeito nos apoios do ultimo tramos
            f_ep[n-1] += (tramo.me_0) # penultimo apoio do sistema
            f_ep[n] += (tramo.md_0)# ultimo apoio do sistema
    ##        print(kij)
            
        elif tramo.situacao == intermediario:
            tramo.calc_semi_rigido(q, k1, k2)
            # caso o tramo seja itnermediario
            # momento na rotação unitaria do apoio da esquerda
            kij[j][j] += tramo.me_1 # apoio da esquerda
            kij[j+1][j] += tramo.md_1 # apoio da direita
            
            # momento na rotação unitaria do apoio da direita
            kij[j][j+1] += tramo.me_2
            kij[j+1][j+1] += tramo.md_2

            # esforços de engaste perfeito nos apoios do ultimo tramos
            f_ep[j] += (tramo.me_0) # penultimo apoio do sistema
            f_ep[j+1] += (tramo.md_0) # ultimo apoio do sistema

    
    kij_inv = inv(kij)
    dij = kij_inv.dot(-f_ep)

    # determinacao das reaçoes
    reacoes = [0] * (n+1)
    for j in range(1, n+1):
        tramo = lista_tramos[j-1]
        if tramo.situacao == ponta_esq:
            reacoes[0] += tramo.ve_0 + dij[0]*tramo.ve_1 + dij[1]*tramo.ve_2
            reacoes[1] += tramo.vd_0 + dij[0]*tramo.vd_1 + dij[1]*tramo.vd_2
        elif tramo.situacao == ponta_dir:
            reacoes[n-1] += tramo.ve_0 + dij[n-1]*tramo.ve_1 + dij[n]*tramo.ve_2
            reacoes[n] += tramo.vd_0 + dij[n-1]*tramo.vd_1 + dij[n]*tramo.vd_2
        elif tramo.situacao == intermediario:
            reacoes[j-1] += tramo.ve_0 + dij[j-1]*tramo.ve_1 + dij[j]*tramo.ve_2
            reacoes[j] += tramo.vd_0 + dij[j-1]*tramo.vd_1 + dij[j]*tramo.vd_2
    return(reacoes)


def calculo_normal( lista_tramos, q):
    n = len(lista_tramos)
    kij = np.zeros((n+1,n+1))
    f_ep = np.zeros((n+1,1))


    for j in range(n):
        tramo = lista_tramos[j] 
        if tramo.situacao == "ponta_esquerda":
            tramo.calc_normal( q)
            # caso o o tramo seja o primeiro tramo, ou seja, o da extrema esquerda
            # momento na rotação unitaria do primeiro apoio
            kij[0][0] += tramo.me_1 # apoio da esquerda do 1 tramo
            kij[1][0] += tramo.md_1 # apoio da direita do 1 tramo

            # momento na rotação unitaria do segundo apoio
            kij[0][1] += tramo.me_2 # apoio da esquerda do 1 tramo
            kij[1][1] += tramo.md_2 # apoio da direita do 1 tramo

            #esforços de engaste perfeito nos apoios do primeiro tramo
            f_ep[0] += (tramo.me_0) # primeiro apoio do sistema
            f_ep[1] += (tramo.md_0) # segundo apoio do sistema
            
        elif tramo.situacao == "ponta_direita":
            tramo.calc_normal( q)
            # caso o o tramo seja o ultimo tramo, ou seja, o da extrema direita
            # momento na rotação unitaria do penultimo apoio
            kij[n-1][n-1] += tramo.me_1 # apoio da esquerda
            kij[n][n-1] += tramo.md_1 # apoio da direita
            
            # momento na rotação unitaria do ultimo apoio 
            kij[n-1][n] += tramo.me_2 
            kij[n][n] += tramo.md_2

            # esforços de engaste perfeito nos apoios do ultimo tramos
            f_ep[n-1] += (tramo.me_0) # penultimo apoio do sistema
            f_ep[n] += (tramo.md_0)# ultimo apoio do sistema
    ##        print(kij)
            
        elif tramo.situacao == intermediario:
            tramo.calc_normal(q)
            # caso o tramo seja itnermediario
            # momento na rotação unitaria do apoio da esquerda
            kij[j][j] += tramo.me_1 # apoio da esquerda
            kij[j+1][j] += tramo.md_1 # apoio da direita
            
            # momento na rotação unitaria do apoio da direita
            kij[j][j+1] += tramo.me_2
            kij[j+1][j+1] += tramo.md_2

            # esforços de engaste perfeito nos apoios do ultimo tramos
            f_ep[j] += (tramo.me_0) # penultimo apoio do sistema
            f_ep[j+1] += (tramo.md_0) # ultimo apoio do sistema

    kij_inv = inv(kij)
    dij = kij_inv.dot(-f_ep)

    # determinacao das reaçoes
    reacoes = [0] * (n+1)
    for j in range(1, n+1):
        tramo = lista_tramos[j-1]
        if tramo.situacao == ponta_esq:
            reacoes[0] += tramo.ve_0 + dij[0]*tramo.ve_1 + dij[1]*tramo.ve_2
            reacoes[1] += tramo.vd_0 + dij[0]*tramo.vd_1 + dij[1]*tramo.vd_2
        elif tramo.situacao == ponta_dir:
            reacoes[n-1] += tramo.ve_0 + dij[n-1]*tramo.ve_1 + dij[n]*tramo.ve_2
            reacoes[n] += tramo.vd_0 + dij[n-1]*tramo.vd_1 + dij[n]*tramo.vd_2
        elif tramo.situacao == intermediario:
            reacoes[j-1] += tramo.ve_0 + dij[j-1]*tramo.ve_1 + dij[j]*tramo.ve_2
            reacoes[j] += tramo.vd_0 + dij[j-1]*tramo.vd_1 + dij[j]*tramo.vd_2
    return(reacoes)




class Tramos:
    def __init__(self, _vao,  _i, _e, _situacao):
        # o tramo é considerado como engastado - engastado
        self.vao = _vao
        self.i = _i
        self.e = _e
        self.situacao = _situacao
        self.ve_0 = 0.0
        self.vd_0 = 0.0
        self.me_0 = 0.0
        self.md_0 = 0.0

    def calc_normal(self, q):
        vao = self.vao
        ei = self.e * self.i
        self.ve_0 = + q * vao / 2
        self.vd_0 = + q * vao / 2
        self.me_0 = + q * vao ** 2 / 12
        self.md_0 = - q * vao ** 2 / 12

        self.ve_1 = + 6  / (vao**2)
        self.vd_1 = - 6  / (vao**2)
        self.me_1 = + 4  / vao
        self.md_1 = + 2  / vao

        self.ve_2 = + 6 / (vao**2)
        self.vd_2 = - 6 / (vao**2)
        self.me_2 = + 2 / vao
        self.md_2 = + 4 / vao
        

    def calc_semi_rigido(self, q, ke, kd):
        vao = self.vao
        ei = self.e * self.i

        k1 = ke
        k2 = kd
        
##        R_ast = (1 + 4*ei / (vao*k2)) * (1 + 4*ei / (vao*k1)) - ((ei/vao)**2)* (4 / (k1*k2))
        
##        sii = (4 + (12*ei/(vao*k1))) / R_ast
##        sjj = (4 + (12*ei/(vao*k2))) / R_ast
##        sij = sji = 2. / R_ast
   
        if self.situacao == "ponta_esquerda":
##            self.ve_0 = q *((vao**4 / (8*ei) + vao**3/(2*kd))/(vao**3/(3*ei) + vao**2/kd))
##            self.vd_0 = q * vao - self.ve_0
##
##            self.me_0 = 0.0#- q * vao**2 * feir(6) / (12 * feir(4))            
##            self.md_0 = - q * vao**2 / 2. + self.ve_0*vao #q * vao**2 / (12 * (feir(4)))

            a = 0.0#(2*ei/vao)*1/ke
            b = (2*ei/vao)*1/kd
            ##
            self.me_0 = + ((3*b + 1) * q * vao ** 2) / (12 *( 3*b*a + 2*b + 2*a + 1))#*ei/vao
            self.md_0 = - ((3*a + 1) * q * vao ** 2) / (12 *( 3*b*a + 2*b + 2*a + 1))#*(ei/vao)
            ##      
            self.ve_0 = (self.md_0 + self.me_0 + q*vao**2/2)/vao#q * vao / (2 + 3 *kd)
            self.vd_0 = q*vao - self.ve_0# (q * vao / (2 + 3 *ke))

            R_ast = (1 + 4*ei / (vao*k2)) * (1 + 0) - ((ei/vao)**2)#* (4 / (k1*k2))
        
            sii = (4 + 0) / R_ast
            sjj = (4 + (12*ei/(vao*k2))) / R_ast
            sij = sji = 2. / R_ast

            # calculo da rigidez, com rotaçao unitaria do apoio esquerdo 
            self.me_1 = sii #* ei/vao #
            self.md_1 = sij #* ei/vao  #
            self.ve_1 = + ( sii + sij ) / vao #* ei/vao #
            self.vd_1 = - ( sii + sij ) / vao #* ei/vao #
            # calculo da rigidez, com rotaçao unitaria do apoio direito
            self.me_2 = sji # * ei/vao #
            self.md_2 = sjj # * ei/vao #
            self.ve_2 = + ( sjj + sij ) / vao #* ei/vao #
            self.vd_2 = - ( sjj + sij ) / vao #* ei/vao #

        elif self.situacao == "ponta_direita":         
            self.vd_0 = q *((vao**4 / (8*ei) + vao**3/(2*ke))/((vao**3)/(3*ei) + (vao**2)/ke))
            self.ve_0 = q * vao - self.vd_0
            
            self.me_0 = + q * vao**2 / 2. - self.vd_0*vao 
            self.md_0 = 0.0

            a = (2*ei/vao)*1/ke
            b = 0.0#(2*ei/vao)*1/kd
            ##
            self.me_0 = + ((3*b + 1) * q * vao ** 2) / (12 *( 3*b*a + 2*b + 2*a + 1))#*ei/vao
            self.md_0 = - ((3*a + 1) * q * vao ** 2) / (12 *( 3*b*a + 2*b + 2*a + 1))#*(ei/vao)
            ##      
            self.ve_0 = (self.md_0 + self.me_0 + q*vao**2/2)/vao#q * vao / (2 + 3 *kd)
            self.vd_0 = q*vao - self.ve_0# (q * vao / (2 + 3 *ke))


            R_ast = (1 + 0) * (1 + 4*ei / (vao*k1)) - ((ei/vao)**2)#* (4 / (k1*k2))
        
            sii = (4 + (12*ei/(vao*k1))) / R_ast
            sjj = (4 + 0) / R_ast
            sij = sji = 2. / R_ast

            # calculo da rigidez, com rotaçao unitaria do apoio esquerdo
            self.me_1 = sii  #* ei/vao #
            self.md_1 = sij  #* ei/vao #
            self.ve_1 = + ( sii + sij ) / vao #* ei/vao #
            self.vd_1 = - ( sii + sij ) / vao #* ei/vao #
            # calculo da rigidez, com rotaçao unitaria do apoio direito
            self.me_2 = sji  #* ei/vao #
            self.md_2 = sjj  #* ei/vao #
            self.ve_2 = + ( sjj + sij ) / vao #* ei/vao #
            self.vd_2 = - ( sjj + sij ) / vao #* ei/vao #      
            
 
        elif self.situacao == "intermediario":
##            self.me_0 = + ((3*kd + 1) * q * vao ** 2) / (12 * 3*kd*ke + 2*kd + 2*ke + 1)*ei/vao
##            self.md_0 = - ((3*ke + 1) * q * vao ** 2) / (12 * 3*kd*ke + 2*kd + 2*ke + 1)*ei/vao
####            self.ve_0 = q * vao / (2 + 3 *kd)*ei
####            self.vd_0 = q * vao / (2 + 3 *ke)*ei
##            self.ve_0 = (-md_0 + me_0 + q*vao**2/2)/vao#q * vao / (2 + 3 *kd)
##            self.vd_0 = q*vao - ve_0# (q * vao / (2 + 3 *ke))

            a = (2*ei/vao)*1/ke
            b = (2*ei/vao)*1/kd
            ##
            self.me_0 = + ((3*b + 1) * q * vao ** 2) / (12 *( 3*b*a + 2*b + 2*a + 1))
            self.md_0 = - ((3*a + 1) * q * vao ** 2) / (12 *( 3*b*a + 2*b + 2*a + 1))
            ##      
            self.ve_0 = (self.md_0 + self.me_0 + q*vao**2/2.0)/vao
            self.vd_0 = q*vao - self.ve_0

            R_ast = (1 + 4*ei / (vao*k2)) * (1 + 4*ei / (vao*k1)) - ((ei/vao)**2)* (4 / (k1*k2))
            
            sii = (4 + (12*ei/(vao*k1))) / R_ast
            sjj = (4 + (12*ei/(vao*k2))) / R_ast
            sij = sji = 2. / R_ast
            
            self.me_1 = sii  #* ei/vao #
            self.md_1 = sij  #* ei/vao #
            self.ve_1 = + ( sii + sij ) / vao #* ei/vao #
            self.vd_1 = - ( sii + sij ) / vao #* ei/vao #
            # calculo da rigidez, com rotaçao unitaria do apoio direito
            self.me_2 = sji  #* ei/vao #
            self.md_2 = sjj  #* ei/vao #
            self.ve_2 = + ( sjj + sij ) / vao #* ei/vao #
            self.vd_2 = - ( sjj + sij ) / vao #* ei/vao #
        
