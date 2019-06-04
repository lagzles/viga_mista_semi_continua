# ve = reaçao do lado esquerdo
# vd = reaçao do lado direito
# me = momento do lado esquerdo
# md = momento do lado direito
# vao = distancia entre apoios da viga
# i =  inercia do tramo
# Livro:  semi-Rigid Connections in Steel Frames
# matriz de rigidez a partir da pagina 78
import propriedades_perfil_i as prop
import dimensionamento_R04 as dim

ponta_esq = "ponta_esquerda"
ponta_dir = "ponta_direita"
intermediario = "intermediario"

class Tramos(object):
    def __init__(self, n, vao, e, situacao, d, bfs, bfi, tw, tfs, tfi):
        # o tramo é considerado como engastado - engastado
        self.vao = vao # valor do vao [m]
        self.n = n # numero do vao / viga
        self.e = e # modulo elasticidade do aço
        self.d = d
        self.bfs = bfs
        self.bfi = bfi
        self.tw = tw
        self.tfs = tfs
        self.tfi = tfi
        
        self.situacao = situacao  # situação do tramo / viga / vao

    def create_subs(self, condicao, vaoad, largInfluencia,
                    interna, hdeck, Asl, fck, fy, E):

        aa = prop.area(self.d, self.tw, self.bfs, self.tfs, self.bfi, self.tfi)
        ia = prop.i_x(self.d, self.tw, self.bfs, self.tfs, self.bfi, self.tfi)

        # Inercia efetiva na regiao negativa
        ds = self.d * .5 + (7.5 + (hdeck - 75) * .05)
        ay_neg = Asl * ds
        ay2_neg = Asl * ds ** 2

        areatotal_neg = aa + Asl
        yg_neg = ay_neg / areatotal_neg
        iefNeg = round(ia + ay2_neg - areatotal_neg * yg_neg ** 2, 2)
        iefNeg = iefNeg * (100 ** -4)

        wefCurta1 = 0
        wefCurta2 = 0
        wefLonga1 = 0
        wefLonga2 = 0

        vvrd = vrd(self.d, self.tw, self.tfs, self.tfi, fy, self.e)
        
        iefPosL = iefPosC = iefPos = 0
##        if condicao == 'pre-cura':
        iefPos, mrdPos, wefCurta1 = dim.inercia_equivalente_curta(self.vao, largInfluencia,
                                                                  interna, hdeck, self.d, self.tw, self.bfs, self.bfi,
                                                                  self.tfs, self.tfi,
                                                                  ia, aa, fck, fy, E)
        iefPos, mrdPos, wefCurta2 = dim.inercia_equivalente_curta(self.vao, largInfluencia,
                                                                  interna, hdeck, self.d, self.tw, self.bfs, self.bfi,
                                                                  self.tfs, self.tfi,
                                                                  ia, aa, fck, fy, E)
        iefPosC = (iefPos)* (100 ** -4)
##        elif condicao == 'pos-cura':
        iefPos, mrdPos, wefLonga1 = dim.inercia_equivalente_longa(self.vao, vaoad[0], largInfluencia,
                                                                  interna, hdeck, self.d, self.tw, self.bfs, self.bfi,
                                                                  self.tfs, self.tfi,
                                                                  Asl, ia, aa, fck, fy, E)
        iefPos, mrdPos, wefLonga2 = dim.inercia_equivalente_longa(self.vao, vaoad[1], largInfluencia,
                                                                  interna, hdeck, self.d, self.tw, self.bfs, self.bfi,
                                                                  self.tfs, self.tfi,
                                                                  Asl, ia, aa, fck, fy, E)
        iefPosL = (iefPos)* (100 ** -4)

        wefCurta1 *= 100 ** -3
        wefCurta2 *= 100 ** -3
        wefLonga1 *= 100 ** -3
        wefLonga2 *= 100 ** -3
        
        if self.situacao == "ponta_esquerda":
            vao1 = self.vao*.85
            vao2 = self.vao*.15

            i1 = iefPos #self.i
            i2 = iefNeg #self.i * .75

            sub1 = SubTramos(self.n, 1, 'pos', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'neg', vao2, i2, self.e)

            sub1.iefPosLonga = (iefPosL)
            sub1.iefPosCurta = (iefPosC)
            sub1.iefNeg = iefNeg
            
            sub2.iefPosLonga = (0)
            sub2.iefPosCurta = (0)
            sub2.iefNeg = iefNeg
                        
            sub1.mrdPos = mrdPos
            sub2.mrdPos = mrdPos

            sub1.vrd = vvrd
            sub2.vrd = vvrd
            
            sub1.wefCurta = (wefCurta1)
            sub2.wefCurta = (wefCurta2)
            
            sub1.wefLonga = (wefLonga1)
            sub2.wefLonga = (wefLonga2)


            return sub1, sub2
        elif self.situacao == "ponta_direita":
            vao1 = self.vao*.15
            vao2 = self.vao*.85

            i1 = iefNeg #self.i * .75
            i2 = iefPos #self.i

            sub1 = SubTramos(self.n, 1, 'neg', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'pos', vao2, i2, self.e)

            sub2.iefPosLonga = (iefPosL)
            sub2.iefPosCurta = (iefPosC)
            sub2.iefNeg = 0
            
            sub1.iefPosLonga = (0)
            sub1.iefPosCurta = (0)
            sub1.iefNeg = iefNeg

            sub1.mrdPos = mrdPos
            sub2.mrdPos = mrdPos

            sub1.vrd = vvrd
            sub2.vrd = vvrd           
            
            sub1.wefCurta = wefCurta1
            sub2.wefCurta = wefCurta2
            
            sub1.wefLonga = wefLonga1
            sub2.wefLonga = wefLonga2

            return sub1, sub2
        elif self.situacao == "intermediario":
            vao1 = self.vao*.15
            vao2 = self.vao*.70
            vao3 = self.vao*.15

            i1 = iefNeg #self.i * .75
            i2 = iefPos #self.i
            i3 = iefNeg #self.i * .75

            sub1 = SubTramos(self.n, 1, 'neg', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'pos', vao2, i2, self.e)
            sub3 = SubTramos(self.n, 3, 'neg', vao3, i3, self.e)

            sub1.iefPosLonga = (0)
            sub1.iefPosCurta = (0)
            sub1.iefNeg = iefNeg

            sub2.iefPosLonga = (iefPosL)
            sub2.iefPosCurta = (iefPosC)
            sub2.iefNeg = iefNeg
            
            sub3.iefPosLonga = (0)
            sub3.iefPosCurta = (0)
            sub3.iefNeg = iefNeg

            sub1.mrdPos = mrdPos
            sub2.mrdPos = mrdPos
            sub3.mrdPos = mrdPos

            sub1.vrd = vvrd
            sub2.vrd = vvrd            
            sub3.vrd = vvrd
                        
            sub1.wefCurta = wefCurta1
            sub2.wefCurta = wefCurta2
            sub3.wefCurta = wefCurta1
            
            sub1.wefLonga = wefLonga1
            sub2.wefLonga = wefLonga2
            sub3.wefLonga = wefLonga1

            return sub1, sub2, sub3

def vrd(d, tw, tfs, tfi, fy, e):
    e = 200000
    hw = (d - tfs - tfi)
    lambda_ = hw / tw
    kv = 5
    lambda_p = 1.10 * (kv * e / (fy*10)) ** 0.5
    lambda_r = 1.37 * ( kv * e) ** 0.5

    aw = hw * tw
    vpl = 0.6 * aw * fy
    cv = 0
    if lambda_ <= lambda_p:
        cv = 1
    elif lambda_ <= lambda_r:
        cv = lambda_p / lambda_
    else:
        cv = 1.51*e*kv/lambda_**2/fy

    vv = 0.9*vpl*cv
    return vv



class SubTramos(Tramos):

    def __init__(self, tramon, idsub, momento, vao, i, e):
        self.vao = vao
        self.n = tramon
        self.i = i
        self.e = e
        self.idSub = idsub
        self.momento = momento
        self.iefNeg = 0
        self.iefPosCurta = 0
        self.iefPosLonga = 0
        self.wefCurta = 0
        self.wefLonga = 0

        self.mrdPos = 0
        self.mrdNeg = 0
        self.vrd = 0
        
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
    

    def rigidez(self, k1, k2, i):
        ei = self.e * i
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
