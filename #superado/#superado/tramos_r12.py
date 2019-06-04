# ve = reaçao do lado esquerdo
# vd = reaçao do lado direito
# me = momento do lado esquerdo
# md = momento do lado direito
# vao = distancia entre apoios da viga
# i =  inercia do tramo
# Livro:  semi-Rigid Connections in Steel Frames
# matriz de rigidez a partir da pagina 78
import propriedades_perfil_i as prop
import dimensionamento_R02 as dim

ponta_esq = "ponta_esquerda"
ponta_dir = "ponta_direita"
intermediario = "intermediario"

class Tramos(object):
    def __init__(self, n, vao, e, situacao, d, bf, tw, tf):
        # o tramo é considerado como engastado - engastado
        self.vao = vao # valor do vao [m]
        self.n = n # numero do vao / viga
        self.e = e # modulo elasticidade do aço
        self.d = d
        self.bf = bf
        self.tw = tw
        self.tf = tf
        self.situacao = situacao  # situação do tramo / viga / vao

    def create_subs(self, condicao, vaoad, largInfluencia,
                    interna, hdeck, Asl, fck, fy, E):

        aa = prop.area(self.d, self.tw, self.bf, self.tf, self.bf, self.tf)
        ia = prop.i_x(self.d, self.tw, self.bf, self.tf, self.bf, self.tf)

        iefNeg1 = iefNeg2 = iefPos1 = iefPos2 = 0
        if condicao == 'pre-cura':
            print('pre-cura')
            iefNeg1, iefPos1 = dim.inercia_equivalente_longa(self.vao, vaoad[0], largInfluencia,
                                                           interna, hdeck, self.d, Asl, ia, aa,
                                                           fck, fy, E)
            iefNeg2, iefPos2 = dim.inercia_equivalente_longa(self.vao, vaoad[1], largInfluencia,
                                                             interna, hdeck, self.d, Asl, ia, aa,
                                                             fck, fy, E)

        elif condicao == 'pos-cura':
            print('pos-cura')
            iefNeg1, iefPos1 = dim.inercia_equivalente_longa(self.vao, vaoad[0], largInfluencia,
                                          interna, hdeck, self.d, Asl, ia, aa,
                                          fck, fy, E)
            iefNeg2, iefPos2 = dim.inercia_equivalente_longa(self.vao, vaoad[1], largInfluencia,
                                                             interna, hdeck, self.d, Asl, ia, aa,
                                                             fck, fy, E)

        print('Tramo %d, Sub tramos iefNeg1 = %.2f \t  iefPos1 = %.2f' % (self.n, iefNeg1, iefPos1))
        print('Tramo %d, Sub tramos iefNeg2 = %.2f \t  iefPos2 = %.2f' % (self.n, iefNeg2, iefPos2))

        listaSubs = []
        if self.situacao == "ponta_esquerda":
            vao1 = self.vao*.85
            vao2 = self.vao*.15

            i1 = iefPos2 #self.i
            i2 = iefNeg2 #self.i * .75

            sub1 = SubTramos(self.n, 1, 'pos', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'neg', vao2, i2, self.e)

            return sub1, sub2
        elif self.situacao == "ponta_direita":
            vao1 = self.vao*.15
            vao2 = self.vao*.85

            i1 = iefNeg1 #self.i * .75
            i2 = iefPos1 #self.i

            sub1 = SubTramos(self.n, 1, 'neg', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'pos', vao2, i2, self.e)

            listaSubs.append(sub1)
            return sub1, sub2
        elif self.situacao == "intermediario":

            vao1 = self.vao*.15
            vao2 = self.vao*.70
            vao3 = self.vao*.15

            i1 = iefNeg1 #self.i * .75
            i2 = min(iefPos2, iefPos1) #self.i
            i3 = iefNeg2 #self.i * .75

            sub1 = SubTramos(self.n, 1, 'neg', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'pos', vao2, i2, self.e)
            sub3 = SubTramos(self.n, 3, 'neg', vao3, i3, self.e)

            return sub1, sub2, sub3


class SubTramos(Tramos):

    def __init__(self, tramon, idsub, momento, vao, i, e):
        self.vao = vao
        self.n = tramon
        self.i = i
        self.e = e
        self.idSub = idsub
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

        # Utilizando a dissertação de André Christoforo
        # pagina 47(pdf)
        eri = ei / (vao * k1)  # equação 54.a
        erj = ei / (vao * k2)  # equação 54.b
        erij = 1 + eri + erj   # equação 54.c
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
