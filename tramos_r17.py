# ve = reaçao do lado esquerdo
# vd = reaçao do lado direito
# me = momento do lado esquerdo
# md = momento do lado direito
# vao = distancia entre apoios da viga
# i =  inercia do tramo
# Livro:  semi-Rigid Connections in Steel Frames
# matriz de rigidez a partir da pagina 78
import propriedades_perfil_i as prop
import dimensionamento_R10 as dim

ponta_esq = "ponta_esquerda"
ponta_dir = "ponta_direita"
intermediario = "intermediario"

class Tramos(object):
    def __init__(self, n, vao, vaoad, bInf, hdeck, ha,
                 Asl, bitola, fck, fy, fys, e, es,
                 situacao, d, bfs, bfi, tw, tfs, tfi):
        # o tramo é considerado como engastado - engastado
        self.vao = vao # valor do vao [m]
        self.n = n # numero do vao / viga
        self.e = e # modulo elasticidade do aço
        self.es = es
        self.d = d
        self.bfs = bfs
        self.bfi = bfi
        self.tw = tw
        self.tfs = tfs
        self.tfi = tfi
        self.vaoad = vaoad
        self.b_inf = bInf
        self.fck = fck
        self.hdeck = hdeck
        self.ha = ha
        self.asl = Asl
        self.fy = fy
        self.fys = fys
        self.wefCurta = 0
        self.wefLonga = 0
        self.iefNeg = 0
        self.iefPos = 0
        self.iefCurta = 0
        self.bitola = bitola
        self.flecha_curta = 0
        self.flecha_longa = 0
        self.flecha_md = 0
        self.nn = 0
        self.peso_perfil = ((d-tfs-tfi)*tw + bfs * tfs + bfi * tfi)/10000 * 7850 * vao
        self.peso_barras = vao * .3 * Asl / 10000 * 7850
        
        # cantoneira de alma 15 x 15 x 6.35, L = 25 [cm]
        peso_cant_alma = .15 * .15 * 0.00635 * .25 * 7850
        # cantoneira inferior 25 x 25 x 9.5, L = 15 [cm]
        peso_cant_inferior = .25 * .25 * 0.0095 * .15 * 7850
        
        self.peso_cantoneiras = 4*peso_cant_alma + peso_cant_inferior*2

        self.aa = prop.area(d, tw, bfs, tfs, bfi, tfi)
        self.ia = prop.i_x(d, tw, bfs, tfs, bfi, tfi)
        self.wa = round(prop.wx(self.ia, d))

        self.mrdNegi = 0
        self.mrdNegf = 0
        self.n_conectores = 0
        self.situacao = situacao  # situação do tramo / viga / vao

        ##### Valores de resistencia para cada verificação do dimensionameno
        ## 1 Verificação
        self.v1rda = 0
        self.v1rdb = 0
        self.v1sd = 0
        self.v1a = 0
        self.v1b = 0
        self.v1 = 0

        ## 2 Verificação
        self.v2mesa = 0 
        self.v2alma = 0
        self.v2 = 0

        ## 3 Verificação
        self.v3rd = 0
        self.v3sd = 0
        self.v3 = 0
        
        ## 4 Verificação
        self.v4rd = 0
        self.v4sd = 0
        self.v4 = 0

        ## 5 Verificação
        self.v5rda = 0
        self.v5sda = 0
        self.v5rdb = 0
        self.v5sdb = 0
        self.v5 = 0

        ## 6 Verificação
        self.v6rd = 0
        self.v6sda = 0
        self.v6sdb = 0
        self.v6 = 0

        ## 7 Verificação
        self.v7rd = 0
        self.v7sd = 0
        self.v7 = 0

        ## 8 Verificação
        self.v8rd = 0
        self.v8sd = 0
        self.v8 = 0

        ## 9 Verificação
        self.v9rd = 0
        self.v9sd = 0
        self.v9 = 0

        ## 10 Verificação
        self.v10rd = 0
        self.v10sd = 0
        self.v10 = 0

        

    def create_subs(self, interna):

        vaoad = self.vaoad
        vaoc = self.vao
        largInfluencia = self.b_inf
        fck = self.fck
        fy = self.fy
        fys = self.fys
        hdeck = self.hdeck
        Asl = self.asl
        e = E = self.e
        es = self.es
        ha = self.ha
        bitola = self.bitola

        d = self.d
        tw = self.tw
        bfs = self.bfs
        tfs = self.tfs
        bfi = self.bfi
        tfi = self.tfi

        vaoad1 = vaoad[0]
        vaoad2 = vaoad[1]
                
        aa = prop.area(d, tw, bfs, tfs, bfi, tfi)
        ia = prop.i_x(d, tw, bfs, tfs, bfi, tfi)

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

        vvrd = vrd(d, tw, tfs, tfi, fy, e)

        # Conforme Item O.2.2.2.b NBR 8800-2008
        # Conforme Item O.2.2.2.a NBR 8800-2008
        if interna == 1:
            larguraEfetivaPos = min(2 * 0.7 * vaoc / 8, largInfluencia)  # interno
            le = vaoc * .7 / 100
        else:
            larguraEfetivaPos = min(2 * 0.8 * vaoc / 8., largInfluencia)  # extremo
            le = vaoc * .85 / 100

        larguraEfetiva1 = min((vaoc / 4 + vaoad1 / 4) * 2 / 8., largInfluencia)
        larguraEfetiva2 = min((vaoc / 4 + vaoad2 / 4) * 2 / 8., largInfluencia)
        
        self.befPos1 = larguraEfetivaPos
        self.befPos2 = larguraEfetivaPos
        
        self.befNegi = larguraEfetiva1
        self.befNegf = larguraEfetiva2

        self.iefNeg = iefNeg
        
        iefPosL = iefPosC = iefPos = 0
        ## inercia Efetiva da Região Positiva, para carregamento de CURTA duração
        dim.inercia_equivalente_curta(self, le)
        dim.inercia_equivalente_curta(self, le)

        ## inercia Efetiva da Região Positiva, para carregamento de LONGA duração
        dim.inercia_equivalente_longa(self, le)
        dim.inercia_equivalente_longa(self, le)

        # Calculo do Vinculo semi-rigido
        C1, tetau1, ylnp1, x1, mrd_neg1, mrd_neg1k, n_conectores = dim.calculo_C(self, vaoad1, "esquerdo")
        C1 *= 1 / 100.
        
        C2, tetau2, ylnp2, x1, mrd_neg2, mrd_neg2k,_ = dim.calculo_C(self, vaoad2, "direito")
        C2 *= 1 / 100.

        self.tetauf = tetau2
        self.tetaui = tetau1
        self.ylnpx1 = x1

        self.mrdNegk = mrd_neg1k
        self.n_conectores = n_conectores
        # Calculo do Vinculo semi-rigido
        ei = e * self.iefPosLonga
        
        
        if self.situacao == "ponta_esquerda":
            vao1 = self.vao*.85
            vao2 = self.vao*.15
            eng1 = (10 ** 9) * ei / vao1
            eng2 = (10 ** 9) * ei / vao2

            i1 = iefPos #self.i
            i2 = iefNeg #self.i * .75

            self.k1 = eng1
            self.k2 = C2

            sub1 = SubTramos(self.n, 1, 'pos', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'neg', vao2, i2, self.e)

            self.subtramos = [sub1, sub2]

            sub1.iefPosLonga = (self.iefPosLonga)
            sub1.iefPosCurta = (self.iefPosCurta)
            sub1.iefNeg = iefNeg
            sub1.k1 = eng1
            sub1.k2 = eng1

            sub1.befPos = larguraEfetivaPos
            sub1.befNeg = 0

            sub2.befPos = larguraEfetivaPos
            sub2.befNeg = larguraEfetiva2
            
            sub1.ylnp = ylnp1
            self.ylnp = ylnp1
            
            sub1.tetau = tetau1            
            sub1.n_conectores = n_conectores
            sub2.n_conectores = n_conectores
            
            sub2.iefPosLonga = (0)
            sub2.iefPosCurta = (0)
            sub2.iefNeg = iefNeg
            sub2.k1 = eng2
            sub2.k2 = C2
            sub2.ylnp = ylnp1
            sub2.tetau = tetau1
                        
            sub1.mrdPos = self.mrdPos
            sub2.mrdPos = self.mrdPos            

            sub1.mrdNeg = 0.0
            sub2.mrdNeg = mrd_neg2

            self.mrdNegi = 0.0
            self.mrdNegf = mrd_neg2            

            sub1.vrd = vvrd
            sub2.vrd = vvrd
            self.vrd = vvrd
            
            sub1.wefCurta = (self.wefCurta)
            sub2.wefCurta = (self.wefCurta)
            self.wefCurta = (self.wefCurta)
            
            sub1.wefLonga = (self.wefLonga)
            sub2.wefLonga = (self.wefLonga)
            self.wefLonga = (self.wefLonga)

            return sub1, sub2
        elif self.situacao == "ponta_direita":
            vao1 = self.vao*.15
            vao2 = self.vao*.85
            eng1 = (10 ** 9) * ei / vao1
            eng2 = (10 ** 9) * ei / vao2

            i1 = iefNeg #self.i * .75
            i2 = iefPos #self.i

            self.k1 = C1
            self.k2 = eng1

            sub1 = SubTramos(self.n, 1, 'neg', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'pos', vao2, i2, self.e)

            self.subtramos = [sub1, sub2]

            sub1.iefPosLonga = (0)
            sub1.iefPosCurta = (0)
            sub1.iefNeg = iefNeg
            sub1.k1 = C1
            sub1.k2 = eng1
            sub1.ylnp = ylnp1
            sub1.tetau = tetau1

            sub1.befPos = larguraEfetivaPos
            sub1.befNeg = larguraEfetiva1

            sub2.befPos = larguraEfetivaPos
            sub2.befNeg = 0
            
            sub1.n_conectores = n_conectores
            sub2.n_conectores = n_conectores
            
            sub2.iefPosLonga = (self.iefPosLonga)
            sub2.iefPosCurta = (self.iefPosCurta)
            sub2.iefNeg = 0
            sub2.k1 = eng2
            sub2.k2 = eng2
            sub2.ylnp = ylnp2
            self.ylnp = ylnp2
            
            sub2.tetau = tetau2
            
            sub1.mrdPos = self.mrdPos
            sub2.mrdPos = self.mrdPos

            sub1.mrdNeg = mrd_neg2
            sub2.mrdNeg = 0.0

            self.mrdNegf = 0.0
            self.mrdNegi = mrd_neg1


            sub1.vrd = vvrd
            sub2.vrd = vvrd
            self.vrd = vvrd
            
            sub1.wefCurta = self.wefCurta
            sub2.wefCurta = self.wefCurta
            self.wefCurta = self.wefCurta
            
            sub1.wefLonga = self.wefLonga
            sub2.wefLonga = self.wefLonga
            self.wefLonga = self.wefLonga

            return sub1, sub2
        elif self.situacao == "intermediario":
            vao1 = self.vao*.15
            vao2 = self.vao*.70
            vao3 = self.vao*.15
            eng1 = (10 ** 9) * ei / vao1
            eng2 = (10 ** 9) * ei / vao2
            eng3 = (10 ** 9) * ei / vao3

            i1 = iefNeg #self.i * .75
            i2 = iefPos #self.i
            i3 = iefNeg #self.i * .75

            self.k1 = C1
            self.k2 = C2

            sub1 = SubTramos(self.n, 1, 'neg', vao1, i1, self.e)
            sub2 = SubTramos(self.n, 2, 'pos', vao2, i2, self.e)
            sub3 = SubTramos(self.n, 3, 'neg', vao3, i3, self.e)

            self.subtramos = [sub1, sub2, sub3]

            sub1.n_conectores = n_conectores
            sub2.n_conectores = n_conectores
            sub3.n_conectores = n_conectores

            sub1.befPos = larguraEfetivaPos
            sub1.befNeg = larguraEfetiva1

            sub2.befPos = larguraEfetivaPos
            sub2.befNeg = 0

            sub3.befPos = larguraEfetivaPos
            sub3.befNeg = larguraEfetiva2

            sub1.iefPosLonga = (0)
            sub1.iefPosCurta = (0)
            sub1.iefNeg = iefNeg
            sub1.k1 = C1
            sub1.k2 = eng1
            sub1.ylnp = ylnp1
            sub1.tetau = tetau1

            self.ylnp = min(ylnp1, ylnp2)

            sub2.iefPosLonga = (self.iefPosLonga)
            sub2.iefPosCurta = (self.iefPosCurta)
            sub2.iefNeg = iefNeg
            sub2.k1 = eng2
            sub2.k2 = eng2
            sub2.ylnp = ylnp2
            sub2.tetau = tetau2
            
            sub3.iefPosLonga = (0)
            sub3.iefPosCurta = (0)
            sub3.iefNeg = iefNeg
            sub3.k1 = eng3
            sub3.k2 = C2
            sub3.ylnp = ylnp1
            sub3.tetau = tetau1

            sub1.mrdPos = self.mrdPos
            sub2.mrdPos = self.mrdPos
            sub3.mrdPos = self.mrdPos

            sub1.mrdNeg = mrd_neg2
            sub2.mrdNeg = 0.0
            sub3.mrdNeg = mrd_neg1

            self.mrdNegi = mrd_neg1
            self.mrdNegf = mrd_neg2            


            sub1.vrd = vvrd
            sub2.vrd = vvrd            
            sub3.vrd = vvrd
            self.vrd = vvrd
                        
            sub1.wefCurta = self.wefCurta
            sub2.wefCurta = self.wefCurta
            sub3.wefCurta = self.wefCurta
            self.wefCurta = self.wefCurta
            
            sub1.wefLonga = self.wefLonga
            sub2.wefLonga = self.wefLonga
            sub3.wefLonga = self.wefLonga
            self.wefLonga = self.wefLonga

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
        self.ylnp = 0
        self.tetau = 0

        self.k1 = 0
        self.k2 = 0

        self.befPos = 0
        self.befNeg = 0
        
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
    

    def rigidez(self, i):
        ei = self.e * i
        vao = self.vao
        k1 = self.k1
        k2 = self.k2
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
