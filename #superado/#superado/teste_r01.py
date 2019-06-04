import numpy as np
from tramos import Tramos 
from numpy.linalg import inv

n_vaos = int(input("Inserir quantidade de vaos:  "))

n_list = []
lista_tramos = []

ponta_esq = "ponta_esquerda"
ponta_dir = "ponta_direita"
intermediario = "intermediario"

i = 0.00015254 # m4 ## I = 15254 # cm4
e = 2.0 * (10 ** 8) # kN/m2 ##E = 200000 # MPa

for j in range(n_vaos):
    vao = (float(input("Inserir valor do %.0f vao:  " % (j +1))))
    if j == 0:
        lista_tramos.append(Tramos(vao, i, e, ponta_esq))
    elif j == n_vaos - 1:
        lista_tramos.append(Tramos(vao, i, e, ponta_dir))
    else:
        lista_tramos.append(Tramos(vao, i, e, intermediario))


q = 2. # kN/m
l1 = 5. #m
l2 = 7. #m

k = 25000 # kN.m/rad

ei = e * i#30508 # kN.m2

n = len(lista_tramos)

kij = np.zeros((n+1,n+1))
f_ep = np.zeros((n+1,1))

s11 = 4. * ei / l1
s12 = 2. * ei / l1

s11 = 4. * ei / l1
s12 = 2. * ei / l1
s13 = 0.

s21 = 2. * ei / l1 
s22 = 4. * ei / l1 + 4 * ei / l2
s23 = 2. * ei / l2

s31 = 0.0
s32 = 2. * ei / l2
s33 = 4. * ei / l2

fep1 = + q * (l1 ** 2) / 12.
fep2 = - q * (l1 ** 2) / 12. + q * (l2 ** 2) / 12.
fep3 = - q * (l2 ** 2) / 12.

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
        kij[j-1][j-1] += tramo.me_1 # apoio da esquerda
        kij[j][j-1] += tramo.md_1 # apoio da direita
        
        # momento na rotação unitaria do apoio da direita
        kij[j-1][j] += tramo.me_2
        kij[j][j] += tramo.md_2

        # esforços de engaste perfeito nos apoios do ultimo tramos
        f_ep[j-1] += tramo.me_0 # penultimo apoio do sistema
        f_ep[j] += tramo.md_0 # ultimo apoio do sistema
##        print(kij)

for j in range(1, n):
    kij[j][j] += k
    print(j)

kij_inv = inv(kij)
dij = kij_inv.dot(-f_ep)

print("**********")
print(kij)
print(f_ep)
print(dij)
print("**********")

fep = np.array([[fep1],
                [fep2],
                [fep3]])

sij = np.array([[s11, s12, s13],
                [s21, s22, s23],
                [s31, s32, s33]]) # *EI


sij[1][1] = sij[1][1] + k  # kelastico = 20.000,0  kN.m/rad
a = np.array([[0.0], [0], [0.0]]) # Forças externas
sij_inv = inv(sij)
d2 = sij_inv.dot(a - fep)

print(sij)
print(fep)
print(d2)
print("**********")
ra = 5 + (.24*d2[0] + .24*d2[1] + 0.00*d2[2])*ei
rb = 12 + (-.24*d2[0] + (-.24+.12245)*d2[1] + .12245*d2[2])*ei
rc = 7 + (0.00*d2[0] -.12245*d2[1] + -.12245*d2[2])*ei

mbe = - ra * l1 + q * (l1 ** 2) * 0.5
mbd = - ra * l1 + q * (l1 ** 2) * 0.5 - k * d2[1]

##print(d2)
print("ra = %0.2f, rb = %0.2f, rc=%0.2f" % (ra, rb, rc))
print("Mbe = %0.2f, Mbd = %0.2f" % (mbe, mbd))

print("##############################")




