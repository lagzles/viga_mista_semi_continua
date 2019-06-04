import matplotlib.pyplot as plt

def plotar_diagramas(x, xn, xp, ypv, ypm,
                     listaCortantes,listaMomentos, listaMomentosPos):
    #################################################################
        # Plotagem do diagrama de Cortante
    plt.subplot(211)
    for valor in listaCortantes:
        plt.text(valor[0], valor[1], '%.2f kN' % valor[1], fontsize=7)


    plt.plot(xp, ypv, 'b')
    plt.plot([x,xn],[0., 0.],'k')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.ylim(min(ypv)*1.5, max(ypv)*1.5)
    plt.legend(['V[x]'])
    plt.title('Cortante [kN] e Momento [kN.m]')
    plt.grid()

    # Diagrama de Momento
    plt.subplot(212)
    for valor in listaMomentos:
        plt.text(valor[0], -valor[1]*1.15, '%.2f kN' % valor[1], fontsize=7)
    for valor in listaMomentosPos:
        plt.text(valor[0], -valor[1]*1.15, '%.2f kN' % valor[1], fontsize=7)
    plt.plot( xp, -ypm, 'k')
    plt.plot([x,xn],[0., 0.],'b')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.ylim(-max(ypm)*1.5, -min(ypm)*2)
    plt.legend(['M[x]'], loc = 'upper left' )
    # plt.title('Momento')
    plt.grid()

    plt.show()








