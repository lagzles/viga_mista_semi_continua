from tkinter import Label, Button, INSERT, END, Checkbutton, IntVar, Tk, Entry
import tkinter as tk
from tkinter import messagebox
import dimensionamento_R01 as dim

class Interface:

    def __init__(self, master):
        self.master = master
        master.title('Calculo Vinculo Semi-Rigido')
        ss = 0

        self.label_vazio2 = Label(master, text='    ', height=1).grid(row=0, column=0)        
        self.label_vazio  = Label(master, text='    ', height=1).grid(row=0, column=4)
        self.label_vazio3 = Label(master, text='    ', height=1).grid(row=0, column=8)
        self.button_about = Button(master, text="Sobre", command=lambda :mostrar_about_box())
        self.button_about.grid(row=0, column=8)

        self.button_calc_c1 = Button(master, text="Calcular C1", command=self.calcular_C)
        self.button_calc_c1.grid(row=0, column=0)

        ## Vaos
        self.label_vao = Label(master, text='Vão [cm]=', height=1, justify=tk.LEFT).grid(row=0, column=1)
        self.text_vao = Entry(master, width=10, validatecommand=self.validate)
        self.text_vao.insert(0, "1000.0")
        self.text_vao.grid(row=0, column=2)
        
        self.label_vaoad = Label(master, text='Vão Adj. [cm]=', height=1, justify=tk.LEFT).grid(row=1, column=1)
        self.text_vaoad = Entry(master, width=10, validatecommand=self.validate)
        self.text_vaoad.insert(0, "1000.0")
        self.text_vaoad.grid(row=1, column=2)
        
        self.label_larg_inf = Label(master, text='Largura Infl [cm]=', height=1, justify=tk.LEFT).grid(row=2, column=1)
        self.text_larg_inf = Entry(master,  width=10)
        self.text_larg_inf.insert(0, "375.0")
        self.text_larg_inf.grid(row=2, column=2)

        self.var_interno = IntVar()
        self.var_interno.set(1)

        self.check_pil_borda = Checkbutton(master, text="Viga Interna?", variable=self.var_interno).grid(row=3, column=1)
        
##        self.label11 = Label(master, text='\t', height=1).grid(row=3, column=1)
##        self.label12 = Label(master, text='\t', height=1).grid(row=3, column=2)
        ##

        ## Dados Propriedades
        self.label_es = Label(master, text='Es [kN/cm2]=', height=1, justify=tk.LEFT).grid(row=1, column=7)
        self.text_es = Entry(master, width=10)
        self.text_es.insert(0, "21000.0")
        self.text_es.grid(row=1, column=8)
        
        self.label_e = Label(master, text='E [kN/cm2]=', height=1, justify=tk.LEFT).grid(row=2, column=7)
        self.text_e = Entry(master, width=10)
        self.text_e.insert(0, "20000.0")
        self.text_e.grid(row=2, column=8)
        
        self.label_fck = Label(master, text='fck [kN/cm2]=', height=1, justify=tk.LEFT).grid(row=3, column=7)
        self.text_fck = Entry(master, width=10)
        self.text_fck.insert(0, "2.0")
        self.text_fck.grid(row=3, column=8)
        
        self.label_fys = Label(master, text='fys [kN/cm2]=', height=1, justify=tk.LEFT).grid(row=4, column=7)
        self.text_fys = Entry(master, width=10)
        self.text_fys.insert(0, "50.0")
        self.text_fys.grid(row=4, column=8)
        
        self.label1 = Label(master, text='\t', height=1).grid(row=0, column=3)
        self.label2 = Label(master, text='\t', height=1).grid(row=1, column=3)
        self.label3 = Label(master, text='\t', height=1).grid(row=2, column=3)

        #Dados perfil
        self.label_d = Label(master, text='Altura Perfil [cm]=', height=1, justify=tk.LEFT).grid(row=0, column=4)
        self.text_d = Entry(master,  width=10)
        self.text_d.insert(0, "57.0")
        self.text_d.grid(row=0, column=5)

        self.label_bf = Label(master, text='Mesa Perfil [cm]=', height=1, justify=tk.LEFT).grid(row=1, column=4)
        self.text_bf = Entry(master,  width=10)
        self.text_bf.insert(0, "17.5")
        self.text_bf.grid(row=1, column=5)

        self.label_tf = Label(master, text='tf [cm]=', height=1, justify=tk.LEFT).grid(row=2, column=4)
        self.text_tf = Entry(master,  width=10)
        self.text_tf.insert(0, "0.8")
        self.text_tf.grid(row=2, column=5)

        self.label_tw = Label(master, text='tw [cm]=', height=1, justify=tk.LEFT).grid(row=3, column=4)
        self.text_tw = Entry(master,  width=10)
        self.text_tw.insert(0, "0.635")
        self.text_tw.grid(row=3, column=5)
        ##
        ## Dados Steel Deck
        self.label_hdeck = Label(master, text='Altura Laje [mm]=', height=1, justify=tk.LEFT).grid(row=4, column=4)
        self.text_hdeck = Entry(master,  width=10)
        self.text_hdeck.insert(0, "150.0")
        self.text_hdeck.grid(row=4, column=5)

        self.label_ha = Label(master, text='Tamanho do apoio [cm]=', height=1, justify=tk.LEFT).grid(row=5, column=4)
        self.text_ha = Entry(master,  width=10)
        self.text_ha.insert(0, "25.0")
        self.text_ha.grid(row=5, column=5)
        ##
        self.label5 = Label(master, text='\t', height=1).grid(row=6, column=4)
        self.label6 = Label(master, text='\t', height=1).grid(row=6, column=5)
        ## Dados da Armadura Negativa
        self.label_nas = Label(master, text='Numero de Barras [un]=', height=1, justify=tk.LEFT).grid(row=7, column=4)
        self.text_nas = Entry(master, width=5)
        self.text_nas.insert(0, "5")
        self.text_nas.grid(row=7, column=5)
        
        self.label_bitola = Label(master, text='Bitola Barras [mm]=', height=1, justify=tk.LEFT).grid(row=8, column=4)
        self.text_bitola = Entry(master, width=5)
        self.text_bitola.insert(0, "16.0")
        self.text_bitola.grid(row=8, column=5)

        self.label_c00 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=22, column=0)
        self.label_c01 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=22, column=1)
        self.label_c02 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=22, column=2)

        self.label_c10 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=23, column=0)
        self.label_c11 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=23, column=1)
        self.label_c12 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=23, column=2)

        self.label_c20 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=24, column=0)
        self.label_c21 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=24, column=1)
        self.label_c22 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=24, column=2)

        self.label_c30 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=22, column=4)
        self.label_c31 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=22, column=5)
        self.label_c32 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=22, column=6)

        self.label_c40 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=23, column=4)
        self.label_c41 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=23, column=5)
        self.label_c42 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=23, column=6)

        self.label_c50 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=24, column=4)
        self.label_c51 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=24, column=5)
        self.label_c52 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=24, column=6)

        self.label_c60 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=25, column=4)
        self.label_c61 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=25, column=5)
        self.label_c62 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=25, column=6)

        self.label_c70 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=26, column=4)
        self.label_c71 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=26, column=5)
        self.label_c72 = Label(master, text='\t', height=1, justify=tk.LEFT).grid(row=26, column=6)


    def calcular_C(self):
        master = self.master
        vao = float(self.text_vao.get())
        vaoad = float(self.text_vaoad.get())

        larginf = float(self.text_larg_inf.get())

        d = float(self.text_d.get())
        bf = float(self.text_bf.get())
        tf = float(self.text_tf.get())
        tw = float(self.text_tw.get())
        ha = float(self.text_ha.get())

        viga_interna = self.var_interno.get()
        
        hdeck = float(self.text_hdeck.get())
        bitola = float(self.text_bitola.get())
        nas = int(self.text_nas.get())
        es = float(self.text_es.get())
        e = float(self.text_e.get())    
        fck = float(self.text_fck.get())    
        fys = float(self.text_fys.get())

        asl = 3.14 * nas * (bitola / 20.) ** 2
        retorno = dim.calculo_C(es, e, asl, fck, fys, ha, d, bf, tw, tf, hdeck, vao, vaoad, larginf, viga_interna)

        self.setar_label_c1(retorno)

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False


    def setar_label_c1(self, lista):
        master = self.master
        self.label_c00 = Label(master, text='C = ', height=1, justify=tk.LEFT).grid(row=22, column=0)
        self.label_c01 = Label(master, text=str(lista[0]), height=1, justify=tk.LEFT).grid(row=22, column=1)
        self.label_c02 = Label(master, text='kNcm/rad', height=1, justify=tk.LEFT).grid(row=22, column=2)

        self.label_c10 = Label(master, text='teta u = ', height=1, justify=tk.LEFT).grid(row=23, column=0)
        self.label_c11 = Label(master, text=str(lista[1]), height=1, justify=tk.LEFT).grid(row=23, column=1)
        self.label_c12 = Label(master, text='mrad', height=1, justify=tk.LEFT).grid(row=23, column=2)

        self.label_c20 = Label(master, text='Ylnp = ', height=1, justify=tk.LEFT).grid(row=24, column=0)
        self.label_c21 = Label(master, text=str(lista[2]), height=1, justify=tk.LEFT).grid(row=24, column=1)
        self.label_c22 = Label(master, text='mm', height=1, justify=tk.LEFT).grid(row=24, column=2)

        self.label_c30 = Label(master, text='Ix  = ', height=1, justify=tk.LEFT).grid(row=22, column=4)
        self.label_c31 = Label(master, text=str(lista[3]), height=1, justify=tk.LEFT).grid(row=22, column=5)
        self.label_c32 = Label(master, text='cm4', height=1, justify=tk.LEFT).grid(row=22, column=6)
        
        self.label_c40 = Label(master, text='aa  = ', height=1, justify=tk.LEFT).grid(row=23, column=4)
        self.label_c41 = Label(master, text=str(lista[4]), height=1, justify=tk.LEFT).grid(row=23, column=5)
        self.label_c42 = Label(master, text='cm2', height=1, justify=tk.LEFT).grid(row=23, column=6)

        self.label_c50 = Label(master, text='Ief (-) = ', height=1, justify=tk.LEFT).grid(row=24, column=4)
        self.label_c51 = Label(master, text=str(lista[5]), height=1, justify=tk.LEFT).grid(row=24, column=5)
        self.label_c52 = Label(master, text='cm4', height=1, justify=tk.LEFT).grid(row=24, column=6)
        
        self.label_c60 = Label(master, text='Ief Longa (+) = ', height=1, justify=tk.LEFT).grid(row=25, column=4)
        self.label_c61 = Label(master, text=str(lista[6]), height=1, justify=tk.LEFT).grid(row=25, column=5)
        self.label_c62 = Label(master, text='cm4', height=1, justify=tk.LEFT).grid(row=25, column=6)
        
        self.label_c70 = Label(master, text='Ief Curta(+) = ', height=1, justify=tk.LEFT).grid(row=26, column=4)
        self.label_c71 = Label(master, text=str(lista[7]), height=1, justify=tk.LEFT).grid(row=26, column=5)
        self.label_c72 = Label(master, text='cm4', height=1, justify=tk.LEFT).grid(row=26, column=6)
        
            

 
def mostrar_about_box():
    messagebox.showinfo("About Box", """Programa desenvolvido para obtenção dos valores de vinculos semi-rigidos
Informações sobre o programa:

    - Stud Bolt = 19 mm
    - Resistência de conector = 70.7 kN
    - Considera-se uma interação parcial de 60%
    - Um conector por onda baixa do steel deck
    - kr definido como 1.000,0 kN/cm
    - Modulo de elasticidade do aço da armadura = 21.000,0 kN/cm2
    - Modulo de elasticidade do concreto = 4760 x (fck)^0.5 [MPa]
    - Modulo de elasticidade do aço do perfil = 200.000,0 kN/cm2
    
    - Resistencia de ruptura das cantoneiras = 45 kN/cm2
    - Espessura das cantoneiras = 9.5mm
    
    - Resistencia a ruptura dos parafusos [fub] = 82.5 kN/cm2
    - Linhas de parafusos na ligação = 2
    - Diametro dos parafusos na ligação = 19.05 mm
    - Espaçamento entre parafusos na direção da força [S] = 75 mm
    - Diamentro de referencia [dm] = 16mm

    - Capacidade de Rotação sem Perda de Resistencia na Ligação:
        - NBR8800 - R.2.3.1
        - NBR8800 - R.2.3.3
        - NBR8800 - R.2.4.3
        - NBR8800 - R.2.5.2    
        - NBR8800 - R.2.5.2.2.3
        - NBR8800 - R.2.5.2.3.3
    
    """  )


root = Tk()

my_gui = Interface(root)
root.mainloop()
