## ve = reaçao do lado esquerdo
## vd = reaçao do lado direito
## me = momento do lado esquerdo
## md = momento do lado direito
## vao = distancia entre apoios da viga
## i =  inercia do tramo
## utiliza a matriz de rigides desenvolvida por Christoforo

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

    def calc(self, q, ke, kd):
        vao = self.vao
        ei = self.e * self.i

        k1 = ke
        k2 = kd
        
        R_ast = (1 + 4*ei / (vao*k1)) * (1 + 4*ei / (vao*k2)) - ((ei/vao)**2)* 4 / (k1*k2)
        
        sii = (4 + (12*ei/(vao*k2))) / R_ast
        sjj = (4 + (12*ei/(vao*k1))) / R_ast
        sij = sji = 2. / R_ast


        if self.situacao == "ponta_esquerda":
            eiR = ei / (vao * kd)
            feir = lambda x: 1 + x*eiR
            self.ve_0 = q*((vao**4 / (8*ei) + vao**3/(2*kd))/(vao**3/(3*ei) + vao**2/kd))
##            self.ve_0 = q * ((vao**3/(6*ei) + vao**2/(2*kd)) / ((vao**2/(2*ei)) + (vao / kd)))
            self.vd_0 = + q*vao - self.ve_0
            print(self.ve_0, self.vd_0)

            self.me_0 = 0.0#- q * vao**2 * feir(6) / (12 * feir(4))            
            self.md_0 = + q * vao**2 / 2. - self.ve_0*vao #q * vao**2 / (12 * (feir(4)))
            print("calculo ponta esquerda")
            eRi = ei / (vao * ke)
            eRj = ei / (vao * kd)

            eRij = 1 + eRi + eRj
            eRi1 = 1 + eRi
            eRj1 = 1 + eRj
            eRi2 = 1 + 2*eRi
            eRj2 = 1 + 2*eRj
            eRi3 = 1 + 3*eRi
            eRj3 = 1 + 3*eRj

            C = 2*ei / ((vao**3) * (4*eRij + 3 * (4*eRi*eRj -1)))
            # calculo da rigidez, com rotaçao unitaria do apoio esquerdo 
            self.me_1 = 2*C*vao**2*eRj3 #sii #* ei/vao #
            self.md_1 =   C*vao**2 #sij #* ei/vao  #
            self.ve_1 = + 3*C*vao*eRj2 #( sii + sij ) / vao #* ei/vao #
            self.vd_1 = - 3*C*vao*eRj2 #( sii + sij ) / vao #* ei/vao #
            # calculo da rigidez, com rotaçao unitaria do apoio direito
            self.me_2 =   C*vao**2 #sji # * ei/vao #
            self.md_2 = 2*C*vao**2*eRi3 #sjj # * ei/vao #
            self.ve_2 = + 3*C*vao*eRi2 #( sii + sij ) / vao #* ei/vao #
            self.vd_2 = - 3*C*vao*eRi2 #( sii + sij ) / vao #* ei/vao #

        elif self.situacao == "ponta_direita":
            eiRd = ei / (kd * vao)            
            feird = lambda x: 1 + x*eiRd            
            self.vd_0 = q*((vao**4 / (8*ei) + vao**3/(2*kd))/((vao**3)/(3*ei) + (vao**2)/kd))
##            self.vd_0 = q * ((vao**3/(6*ei) + vao**2/(2*kd)) / ((vao**2/(2*ei)) + (vao / kd)))
            self.ve_0 = + q*vao - self.vd_0
            
            self.me_0 = + q * vao**2 / 2. - self.vd_0*vao 
            self.md_0 = 0.0
            print("calculo ponta direita")
            # calculo da rigidez, com rotaçao unitaria do apoio esquerdo
##            R_ast = (1 + 4*ei / (vao*k2)) * (1 + 4*ei / (vao*k1)) - ((ei/vao)**2)* 4 / (k1*k2)
##        
##            sii = (4 + (12*ei/(vao*k2))) / R_ast
##            sjj = (4 + (12*ei/(vao*k1))) / R_ast
##            sij = sji = 2. / R_ast

            eRi = ei / (vao * ke)
            eRj = ei / (vao * kd)
            
            eRij = 1 + eRi + eRj
            eRi1 = 1 + eRi
            eRj1 = 1 + eRj
            eRi2 = 1 + 2*eRi
            eRj2 = 1 + 2*eRj
            eRi3 = 1 + 3*eRi
            eRj3 = 1 + 3*eRj

            C = 2*ei / ((vao**3) * (4*eRij + 3 * (4*eRi*eRj -1)))

            self.me_1 = 2*C*vao**2*eRj3 #sii  #* ei/vao #
            self.md_1 =   C*vao**2 # sij  #* ei/vao #
            self.ve_1 = + 3*C*vao*eRj2 # + ( sii + sij ) / vao #* ei/vao #
            self.vd_1 = - 3*C*vao*eRj2 # - ( sii + sij ) / vao #* ei/vao #
            # calculo da rigidez, com rotaçao unitaria do apoio direito
            self.me_2 =   C*vao**2 # sji  #* ei/vao #
            self.md_2 = 2*C*vao**2*eRi3 # sjj  #* ei/vao #
            self.ve_2 = + 3*C*vao*eRi2 #+ ( sii + sij ) / vao #* ei/vao #
            self.vd_2 = - 3*C*vao*eRi2 # - ( sii + sij ) / vao #* ei/vao #
      
            
 
        elif self.situacao == "intermediario":
            self.me_0 = - ((3*kd + 1) * q * vao ** 2) / (12 * 3*kd*ke + 2*kd + 2*ke + 1)
            self.md_0 = - ((3*ke + 1) * q * vao ** 2) / (12 * 3*kd*ke + 2*kd + 2*ke + 1)
            self.ve_0 = q * vao / (2 + 3 *kd)
            self.vd_0 = q * vao / (2 + 3 *ke)
##            print(self.ve_0 + self.vd_0)
        
