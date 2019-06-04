## rotina de dimensionamentos de vigas mistas semi continuas, conforme NBR 8800
import propriedades_perfil_i as prop
from math import ceil

#TODO concluir verificações

interacao = 1#0.75

def calculo_C(Es, E, Asl, fck, fys, ha, d, bfs, bfi, tw, tfs, tfi, hdeck, vao, vaoad, largInfluencia):
    L = 200.    # comprimento de referencia para levar em conta o efeito do concreto
                # que envolve a armadura, podendo ser tomado igual a 200 mm
                # sendo que a distancia do primeiro conecto ate a face e ate o centro do elemento de apoio
                # nao podem ser inferiores a 100 e 200mm, respectivamente
    
    ## aa = area de aço do perfil metalico [cm2]
    ## ia = inercia do perfil metalico [cm4]
    ## ea = E = Modulo de elasticidade do perfil metalico [kN/cm2]
    ## ycgLaje = altura do centro geometrico da laje [cm]
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
       
    areaPerfil = round(prop.area(d, tw, bfs, tfs, bfi, tfi), 2)    
    ia = round(prop.i_x(d, tw, bfs, tfs, bfi, tfi), 2)
    wa = round(prop.wx(ia,d))
    Es = Es / 10000
    E = E / 10000
    vao *= 100
    vaoad *= 100
    largInfluencia *= 100
    ea = E
    ycgLaje = 7.5 + (hdeck - 75) * .05 # altura do centro geometrico da laje
    tc = (hdeck - 75) / 10 #6.5 # altura concreto laje steeldeck
    ds = yLaje = d * .5 + ycgLaje
    #####################################
    ##### PARAMTROS DE DEFINIÇÃO PARA O KI
    nl = 2 # numero de linhas de parafusos
    db = 19.05 # diametro dos parafusos

    fu1 = fu2 = 45 # resistencia a ruptura do aço das cantoneiras kN/cm2
    fub = 82.5 # resistencia a ruptura do aço dos parafusos
    dm = 16 # mm  - diametro de referencia tomado 16mm NBR 8800
    S = 75  # espaçamento entre parafusos na direção da força
    tp1 = tp2 = 9.5 # espessura das cantoneiras
    #######################################

    ##### PARAMTROS DE DEFINIÇÃO PARA O KCS
    tds = Asl * fys / 1.15    
    Qrd = 70.7 # resistencia de cada conector
    n = tds / Qrd #  numero de conectores
    kr = 1000. #  definido no capitulo 2 do manual
    #######################################

    ##### PARAMTROS DE DEFINIÇÃO PARA O KS
    h = d + ycgLaje

    # Capacidade de deformação
    Bt = 0.4
    sigma0 = 0.8
    fctm = 0.3 * (fck * 10) ** (2. / 3.) / 10 # kN/cm2
    Ec = 4760 * ((10 * fck) ** 0.5) / 10. # kN/cm2
    RzE = E / Ec

    esu = 0.08   #  8% rpedefinido
    #######################################
    #regiao momento negativo
    larguraEfetiva = min((vao / 4 + vaoad / 4) * 2 / 8., largInfluencia)
##    print('largura efetiva = %.2f' % larguraEfetiva)

    #larguraEfetiva = min(larInfluencia / 2., vaoc / 8.) # vao intermediarios
    # rigidez inicial das barras de amradura da laje de steel deck
    # NBR8800 - R.2.3.1
    ks = 2 * Asl * Es / ha
    ###
    ############################################################
    # Definição do centro de geometria da seção transformada, para capacidade de deformação
    larguraTransformada = larguraEfetiva / RzE

    areaTransformada = larguraTransformada * tc

    Ay = areaTransformada * yLaje

    yg = Ay / (areaPerfil + areaTransformada)
    y0 = d * .5 - yg + ycgLaje

    # capacidade de deformação das barras da armadura
    # R.2.3.3
    # esm deformação da armadura envolvida pelo concreto
    # dus - capacidade de alongamento das barras de armadura
    # NBR8800 - R.2.3.3
    rho = Asl / (larguraEfetiva * tc - Asl)
    kc = 1 / (1 + tc / (2 * y0))

    desr = fctm * kc / ( rho * Es)
    teta_srl = (fctm * kc / rho) * (1 + rho * Es / Ec)
    esy = fys / Es

    esmu = esy - Bt*desr + sigma0 * (1 - teta_srl/fys) * (esu - esy)
    dus = L * esmu
    ##################################################
    ##################################################

    ## definição do kcS
    rdArmaduras = tds = Asl * fys / 1.15

    if n * Qrd < tds:
        print('n conectores insuficiente:  %f  <  %f' % (n*Qrd, tds))

    Ll = .15 * vao
    # print('numero de conectores  %d' % n)

    ee = ia / (Asl * (ds ** 2))
    vv = ((ee + 1)*n *kr * Ll*(ds**2) / (ea*ia)) ** (.5)
    alpha = vv - (vv - 1)*(d + ycgLaje) / ((ds * (ee + 1)))

    kcs = n * kr / alpha

    #################
    # capacidade de deformação dos conectores de cisalhamento
    # sb - capacidade de escorregamento associada a deformação dos conectores
    # NBR8800 - R.2.4.3
    sa = 0.7 * 1.25 * Qrd / kr
    fsb = fys * Asl
    fsa = kcs * sa

    sb = 2 * sa * fsb / fsa # retornado em cm
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

    ## capacidade de rotação, sem perda de resistencia na ligação
    ## para calculo do tetau - valores precisam estar em mm
    ## tetau retornado em radianos
    ## dui - capacidade de desolcamento da ligação inferior
    ## NBR8800 - R.2.5.2.2.3 - para ligação soldadas, capacidade dui = 0
    ## NBR8800 - R.2.5.2.3.3 - limite deslocamento horizontal da extremidade da mesa inferior dui = 3mm
    dui = 3
    tetau = round(( dus + dui + sb * 10) / ( h * 10 ), 5)
    ## converter radianos para m.rad
    tetau *=1000

    ## posição da linha neurtra plastica ylnp
    ## a partir da face inferior da viga
    ylnp = round((h*10 ) * dui / ( dus + dui + sb*10), 2) ## valor em mm

    mrd_neg = 0
    if (ylnp/10) >= tfi and (ylnp/10) <= (d - tfi):
        fat = bfs*tfs*(ylnp-tfs*.5) + ylnp*tw*ylnp*.5
        fac = bfi*tfi*(d-ylnp-tfi*.5) + (d-ylnp)*tw*(d-ylnp)*.5

        d3 = d - ylnp/10 + 7.5 + 3.5  # 3,5 cm cobrimento armaduras negativas

        mrd_neg = tds * d3 + fat + fac

    return (C1, tetau, ylnp, mrd_neg)


def inercia_equivalente_curta(vao, largInfluencia, interna, hdeck, d, tw, bfs,bfi, tfs,tfi, ia, aa, fck, fy, E):
    # print('inercia curta')
    Qrd = 70.7

    E = E / 10000
    vao *= 100
    largInfluencia *= 100

    ycgLaje = 7.5 + (hdeck - 75) * .05 # altura do centro geometrico da laje
    tc = (hdeck - 75) / 10 #6.5 # altura concreto laje steeldeck
    ds = yLaje = d * .5 + ycgLaje
    Ec = 4760 * ((10 * fck) ** 0.5) / 10. # kN/cm2
    RzE = E / (Ec)

    # regiao de momento positivo
    if interna == 1:
        larguraEfetivaPos = min(2 * 0.7 * vao / 8., largInfluencia)  # interno
    else:
        larguraEfetivaPos = min(2 * 0.8 * vao / 8., largInfluencia)  # extremo

    ## regiao momento positivo Curta Duração
    larguraTransformada = larguraEfetivaPos / RzE
    areaTransformada = larguraTransformada * tc
    inerciaLajeTransformada = larguraTransformada * tc ** 3 / 12.

    ay_pos = areaTransformada * ds
    ay2_pos = areaTransformada * ds ** 2

    fhrd = min(0.85 * fck * larguraEfetivaPos * tc / 1.4, aa * fy / 1.1)
    cd = round(fhrd * interacao / (Qrd), 0) * Qrd
    nn = cd / fhrd
    
    # LNP1
    a = cd / (0.85 * fck * larguraEfetivaPos / 1.4)
    af = tfs*bfs

    x2 = (- cd * 1.1 / fy + bfs * tfs + aa - af) / (bfs + bfi)

    mrd_pos = 0
    if x2 <= tfs:
        mrd_pos = cd * (hdeck/10. - a*.5 + x2) + (bfs*(x2**2/2 + (bfs-x2)**2/2)
                                                  + (d-tfs-tfi)*tw*(d/2-x2)
                                                  + bfi*tfi*(d-tfi*.5-x2)) * fy / 1.1

    else:        
        mrd_pos = cd * (hdeck/10. - a*.5 + x2) + (+ (d-tfs-tfi-x2)*tw*((d-tfs-tfi-x2)/2)
                                                  + bfi*tfi*(d-tfi*.5-x2)) * fy / 1.1

    wa = round(prop.wx(ia,d))
    
    areatotal_pos = areaTransformada + aa
    yg = ay_pos / areatotal_pos
    inerciaTotalPos = ia + inerciaLajeTransformada
    itr = ay2_pos + inerciaTotalPos - areatotal_pos * yg ** 2
    iefPosCurta = round(ia + (itr - ia) * ((nn) ** .5), 2)
    
    wtr = itr / (yg + d/2.)
    wef = round(wa + (wtr - wa) * ((nn) ** .5), 2)

##    print('\n')
##    print(larguraTransformada)
##    print(ay_pos)
##    print(areatotal_pos)
##    print(ay2_pos)
##    print(yg)
##    print(inerciaTotalPos)
##    print(itr)
##    print(nn,cd, fhrd)
##    print('\n')

    return iefPosCurta, mrd_pos, wef


def inercia_equivalente_longa(vao, vaoad, largInfluencia, interna, hdeck, d, tw, bfs,bfi, tfs,tfi, Asl, ia, aa, fck, fy, E):
    # print('inercia longa')

    E = E / 10000
    vao *= 100
    vaoad *= 100

    largInfluencia *= 100
    Qrd = 70.7
    larguraEfetiva = min((vao / 4 + vaoad / 4) * 2 / 8., largInfluencia)

    areaPerfil = round(prop.area(d, tw, bfs, tfs, bfi, tfi), 2)    
    ia = round(prop.i_x(d, tw, bfs, tfs, bfi, tfi), 2)
    wa = round(prop.wx(ia,d))

    ycgLaje = 7.5 + (hdeck - 75) * .05 # altura do centro geometrico da laje
    tc = (hdeck - 75) / 10 #6.5 # altura concreto laje steeldeck
    ds = yLaje = d * .5 + ycgLaje
    Ec = 4760 * ((10 * fck) ** 0.5) / 10. # kN/cm2
    RzE2 = E / (Ec/3)

    # regiao de momento positivo
    if interna == 1:
        larguraEfetivaPos = min(2 * 0.7 * vao / 8., largInfluencia)  # interno
    else:
        larguraEfetivaPos = min(2 * 0.8 * vao / 8., largInfluencia)  # extremo

    ##Propriedaedes elasticas
    ## regiao momento negativo
##    ay_neg = Asl * ds
##    ay2_neg = Asl * ds ** 2
##
##    areatotal_neg = aa + Asl
##    yg_neg = ay_neg / areatotal_neg
##    iefNeg = round(ia + ay2_neg - areatotal_neg * yg_neg ** 2, 2)

    ## regiao momento positivo Longa Duração
    larguraTransformada = larguraEfetivaPos / RzE2
    areaTransformada = larguraTransformada * tc
    inerciaLajeTransformada = larguraTransformada * tc ** 3 / 12.
    
    ay_pos = areaTransformada * yLaje
    ay2_pos = areaTransformada * yLaje ** 2

    fhrd = min(0.85 * fck * larguraEfetivaPos * tc / 1.4, aa * fy / 1.1)
    cd = round(fhrd * interacao / (Qrd), 0) * Qrd
    nn = cd / fhrd
    
    # LNP1
    a = cd / (0.85 * fck * larguraEfetivaPos / 1.4)
    af = tfs*bfs

    x2 = (- cd * 1.1 / fy + bfs * tfs + aa - af) / (2 * bfs)
##    print('\n x2 = %.2f \n' % x2)

    mrd_pos = 0
    if x2 <= tfs:
        mrd_pos = cd * (hdeck/10. - a*.5 + x2) + (bfs*(x2**2/2 + (bfs-x2)**2/2)
                                                  + (d-tfs - tfi)*tw*(d/2-x2)
                                                  + bfi*tfi*(d-tfi*.5-x2)) * fy / 1.1

    else:        
        mrd_pos = cd * (hdeck/10. - a*.5 + x2) + (+ (d-tfs - tfi-x2)*tw*((d-tfs-tfi-x2)/2)
                                                  + bfi*tfi*(d-tfi*.5-x2)) * fy / 1.1
        
    wa = round(prop.wx(ia,d))
    
    areatotal_pos = areaTransformada + aa
    yg = ay_pos / areatotal_pos

    inerciaTotalPos = ia + inerciaLajeTransformada
    itr = ay2_pos + inerciaTotalPos - areatotal_pos * yg ** 2
    iefPosLonga = round(ia + (itr - ia) * ((nn) ** .5), 2)
    
    wtr = itr / (yg + d/2.)
    wef = round(wa + (wtr - wa) * ((nn) ** .5), 2)

##    print('\n')
##    print('larguraEfetivaPos',larguraEfetivaPos )
##    print('larguraTransformada',larguraTransformada )
##    print('areatransformada',areaTransformada )
##    
##    print('yLaje',yLaje )
##    print('yg',yg )
##    print('itr',itr )
##    print('areatotal_pos',areatotal_pos )
##    print('iefPosLonga',iefPosLonga )
##    print('\n')

    return (iefPosLonga, mrd_pos, wef)
