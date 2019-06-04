## rotina de dimensionamentos de vigas mistas semi continuas, conforme NBR 8800
import propriedades_perfil_i as prop
from propriedades_perfil_i import wx, i_x, area, i_y, ycg, j_
from math import ceil

import vm_db as datab
import vm_db_gerais as datab_g
import vm_db_relatorio as db_relatorio


data_b = r'vmsc.db'

dbg = r'vmsc_g.db'
db_rel = r'vmsc_relatorio.db'

#TODO concluir verificações

interacao = 0.75
G = 77.0 * (10 ** 8)

Qrd = 70.7
# fub ASTM A325 fu = 825 MPa
# fub ASTM A490 fu = 1025 MPa
fub = 82.5 # resistencia a ruptura do aço dos parafusos [kN/cm2]
fu1 = fu2 = 46.0 # resistencia a ruptura do aço das cantoneiras kN/cm2
db = 19.05 # diametro dos parafusos [mm]

#  cantoneira laminada de alma => 2" b=50.8mm  t=6.35mm  y=4.74kg/m
#  cantoneira laminada de alma => 3" b=76.2mm  t=6.35mm  y=7.29kg/m

#  cantoneira laminada de base => 5" b=127.0mm  t=7.94mm  y=15.31kg/m
#  cantoneira laminada de base => 6" b=152.4mm  t=9.52mm  y=22.2kg/m


tp1 = tp2 = 9.5  #  9.5 # espessura das cantoneiras inferiores
tps = 6.35  # espessura das cantoneiras de alma

##def calculo_C(Es, E, Asl, bitola, fck, fy, fys, ha, d, bfs, bfi, tw, tfs, tfi, hdeck, vao, vaoad, largura_influencia):
def calculo_C(tramo, vaoad, lado):
    L = 200.    # comprimento de referencia para levar em conta o efeito do concreto
                # que envolve a armadura, podendo ser tomado igual a 200 mm
                # sendo que a distancia do primeiro conector ate a face e ate o centro do elemento de apoio
                # nao podem ser inferiores a 100 e 200mm, respectivamente
    relatorio = ""
    ## aa = area de aço do perfil metalico [cm2]
    ## ia = inercia do perfil metalico [cm4]
    ## ea = E = Modulo de elasticidade do perfil metalico [kN/cm2]
    ## ycg_laje = altura do centro geometrico da laje [cm]
    ## tc = altura concreto laje steeldeck [cm]
    ## nl = numero de linhas de parafusos
    ## db = diametro dos parafusos
    ## fu1 = fu2 = resistencia a ruptura do aço das cantoneiras kN/cm2
    ## fub = resistencia a ruptura do aço dos parafusos
    ## dm =  diametro de referencia tomado 16mm NBR 8800
    ## tp1 = tp2 = espessura das cantoneiras
    ## Qrd = resistencia de cada conector
    ## n = numero de conectores
    ## kr = definido no capitulo 2 do manual
    ## S = espaçamento entre parafusos na direção da força    
       
    ## Parametros pegos no objeto TRAMO
    hdeck = tramo.hdeck
    largura_influencia = tramo.b_inf
    Asl = tramo.asl
    bitola = tramo.bitola
    
    fck = tramo.fck
    fy = tramo.fy
    fys = tramo.fys

    ha = tramo.ha
        
    d = tramo.d
    bfs = tramo.bfs
    bfi = tramo.bfi
    tfs = tramo.tfs
    tfi = tramo.tfi
    tw = tramo.tw
    
    area_perfil = tramo.aa
    ia = tramo.ia  ## round(prop.i_x(d, tw, bfs, tfs, bfi, tfi), 2)    
    wa = tramo.wa  # wa = round(prop.wx(ia, tramo.d))
    
    Es = tramo.es / 10000.0  # Es / 10000
    E = tramo.e / 10000.0  # E / 10000
    vao = tramo.vao * 100 ##  *= 100

    relatorio += "\nParametros do Tramo em analise\n"
    relatorio += "hdeck   =   {}  [mm]\n".format(hdeck)
    relatorio += "largura influencia = {} [m]\n".format( largura_influencia)
    relatorio += "Asl     =   {}  [cm2]\n".format(Asl)
    relatorio += "bitola  =   {}  [cm]\n".format(bitola)
    relatorio += "fck     =   {}  [kN/cm2];\n".format(fck)
    relatorio += "fy      =   {}  [kN/cm2];\n".format(fy)
    relatorio += "fys     =   {}  [kN/cm2];\n".format(fys)
    relatorio += "Ap      =   {}  [cm2];\n".format(area_perfil)
    relatorio += "ia      =   {}  [cm4];\n".format(ia)
    relatorio += "wa      =   {}  [cm3];\n".format(wa)
    relatorio += "Es      =   {}  [kN/cm2];\n".format(Es)
    relatorio += "E       =   {}  [kN/cm2];\n".format(E)
    relatorio += "vão     =   {}  [m];\n".format(vao)

    relatorio += "O comprimento de referencia (L) para levar em conta o efeito do concreto"
    relatorio += " que envolve a armadura, podendo ser tomado igual a 200 mm"
    relatorio += " sendo que a distancia do primeiro conector ate a face e ate o centro do elemento de apoio"
    relatorio += " nao podem ser inferiores a 100 e 200mm, respectivamente. "
    relatorio += "L = 200\n"
 
    ###################################
    
    vaoad *= 100
    largura_influencia *= 100
    ea = E
    ycg_laje = 7.5 + (hdeck - 75) * .05 # altura do centro geometrico da laje
    tc = (hdeck - 75) / 10 #6.5 # altura concreto laje steeldeck
    ds = y_laje = d * .5 + ycg_laje
  
    relatorio += "tc = (hdeck - 75mm) / 10 = {}\n".format(tc)
    relatorio += "ycg_laje = 7.5 + (tc / 2) = {}\n".format(ycg_laje)
    relatorio += "ds = y_laje = d / 2 + ycg_laje = {}\n".format(ds)
    
    #####################################
    ##### PARAMTROS DE DEFINIÇÃO PARA O KI
    nl = 2 # numero de linhas de parafusos
    db = 19.05 # diametro dos parafusos - [mm]

    dm = 16 # mm  - diametro de referencia tomado 16mm NBR 8800
    S = 75  # espaçamento entre parafusos na direção da força
    relatorio += "\nParametros de definição para KI\n"
    relatorio += "nl = 2; numero de linhas de parafusos\n"
    relatorio += "db = 19.05; diametro dos parafusos - [mm]\n"
    relatorio += "dm = 16; mm  - diametro de referencia tomado 16mm NBR 8800\n"
    relatorio += "S  = 75; espaçamento entre parafusos na direção da força\n"
    #######################################

    ##### PARAMTROS DE DEFINIÇÃO PARA O KCS
    # O.2.4.1.2  NBR8800-2008
    tds = Asl * fys / 1.15
    rrcd = 0.85 * fck * tc * largura_influencia / 1.4
    fhrd = min(rrcd, tds) * interacao
    
##    Qrd = 70.7 # resistencia de cada conector #3/4
    n = round(fhrd / Qrd,0) #  numero de conectores)
##    print('n   ',  n)
    kr = 1000. #  definido no capitulo 2 do manual
 
    relatorio += "\nParametros de definição para KCS\n"
    relatorio += "Item O.2.4.1.2 da NBR8800-2008:\n"
    relatorio += "tds = Asl * fys / 1.15 = {}\n".format(round(tds,2))
    relatorio += "n   = tds / Qrd = {} (Calculo de numero de conectores)\n".format(n)
    relatorio += "kr  = 1000 (valor pre-definido)\n"
    #######################################

    ##### PARAMTROS DE DEFINIÇÃO PARA O KS
    h = d + ycg_laje

    # Capacidade de deformação
    Bt = 0.4
    sigma0 = 0.8
    fctm = 0.3 * (fck * 10) ** (2. / 3.) / 10 # kN/cm2
    Ec = 4760 * ((10 * fck) ** 0.5) / 10. # kN/cm2
    RzE = E / Ec

    esu = 0.08   #  8% rpedefinido

    relatorio += "\n Parametros de Definição para o KS\nCapacidade de deformação.\n"
    relatorio += "Bt     = {};\n".format(Bt)
    relatorio += "sigma0 = {};\n".format(sigma0)
    relatorio += "fctm = 0.3 * (fck[MPa]) ^ (2/3) = {}\n".format(round(fctm,2))
    relatorio += "Ec  = 4760 * (fck[MPa]) ^ (1/2) = {}\n".format(Ec)
    relatorio += "RzE = E / Ec = {}\n".format(round(RzE,2))
 
    #######################################
    #regiao momento negativo
    # Conforme Item O.2.2.2.b NBR 8800-2008
    largura_efetiva = min((vao / 4 + vaoad / 4) * 2 / 8., largura_influencia)

    # rigidez inicial das barras de amradura da laje de steel deck
    # NBR8800 - R.2.3.1
    ks = 2 * Asl * Es / ha

    relatorio += "\nRigidez inicial das barras de amradura da laje de steel deck\n"
    relatorio += "Conforme Item R.2.3.1 da NBR8800-2008\n"
    relatorio += "ks = 2 * Asl * Es / ha = {};\n".format(ks)
    
    ###
    ############################################################
    # Definição do centro de geometria da seção transformada, para capacidade de deformação
    largura_transformada = largura_efetiva / RzE

    area_transformada = largura_transformada * tc

    Ay = area_transformada * y_laje

    yg = Ay / (area_perfil + area_transformada)
    y0 = d * .5 - yg + ycg_laje

    relatorio += "\nNa região de Momento Negativo.\nConforme Item O.2.2.2.b NBR 8800-2008\n"
    relatorio += "largura efetiva = menor valor entre: \n\t(vão + vão adjacente)/4 * 2/8 ;\n\tlargura de influência = {}\n".format(largura_efetiva)
    relatorio += "Definição do centro de geometria da seção transformada, para capacidade de deformação\n"
    relatorio += "largura transformada = largura efetiva / RzE = {}\n".format(round(largura_transformada,2))
    relatorio += "area transformada = largura transformada * tc = {}\n".format(round(area_transformada,2))
    relatorio += "Ay = area transformada * y_laje = {}\n".format(round(Ay,2))
    relatorio += "yg = Ay / (Ap + area transformada) = {}\n".format(round(yg,2))
    relatorio += "y0 = d/2 - yg + ycg_laje = {}\n".format(round(y0,2))
     
    # capacidade de deformação das barras da armadura
    # R.2.3.3
    # esm deformação da armadura envolvida pelo concreto
    # dus - capacidade de alongamento das barras de armadura
    # NBR8800 - R.2.3.3
    rho = Asl / (largura_efetiva * tc - Asl)
    kc = min(1 / (1 + tc / (2 * y0)) + 0.3 ,1.)

    desr = fctm * kc / ( rho * Es)
    teta_srl = (fctm * kc / rho) * (1 + rho * Es / Ec)
    esy = fys / Es
    
    esmu = esy - Bt*desr + sigma0 * (1 - teta_srl/fys) * (esu - esy)
    dus = L * esmu

    relatorio += "\nCapacidade de deformação das barras da armadura\n"
    relatorio += "Conforme Item R.2.3.3 da NBR8800-2008\n"
    relatorio += "esm deformação da armadura envolvida pelo concreto\n"
    relatorio += "dus - capacidade de alongamento das barras de armadura\n"

    relatorio += "rho = Asl / (largura efetiva * tc - Asl) = {}\n".format(round(rho,6))
    relatorio += "desr = fctm * kc / ( rho * Es) = {}\n".format(round(desr,6))
    relatorio += "teta_srl = (fctm * kc / rho) * (1 + rho * Es / Ec) = {}\n".format(round(teta_srl,4))
    relatorio += "esy = fys / Es = {}\n".format(round(esy,6))
    relatorio += "esmu = esy - Bt*desr + sigma0 * (1 - teta_srl/fys) * (esu - esy) = {}\n".format(round(esmu,6))
    relatorio += "dus = L * esmu = {}\n".format(round(dus,4))
 
    ##################################################

##    ds = 25.5
##    n = 3
    ## definição do kcS
##    rdArmaduras = tds = Asl * fys / 1.15    
    nqrd = round(n * round(Qrd,2),2)
        
    if (round(tds,2)) / (nqrd) > 1.03:
        n += 1
    
    Ll = .15 * vao
    # print('numero de conectores  %d' % n)

    ee = ia / (Asl * (ds ** 2))
    vv = ((ee + 1)* n *kr * 1 * Ll*(ds**2) / (ea*ia)) ** (.5)
    alpha = vv - (vv - 1)*(d + ycg_laje) / ((ds * (ee + 1)))

    kcs = n * kr / alpha

    relatorio += "\nDefiniçao do KCS:\n"
    relatorio += "Rd armaduras = tds = Asl * fys / 1.15\n".format()
    relatorio += "nqrd = n * Qrd = {}\n".format(nqrd)
    relatorio += "ee = ia / (Asl * (ds ** 2)) = {}\n".format(round(ee,2))
    relatorio += "vv = ((ee + 1)* n * kr * 1 * Ll*(ds^2) / (ea*ia)) ^ (1/2) = {}\n".format(round(vv,2))
    relatorio += "alpha = vv - (vv - 1)*(d + ycg_laje) / ((ds * (ee + 1))) = {}\n".format(round(alpha,2))
    relatorio += "kcs = n * kr / alpha  =  {}\n".format(round(kcs,2))
    
    #################
    # capacidade de deformação dos conectores de cisalhamento
    # sb - capacidade de escorregamento associada a deformação dos conectores
    # NBR8800 - R.2.4.3
    sa = 0.7 * 1.25 * Qrd / kr
    fsb = fys * Asl
    fsa = kcs * sa

    sb = 2 * sa * fsb / fsa # retornado em cm

    relatorio += "\nCapacidade de deformação dos conectores de cisalhamento\n"
    relatorio += "sb - capacidade de escorregamento associada a deformação dos conectores\n"
    relatorio += "Conforme Item R.2.4.3 da NBR8800-2008:\n"
    relatorio += "sa = 0.7 * 1.25 * Qrd / kr = {}\n".format(round(sa,4))
    relatorio += "fsb = fys * Asl = {}\n".format(round(fsb,2))
    relatorio += "fsa = kcs * sa  = {}\n".format(round(fsa,2))
    relatorio += "sb = 2 * sa * fsb / fsa = {}; em cm\n".format(round(sb,4))
 
    ##################################################
    ##################################################
    
    ###################
    # rigidez inicial da ligação parafusada
    # NBR8800 - R.2.5.2

    ks2 = min(S / (4 * db) + 0.375, 1.25)
    kt1 = min(1.5 * tp1 / dm, 2.5)
    kt2 = min(1.5 * tp2 / dm, 2.5)

    kp1 = 24 * ks2 * kt1 * db/10 * fu1
    kp2 = 24 * ks2 * kt2 * db/10 * fu2
    kb = 16 * fub * (db/10) ** 2 / (dm/10)
    ki = nl / ( 1 / kp1 + 1 / kp2 + 1 / kb)

    C1 = round(h ** 2 / (1. / ks + 1. / kcs + 1. / ki), 2)

    relatorio += "\nRigidez inicial da ligação parafusada\n"
    relatorio += "Conforme Item R.2.5.2 da NBR8800-2008:\n"

    relatorio += "ks2 = Menor valor entre: (S / (4 * db) + 0.375) ;  (1.25) = {}\n".format(round(ks2,3))
    relatorio += "kt1 = Menor valor entre: (1.5 * tp1 / dm) ;  (2.5) = {}\n".format(round(kt1,3))
    relatorio += "kt2 = Menor valor entre: (1.5 * tp2 / dm) ;  (2.5) = {}\n".format(round(kt2,3))

    relatorio += "kp1 = 24 * ks2 * kt1 * db/10 * fu1 = {}\n".format(round(kp1,3))
    relatorio += "kp2 = 24 * ks2 * kt2 * db/10 * fu2 = {}\n".format(round(kp2,3))
    relatorio += "kb = 16 * fub * (db/10) ** 2 / (dm/10) = {}\n".format(round(kb,3))
    relatorio += "ki = nl / ( 1 / kp1 + 1 / kp2 + 1 / kb) = {}\n".format(round(ki,3))

    relatorio += "C1 = h^2 / (1. / ks + 1. / kcs + 1. / ki = {} kN/rad\n".format(round(C1,3))
    
    ## capacidade de rotação, sem perda de resistencia na ligação
    ## para calculo do tetau - valores precisam estar em mm
    ## tetau retornado em radianos
    ## dui - capacidade de desolcamento da ligação inferior
    ## NBR8800 - R.2.5.2.2.3 - para ligação soldadas, capacidade dui = 0
    ## NBR8800 - R.2.5.2.3.3 - limite deslocamento horizontal da extremidade da mesa inferior dui = 3mm
    dui = 3
    tetau = round(( dus + dui + sb * 10) / ( h * 10 ), 8)*1.1
    ## converter radianos para m.rad
    tetau *=1000

    ## posição da linha neutra plastica ylnp
    ## a partir da face inferior da viga
    afs = bfs * tfs
    afi = tfi * bfi
    hw = d - tfs - tfi
    
    # linha neutra plastica DA LIGAÇÂO
    ylnp = round((h*10 ) * dui / ( dus + dui + sb*10), 2) ## valor em mm

    relatorio += "\nCapacidade de rotação, sem perda de resistencia na ligação.\n"
    relatorio += "Para o calculo do tetau, os valores precisam estar em mm. Tetau é retornado em radianos\n"
    relatorio += "dui - capacidade de desolcamento da ligação inferior\n"

    relatorio += "Item R.2.5.2.2.3 da NBR8800/2008 - para ligação soldadas, capacidade dui = 0\n"
    relatorio += "Item R.2.5.2.3.3 da NBR8800/2008  - limite deslocamento horizontal da extremidade da mesa inferior dui = 3mm\n"
    
    relatorio += "tetau = ( dus + dui + sb * 10) / ( h * 10 ) * 1.1\n"
    ## converter radianos para m.rad
    relatorio += "tetau = {}; Em radianos\n".format(round(tetau,2))

    relatorio += "afs = bfs * tfs = {}\n".format(round(afs,2))
    relatorio += "afi = tfi * bfi = {}\n".format(round(afi,2))
    relatorio += "hw = d - tfs - tfi = {}\n".format(round(hw,2))
    
    relatorio += "Posição da linha neutra plastica da Ligação, valor a partir da face inferior da viga:\n "  
    relatorio += "ylnp = (h*10) * dui / ( dus + dui + sb*10) = {} ; valor em mm\n".format(round(ylnp,2))

##    ###########################################
##    # Armadura Minima para tração sob deformações impostas
##    tst = min(810 * (0.3**.5) * ( (3**(2/3))/(bitola*10))**.5, fys*10)
##    Asss = 0.8 * 0.9 * ks
    
    #Calculo da linha neutra do perfil
    x1 = (afi * fy / 1.1 - tds - afs * fy / 1.1 + hw*tw*fy/1.1) / (2*tw*fy/1.1)

    mrd_neg = 0
    yp = x1 #/ 10.
    d3 = hwt = d4 = hwc = aac = d5 = aat = 0
    
    relatorio += "\nCalculo da linha neutra do perfil\n"
    relatorio += "linha neutra = (afi * fy / 1.1 - tds - afs * fy / 1.1 + hw*tw*fy/1.1) / (2*tw*fy/1.1)\nlinha neutra = {} mm\n".format(round(x1,2))

    if (yp) >= tfs and (yp) <= (d - tfi): # linha neutra na alma do perfil
##        print('Linha neutra na alma do perfil')
        d3 = d - x1 + 7.5 + 3.5  # 3,5 cm cobrimento armaduras negativas - braço das barras de reforço

        hwt = yp - tfs # dimensão tracionada da alma
        aat = bfs*tfs + hwt*tw  # area tracionada do perfil
        d4 = ((bfs*tfs*(yp-tfs/2.)) + (hwt*tw*(hwt/2.)))/aat  # braço da area tracionada do perfil

        hwc = d - tfi - yp  # dimensao comprimida da alma
        aac = (bfi*tfi) + (hwc *tw)  # area comprimida do perfil metalico
        d5 = ((bfi*tfi*(d-tfi/2.-yp)) + (hwc*tw)*(d-tfi-yp)*.5)/aac  # braço da area comprimida do perfil

        relatorio += "linha neutra na alma do perfil\n"

    elif yp < tfs: # linha neutra na mesa superior do perfil
##        print('Linha neutra na mesa superior')
        d3 = d - x1 + 7.5 + 3.5  # 3,5 cm cobrimento armaduras negativas - braço das barras de reforço

        hwt = yp  # dimensão tracionada da alma
        aat = bfs*hwt  # area tracionada do perfil
        d4 = yp  # braço da area tracionada do perfil

        hwc = d - tfi - tfs  # dimensao comprimida da alma
        aac = (bfi*tfi) + (hwc *tw) + (bfs*(tfs-yp))  # area comprimida do perfil metalico
        d5 = ((bfi*tfi*(d-tfi/2.+tfs-yp)) + (hwc*tw)*(hwc/2.+tfs-yp)*.5 + (bfs*(tfs-yp)*(tfs-yp)/2.))/aac

        relatorio += "linha neutra na mesa superior do perfil\n"

    # O.2.4.1.3 NBR8800-2008
    if d3 != 0 :
        mrd_neg = tds * d3 + aat*fy/1.25*d4 + aac*fy*d5/1.25
        mrd_neg_k = tds * d3 + aat*fy/1*d4 + aac*fy*d5/1
    else:
        mrd_neg = 1
        mrd_neg_k = 1

    relatorio += "Conforme O.2.4.1.3 da NBR8800-2008\n"
    relatorio += "Valores calculados para definição do momento negativo resistente:\n d3 = {}; d4 = {}; d5 = {}; aat = {}; aac = {}\n".format(round(d3,2),
                                                                                                round(d4,2),
                                                                                                round(d5,2),
                                                                                                round(aat,2),
                                                                                                round(aac,2))
    relatorio += "mrd_neg   = tds * d3 + aat*fy/1.25*d4 + aac*fy*d5/1.25  = {}\n".format(round(mrd_neg,2))
    relatorio += "mrd_neg_k = tds * d3 + aat*fy/1*d4    + aac*fy*d5/1 = {}\n".format(round(mrd_neg_k,2))

    if lado == "esquerdo":
        db_relatorio.insert_data(db_rel, 'Calculo do C', "{}esquerdo".format(tramo.n), relatorio)
    else:
        db_relatorio.insert_data(db_rel, 'Calculo do C', "{}direito".format(tramo.n), relatorio)

    return (C1, tetau, ylnp, x1, mrd_neg, mrd_neg_k, n)


##def inercia_equivalente_curta(vao, largura_efetiva_pos, le, hdeck, d, tw, bfs,bfi, tfs,tfi, ia, aa, fck, fy, E):
def inercia_equivalente_curta(tramo, le):
    ## Parametros pegos no objeto TRAMO
    relatorio = ""
    hdeck = tramo.hdeck
    largura_influencia = tramo.b_inf # [m]
    largura_efetiva_pos = tramo.befPos1
    
    Asl = tramo.asl
    bitola = tramo.bitola
    
    fck = tramo.fck
    fy = tramo.fy
    fys = tramo.fys

    ha = tramo.ha
        
    d = tramo.d
    bfs = tramo.bfs
    bfi = tramo.bfi
    tfs = tramo.tfs
    tfi = tramo.tfi
    tw = tramo.tw
    
    area_perfil = aa = tramo.aa
    ia = tramo.ia  ## round(prop.i_x(d, tw, bfs, tfs, bfi, tfi), 2)    
    wa = tramo.wa  # wa = round(prop.wx(ia, tramo.d))
    
    Es = tramo.es / 10000.0  # Es / 10000
    E = tramo.e / 10000.0  # E / 10000
    vao = tramo.vao # [m]

    relatorio += "\nParametros do Tramo em analise\n"
    relatorio += "hdeck  =   {}  [mm] \t\t largura influencia = {} [m]\n".format(hdeck, largura_influencia)
    relatorio += "Asl    =   {}  [cm2]\t\t bitola             = {} [cm]\n".format(round(Asl,2), bitola)
    relatorio += "Ap   =  {} [cm2]   ; ia  =  {} [cm4];\n".format(round(area_perfil,2),round(ia,2))
    relatorio += "wa   =  {} [cm3];\n".format(round(wa,2))
    relatorio += "Es   =  {} [kN/cm2]; E   =  {} [kN/cm2]\n".format(Es,E)
    relatorio += "vão  =  {} [m];\n".format(vao)
    #####
    # print('inercia curta')

    vao *= 100 # para cm
    largura_efetiva_pos *= 100 # para cm

    ycg_laje = 7.5 + (hdeck - 75) * .05 # altura do centro geometrico da laje
    tc = (hdeck - 75) / 10 #6.5 # altura concreto laje steeldeck
    ds = y_laje = d * .5 + ycg_laje
    Ec = 4760 * ((10 * fck) ** 0.5) / 10. # kN/cm2
    RzE = E / (Ec)

    relatorio += "tc = (hdeck - 75mm) / 10 = {}\n".format(tc)
    relatorio += "ycg_laje = 7.5 + (tc / 2) = {}\n".format(round(ycg_laje,2))
    relatorio += "ds = y_laje = d / 2 + ycg_laje = {}\n".format(ds)
    relatorio += "Ec  = 4760 * (fck[MPa]) ^ (1/2) = {}\n".format(Ec)
    relatorio += "RzE = E / Ec = {}\n".format(round(RzE,2))

    ## regiao momento positivo Curta Duração
    largura_transformada = largura_efetiva_pos / RzE
    area_transformada = largura_transformada * tc
    inercia_laje_transformada = (largura_transformada) * tc ** 3 / 12.

    ay_pos = area_transformada * ds
    ay2_pos = area_transformada * ds ** 2

    relatorio += "\nRegiao momento positivo - Curta Duração\n"
    relatorio += "largura efetiva positiva =  {}\n".format(largura_efetiva_pos)
    relatorio += "Definição do centro de geometria da seção transformada\n"
    relatorio += "largura transformada = largura efetiva / RzE = {}\n".format(round(largura_transformada,2))
    relatorio += "area transformada = largura transformada * tc = {}\n".format(round(area_transformada,2))
    relatorio += "Ay = area transformada * y_laje = {}\n".format(round(ay_pos,2))
    relatorio += "Ay2 = area transformada * y_laje^2 = {}\n".format(round(ay2_pos,2))

##    relatorio += "yg = Ay / (Ap + area transformada) = {}\n".format(round(yg,2))
##    relatorio += "y0 = d/2 - yg + ycg_laje = {}\n".format(round(y0,2))

    fhrd = min(0.85 * fck * largura_efetiva_pos * tc / 1.4, aa * fy / 1.1)
    cd = round(fhrd * interacao / (Qrd), 0) * Qrd
    nn = cd / fhrd

    relatorio += "fhrd = minimo entre:\n\t(0.85 * fck * largura_efetiva_pos * tc / 1.4)\n\t(aa * fy / 1.1)\nfhrd = {}\n".format(round(fhrd,2))
    relatorio += "interacao da ligação = {}\n".format(interacao)
    relatorio += "cd = fhrd * interacao / Qrd) * Qrd = {}\n".format(round(cd,2))
    relatorio += "nn = cd / fhrd= {} (Numero de conectores entre a seção de momento nulo e a seção de maior momento positivo)\n".format(round(nn,2))

    # grau de interação pela NBR 8800 O.2.3.1.1.2
    if bfs != bfi or tfs != tfi:
        # O.2.3.1.1.2.b
        ni = max(1 - (E / (578*fy))*(0.3 - 0.015 * le), .4) # le em metros
    else:
        # O.2.3.1.1.2.a
        ni = max(1 - (E / (578*fy))*(0.75 - 0.03 * le), .4)

    relatorio += "\nGrau de interação pela NBR 8800 O.2.3.1.1.2\n"
    relatorio += "O.2.3.1.1.2.a\n maior entre: 1 - (E / (578*fy))*(0.75 - 0.03 * le) ; 0.4\n"
    relatorio += "O.2.3.1.1.2.b\n maior entre: 1 - (E / (578*fy))*(0.3 - 0.015 * le) ; 0.4\n"
    relatorio += "ni = {} \n".format(round(ni,3))

##    nn = ni
    
    ## Calculo do Momento Fletor Resistente    
    ## NBR8800 - O.2.3.c
    hw = d - tfs - tfi
    cad = 0.5 * (aa*fy/1.1 - cd)
    tad = cd + cad
    yp = yt = yc = 0
    af = tfs*bfs
    aw = hw*tw

    # O.2.3.1.1.1.b
    if cad <= (af*fy/1.1):
        yp = (cad / (af * fy / 1.1 ))* tfs
    elif cad > (af*fy/1.1):
        yp = tfs + hw*((cad-af*fy/1.1) / (aw*fy/1.1))

    relatorio += "\nCalculo do Momento Fletor Resistente\n"
    relatorio += "Conforme Item O.2.3.c da NBR8800/2008\n"
    relatorio += "hw = d - tfs - tfi = {} \n".format(round(hw,2))
    relatorio += "cad = 0.5 * (aa*fy/1.1 - cd) = {} \n".format(round(cad,2))
    relatorio += "tad = cd + cad = {} \n".format(round(tad,2))
    relatorio += "af = tfs*bfs = {} \n".format(round(af,2))
    relatorio += "aw = hw*tw = {} \n".format(round(aw,2))

    relatorio += "\nConforme Item O.2.3.1.1.1.b\n"
    relatorio += "Caso cad <= (af*fy/1.1) .: yp = (cad / (af * fy / 1.1 ))* tfs\n"
    relatorio += "Caso cad > (af*fy/1.1) .: yp = tfs + hw*((cad-af*fy/1.1) / (aw*fy/1.1))\n"
    relatorio += "yp = {}\n".format(round(yp,2))

    # centro geometrico da regiao tracionada do perfil de aço
    afi = bfi*tfi
    a = cd / (0.85 * fck * largura_efetiva_pos / 1.4)
    if yp >= tfs: # linha neutra na alma do perfil
        relatorio += "\nLinha neutra na alma do perfil .: yp >= tfs\n"
        hwt = (d - yp - tfi)
        awt = hwt*tw
        
        yt =  ((afi * tfi * .5) + (awt * (hwt * .5+tfi))) / (afi + awt)
        hwc = yp-tfs
        awc = hwc * tw
        yc =  ((af * tfs * .5) + (awc * (hwc * .5+tfs))) / (af + awc)

    elif yp < tfs: # linha neutra na mesa superior do perfil
        relatorio += "\nLinha neutra na mesa superior do perfil .: yp < tfs\n"
        afs = bfs * (tfs-yp)
        yt =  ((afi*tfi*.5) +      #mesa inferior
               (aw*(hw*.5+tfi)) +  #alma
               afs*((tfs-yp)*.5+hw*.5+tfi)) / (afi + aw + afs) #mesa superior
               
        yc =  yp

    relatorio += "yc = {}\n".format(round(yc,2))
    # O.2.3.1.1.1.c
    mrd_pos = 0.95 * (cad * ( d - yt -yc) + cd * (tc - a/2.+7.5+d-yt))    

    wa = round(prop.wx(ia,d))
  
    areatotal_pos = area_transformada + aa
    yg = ay_pos / areatotal_pos
    inercia_total_pos = ia + inercia_laje_transformada
    itr = ay2_pos + inercia_total_pos - areatotal_pos * (yg) ** 2
    ief_pos_curta = round(ia + (itr - ia) * ((nn) ** .5), 2)
    
    wtr = itr / ((yg) + d/2.)
    wef = round(wa + (wtr - wa) * ((nn) ** .5), 2)

    relatorio +="\nConforme Item O.2.3.1.1.1.c da NBR 8800/2008\n"
    relatorio += "mrd_pos = 0.95 * (cad * ( d - yt -yc) + cd * (tc - a/2.+7.5+d-yt))   = {}\n".format(round(yp,2))  

    relatorio += "wa = round(prop.wx(ia,d)) = {}\n".format(round(yp,2))
  
    relatorio += "areatotal_pos = area_transformada + aa = {}\n".format(round(areatotal_pos,2))
    relatorio += "yg = ay_pos / areatotal_pos= {}\n".format(round(yg,2))
    relatorio += "inercia_total_pos = ia + inercia_laje_transformada = {}\n".format(round(inercia_total_pos,2))
    relatorio += "itr = ay2_pos + inercia_total_pos - areatotal_pos * (yg) ^ 2 = {}\n".format(round(itr,2))
    relatorio += "ief_pos_curta = ia + (itr - ia) * ((nn) ^ .5) = {}\n".format(round(ief_pos_curta,2))
    
    relatorio += "wtr = itr / ((yg) + d/2.) = {}\n".format(round(wtr,2))
    relatorio += "wef = wa + (wtr - wa) * ((nn) ^ .5) = {}\n".format(round(wef,2))

    db_relatorio.insert_data(db_rel, 'Equivalente Curta', "{}".format(tramo.n), relatorio)

##    print('\nCURTA DURAÇÂO')
##    print('largura_efetiva_pos' , largura_efetiva_pos)
##    print('le' , le)
##    print('largura_transformada' , largura_transformada)
##    print('area_transformada' , area_transformada)
##    print('aa' ,aa)
##    print('areatotal_pos' ,areatotal_pos)
##    print('ay_pos' ,ay_pos)    
##    print('ay2_pos' ,ay2_pos)    
##    
##    print('yg' ,yg)
##    print('inercia_total_pos' ,inercia_total_pos)
##    
##    # ni = max(1 - (E / (578*fy))*(0.75 - 0.03 * le), .4)
##    #inercia_laje_transformada = largura_transformada * tc ** 3 / 12.
##    print('tc' ,tc)
##    print('inercia_laje_transformada' ,inercia_laje_transformada)
##    print('areatotal_pos * yg ** 2' ,areatotal_pos * yg ** 2)
##    print('ia' ,ia)
##    print('itr' ,itr)
##    print('nn' ,nn)
##    print('cd' ,cd)
##    print('fhrd' ,fhrd)
##    print('ief_pos_curta' ,ief_pos_curta)
##    print('wa' ,wa)
##    print('wtr' ,wtr)
##    print('wef' ,wef)
    
##    print('\n')
    ## Pagina 33
    tramo.nn = nn

    tramo.iefPosCurta = ief_pos_curta * (100**-4)
    tramo.mrdPos = mrd_pos
    tramo.wefCurta1 = tramo.wefCurta2 = wef * (100 ** -3)
    tramo.wefCurta =  wef * (100 ** -3)
    
##    return ief_pos_curta, mrd_pos, wef


#def inercia_equivalente_longa(vao, largura_efetiva_pos, le, hdeck, d, tw, bfs,bfi, tfs,tfi, Asl, ia, aa, fck, fy, E):
def inercia_equivalente_longa(tramo, le):
    ## Parametros pegos no objeto TRAMO
    hdeck = tramo.hdeck
    largura_influencia = tramo.b_inf # [m]
    largura_efetiva_pos = tramo.befPos1
    
    Asl = tramo.asl
    bitola = tramo.bitola
    
    fck = tramo.fck
    fy = tramo.fy
    fys = tramo.fys

    ha = tramo.ha
        
    d = tramo.d
    bfs = tramo.bfs
    bfi = tramo.bfi
    tfs = tramo.tfs
    tfi = tramo.tfi
    tw = tramo.tw
    
    area_perfil = aa = tramo.aa
    ia = tramo.ia  ## round(prop.i_x(d, tw, bfs, tfs, bfi, tfi), 2)    
    wa = tramo.wa  # wa = round(prop.wx(ia, tramo.d))
    
    Es = tramo.es / 10000.0  # Es / 10000
    E = tramo.e / 10000.0  # E / 10000
    vao = tramo.vao # [m]

    relatorio = ""

    relatorio += "\nParametros do Tramo em analise\n"
    relatorio += "hdeck  =   {}  [mm] \t\t largura influencia = {} [m]\n".format(hdeck, largura_influencia)
    relatorio += "Asl    =   {}  [cm2]\t\t bitola             = {} [cm]\n".format(round(Asl,2), bitola)
    relatorio += "Ap   =  {} [cm2]   ; ia  =  {} [cm4];\n".format(round(area_perfil,2),round(ia,2))
    relatorio += "wa   =  {} [cm3];\n".format(round(wa,2))
    relatorio += "Es   =  {} [kN/cm2]; E   =  {} [kN/cm2]\n".format(round(Es,2),E)
    relatorio += "vão  =  {} [m];\n".format(vao)
    #################################################################
    
    # print('inercia longa')
    vao *= 100
    largura_efetiva_pos *= 100

    ycg_laje = 7.5 + (hdeck - 75) * .05 # altura do centro geometrico da laje
    tc = (hdeck - 75) / 10 #6.5 # altura concreto laje steeldeck
    ds = y_laje = d * .5 + ycg_laje
    Ec = 4760 * ((10 * fck) ** 0.5) / 10. # kN/cm2
    RzE2 = E / (Ec/3)

    relatorio += "tc = (hdeck - 75mm) / 10 = {}\n".format(tc)
    relatorio += "ycg_laje = 7.5 + (tc / 2) = {}\n".format(round(ycg_laje,2))
    relatorio += "ds = y_laje = d / 2 + ycg_laje = {}\n".format(ds)
    relatorio += "Ec  = 4760 * (fck[MPa]) ^ (1/2) = {}\n".format(Ec)
    relatorio += "RzE2 = E / (Ec/3) = {}\n".format(round(RzE2,2))

    ## Propriedaedes elasticas
    ## regiao momento positivo Longa Duração
    largura_transformada = largura_efetiva_pos / RzE2
    area_transformada = largura_transformada * tc
    inercia_laje_transformada = largura_transformada * tc ** 3 / 12.
    
    ay_pos = area_transformada * y_laje
    ay2_pos = area_transformada * y_laje ** 2
    
    relatorio += "\nRegiao momento positivo - Curta Duração\n"
    relatorio += "largura efetiva positiva =  {}\n".format(largura_efetiva_pos)
    relatorio += "Definição do centro de geometria da seção transformada\n"
    relatorio += "largura transformada = largura efetiva / RzE2 = {}\n".format(round(largura_transformada,2))
    relatorio += "area transformada = largura transformada * tc = {}\n".format(round(area_transformada,2))
    relatorio += "Ay = area transformada * y_laje = {}\n".format(round(ay_pos,2))
    relatorio += "Ay2 = area transformada * y_laje^2 = {}\n".format(round(ay2_pos,2))

    fhrd = min(0.85 * fck * largura_efetiva_pos * tc / 1.4, aa * fy / 1.1)
    cd = round(fhrd * interacao / (Qrd), 0) * Qrd
    nn = cd / fhrd # grau de interação pelo manual
    
    relatorio += "fhrd = minimo entreo:\n\t(0.85 * fck * largura_efetiva_pos * tc / 1.4)\n\t(aa * fy / 1.1)\nfhrd = {}\n".format(round(fhrd,2))
    relatorio += "cd = fhrd * interacao / Qrd) * Qrd = {}\n".format(round(cd,2))
    relatorio += "nn = cd / fhrd= {}\n".format(round(nn,2))

    # grau de interação pela NBR 8800 O.2.3.1.1.2
    if bfs != bfi or tfs != tfi:
        # O.2.3.1.1.2.b
        ni = max(1 - (E / (578*fy))*(0.3 - 0.015 * le), .4) # le em metros
    else:
        # O.2.3.1.1.2.a
        ni = max(1 - (E / (578*fy))*(0.75 - 0.03 * le), .4)

    relatorio += "\nGrau de interação pela NBR 8800 O.2.3.1.1.2\n"
    relatorio += "O.2.3.1.1.2.a\n maior entre: 1 - (E / (578*fy))*(0.75 - 0.03 * le) ; 0.4\n"
    relatorio += "O.2.3.1.1.2.b\n maior entre: 1 - (E / (578*fy))*(0.3 - 0.015 * le) ; 0.4\n"
    relatorio += "ni = {} \n".format(round(ni,3))

    wa = round(prop.wx(ia,d))
    areatotal_pos = area_transformada + aa
    yg = ay_pos / areatotal_pos

    inercia_total_pos = ia + inercia_laje_transformada
    itr = ay2_pos + inercia_total_pos - areatotal_pos * yg ** 2
    ief_pos_longa = round(ia + (itr - ia) * ((nn) ** .5), 2)
    
    wtr = itr / (yg + d/2.)
    wef = round(wa + (wtr - wa) * ((nn) ** .5), 2)

    relatorio +="\nConforme Item O.2.3.1.1.1.c da NBR 8800/2008\n"

    relatorio += "wa = round(prop.wx(ia,d)) = {}\n".format(round(wa,2))
    relatorio += "areatotal_pos = area_transformada + aa = {}\n".format(round(areatotal_pos,2))
    relatorio += "yg = ay_pos / areatotal_pos= {}\n".format(round(yg,2))
    relatorio += "inercia_total_pos = ia + inercia_laje_transformada = {}\n".format(round(inercia_total_pos,2))
    relatorio += "itr = ay2_pos + inercia_total_pos - areatotal_pos * (yg) ^ 2 = {}\n".format(round(itr,2))
    relatorio += "ief_pos_longa = ia + (itr - ia) * ((nn) ^ .5) = {}\n".format(round(ief_pos_longa,2))
    
    relatorio += "wtr = itr / ((yg) + d/2.) = {}\n".format(round(wtr,2))
    relatorio += "wef = wa + (wtr - wa) * ((nn) ^ .5) = {}\n".format(round(wef,2))

    db_relatorio.insert_data(db_rel, 'Equivalente Longa', "{}".format(tramo.n), relatorio)
##
##    print('\nLonga Duração')
##    print('largura_efetiva_pos' , largura_efetiva_pos)
##    print('le' , le)
####    print('largura_transformada' , largura_transformada)
####    print('area_transformada' , area_transformada)
####    print('aa' ,aa)
##    
##    print('ay_pos' ,ay_pos)
##    print('areatotal_pos' ,areatotal_pos)
##    
##    print('yg' ,yg)
##    
##    print('ay2_pos' ,ay2_pos)    
##    print('inercia_total_pos' ,inercia_total_pos)
##    
##    print('areatotal_pos * yg ** 2' ,areatotal_pos * yg ** 2)
##    print('itr' ,itr)
##    # ni = max(1 - (E / (578*fy))*(0.75 - 0.03 * le), .4)
##    #inercia_laje_transformada = largura_transformada * tc ** 3 / 12.
####    print('tc' ,tc)
##    print('inercia_laje_transformada' ,inercia_laje_transformada)    
##    print('ia' ,ia)    
##    print('nn' ,nn)
##    print('ief_pos_longa' ,ief_pos_longa)
##    print('wa' ,wa)
##    print('wtr' ,wtr)
##    print('wef' ,wef)
##
##    print('\n')
    ## Pagina 33
    
    tramo.iefPosLonga = ief_pos_longa * (100**-4)
    
    tramo.wefLonga1 = tramo.wefLonga2 = wef * (100 ** -3)
    tramo.wefLonga =  wef * (100 ** -3)



dtb = r'vmsc.db'

## FINALIZAR METODO DE DIMENSIONAMENTO
def verificar_tramos(lista_tramos, lista_dx_vaos, lista_cargas,
                     lista_MD_pos, lista_MD_neg,
                     lista_MCurta_pos, lista_MCurta_neg,
                     lista_MLonga_pos, lista_MLonga_neg,
                     lista_Cortantes, lista_Momentos_Zero,
                     nb, save):
##    print(lista_MD_pos)
##    print(lista_MCurta_pos)
##    print(lista_MLonga_pos)
##    print(lista_MD_neg)
##    print(lista_Cortantes)
##    print(lista_Momentos_Zero)
    retorno = []
    relatorio = ""
    
    for tramo in lista_tramos:
        relatorio = ""
        n = tramo.n
        data_return = datab.get_data(dtb, 'novo',n)
        bitola = data_return[9]        
        vao = tramo.vao
        d = tramo.d
        bfs = tramo.bfs
        bfi = tramo.bfi
        tw = tramo.tw
        tfs = tramo.tfs
        tfi = tramo.tfi
        situacao = tramo.situacao
        
        bef_pos  = min(tramo.befPos1, tramo.befPos2)
        hdeck = tramo.hdeck
        Asl = tramo.asl
        fy = tramo.fy
        fys = tramo.fys
        fck = tramo.fck
        e = tramo.e
        ylnp = tramo.ylnp           # Linha neutra do platisca da ligacao
        x1 = tramo.ylnpx1           # Linha neutra do perfil/secao

        v_poisson = 0.3
        b_inf = tramo.b_inf

        n_conectores = tramo.n_conectores
        
        tds = Asl * fys / 1.15
        hf = 7.5
        tc = (hdeck - hf*10) / 10
        Afs = bfs * tfs
        Afi = tfi * bfi
        hw = d - tfs - tfi
##        print(x1)  # esse x1
        
        x1 = ((- tds - Afs * fy / 1.1) + (Afi * fy / 1.1 + hw*tw*fy/1.1)) / (2*tw*fy/1.1)
##        print(x1)  # esta igual a este
        
        hwc = hw - x1
        
        ycg_laje = 7.5 + (hdeck - 75) * .05 # altura do centro geometrico da laje

        ycg_perfil = ycg(d, tw, bfs, tfs, bfi, tfi)
        ho = d - tfs*.5 - tfi *.5
                
        wPosLonga = tramo.wefLonga
        wPosCurta = tramo.wefCurta

        ief_neg = tramo.iefNeg
        ief_pos_curta = tramo.iefPosCurta
        ief_pos_longa = tramo.iefPosLonga

        mrdPos = tramo.mrdPos / 100   # kN.m
        mrdNegi = tramo.mrdNegi / 100 # kN.m
        mrdNegf = tramo.mrdNegf / 100 # kN.m
        mrdNegk = tramo.mrdNegk       # kN.cm

        tetaui = tramo.tetaui
        tetauf = tramo.tetauf

        befNegi = tramo.befNegi
        befNegf = tramo.befNegf
        
        xf = lista_dx_vaos[tramo.n+1]
        
        xi = xf - vao
        mg = mdlinha = 0
        for text, carr in lista_cargas:
            if text == 'g\'':
                q_glinha = carr  # carregamento antes da cura, para analise de flecha
                mg = carr * vao ** 2 / 8.  # momento antes da cura, bi-apoiada
            if text == 'd\'':
                mdlinha = carr * vao ** 2 / 8.  # momento antes da cura, bi-apoiada
            if text == 'Curta':
                q_sc = carr  # carregamento de curta duração, sobrecarga pós cura
            if text == 'Longa':
                q_longa = carr  # carregamento de longa duração, permanente pós cura
            
        # definição dos momentos solicitantes POSITIVOS para o tramo
        x_md = msd_md_pos = msd_mlonga_pos = msd_mcurta_pos = 0
        for x, momento in lista_MD_pos:
            if x >= xi and x <= xf:
                if momento > 1:
                    msd_md_pos = momento
                    x_md = x - xi
                
        for x, momento in lista_MLonga_pos:
            if x >= xi and x <= xf:
                if momento > 1:
                    msd_mlonga_pos = momento

        for x, momento in lista_MCurta_pos:
            if x >= xi and x <= xf:
                if momento > 1:
                    msd_mcurta_pos = momento
                    
        # definição do momento positivo msd_q para 3 verificação
        msd_q = 0
        for text, carr in lista_cargas:
            if text == 'd':
                q_d = carr  # carregamento antes da cura, para analise de flecha
                re_d = carr * vao / 2
                msd_q = +re_d * x_md - carr*x_md**2/2

        # Definição dos comprimentos negativos e positivos
        xi_mnulo = xf_mnulo = 0
        vao_negi = vao_negf = vao_pos = 0
        meio_vao = xi + 0.5 * vao
        for i in lista_Momentos_Zero:
            if i >= xi and i < meio_vao:
                xi_mnulo = i
            if i > meio_vao and i <= xf:
                xf_mnulo = i
        vao_negi = xi_mnulo - xi  # dimensão do trecho negativo inicial
        vao_negf = xf - xf_mnulo  # dimensão do trecho negativo final
        vao_pos = vao - vao_negi - vao_negf # dimensão do trecho positivo
     

        # definição dos cortantes no vão
        vdi = vdf = 0
        for i in range(0,len(lista_Cortantes)-2):
            xio = lista_Cortantes[i][0]
            xioo = lista_Cortantes[i+1][0]
            xfo = lista_Cortantes[i+2][0]
            if i != len(lista_Cortantes)-3:
                xfoo = lista_Cortantes[i+3][0]
            else:
                xfoo = xfo

            if xio == xi and xioo == xi and xfo == xf and xfoo == xf:
                vdi = max(abs(lista_Cortantes[i][1]),abs(lista_Cortantes[i+1][1]))
                if i != len(lista_Cortantes)-3:
                    vdf = max(abs(lista_Cortantes[i+2][1]),abs(lista_Cortantes[i+3][1]))
                else:
                    vdf = abs(lista_Cortantes[i+2][1])


        # definição dos momentos solicitantes NEGATIVOS para o tramo
        msd_md_negi = msd_md_negf = 0
        msd_mlonga_negf = msd_mlonga_negi = 0
        msd_mcurta_negi = msd_mcurta_negf = 0
        
        for x, momento in lista_MD_neg:
            if x == xi:
                msd_md_negi = momento
            if x == xf:
                msd_md_negf = momento

        for x, momento in lista_MLonga_neg:
            if x == xi:
                msd_mlonga_negi = momento
            if x == xf:
                msd_mlonga_negf = momento
                
        for x, momento in lista_MCurta_neg:
            if x == xi:
                msd_mcurta_negi = momento
            if x == xf:
                msd_mcurta_negf = momento
                
        md = msd_md_pos
        mlCurta = float(msd_mcurta_pos)*1.
        mlLonga = float(msd_mlonga_pos)*1.
        mlPos  = abs(mlLonga) * 1. + abs(mlCurta) * 1.

        mlNeg = max(abs(msd_mcurta_negi), abs(msd_mcurta_negf))*1.6 + max(abs(msd_mlonga_negi),abs(msd_mlonga_negf))*1.2  # min(ypm)
        mrdNeg = max(mrdNegi, mrdNegf)

        mrdLig  = tds * (d + ycg_laje)
        mrdLigi = mrdLigf = 0
        mrdLigi = min(mrdLig, mrdNegi)
        mrdLigf = min(mrdLig, mrdNegf)
                
        msdNeg = max(abs(msd_md_negi), abs(msd_md_negf))
##        print(msd_md_negi,msd_md_negf , lista_MD_neg)
        
        iax = ia = round(i_x(d, tw, bfs, tfs, bfi, tfi), 2)
        iay = round(i_y(d, tw, bfs, tfs, bfi, tfi), 2)
        j_perfil = round(j_(d, tw, bfs, tfs, bfi, tfi), 2)
        aa = round(area(d, tw, bfs, tfs, bfi, tfi),2)
##        print()
        ###################################################
        # 1 verificação ############
        
        h = d - tfs - tfi
        bi = bfs - tw
        yi =(bfi*d**2/2-h*bi*(h/2+tfi))/aa
        ys = d-yi
        hi = d - tfs/2 - tfi/2
        hc = 2 * (ys - tfs)

        verificacao_h_hc = ''
        if h/hc>=.75  and h/hc>=1.5:
            verificacao_h_hc = 'OK'
        else:
            verificacao_h_hc = 'NÃO OK'

        ypi = h/2-bfs*(tfi-tfs)/2/tw
        yps=h-ypi
        zx =bfs*tfs*(yps+tfs/2)+yps**2*tw/2+ypi**2*tw/2+bfi*tfi*(ypi+tfi/2)

        wxs = ia / ys
        wxi = ia / yi

        # Definição do FLM
        em = (min(bfs,bfi)*.5/min(tfs,tfi))

        if 4/((h/tw)**0.5) >= 0.35:
            if 4/((h/tw)**0.5) <= 0.763:
                kc = 4/((h/tw)**0.5)
            else:
                kc = 0.763
        else:
            kc = 0.35

        lpm= 1.71 * (fy)**.5
        lrm= 425/(((fy*10-115)/kc)**.5)
        mpm = fy * zx /1.
        mrm = (fy - 11.5)*wxs
        mnm = 0
        if em <= lpm:
            mnm = mpm
        elif em <= lrm:
            mnm = mpm-(mpm-mrm)*(em-lpm)/(lrm-lpm)
        else:
            mnm = 181000 * kc * wxs/em**2

        flm = 0.9 * mnm / 100. # kN.m

        ea = h / tw
        lpa = 16.80 / (fy)**.5
        lra = 664 / (fy)**.5 *(1 + 2.83 *h/hc)

        mra = fy * wxs
        mna = 0
        if ea <= lpa:
            mna = mpm
        elif ea <= lra:
            mna = mpm - (mpm - mra) * (ea-lpa)/(lra-lpa)
        else:
            mna = 0

        valor_limite_antes_cura = 1.5*wxs*fy/1.1/100
 
        v1a = mdlinha / valor_limite_antes_cura
        v1b = mdlinha / flm
        
        # Atribuindo valores finais da verificação ao objeto
        tramo.v1rda = valor_limite_antes_cura
        tramo.v1rdb = flm
        tramo.v1sd = mdlinha
        tramo.v1a = v1a
        tramo.v1b = v1b

##        datab.update_v1a(db, tramo.n, v1a)
##        datab.update_v1b(db, tramo.n, v1b)

##        datab.update_data(data_b, 'v1a', tramo.n, v1a)
##        datab.update_data(data_b, 'v1b', tramo.n, v1b)
        
        relatorio += "1 Verificação\n"
        relatorio += "MD' = {}\n".format(round(mdlinha,2))
        relatorio += "Valor Limite Antes da Cura (lim) = {}\n".format(round(valor_limite_antes_cura,2))
        relatorio += "FLM = {}\n".format(round(flm,2))
        relatorio += "MD' / lim = {} \t\t MD' / FLM = {} \n".format(round(v1a,2), round(v1b,2))
        
        ##########################################################
        # 2 verificação ########################
        lambdaFi = (bfi)*.5/(tfi)
        lambdaFs = (bfs)*.5/(tfs)
        lambda_mesa_perfil = max(lambdaFi, lambdaFs)
        lambda_mesa_limite = 0.38*(e/fy/10000)**.5

        afs = bfs * tfs
        afi = tfi * bfi

        hwc = d  - tfs - tfi - x1
        lambda_alma_perfil = 2 * hwc /tw
        lambda_alma_limite = 3.76*(e/fy/10000)**.5

        msg_mesa = ''
        msg_alma = ''
        relatorio += "\n2 Verificação\n"
        relatorio += "lambda_mesa_limite = 0.38*(e/fy/10000)^.5 = {}\n".format(round(lambda_mesa_limite,2))
        relatorio += "lambda_mesa_perfil = bf / (2 * tf) = {}\n".format(round(lambda_mesa_perfil,2))
        
        if lambda_mesa_perfil > lambda_mesa_limite:
            msg_mesa = 'Esbeltez da mesa: Não OK - Flambagem Local'
            relatorio += msg_mesa

        relatorio += "lambda_alma_limite = 3.76*(e/fy/10000)^.5 = {}\n".format(round(lambda_alma_limite,2))
        relatorio += "lambda_alma_perfil = 2 * hwc /tw = {}\n".format(round(lambda_alma_perfil,2))
        
        if lambda_alma_perfil > lambda_alma_limite:
            msg_alma = 'Esbeltez da alma: Não OK - Flambagem Local'
            relatorio += msg_alma

        ## Atribuindo valores de esbeltez
        tramo.v2alma = lambda_alma_perfil
        tramo.v2mesa = lambda_mesa_perfil
        
##        datab.update_v2almaa(data_b, tramo.n, str(lambda_alma_perfil))
##        datab.update_v2almab(data_b, tramo.n, str(lambda_mesa_limite))
##        datab.update_v2mesaa(data_b, tramo.n, str(lambda_mesa_perfil))
##        datab.update_v2mesab(data_b, tramo.n, str(lambda_alma_limite))

        ###########################################################
        # 3 Verificação - Verificação a Momento Positivo Reduzido    
        # conforme manual de viga mista semi-continua
        # B.12.3 Plastificação da seção pelo momento fletor positivo

        if msd_q - mrdLigi *(vao-x_md)/vao - mrdLigf*x_md/vao > 0:
            msd3 = msd_q - mrdLigi *(vao-x_md)/vao - mrdLigf*x_md/vao
        elif max(msd_q - mrdLigi *(vao-x_md)/vao, msd_q  - mrdLigf*x_md/vao) > 0:
            msd3 = max(msd_q - mrdLigi *(vao-x_md)/vao, msd_q  - mrdLigf*x_md/vao)
        else:
            msd3 = msd_q

        v3 = msd3 /(0.85*mrdPos)

        relatorio += "\n3Verificação - Verificação a Momento Positivo Reduzido\n"
        relatorio += "Conforme manual de viga mista semi-continua.\n"
        relatorio += "B.12.3 Plastificação da seção pelo momento fletor positivo.\n"
        relatorio += "Mrd Ligação Esquerda = {}\n".format(round(mrdLigi,2))
        relatorio += "Mrd Ligação Direita  = {}\n".format(round(mrdLigf,2))
        relatorio += "Msd = {}\n".format(round(msd3,2))
        relatorio += "Msd / (0.85*mrdPos) = {}\n".format(round(v3,2))

        ## Atribuindo valores de resistencia e solicitação
        tramo.v3rd = (0.85*mrdPos)
        tramo.v3sd = msd3

        tramo.v3 = v3
##        datab.update_v3(db, str(tramo.n), str(v3))


        ###########################################################
        # 4 Verificação - Verificação a Cortante
        kv = 5
        eac = e

        vd = max(vdi, vdf)
        vsd = vd * 1.4
        vrd = tramo.vrd

        v4 = vsd / vrd

        relatorio += "\n4 Verificação - Verificação a Cortante\n"

        relatorio += "lambda = hw / tw\n"
        relatorio += "lambda_p = 1.10 * (kv * e / (fy*10)) ** 0.5\n"
        relatorio += "lambda_r = 1.37 * ( kv * e) ** 0.5\n"
        relatorio += "vpl = 0.6 * aw * fy\n"

        relatorio += "Se lambda <= lambda_p : cv = 1\n"
        relatorio += "Se lambda <= lambda_r : cv = lambda_p / lambda\n"
        relatorio += "Se lambda > lambda_r : cv = 1.51*e*kv/lambda_**2/fy"
        relatorio += "vrd = 0.9 * vpl * cv\n"
        
        relatorio += "Vsd = {} kN\n".format(round(float(vsd),2))
        relatorio += "Vrd = {} kN\n".format(round(vrd,2))

        ## Atribuindo valores de resistencia e solicitação
        tramo.v4rd = vrd
        tramo.v4sd = vsd

        tramo.v4 = v4        
##        datab.update_v4(db, str(tramo.n), str(v4))
        
        ##########################################################
        
        ##########################################################
        # 5 Verificação - Capacidade de Rotação x Rotação necessaria
        # tetaui, tetauf

        # Tabela R.3 NBR8800/2008
        l_dt = (vao*100) / (d + hdeck/10)
        
        mrad_necessario = 0
        if l_dt <= 15:
            mrad_necessario = 15
            
        elif l_dt <= 20:
            mrad_necessario = 23
            
        elif l_dt <= 25:
            mrad_necessario = 29
            
        elif l_dt <= 30:
            mrad_necessario = 34
            
        elif l_dt > 30:
            mrad_necessario = 34

        mrad_disponivel = min(tetaui, tetauf)

        v5 = mrad_necessario/mrad_disponivel
        v5b = mrdLig  / (mrdPos*100)

        relatorio += "\n5Verificação - Capacidade de Rotação x Rotação necessaria\n"
        relatorio += "Utilizando a Tabela R.3 NBR8800/2008\n"
        relatorio += "Rotação necessaria = {} mrad\n".format(round(mrad_necessario,2))
        relatorio += "Rotação disponivel = {} mrad\n".format(round(mrad_disponivel,2))
        relatorio += "mrdLig  / (mrdPos*100) = {}\n".format(round(v5b,2))

        ## Atribuindo valores de resistencia e solicitação
        tramo.v5rda = mrad_necessario
        tramo.v5sda = mrad_disponivel
        
        tramo.v5rdb = (mrdPos*100)
        tramo.v5sdb = mrdLig
        tramo.v5 = v5

##        datab.update_v5(db, str(tramo.n), str(v5))                
        
        ##########################################################
        # 6 Verificação
        # Verificação da flambagem lateral com distorção da seção transversal

        relatorio += "\n 6 Verificação\n"
        relatorio += "Verificação da flambagem lateral com distorção da seção transversal.\n"
        
        porcent = 0.26 # 26 %
        mrd_neg_lig = 30. / porcent * mrdNeg
        e_cm = e * 0.0001   # kN/cm2

        relatorio += "mrd_neg_lig = 30. / porcent * mrdNeg = {} \n".format(round(mrd_neg_lig,2))
        
        mrd_vm = mrdNeg # solicitação Momento negativo pela analise
        a = b_inf * 100  # cm
        alpha = 0
        if situacao == 'intermediario':
            alpha = 4
        else:
            alpha = 2

        relatorio += "alpha = {}\n".format(round(alpha,2))
        relatorio += "a = largura influencia * 100 = {} cm\n".format(round(a,2))

        ii = min(ief_neg, ief_pos_longa, ief_pos_curta)*(100 ** 4)
        ei2 = e_cm * ii  # kN/cm2 * cm4

        relatorio += "Inercia = {} cm4\n".format(round(ii,2))
        relatorio += "Ei2 = {} Kn/cm2 * cm4\n".format(round(ei2,2))

        k1 = alpha * (ei2) / a
        k2 = e_cm * 0.0001 * tw**3 / (4*ho*(1-v_poisson**2))

        kr = k1 * k2 / (k1 + k2)

        relatorio += "k1 = alpha * (ei2) / a = {}\n".format(round(k1,2))
        relatorio += "k2 = e_cm * 0.0001 * tw ^ 3 / (4 * ho * (1 - v_poisson ^ 2)) = {}\n".format(round(k2,2))
        relatorio += "kr = k1 * k2 / (k1 + k2) = {} \n".format(round(kr,2))

        iaf_y = tfi * (bfi**3) / 12     # cm4
        
        yc = d - ycg_perfil + ycg_laje  # cm
        ys = ycg_perfil                 # cm
        yf = ho * iaf_y / iay           # cm

        relatorio += "iaf_y = tfi * (bfi**3) / 12 = {} cm4\n".format(round(iaf_y,2))        
        relatorio += "yc = d - ycg_perfil + ycg_laje = {} cm\n".format(round(yc,2))
        relatorio += "ys = ycg_perfil = {} cm\n".format(round(ys,2))
        relatorio += "yf = ho * iaf_y / iay  = {} cm\n".format(round(yf,2))

        yj = 0

        if iaf_y > 0.5 * iay:
            yj = 0.4 * ho * ( 2 *iaf_y/iay - 1)
        else:
            print(iaf_y ,0.5 * iay,iaf_y > 0.5 * iay)
            yj = ys - 1

        relatorio += "Se iaf_y > iay/2: yj = 0.4 * ho * ( 2 *iaf_y/iay - 1)\n"
        relatorio += "Caso contrario: yj = ys - 1\n"
        relatorio += "yj = {}\n".format(round(yj,2))

        eee = (aa + Asl) * ia / (aa*yc*(Asl))
        alpha_g = (ho*(ief_neg*100**4)/ia) / ((((yf - ys)**2 + ((iax + iay)/aa)) / eee) + 2 *(yf-yj))
        
        msd_neg = msdNeg  # min(mrd_neg_lig*1.55, mrd_vm)
        psi1 = round(mrdNeg / mrdPos,1)

        relatorio += "eee = (aa + Asl) * ia / (aa*yc*(Asl)) = {}\n".format(round(eee,2))
        relatorio += "alpha_g = (ho*(ief_neg*100**4)/ia) / ((((yf - ys)^2 + ((iax + iay)/aa)) / eee) + 2 *(yf-yj)) = {}\n".format(round(alpha_g,2))
        
        relatorio += "msd_neg = {}\n".format(round(msd_neg[0],2))
        relatorio += "psi1 = mrdNeg / mrdPos = {}\n".format(round(psi1,2))

        c_dist = psi2 = 0
        
        if situacao == 'intermediario':
            psi2 = 1.0 # considerando momentos negativos iguais em ambos apoios
            psi2 = min(mrdNegi,mrdNegf) / max(mrdNegi,mrdNegf)
        else:
            psi2 = 0.0
            
        if psi2 == 1.0:
            if psi1 >= 1.0:
                c_dist = 21.9
            elif psi1 < 1.0 and psi1 >= 0.8:
                c_dist = 24.0
            elif psi1 < 0.8 and psi1 >= 0.6:
                c_dist = 26.7
            elif psi1 < 0.6 and psi1 >= 0.4:
                c_dist = 29.5
            elif psi1 < 0.4 and psi1 >= 0.2:
                c_dist = 32.7
            elif psi1 < 0.2 and psi1 >= 0.1:
                c_dist = 34.2
                
        elif psi2 < 1.0 and psi2 > 0.75:
            if psi1 >= 1.0:
                c_dist = 26.5
            elif psi1 < 1.0 and psi1 >= 0.8:
                c_dist = 29.0
            elif psi1 < 0.8 and psi1 >= 0.6:
                c_dist = 32.
            elif psi1 < 0.6 and psi1 >= 0.4:
                c_dist = 35.
            elif psi1 < 0.4 and psi1 >= 0.2:
                c_dist = 38.
            elif psi1 < 0.2 and psi1 >= 0.1:
                c_dist = 39.8
                
        elif psi2 < 0.75 and psi2 > 0.5:
            if psi1 >= 1.0:
                c_dist = 30.5
            elif psi1 < 1.0 and psi1 >= 0.8:
                c_dist = 33.9
            elif psi1 < 0.8 and psi1 >= 0.6:
                c_dist = 37.
            elif psi1 < 0.6 and psi1 >= 0.4:
                c_dist = 40.4
            elif psi1 < 0.4 and psi1 >= 0.2:
                c_dist = 44.3
            elif psi1 < 0.2 and psi1 >= 0.1:
                c_dist = 45.7
                
        else:
            if psi1 >= 1.0:
                c_dist = 32.4
            elif psi1 < 1.0 and psi1 >= 0.8:
                c_dist = 36.5
            elif psi1 < 0.8 and psi1 >= 0.6:
                c_dist = 42.6
            elif psi1 < 0.6 and psi1 >= 0.4:
                c_dist = 47.6
            elif psi1 < 0.4 and psi1 >= 0.2:
                c_dist = 51.8
            elif psi1 < 0.2 and psi1 >= 0.1:
                c_dist = 53.5
        
        mcr = alpha_g * (c_dist / (vao*100)) * ((7700*(j_perfil) +
                                         kr*((vao*100)**2)/(3.14**2))*(e_cm)*(iaf_y))**.5

        relatorio += "alpha_g * (c_dist / (vao*100)) * ((7700*(j_perfil) + kr*((vao*100)^2)/(3.14^2))*(e_cm)*(iaf_y))^(1/2) = {}\n".format(round(alpha_g,2))

        
        if mcr == 0:
            mcr = 1
        
        if bfs*tfs == tfi*bfi:
            relatorio += "Mesa superior e inferior iguais.\n"
            l_dist = 5 *(1 + (tw * ho)/(4*bfs*tfs)) * (((fy / (e/10000*c_dist))**2) * ((ho/tw)**3) * (tfs/bfs))**0.25
            relatorio += "l_dist = 5 *(1 + (tw * ho)/(4*bfs*tfs)) * (((fy / (e/10000*c_dist))**2) * ((ho/tw)**3) * (tfs/bfs))**0.25 = {}\n".format(round(l_dist,2))
        else:
            relatorio += "Mesa superior e inferior diferentes.\n"
            l_dist = (mrdNegk / mcr) ** .5
            relatorio += "l_dist = (mrdNegk / mcr) ^ (1/2) = {}\n".format(round(l_dist,2))
        
        x_dist = 0
        if l_dist <= 0.4:
            relatorio += "Se l_dist <= 0.4 : x_dist = 1.0 \n"
            x_dist = 1.0
            
        elif l_dist > 1.5:
            relatorio += "Se l_dist > 1.5: \n"
            x_dist = 0.877/(l_dist**2)
            relatorio += "x_dist = 0.877/(l_dist^2) = {}\n".format(round(x_dist,2))
            relatorio += "l_dist excede o valor de 0.4 - não atende Item R.2.5.1 NBR8800 \n"
##            print('\nTramo %.0f' % tramo.n)
##            print('l_dist excede o valor de 0.4 - não atende Item R.2.5.1 NBR8800')
        else:
            relatorio += "Se l_dist < 1.5 e l_dist >= 0.4: \n"
            x_dist = 0.658**(l_dist**2)
            relatorio += "x_dist = 0.658^(l_dist^2) = {}\n".format(round(x_dist,2))
            relatorio += "l_dist excede o valor de 0.4 - não atende Item R.2.5.1 NBR8800 \n"
##            print('\nTramo %.0f' % tramo.n)
##            print('l_dist excede o valor de 0.4 - não atende Item R.2.5.1 NBR8800')
        
        mrd_dist = x_dist * mrdNeg
        relatorio += "mrd_dist = x_dist * mrdNeg = {}\n".format(round(mrd_dist,2))        

        v6 = max(abs(msd_md_negi) / mrd_dist, abs(msd_md_negf) / mrd_dist)
        relatorio += "Msd(-) lado esquerdo = {}\n".format(round(float(msd_md_negi),2))
        relatorio += "Msd(-) lado direito = {}\n".format(round(float(msd_md_negf),2))
        relatorio += "v6 = Msd(-) / mrd_dist = {}\n".format(round(float(v6),2))

##        datab.update_v6(db, str(tramo.n), str(v6))

        ## Atribuindo valores de resistencia e solicitação
        tramo.v6rd = mrd_dist
        tramo.v6sda = abs(msd_md_negi)
        tramo.v6sdb = abs(msd_md_negf)
        tramo.v6 = v6        

        ##########################################################
        n_conectores_pos = (vao_pos * 100 / 27.7)
        
        n_conectores_negi = n_conectores_negf = 0
        n_conectores_negi = (vao_negi * 100 / 27.7)
        n_conectores_negf = (vao_negf * 100 / 27.7)

        if ceil(n_conectores_pos)-n_conectores_pos != 0:
            n_conectores_pos = ceil(n_conectores_pos)-1
            
        if ceil(n_conectores_negi)-n_conectores_negi != 0:
            n_conectores_negi = ceil(n_conectores_negi)-1
            
        if ceil(n_conectores_negf)-n_conectores_negf != 0:
            n_conectores_negf = ceil(n_conectores_negf)-1
        ##########################################################
        # O.2.4.1.2  NBR8800-2008
######        tds = Asl * fys / 1.15    
######        Qrd = 70.7 # resistencia de cada conector #3/4
######        n = round(tds / Qrd,0) #  numero de conectores)
        ##########################################################
        # 7 Verificação
        # Item O.2.4 NBR 8800/2008        
        # e_qrd = n_conectores * 1.00 * Qrd

        relatorio += "\n7 Verificação\n"
        relatorio += "Item O.2.4 da NBR 8800/2008\n"
        relatorio += "Quantidade de conectores no trecho de momento positivo = {} (e=27.7cm)\n".format(round(n_conectores_pos,2))
        relatorio += "Quantidade de conectores no trecho de momento negativo direito = {} (e=27.7cm)\n".format(round(n_conectores_negi,2))
        relatorio += "Quantidade de conectores no trecho de momento negativo esquerdo = {} (e=27.7cm)\n".format(round(n_conectores_negf,2))
        relatorio += "verificação dos conectores do trecho negativo\n"
        
        # conectores no trecho negativo + 1 do trecho positivo
        n_conect = max(n_conectores_negi,n_conectores_negf)+1 
        e_qrd = (n_conect) * Qrd

        v7 = tds / e_qrd

        relatorio += "Qrd = {} kN\n".format(round(Qrd,2))
        relatorio += "e_qrd = (n_conectores) * Qrd = {} kN\n".format(round(e_qrd,2))
        relatorio += "v7 = tds / e_qrd = {}\n".format(round(v7,2))

        n_conect1 = n_conect
        e_qrd_neg = 0
        num = 1

        # caso um conector por onda não seja suficiente
        # calcular com dois conectores por onda
        if v7 > 1.03:
            relatorio += "Como 1 conector por onda não é suficiente, utilizaremos 2.\n"
            num = 2
            n_conect *= num
            e_qrd_neg = (n_conect * 0.85 * Qrd)            
            v7 = tds / e_qrd_neg
            relatorio += "e_qrd = (n_conect * 0.85 * Qrd) = {}\n".format(round(e_qrd_neg,2))
            relatorio += "v7 = tds / e_qrd = {}\n".format(round(e_qrd_neg,2))

        if v7 > 1.03:
            relatorio += "Como 2 conectores por onda não é suficiente, utilizaremos 3.\n"
            num = 3
            n_conect *= num
            e_qrd_neg = (n_conect * 0.70 * Qrd)
            v7 = tds / e_qrd_neg
            relatorio += "e_qrd = (n_conect * 0.70 * Qrd) = {}\n".format(round(e_qrd_neg,2))
            relatorio += "v7 = tds / e_qrd = {}\n".format(round(e_qrd_neg,2))

        ## Atribuindo valores de resistencia e solicitação
        tramo.v7rd = e_qrd_neg
        tramo.v7sd = tds
        tramo.v7 = v7


        ##########################################################
        # 8 Verificação - Cisalhamento longitudinal da Laje
        # O.1.3.4 NBR 8800/2008

        relatorio += "\n8 Verificação - Cisalhamento longitudinal da Laje\n"
        relatorio += "Item O.1.3.4 da NBR 8800/2008\n"
                
        e_qrd_negi = n_conect * 1.00 * Qrd
        e_qrd_negf = n_conect * 1.00 * Qrd
        e_qrd_pos = (n_conectores_pos) * Qrd

        vsd_pos = (e_qrd_pos - 100 * bef_pos *tc/2*fck/1.4)/ (vao_pos / 2)  # - Asl*fys - 100*bef_pos *tc/2*fck/1.4) / vao_pos

        if vsd_pos < 0:
            vsd_pos = (e_qrd_pos)/ (vao_pos / 2)

        relatorio += "Considerando somatorio de forças resistentes dos conectores, da regiao positiva: {} kN\n".format(round(e_qrd_pos,2))
        relatorio += "Distancia entre seções na região de momento positivo: {} cm\n".format(round(vao_pos/2,2))
        relatorio += "Considerando somatorio de forças resistentes dos conectores, da regiao negativa esquerda: {} kN\n".format(round(e_qrd_negi,2))
        relatorio += "Distancia entre seções na região de momento negativo esquerdo: {} cm\n".format(round(vao_negi,2))
        relatorio += "Considerando somatorio de forças resistentes dos conectores, da regiao negativa direita: {} kN\n".format(round(e_qrd_negf,2))
        relatorio += "Distancia entre seções na região de momento negativo direito: {} cm\n".format(round(vao_negf,2))

        

        vsd_negi = vsd_negf = 0
        e_qrdi = e_qrdf = 0

        nnn = 1.0  # 0.3 + 0.7 * (yc / 2400)  # yc = 2400 massa especifica do concreto
        fctk = .21*(fck**0.66667)

        # area de cisalhamento do concreto no plano considerado, por unidade de comprimento da viga
        acv = tc * 100
        
        sd_text = datab_g.get_data(dbg, 'novo', 'SD')

        # Af = area da fpr,a de aço incorporada no plano de cisalhamento, por unidade de comprimento
        af = 0
        if sd_text == '0.80':
            # SD 0.80 =  9.92 cm2/m
            af = 9.92
        elif sd_text == '0.95':
            # SD 0.95 = 11.88 cm2/m
            af = 11.88
        elif sd_text == '1.25':
            # SD 1.25 = 15.80 cm2/m
            af = 15.80
            
        aS = 0 # O.1.3.4 NBR 8800/2008
        # As = area de armadura transversal disponivel na seção da laje considerada
        aS = max(1.5, acv*.1/100, Asl/1)
        
        if vao_negi != 0:
            vsd_negi = (e_qrd_negi - Asl*fys ) / (vao_negi) # kN/m
            e_qrdi = e_qrd # e_qrd_negi # kN
            
        if vao_negf != 0:
            vsd_negf = (e_qrd_negf - Asl*fys ) / (vao_negf) # kN/m
            e_qrdf = e_qrd # e_qrd_negf # kN

        relatorio += "fctk = {} \n".format(round(fctk,2))
        relatorio += "acv = {} cm2/m \n".format(round(acv,2))
        relatorio += "Espessura do Steel Deck {}\n".format(round(sd_text,2))
        relatorio += "Area da forma de aço: {} cm2/m".format(round(af,2))
        relatorio += "Area da armadura transversal: {} cm2\n".format(round(aS,2))
        
        relatorio += "Para a região de momento positivo da viga.\n"        
        relatorio += "vsd = {} kN\n".format(round(vsd_pos,2))
        relatorio += "Para a região de momento negativo, lado esquerdo da viga.\n"
        relatorio += "vsd = {} kN\n".format(round(vsd_negi,2))
        relatorio += "Para a região de momento negativo, lado direito da viga.\n"
        relatorio += "vsd = {} kN\n".format(round(vsd_negf,2))

                 
        # considera-se vigas que não são de borda, ou seja, resultando na relação b1/(b1+b2) = 0.5
        vsd_plano = max(vsd_negi, vsd_negf, vsd_pos) * .5

        relatorio += "Considera-se vigas que não são de borda, ou seja, resultando na relação b1/(b1+b2) = 0.5\n"
        relatorio += "vsd utilizado = {} kN/m \n".format(round(vsd_plano,2))

        vrd_a = 0.6 * nnn * acv * fctk / 1.4 + aS*fys / 1.15 + af*(28)/1.1
        vrd_b = 0.2 * nnn * acv * fck / 1.4 + 0.6 * af * 28 / 1.1
        vrd = min(vrd_a, vrd_b)

        v8 = vsd_plano / vrd

        relatorio += "vrd = {} <= {} \n".format(round(vrd_a,2), round(vrd_b,2))
        relatorio += "vsd_plano / vrd = {}\n".format(round(v8,2))
        
        ## Atribuindo valores de resistencia e solicitação
        tramo.v8rd = vrd
        tramo.v8sd = vsd_plano
        tramo.v8 = v8
        
        
        ##########################################################
        # 9 Verifficação - Relação entre momento Resistivo Negativo / Positivo
        relatorio += "\n9 Verificação - Relação entre Momento Fletor Resistente da Ligação x Momento Fletros Resistente Positivo da Viga.\n"
        relatorio += "A NBR8800 estabeleze que o meomento resistente da ligação mista seja igual ou superior a 30% do momento fletor positivo "
        relatorio += "resistente da viga mista.\n"

        relatorio += "Mrd Ligação esquerda = {} \n".format(round(mrdLigi,2))
        relatorio += "Mrd Ligação direita = {} \n".format(round(mrdLigf,2))
        relatorio += "Mrd Momento Positivo = {} \n".format(round(mrdPos,2))
        
        v9 = min(mrdLigi / mrdPos, mrdLigf / mrdPos)
        
        relatorio += "Mrd ligação / Mrd Positivo = {}\n".format(round(v9,2))

        ## Atribuindo valores de resistencia e solicitação
        tramo.v9rd = mrdPos
        tramo.v9sd = mrdNeg
        tramo.v9 = v9
        

        ##########################################################
        # 10 verificação - Limitação das tensões de serviço

        relatorio += "\n10 verificação - Limitação das tensões de serviço\n"
        relatorio += "(Combinação rara de ações de serviços)\n"
        relatorio += "Conforme verificação B.9 do manual de estruturas mistas.\n"
        
        wa = round(wx(ia,d))
        relatorio += "Considerando para calculo:\n"
        relatorio += "yi = (bfi * d^2 / 2 - h * bi * (h / 2 + tfi)) / aa = {}\n".format(round(yi,2))
        relatorio += "ia = {}\n".format(round(ia,2))
        relatorio += "wxi = ia / yi = {}\n".format(round(yi,2))
        relatorio += "w Curta Duração = {} cm3\n".format(round((wPosCurta*100**3),2))
        relatorio += "w Longa Duração = {} cm3\n".format(round((wPosLonga*100**3),2))
        relatorio += "Mg = {} kN.cm\n".format(round(mg*100,2))
        relatorio += "Ml Curta Duração = {} kN.cm\n".format(round(mlCurta*100,2))
        relatorio += "Ml Longa Duração = {} kN.cm\n".format(round(mlLonga*100,2))
        relatorio += "Ml Negativo = {} kN.cm\n".format(round(float(mlNeg)*100,2))

        t11 = mg*100 / wxi
        t12 = mlCurta*100/(wPosCurta*100**3)
        t13 = mlLonga*100/(wPosLonga*100**3)
        t1 = round((t11 + t12+ t13),3)        
        ftc = round(abs(mlNeg[0]*100) / (d + ycg_laje),2)
##        print('ftc',ftc)
##        print('mlneg', mlNeg*100)
        t2 = round(ftc / Asl,2)
        t3 = round(ftc / ((bfi * tfi)/1.1),2)

        relatorio += "ftc = Ml(-) / (d + ycg_laje) = {}\n".format(round(ftc,2))
        relatorio += "Tensão de serviço antes da cura = {}\n".format(round(t11,2))
        relatorio += "Tensão de serviço depois da cura de curta duração = {}\n".format(round(t12,2))
        relatorio += "Tensão de serviço depois da cura de longa duração = {}\n".format(round(t13,2))
        relatorio += "Tensão de serviço = {}\n".format(round(t1,2))
        relatorio += "Tensão de serviço nas barras de armadura = {}\n".format(round(t2,2))
        relatorio += "Tensão de serviço na inferior do perfil = {}\n".format(round(t3,2))

        
        ## Atribuindo valores de resistencia e solicitação
        tramo.v10rd = mrdPos
        tramo.v10sd = ftc

        ##########################################################
        # 11 Verificação ######
        relatorio += "\n11ª Verificação - Flecha/Deslocamentos\n"
        relatorio += "O programa realiza um calculo aproximado das flechas do sistema de vigas com vinculação semi-rigida.\n"
        # flecha antes da cura
        d_ac = (5 * (q_glinha) * vao**4) / (384 * e * (ia / 100**4)) * 100  #cm
        relatorio += "Flecha do tramo antes da cura. Viga bi-apoiada.\ndac = {:.2f} cm\n".format(d_ac)
        # flecha depois da cura, carregamento longa duração
        d_cpdc = tramo.flecha_longa * 1.25
        relatorio += "Flecha do tramo depois da cura do carregamento de longa duração. Viga semi-continua.\nd cpdc = {:.2f} cm\n".format(d_cpdc)
        # flecha depois da cura, carregamento curta duração
        d_scdc = tramo.flecha_curta * 1.25
        relatorio += "Flecha do tramo depois da cura do carregamento de curta duração. Viga semi-continua.\nd scdc = {:.2f} cm\n".format(d_scdc)
        #flecha limite
        d_adm = vao / 350.0 * 100
        d_total = d_ac + d_cpdc + d_scdc

        relatorio += "Sugestão de contra flecha, menor valor entre:\n"
##        cf_85_ac = 0.85 * d_ac  # mm
        if tramo.situacao != 'ponta_esquerda' and tramo.situacao != 'ponta_direita':
            cf_85_ac = 0.85 * d_ac  # mm
            relatorio += "\t0.85% * d_ac  = {:.2f} cm\n".format(cf_85_ac)
        else:
            cf_85_ac = 1.0 * d_ac  # mm
            relatorio += "Por ser um tramo de extremidade:\n"
            relatorio += "\t1.00% * d_ac  = {:.2f} cm\n".format(cf_85_ac)

        cf_70_tot_sc = 0.7 * (d_total - d_scdc)  # mm
        cf_adotada = min(cf_85_ac, cf_70_tot_sc)
        
        relatorio += "\t0.7% * (flecha total - d scdc) = {:.2f} cm\n".format(cf_70_tot_sc)
        relatorio += "Contra flecha adotada = {:.2f} cm\n".format(cf_adotada)

        d_final = d_total - cf_adotada
        relatorio += "Flecha final = {:.2f} cm\n".format(d_final)
        relatorio += "Flecha limite: d adm = {:.2f} cm \n".format(d_adm)
        v11 = d_final / d_adm
        
        ###########################################
        # 12 Verificação ##########################
        relatorio += "\n12ª Verificação - Limite de vibração excessiva\n"
        relatorio += "Conforme item L.3.2, avaliação simplificada para as atividades humanas normais."
        relatorio += "Caso atividades não sejam normais, nem humanas, estes calculos não são validos."

        q_vibracao = q_glinha + q_sc + q_longa

        Ec = 4760 * ((10 * fck) ** 0.5) / 10.

        RzE = tramo.e / (Ec)
        b_ef = min(tramo.vao / 4., b_inf)
        b_transformada = b_ef / RzE

        w_12 = d / 2.0 + tc + hf
        y_12 = d / 2.0 + hf + tc / 2.0

        a_12 = min((((aa ** 2 + 2 * b_transformada * aa * w_12) ** 0.5) - aa) / b_transformada, tc)
        a_transformada = b_transformada * a_12
        ix_laje = (b_transformada * tc ** 3) / 12.0
        
        ay_laje = a_transformada * y_12
        ay_2_laje = a_transformada * y_12 ** 2

        ix_total = iax + ix_laje
        a_total = aa + a_transformada
        yg_12 = ay_laje / a_total

        itr_12 = ay_2_laje + ix_total - a_total * (yg_12**2)

        ief_12 = iax + (itr_12 - iax)*(tramo.nn)**0.5

        # Flecha da viga biapoiada:

        flecha_vibracao = (5 * (q_vibracao) * vao**4) / (384 * e * (ief_12 / 100**4)) * 100  #cm
##        print('flecha de vibracao {} \t '.format(flecha_vibracao))

        v12 = round(flecha_vibracao / 2.0,3)
        
        
        ###########################################
        # 13 Verificação ##########################
        relatorio += "\n13ª Verificação - Fissuração do Concreto sobre os apoios.\n"
        relatorio += "Conforme Item O.5.3.1 da NBR 8800 - 2008\n"
        
        acr = (7.5 * bitola + 7.5 * bitola) * (7.5 * bitola + 3.5)
        pri = ((3.14 * (bitola ** 2)) / 4) / acr
        nn1 = 2.25

        es  = 21000
        fctm = 0.3 * (fck ** 0.66)
        tsi = (mlCurta * 0.4 + mlLonga)*100 / (d + (tc+hf-3.5))/ Asl

        w1 = (bitola/(12.5*nn1)) * (tsi/es) * ((3*tsi)/fctm)*10
        w2 = (12.25/(12.25*nn1))*((tsi/es)*((4/pri)+45))*10

        valor = min(w1,w2)

        relatorio += "Acr = {:.2f} \n".format(round(acr,2))
        relatorio += "pri = ((3.14 * (bitola ** 2)) / 4) / acr = {:.2f} \n".format(round(pri,2))
        relatorio += "nn1 = 2.25 \n"
        relatorio += "fctm = 0.3 * (fck ** 0.66) = {:.2f} \n".format(round(fctm,2))
        relatorio += "tsi = (mlCurta * 0.4 + mlLonga)*100 / (d + (tc+hf-3.5))/ Asl = {:.2f} \n".format(round(tsi,2))
        relatorio += "w1 = {:.2f} \n".format(round(w1,2))
        relatorio += "w2 = {:.2f} \n".format(round(w2,2))
        relatorio += "A grandeza da abertura das fissuras, é a menor dentre w1 e w2\n"
        relatorio += "O valor limite para fissuras deve atender a tabela O.4 c, apresentada na NBR 8800, conforme classe de agressividade ambiental.\n"

        classe_agressividade = datab_g.get_data(dbg, 'novo', 'classe_agressividade')

        valor_limite = 0.0
        if classe_agressividade == 'fraca':
            valor_limite = 0.4
        elif classe_agressividade == 'moderada':
            valor_limite = 0.3
        elif classe_agressividade == 'forte':
            valor_limite = 0.3
        elif classe_agressividade == 'muito forte':
            valor_limite = 0.2

        relatorio += "Valor limite de fissuração = {:.3f}mm \n".format(valor_limite)
            
        v13 = valor / valor_limite
        
        ###########################################
        # Armadura Minima de Tração sob Deformações
        # NBR 8800 - 2008
        # Item O.5.2

        relatorio += "\nArmadura Minima de Tração sob Deformações  \n"
        relatorio += "Item O.5.2 da NBR 8800 - 2008\n"
        
        yo = x1
        fctef = 0.3  # item O.5.2.3
        wk = valor_limite
        
        teta_st = min(810 * wk**.5 * ((fck**(2/3.)/(bitola/10))),fys)
        relatorio += "yo = {:.2f}\n".format(round(yo,2))
        relatorio += "fctef = {:.2f} (Item O.5.2.3)\n".format(round(fctef,2))
        relatorio += "wk = {:.2f}\n".format(round(wk,2))
        relatorio += "teta_st = menor entre: 810 * wk ^ .5 * ((fck^(2/3.)/(bitola/10)))  ou  fys  = {:.2f}\n".format(round(teta_st,2))
        
        kc = 1 / (1 + tc / (2*yo)) + 0.3

        k = 0.8
        ks = 0.9

        relatorio += "kc = 1 / (1 + tc / (2*yo)) + 0.3 = {:.2f}\n".format(round(kc,2))
        relatorio += "k = 0.8 \nks = 0.9\n"

        act = tc * max(befNegi, befNegf)*100  # cm2

        as_minima = k * kc * ks * fctef * act / teta_st  #  cm2

        relatorio += "act = {:.2f} \n".format(round(act,2))
        relatorio += "As minima = k * kc * ks * fctef * act / teta_st = {:.2f}\n".format(round(as_minima,2))

        ###########################################
        # Espaçamento das barras de armadura

        volumei = befNegi*vao_negi*.11*100
        volumef = befNegf*vao_negf*.11*100
        peso_armadura = Asl * 7850 / 100 ** 2*(vao_negi + vao_negf)

        taxa_armadura = [peso_armadura / max(volumei, volumef),
                         peso_armadura ]
        
        ###################################################
        
        verificacao1 = [v1a, v1b]
        verificacao2 = [lambda_mesa_perfil, lambda_mesa_limite, lambda_alma_perfil, lambda_alma_limite]
        verificacao3 = [v3]
        verificacao4 = [vsd, vrd, v4]
        verificacao5 = [tetaui, tetauf, v5, l_dt, v5b]
        verificacao6 = [msd_neg, mrd_dist, v6, l_dist]
        verificacao7 = [e_qrd, tds, v7, num]
        verificacao8 = [vsd_plano, vrd, v8]
        verificacao9 = [mrdNeg, mrdPos, v9]
        verificacao10 = [t1/fy, t2/fys, t3/(fy/1.1), t11/fy, t12/fy, t13/fy]
        verificacao11 = [v11]
        verificacao12 = [v12]
        verificacao13 = [v13]
        pesos = [tramo.peso_perfil, tramo.peso_barras, tramo.peso_cantoneiras]

        retorno0 = [tramo,
                    verificacao1, verificacao2, verificacao3,
                    verificacao4, verificacao5, verificacao6,
                    verificacao7, verificacao8, verificacao9,
                    verificacao10, verificacao11, verificacao12 ,verificacao13, pesos]
        retorno.append(retorno0)

        relatorio += "\nFim das verificações de dimensionamento.\n"

       
        db_relatorio.insert_data(db_rel, 'Verificacao', str(tramo.n), relatorio)
        

    return retorno

       
       
       



