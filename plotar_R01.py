import matplotlib.pyplot as plt

def plotar_diagramas(x, xn, xp, ypv, ypm, ypf,
                     listaCortantes, listaMomentos, listaMomentosPos, listaFlechas):
    #################################################################
    # Plotagem do diagrama de Cortante
    plt.subplot(311)
    for valor in listaCortantes:
        plt.text(valor[0], valor[1], '%.2f kN' % valor[1], fontsize=7)


    plt.plot(xp, ypv, 'b')
    plt.plot([x,xn],[0., 0.],'k')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.ylim(min(ypv)*1.5, max(ypv)*1.5)
    plt.legend(['V[x]'])
    plt.title('Cortante [kN], Momento [kN.m] Flecha [cm]')
    plt.grid()

    # Diagrama de Momento
    plt.subplot(312)
    for valor in listaMomentos:
        plt.text(valor[0], (-valor[1]*1.15), '%.2f kN.m' % valor[1], fontsize=7)
        
    for valor in listaMomentosPos:
        plt.text(valor[0], (-valor[1]*1.15), '%.2f kN.m' % valor[1], fontsize=7)
        
    plt.plot( xp, -ypm, 'k')
    plt.plot([x,xn],[0., 0.],'b')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.ylim(-max(ypm)*1.5, -min(ypm)*1.75)
    plt.legend(['M[x]'], loc = 'upper left' )
    plt.grid()

    # Diagrama de flechas
    plt.subplot(313)
##    print(listaFlechas)
    for valor in listaFlechas:
        plt.text(valor[0], -(valor[1]*1+0.1), '%.2f cm' % valor[1], fontsize=7)

    plt.plot( xp, -ypf*100, 'k')
    plt.plot([x,xn],[0., 0.],'b')
    plt.xlabel('x [m]')
    plt.ylabel('y [cm]')
    plt.ylim(-max(ypf)*175, 0.25)
    plt.legend(['f[x]'], loc = 'upper left' )    
    plt.grid()

    plt.show()








