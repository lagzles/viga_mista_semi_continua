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

    def calc(self, q, ke,kd):
        vao = self.vao
        ei = self.e * self.i

##        if ke == 0:
##            ke = ei
##
##        if kd == 0:
##            kd = ei
        
        # o tramo é considerado como engastado - engastado
        # calculo das forças de engaste perfeito
        self.ve_0 = + q * vao / 2.
        self.vd_0 = + q * vao / 2.
        self.me_0 = + q * vao ** 2 / 12.
        self.md_0 = - q * vao ** 2 / 12.

        # o tramo é considerado como engastado - engastado
        # calculo da rigidez, com rotaçao unitaria do apoio esquerdo        
##        self.ve_1 = + 6. * (ei-ke) / vao **2
##        self.vd_1 = - 6. * (ei-kd) / vao **2
        self.me_1 = + 4. * (ei) / vao - ke#- 4. * (ke) / vao
        self.md_1 = + 2. * (ei) / vao - ke*.5#+kd#- 2. * (ke) / vao
        self.ve_1 = + abs((self.me_1 + self.md_1) / vao)
        self.vd_1 = - abs((self.md_1 + self.me_1) / vao)

        # calculo da rigidez, com rotaçao unitaria do apoio direito        
##        self.ve_2 = + 6. * (ei-kd) / vao **2
##        self.vd_2 = - 6. * (ei-kd) / vao **2
        self.me_2 = + 2. * (ei) / vao - kd*.5#+ke#- 2. * (kd) / vao        
        self.md_2 = + 4. * (ei) / vao - kd#- 4. * (kd) / vao
        self.ve_2 = + abs((self.me_2 + self.md_2) / vao)
        self.vd_2 = - abs((self.md_2 + self.me_2) / vao)
