import numpy as np
from tramos_r02 import Tramos 
from numpy.linalg import inv

n_vaos = int(input("Inserir quantidade de vaos:  "))

n_list = []
lista_tramos = []

ponta_esq = "ponta_esquerda"
ponta_dir = "ponta_direita"
intermediario = "intermediario"

i = 0.00015254 # m4 ## I = 15254 # cm4
e = 2.0 * (10 ** 8) # kN/m2 ##E = 200000 # MPa

q = 2. # kN/m
k = 25000 # kN.m/rad
ei = e * i#30508 # kN.m2

for j in range(n_vaos):
    vao = (float(input("Inserir valor do %.0f vao:  " % (j +1))))
    if j == 0:
        print("esquerda")
        lista_tramos.append(Tramos(vao, i, e, ponta_esq))
    elif j == n_vaos - 1:
        print("direita")
        lista_tramos.append(Tramos(vao, i, e, ponta_dir))
    else:
        print("intermed")
        lista_tramos.append(Tramos(vao, i, e, intermediario))

n = len(lista_tramos)

kij = np.zeros((n+1,n+1))
f_ep = np.zeros((n+1,1))

# determinaçao da matriz de rigidez
for j in range(n):
    tramo = lista_tramos[j]
    tramo.calc(q)
##    print(j)
    if tramo.situacao == ponta_esq:
        # caso o o tramo seja o primeiro tramo, ou seja, o da extrema esquerda
        # momento na rotação unitaria do primeiro apoio
        kij[0][0] += tramo.me_1 # apoio da esquerda do 1 tramo
        kij[1][0] += tramo.md_1 # apoio da direita do 1 tramo

        # momento na rotação unitaria do segundo apoio
        kij[0][1] += tramo.me_2 # apoio da esquerda do 1 tramo
        kij[1][1] += tramo.md_2 # apoio da direita do 1 tramo

        #esforços de engaste perfeito nos apoios do primeiro tramo
        f_ep[0] += tramo.me_0 # primeiro apoio do sistema
        f_ep[1] += tramo.md_0 # segundo apoio do sistema
##        print(kij)
        
    elif tramo.situacao == ponta_dir:
        # caso o o tramo seja o ultimo tramo, ou seja, o da extrema direita
        # momento na rotação unitaria do penultimo apoio
        kij[n-1][n-1] += tramo.me_1 # apoio da esquerda
        kij[n][n-1] += tramo.md_1 # apoio da direita
        
        # momento na rotação unitaria do ultimo apoio 
        kij[n-1][n] += tramo.me_2
        kij[n][n] += tramo.md_2

        # esforços de engaste perfeito nos apoios do ultimo tramos
        f_ep[n-1] += tramo.me_0 # penultimo apoio do sistema
        f_ep[n] += tramo.md_0 # ultimo apoio do sistema
##        print(kij)
        
    elif tramo.situacao == intermediario:
        # caso o tramo seja itnermediario
        # momento na rotação unitaria do apoio da esquerda
        kij[j][j] += tramo.me_1 # apoio da esquerda
        kij[j+1][j] += tramo.md_1 # apoio da direita
        
        # momento na rotação unitaria do apoio da direita
        kij[j][j+1] += tramo.me_2
        kij[j+1][j+1] += tramo.md_2

        # esforços de engaste perfeito nos apoios do ultimo tramos
        f_ep[j] += tramo.me_0 # penultimo apoio do sistema
        f_ep[j+1] += tramo.md_0 # ultimo apoio do sistema
##        print(kij)

for j in range(1, n):
    print(j)
    kij[j][j] += k

kij_inv = inv(kij)
dij = kij_inv.dot(-f_ep)

print("**********")
print("k = ")
print(kij)
print("  ")
print("fep = ")
print(f_ep)
print("  ")
print("d = ")
print(dij)
print("**********")

# determinacao das reaçoes
reacoes = [0] * (n+1)
for j in range(1, n+1):
    tramo = lista_tramos[j-1]
    if tramo.situacao == ponta_esq:
        reacoes[0] += tramo.ve_0 + dij[0]*tramo.ve_1 + dij[1]*tramo.ve_2
        reacoes[1] += tramo.vd_0 + dij[0]*tramo.vd_1 + dij[1]*tramo.vd_2
    elif tramo.situacao == ponta_dir:
        reacoes[n-1] += tramo.ve_0 + dij[n-1]*tramo.ve_1 + dij[n]*tramo.ve_2
        reacoes[n] += tramo.vd_0 + dij[n-1]*tramo.vd_1 + dij[n]*tramo.vd_2
    elif tramo.situacao == intermediario:
        reacoes[j-1] += tramo.ve_0 + dij[j-1]*tramo.ve_1 + dij[j]*tramo.ve_2
        reacoes[j] += tramo.vd_0 + dij[j-1]*tramo.vd_1 + dij[j]*tramo.vd_2

print(reacoes)

print("ra = %0.2f, rb = %0.2f, rc=%0.2f" % (reacoes[0],reacoes[1],reacoes[2]))

print("##############################")




