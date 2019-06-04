## ve = reaçao do lado esquerdo
## vd = reaçao do lado direito
## me = momento do lado esquerdo
## md = momento do lado direito
## vao = distancia entre apoios da viga
## i =  inercia do tramo

class Tramos:
    def __init__(self, _vao, _i, _e, _situacao):
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
        
        R_ast = (1 + 4*ei / (vao*k1)) * (1 + 4*ei / (vao*k2)) - ((ei/vao)**2)* 4 / (k1*k2)
        
        sii = (4 + (12*ei/(vao*k2))) / R_ast
        sjj = (4 + (12*ei/(vao*k1))) / R_ast
        sij = sji = 2. / R_ast


        if self.situacao == "ponta_esquerda":
            eiR = ei / (vao * kd)
            feir = lambda x: 1 + x*eiR
            self.ve_0 = + q * vao * feir(5) / ( 2*(feir(4)))
            self.vd_0 = + q * vao * feir(3) / ( 2*(feir(4)))

            self.me_0 = - q * vao**2 * feir(6) / (12 * feir(4))            
            self.md_0 = + q * vao**2 / (12 * (feir(4)))
            print("calculo ponta esquerda")
            # o tramo é considerado como engastado - engastado
            # calculo da rigidez, com rotaçao unitaria do apoio esquerdo 
            self.me_1 = sii #
            self.md_1 = sij #
            self.ve_1 = + ( sii + sij ) / vao#
            self.vd_1 = - ( sii + sij ) / vao#
            # calculo da rigidez, com rotaçao unitaria do apoio direito
            self.me_2 = sji #
            self.md_2 = sjj #
            self.ve_2 = + ( sii + sij ) / vao#
            self.vd_2 = - ( sii + sij ) / vao#
       
##            print(self.ve_0, self.vd_0)
##            print(self.me_0, self.md_0)
##            
        elif self.situacao == "ponta_direita":
            eiRd = ei / (ke * vao)
            print(eiRd)
            
            feird = lambda x: 1 + x*eiRd
            self.ve_0 = + q * vao * feird(3) / ( 2*(feird(4)))
            self.vd_0 = + q * vao * feird(5) / ( 2*(feird(4)))

            self.me_0 = + q * vao**2 / (12 * (feird(4)))
            self.md_0 = - q * vao**2 * feird(6) / (12 * feird(4))            
            print("calculo ponta direita")
            # calculo da rigidez, com rotaçao unitaria do apoio esquerdo 
            self.md_1 = sii #
            self.me_1 = sij #
            self.vd_1 = + ( sii + sij ) / vao#
            self.ve_1 = - ( sii + sij ) / vao#
            # calculo da rigidez, com rotaçao unitaria do apoio direito
            self.md_2 = sji #
            self.me_2 = sjj #
            self.vd_2 = + ( sii + sij ) / vao#
            self.ve_2 = - ( sii + sij ) / vao#
           
##            print(self.ve_0, self.vd_0)
##            print(self.me_0, self.md_0)            
##            

        elif self.situacao == "intermediario":
            self.me_0 = - ((3*kd + 1) * q * vao ** 2) / (12 * 3*kd*ke + 2*kd + 2*ke + 1)
            self.md_0 = - ((3*ke + 1) * q * vao ** 2) / (12 * 3*kd*ke + 2*kd + 2*ke + 1)
            self.ve_0 = q * vao / (2 + 3 *kd)
            self.vd_0 = q * vao / (2 + 3 *ke)
##            print(self.ve_0 + self.vd_0)
            

        k1 = ke
        k2 = kd

        eRi = ei / (vao*k1)
        eRj = ei / (vao*k2)
        eRij = 1 + eRi + eRj
        
        eRi1 = 1 + eRi
        eRj1 = 1 + eRj
        
        eRi2 = 1 + 2*eRi
        eRj2 = 1 + 2*eRj
        
        eRi3 = 1 + 3*eRi
        eRj3 = 1 + 3*eRj

        C = 2 * ei / ((vao**3) * (4*eRij + 3 *(4*eRi*eRj - 1)))

        R_ast = (1 + 4*ei / (vao*k1)) * (1 + 4*ei / (vao*k2)) - ((ei/vao)**2)* 4 / (k1*k2)
        
        sii = (4 + (12*ei/(vao*k2))) / R_ast
        sjj = (4 + (12*ei/(vao*k1))) / R_ast
        sij = sji = 2. / R_ast

##
##        # o tramo é considerado como engastado - engastado
##        # calculo da rigidez, com rotaçao unitaria do apoio esquerdo 
##        self.me_1 = sii #2*C*(vao**2)*eRj3# + 4. * (ei) / vao
##        self.md_1 = sij #  C*(vao**2)# + 2. * (ei) / vao
##        self.ve_1 = + ( sii + sij ) / vao#+ 3*C*vao*eRj2#+ abs((self.me_1 + self.md_1) / vao)
##        self.vd_1 = - ( sii + sij ) / vao#- 3*C*vao*eRj2#- abs((self.md_1 + self.me_1) / vao)
##
##        # calculo da rigidez, com rotaçao unitaria do apoio direito
##        self.me_2 = sji # C*(vao**2)#+ 2. * (ei) / vao - kd*.5#+ke#- 2. * (kd) / vao        
##        self.md_2 = sjj #2*C*(vao**2)*eRi3#+ 4. * (ei) / vao - kd#- 4. * (kd) / vao
##        self.ve_2 = + ( sii + sij ) / vao# + 3*C*vao*eRi2#+ abs((self.me_2 + self.md_2) / vao)
##        self.vd_2 = - ( sii + sij ) / vao# - 3*C*vao*eRi2#- abs((self.md_2 + self.me_2) / vao)
        print("ve   vd  1 ")
        print(self.ve_1, self.vd_1)
        print(self.me_1, self.md_1)
        print("ve  vd 2")
        print(self.ve_2, self.vd_2)
        print(self.me_2, self.md_2)

        print("##################")

##        elif self.situacao == "ponta_direita":
##            # o tramo é considerado como engastado - engastado
##            # calculo da rigidez, com rotaçao unitaria do apoio esquerdo 
##            self.me_1 = -2*C*(vao**2)*eRj3# + 4. * (ei) / vao
##            self.md_1 = -  C*(vao**2)# + 2. * (ei) / vao
##            self.ve_1 = + 3*C*vao*eRj2#+ abs((self.me_1 + self.md_1) / vao)
##            self.vd_1 = - 3*C*vao*eRj2#- abs((self.md_1 + self.me_1) / vao)
##
##            # calculo da rigidez, com rotaçao unitaria do apoio direito
##            self.me_2 =   C*(vao**2)#+ 2. * (ei) / vao - kd*.5#+ke#- 2. * (kd) / vao        
##            self.md_2 = 2*C*(vao**2)*eRi3#+ 4. * (ei) / vao - kd#- 4. * (kd) / vao
##            self.ve_2 = + 3*C*vao*eRi2#+ abs((self.me_2 + self.md_2) / vao)
##            self.vd_2 = - 3*C*vao*eRi2#- abs((self.md_2 + self.me_2) / vao)
            
            
