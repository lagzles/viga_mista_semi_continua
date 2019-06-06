print('Aguarde uns instantes, enquanto o programa é iniciado')

from tkinter import *
from tkinter import messagebox, filedialog
import vm_db as datab
import vm_db_gerais as datab_gerais
import vm_db_relatorio as db_relatorio
import salvar_relatorio_R01 as salvar
import analise_r16 as analisar
import os


lista_n_vaos = []
lista_n_vaos2 = []
lista_n_mezx = []
lista_n_mezy = []
lista_n_check_e = []
lista_n_check_d = []
lista_n_var_e = []
lista_n_var_d = []
n_vaos = 0

trocar_text = False
root_box = None
root_gerais = None
root = None
n_vaos = 0
container_tramos = None
container_gerais = None
container_cargas = None
classe_agressividade = ''

steeldeck_str = ''
db = r'vmsc.db'
dbg = r'vmsc_g.db'
db_rel =  r'vmsc_relatorio.db'


def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def find_in_grid(frame, row, column):
    for children in frame.children.values():
        info = children.grid_info()
        try:
            if info['row'] == (row) and info['column'] == (column):
                return children
        except:
            a = 1
    return None

 
#######################################################################
#######################################################################
        

class Interface:
    def __init__(self, master):
        self.master = master
        global n_vaos
        master.title('Vigas Mistas Semi-Continuas (VMSC)')
        ss = 0
        # Cria os bancos de dados gerais
        datab.create_db(db)
        datab_gerais.create_db(dbg)        
        db_relatorio.create_db(db_rel)


        datab_gerais.insert_data(dbg, 'novo', 'fy', 34.5)           # kN/cm2
        datab_gerais.insert_data(dbg, 'novo', 'fys', 50.0)          # kN/cm2
        datab_gerais.insert_data(dbg, 'novo', 'fck', 2.5)           # kN/cm2
        datab_gerais.insert_data(dbg, 'novo', 'ha', 15.0)           # cm
        datab_gerais.insert_data(dbg, 'novo', 'e', 2.0*(10**8))     # kN/m2
        datab_gerais.insert_data(dbg, 'novo', 'es', 2.1*(10**8))    # kN/m2
        datab_gerais.insert_data(dbg, 'novo', 'G', 77.0*(10**8))    # kN/m2
        datab_gerais.insert_data(dbg, 'novo', 'classe_agressividade', 'forte' )    # kN/m2
        
        fy = datab_gerais.get_data(dbg, 'novo', 'fy')
        fck = datab_gerais.get_data(dbg, 'novo', 'fck')
        fys = datab_gerais.get_data(dbg, 'novo', 'fys')
        ha = datab_gerais.get_data(dbg, 'novo', 'ha')
        classe_agressividade = datab_gerais.get_data(dbg, 'novo', 'classe_agressividade')
        
        ############################################
        self.fonte = ("Verdana", "8")
        # Container contendo as Opões Gerais
        self.container_topo = Frame(master)  # 
        self.container_topo["pady"] = 10
        self.container_topo["padx"] = 10
        self.container_topo.pack(side=TOP)

        self.container_info = Frame(self.container_topo)
        self.container_info.pack(side=LEFT)
        
        self.container_nvaos = Frame(self.container_topo)
        self.container_nvaos["pady"] = 10
        self.container_nvaos["padx"] = 15
        self.container_nvaos.pack(side=LEFT)
        
        self.container_gerais = Frame(self.container_topo)
        self.container_gerais["pady"] = 10
        self.container_gerais["padx"] = 10
        self.container_gerais.pack(side=LEFT)
        
        global container_gerais
        container_gerais = self.container_gerais

        self.container_calculo = Frame(self.master)
        self.container_calculo["pady"] = 10
        self.container_calculo["padx"] = 10
        self.container_calculo.pack(side=LEFT)

        self.container_mid = Frame(master)
        self.container_mid["pady"] = 10
        self.container_mid["padx"] = 10
        self.container_mid.pack(side=LEFT)

        self.container_cargas = Frame(self.container_mid)
        self.container_cargas["pady"] = 10
        self.container_cargas["padx"] = 10
        self.container_cargas.pack()
        
        # Frame contendo os botões de definição dos tramos
        self.container_tramos = Frame(self.container_mid)
        self.container_tramos["pady"] = 10
        self.container_tramos["padx"] = 10
        self.container_tramos.pack_propagate(1)
        self.container_tramos.pack()

        global container_tramos
        container_tramos = self.container_tramos

        ###########################################################
        ## Container com informativos
        self.button_about = Button(self.container_info, text="Sobre?", command=lambda :mostrar_about_box())
        self.button_about.pack()  # grid(row=1, column=0)
        self.button_about.config(width=12)

        self.button_verification = Button(self.container_info, text="Verificações?", command=lambda :mostrar_verification_box())
        self.button_verification.pack()  # .grid(row=3, column=0)
        self.button_verification.config(width=12)

        #mostrar_verification_box
        ## Container com quantidade de vaos
        self.label_n_vaos = Label(self.container_nvaos, text='Número de Vãos', height=1).pack()  # .grid(row=0, column=1)

        self.variable = IntVar(master)
        self.variable.set(5)
        n_vaos = 5
        self.w = OptionMenu(self.container_nvaos, self.variable, 1,2,3,4,5,6,7,8,9,10,
                            command=lambda y: self.create_buttons(self.variable.get())) #command=lambda x: self.create_vaos_label(variable.get()))
        self.w.pack()  # .grid(row=1, column=1)
        self.w.config(width=9)

        ## Container com Propriedades Gerais
        
        self.label_fy = Label(self.container_gerais, text=('fy = {} kN/cm2'.format(fy)), height=1,width=15).grid(row=1, column=3)
        self.label_fys = Label(self.container_gerais, text=('fys = %.1f kN/cm2' % fys), height=1,width=15).grid(row=1, column=4)
        self.label_fck = Label(self.container_gerais, text=('fck = %.1f kN/cm2' % fck), height=1,width=15).grid(row=1, column=5)
        self.label_ha = Label(self.container_gerais, text=('ha = %.1f cm' % ha), height=1,width=15).grid(row=1, column=6)
        self.label_classe_agressividade = Label(self.container_gerais, text=('C.A. = %s' % classe_agressividade), height=1,width=15).grid(row=2, column=4)

        self.button_gerais = Button(self.container_gerais, text="Opções", command=lambda :self.opcoes_gerais())
        self.button_gerais.grid(row=1, column=7)
        
        ###################################################################################
        ## Container com botões de Cálculos
        self.button_calcular = Button(self.container_calculo, text="Calcular", command=lambda :self.calcular_sistema())
        self.button_calcular.config(width=12)
        self.button_calcular.grid(row=1, column=1)

        self.label_vazio41 = Label(self.container_calculo, text='\t', height=1).grid(row=8, column=1)

        self.label_diagramas = Label(self.container_calculo, text=('Diagramas:'), height=1).grid(row=4, column=1)
        self.label_vazio4 = Label(self.container_calculo, text='\t', height=1).grid(row=3, column=1)

        self.button_diagramasC = Button(self.container_calculo, text="Curta", command=lambda :self.calcular_diagramas('curta'))
        self.button_diagramasC.config(width=12)
        self.button_diagramasC.grid(row=5, column=1)
        
        self.button_diagramasL = Button(self.container_calculo, text="Longa", command=lambda :self.calcular_diagramas('longa'))
        self.button_diagramasL.config(width=12)
        self.button_diagramasL.grid(row=6, column=1)

        self.button_diagramasMD = Button(self.container_calculo, text="MD", command=lambda :self.calcular_diagramas('D'))
        self.button_diagramasMD.config(width=12)
        self.button_diagramasMD.grid(row=7, column=1)

        self.button_salvar = Button(self.container_calculo, text="Carregar", command=lambda : self.carregar())
        self.button_salvar.config(width=12)
        self.button_salvar.grid(row=9, column=1)

        self.button_salvar = Button(self.container_calculo, text="Salvar", command=lambda :self.salvar())
        self.button_salvar.config(width=12)
        self.button_salvar.grid(row=10, column=1)

        self.label_vazio00 = Label(self.container_calculo, text='novo', height=1).grid(row=11, column=1)
        
        ###################################################################################
        ## Começa com 4 botões já criados, pq sim
        ## Container de Tramos
        r = 8
        vao = 7.5
        binf = 2.5
        alma = 300
        mesa = 150
        tw = 4.75
        tfs = 6.35
        tfi = 6.35
        nb = 4
        fi = 1.25
        for i in range(5):
            c = i+2
            x = 0
            text = "%.0f\nVão=%.2fm \nb inf=%.2fm \n%.1fx%.1f \n%.2fx%.2fx%.2f\n%.0f # %.2f" % (i, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi)
            self.botao = Button(self.container_tramos, text=text,
                                command=lambda r=r,c=c: self.modificar_tramos(r,c))
            self.botao.grid(row=r, column=c)  # .pack(side = LEFT)
            self.botao.config(width=15)
            
            datab.insert_data(db, 'novo', i, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi)
        ###################################################################################
        global container_cargas
        container_cargas = self.container_cargas
        # valores de carregamentos/ geometrias para calculo
        self.label_carga_cp_sd = Label(self.container_cargas, text='P.P. Steel Deck', height=1,width=15).grid(row=3, column=3)
        steeldeckpp = StringVar(master)
        options = ['-.--', '0.80', '0.95', '1.25']        
        self.ww = OptionMenu(self.container_cargas, steeldeckpp, *options, command=lambda _: self.update_steel_deck(steeldeckpp.get()))
        steeldeckpp.set(options[0])
        self.ww.config(width=9)
        self.ww.grid(row=4, column=3)

        self.label_hdeck = Label(self.container_cargas, text='h deck [mm]', height=1,width=15).grid(row=3, column=4)
        self.text_hdeck = Entry(self.container_cargas, width=10)
        self.text_hdeck.insert(0, "140.0")
        self.text_hdeck.grid(row=4, column=4)
        
        self.label_carga_perm = Label(self.container_cargas, text='C.P. [kgf/m2]', height=1,width=15).grid(row=3, column=5)
        self.text_carga_perm = Entry(self.container_cargas, width=10)
        self.text_carga_perm.insert(0, "150.0")
        self.text_carga_perm.grid(row=4, column=5)
        
        self.label_sc_norma = Label(self.container_cargas, text='SC [kgf/m2]', height=1,width=15).grid(row=3, column=6)
        self.text_sc_norma = Entry(self.container_cargas, width=10)
        self.text_sc_norma.insert(0, "250.0")
        self.text_sc_norma.grid(row=4, column=6)
        
        
        ###################################################################################

    def update_steel_deck(self, n):
        global steeldeck_str
        steeldeck_str = n

    def create_buttons(self, n):
        master = self.master
        global n_vaos
        n_vaos = n
        r = 8
        for i in range(11):
            if i > 4:
                c = i + 2 - 5
                r = 9
            else:
                c = i+2
                r = 8
            butao = find_in_grid(self.container_tramos, r, c)
            if butao != None:
                butao.grid_forget()
                
        for i in range(n):            
            if datab.get_data(db, 'novo',i) != None:
                retorno = datab.get_data(db, 'novo',i)
                vao = float(retorno[2])
                binf = float(retorno[3])

                alma = float(retorno[4])
                mesa = float(retorno[5])
                
                tw = float(retorno[6])
                tfs = float(retorno[7])
                tfi = float(retorno[8])
                nb = float(retorno[9])
                fi = float(retorno[10])
                
            else:
                vao = 7.5
                binf = 2.5
                alma = 300
                mesa = 150
                tw = 4.75
                tfs = 6.35
                tfi = 6.35
                nb = 4
                fi = 1.25        
            if i > 4:
                c = i + 2 - 5
                r = 9
            else:                
                c = i+2
                r = 8
                
            x = 0
            text = "%.0f\nVão=%.2fm \nb inf=%.2fm \n%.2fx%.2f\n%.2fx%.2fx%.2f\n%.0f # %.2f" % (i, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi)
            self.botao = Button(self.container_tramos, text=text, command=lambda r=r,c=c: self.modificar_tramos(r,c))
            self.botao.grid(row=r, column=c)
            self.botao.config(width=15)
            datab.insert_data(db, 'novo', i, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi)

        # conta quantos perfis estão inseridos no banco de dados, e exclui os excedentes
        nf = datab.count_data(db, 'novo')
        if nf > n:
            for i in range(n, nf):
                datab.delete_data(db,i)
                

    def modificar_tramos(self, r, c):
        master = self.master
        root2 = Tk()
        global root_box
        root_box = root2

        try:
            butao = find_in_grid(self.container_tramos, r, c)
##            print('clicado \n%s' % butao['text'])
            texto = butao['text']
        except:
            True

        # Texto do botão contem todas informações do vão
        # indice, vao, numero de barras, geometria do perfil
        texto_split = texto.split('\n')       
        nb_fi = ((texto_split[-1].split('#')))        
        perfil_mesa_alma = ((texto_split[-3].split('x')))
        perfil_espessuras = ((texto_split[-2].split('x')))
        binf_split = ((texto_split[2].split('=')))        
        vao_split = ((texto_split[1].split('=')))
        
        indice = texto_split[0]
        vao = vao_split[1][0:-2]
        binf = binf_split[1][0:-2]
        alma = perfil_mesa_alma[0]
        mesa = perfil_mesa_alma[1]
        tw = perfil_espessuras[0]
        tfs = perfil_espessuras[1]
        tfi = perfil_espessuras[2]
        nb = nb_fi[0]
        fi = nb_fi[1]
        
        showbox = TramoBox(root2, r, c, indice, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi)
        center(root2)

    def opcoes_gerais(self):
        master = self.master
        root3 = Tk()
        global root_gerais
        root_gerais = root3
        showbox = GeraisBox(root3)

    def calcular_sistema(self):
        master = self.master
        root4 = Tk()
        global n_vaos
        nvaos = n_vaos

        steeldeck = steeldeck_str        
        dict_steel_deck = {'0.80': 295.05, '0.95': 296.21, '1.25': 298.54}
        if steeldeck_str != '':
            q_cpsd = dict_steel_deck[steeldeck_str] / 100.
            datab_gerais.insert_data(dbg, 'novo', 'SD', steeldeck) 
        else:
            q_cpsd = 0.0

        q_sc = float(self.text_sc_norma.get()) / 100.
        q_cp = float(self.text_carga_perm.get()) / 100.
        hdeck = float(self.text_hdeck.get())

        datab_gerais.insert_data(dbg, 'novo', 'q_cpsd', q_cpsd)      # kg/m2
        datab_gerais.insert_data(dbg, 'novo', 'q_cp', q_cp)          # kg/m2
        datab_gerais.insert_data(dbg, 'novo', 'q_sc', q_sc)          # kg/m2
        datab_gerais.insert_data(dbg, 'novo', 'hdeck', hdeck)        # cm
        datab_gerais.insert_data(dbg, 'novo', 'deck', steeldeck_str) # cm
        datab_gerais.insert_data(dbg, 'novo', 'n_vaos', n_vaos)
        
        print('\nCalcular')
        lista_vaos = []
        ppi = ppf = pp =  binff = binfi = bInfl = 0

        retorno = analisar.analisar_sistema(n_vaos, hdeck, q_cp, q_cpsd, q_sc, 1.0)

        showbox = RetornoBox(root4, retorno)
        center(root4)

    def calcular_diagramas(self, carregamento):
        master = self.master
        global n_vaos
        nvaos = n_vaos

        steeldeck = steeldeck_str        
        dict_steel_deck = {'0.80': 295.05, '0.95': 296.21, '1.25': 298.54}
        if steeldeck_str != '':
            q_cpsd = dict_steel_deck[steeldeck_str] / 100.
        else:
            q_cpsd = 0.0

        q_sc = float(self.text_sc_norma.get()) / 100.
        q_cp = float(self.text_carga_perm.get()) / 100.
        hdeck = float(self.text_hdeck.get())

        print('\nDiagrama')
        lista_vaos = []
##        ppi = ppf = pp = binff = binfi = bInfl = 0

        analisar.plotar_diagramas(n_vaos, hdeck, q_cp, q_cpsd, q_sc, 1.0, carregamento)

        
    def salvar(self):
        master = self.master
        steeldeck = steeldeck_str        
        dict_steel_deck = {'0.80': 295.05, '0.95': 296.21, '1.25': 298.54}
        if steeldeck_str != '':
            q_cpsd = dict_steel_deck[steeldeck_str] / 100.
            datab_gerais.insert_data(dbg, 'novo', 'SD', steeldeck) 
        else:
            q_cpsd = 0.0

        q_sc = float(self.text_sc_norma.get()) / 100.
        q_cp = float(self.text_carga_perm.get()) / 100.
        hdeck = float(self.text_hdeck.get())
        
        print('\nSalvar')
        root4 = Tk()
        center(root4)
        JanelaSalvar(root4, q_sc, q_cp, q_cpsd, hdeck, steeldeck_str)

    def carregar(self):
        master = self.master
        print('\nSalvar')
        root4 = Tk()
        center(root4)
        JanelaCarregar(root4)
        

        
#################################################################################################
class GeraisBox:
    def __init__(self, master):
        self.master = master
        self.master.title('Opções Gerais')
        
        fy = datab_gerais.get_data(dbg, 'novo', 'fy')
        fck = datab_gerais.get_data(dbg, 'novo', 'fck')
        fys = datab_gerais.get_data(dbg, 'novo', 'fys')
        ha = datab_gerais.get_data(dbg, 'novo', 'ha')
        es = datab_gerais.get_data(dbg, 'novo', 'es')
        e = datab_gerais.get_data(dbg, 'novo', 'e')
        g = datab_gerais.get_data(dbg, 'novo', 'G')
        classe_agressividade = datab_gerais.get_data(dbg, 'novo', 'classe_agressividade')

        var_fy = DoubleVar(master)
        var_fys = DoubleVar(master)
        var_fck = DoubleVar(master)
        var_ha = DoubleVar(master)
        var_es = DoubleVar(master)
        var_e = DoubleVar(master)
        var_g = DoubleVar(master)
        var_classe_agressividade = StringVar(master)

        var_fy.set(fy)
        var_fys.set(fys)
        var_fck.set(fck)
        var_ha.set(ha)
        var_es.set(es)
        var_e.set(e)
        var_g.set(g)
        var_classe_agressividade.set(classe_agressividade)

        self.fylabel = Label(master, text='fy [kN/cm2] =', height=1).grid(row=1, column=1)
        self.fytext = Entry(master, textvariable=var_fy, width=10)
        self.fytext.grid(row=1, column=2)
        
        self.fyslabel = Label(master, text='fys [kN/cm2] =', height=1).grid(row=2, column=1)
        self.fystext = Entry(master, textvariable=var_fys, width=10)
        self.fystext.grid(row=2, column=2)
        
        self.fcklabel = Label(master, text='fck [kN/cm2] =', height=1).grid(row=3, column=1)
        self.fcktext = Entry(master, textvariable=var_fck, width=10)
        self.fcktext.grid(row=3, column=2)
        
        self.halabel = Label(master, text='ha [cm] =', height=1).grid(row=4, column=1)
        self.hatext = Entry(master, textvariable=var_ha, width=10)
        self.hatext.grid(row=4, column=2)
        
        self.elabel = Label(master, text='E [kN/m2] =', height=1).grid(row=1, column=3)
        self.etext = Entry(master, textvariable=var_e, width=15)
        self.etext.grid(row=1, column=4)

        self.eslabel = Label(master, text='Es [kN/m2] =', height=1).grid(row=2, column=3)
        self.estext = Entry(master, textvariable=var_es, width=15)
        self.estext.grid(row=2, column=4)
        
        self.glabel = Label(master, text='G [kN/m2] =', height=1).grid(row=3, column=3)
        self.gtext = Entry(master, textvariable=var_g, width=15)
        self.gtext.grid(row=3, column=4)

        self.classe_agressividade = Label(master, text='C. Agressividade', height=1, width=20).grid(row=4, column=4)
        
        options = ['fraca', 'moderada', 'forte', 'muito forte']        
        self.ww = OptionMenu(master, var_classe_agressividade, *options, command=lambda _: update_classe_agressividade(master, var_classe_agressividade.get()))
        var_classe_agressividade.set(options[0])
        self.ww.config(width=9)
        self.ww.grid(row=5, column=4)

        self.button = Button(master, text="OK", command=lambda :fechar_gerais_box(self))
        self.button.grid(row=6, column=4)


        def update_classe_agressividade(self, n):
            global classe_agressividade
            classe_agressividade = n


        def fechar_gerais_box(self):
            global root_gerais
            global root
            master = self.master  # master do box do tramo
            master1 = root  # principal.master # master da GUI Principal
            
            fy = var_fy.get()
            fys = var_fys.get()
            fck = var_fck.get()
            ha = var_ha.get()
            es = var_es.get()
            e = var_e.get()
            g = var_g.get()
            classe_agressividade = var_classe_agressividade.get()

            try:
                datab_gerais.insert_data(dbg,'novo', 'fy', fy)
                datab_gerais.insert_data(dbg,'novo', 'fck', fck)
                datab_gerais.insert_data(dbg,'novo', 'fys', fys)
                datab_gerais.insert_data(dbg,'novo', 'ha', ha)
                datab_gerais.insert_data(dbg,'novo', 'es', es)
                datab_gerais.insert_data(dbg,'novo', 'e', e)
                datab_gerais.insert_data(dbg,'novo', 'G', g)
                datab_gerais.insert_data(dbg,'novo', 'classe_agressividade', classe_agressividade)
##                print(classe_agressividade)

                label = find_in_grid(container_gerais, 1, 3)
                label['text'] = 'fy = %.1f kN/cm2' % fy
                label = find_in_grid(container_gerais, 1, 4)
                label['text'] = 'fys = %.1f kN/cm2' % fys
                label = find_in_grid(container_gerais, 1, 5)
                label['text'] = ('fck = %.1f kN/cm2' % fck)
                label = find_in_grid(container_gerais, 1, 6)
                label['text'] = ('ha = %.1f cm' % ha)
                label = find_in_grid(container_gerais, 2, 4)
                label['text'] = ('C.A. = %s' % classe_agressividade)
                
            except Exception as e:
                print(e)
            root_gerais.destroy()
 
#################################################################################################
## GUI para preencher valores geometricos de cada tramo/vao da viga

class TramoBox:
    def __init__(self, masterr, r,c, n, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi):
        self.master = masterr
        self.master.title('Tramo - Viga Mista Semi-Continua')
        master = self.master

        var_indice = IntVar(master)
        var_binf = DoubleVar(master)
        var_nb = DoubleVar(master)
        var_fi = DoubleVar(master)
        var_alma = DoubleVar(master)
        var_mesa = DoubleVar(master)
        var_tw = DoubleVar(master)
        var_tfs = DoubleVar(master)
        var_tfi = DoubleVar(master)
        var_vao = DoubleVar(master)

        var_indice.set(n)
        var_vao.set(vao)
        var_binf.set(binf)
        var_alma.set(alma)
        var_mesa.set(mesa)
        var_tw.set(tw)
        var_tfs.set(tfs)
        var_tfi.set(tfi)
        var_nb.set(nb)
        var_fi.set(fi)
        
        self.vaolabel = Label(master, text='Vão [m] =', height=1).grid(row=1, column=1)
        self.vaotext = Entry(master, textvariable=var_vao, width=10)
        self.vaotext.grid(row=1, column=2)
        
        self.binflabel = Label(master, text='b inf [m] =', height=1).grid(row=2, column=1)
        self.binftext = Entry(master, textvariable=var_binf, width=10)
        self.binftext.grid(row=2, column=2)
        
        self.nblabel = Label(master, text='nb [un.] =', height=1).grid(row=3, column=1)
        self.nbtext = Entry(master, textvariable=var_nb, width=10)
        self.nbtext.grid(row=3, column=2)
        
        self.filabel = Label(master, text='fi [cm] =', height=1).grid(row=4, column=1)
        self.fitext = Entry(master, textvariable=var_fi, width=10)
        self.fitext.grid(row=4, column=2)
        
        self.almalabel = Label(master, text='alma [mm] =', height=1).grid(row=5, column=1)
        self.almatext = Entry(master, textvariable=var_alma, width=10)
        self.almatext.grid(row=5, column=2)

        self.label_vazio4 = Label(master, text='\t', height=1).grid(row=1, column=3)
        
        self.mesalabel = Label(master, text='mesa [mm] =', height=1).grid(row=1, column=4)
        self.mesatext = Entry(master, textvariable=var_mesa, width=10)
        self.mesatext.grid(row=1, column=5)

        self.twlabel = Label(master, text='tw [mm] =', height=1).grid(row=2, column=4)
        self.twtext = Entry(master, textvariable=var_tw, width=10)
        self.twtext.grid(row=2, column=5)

        self.tfslabel = Label(master, text='tfs [mm] =', height=1).grid(row=3, column=4)
        self.tfstext = Entry(master, textvariable=var_tfs, width=10)
        self.tfstext.grid(row=3, column=5)

        self.tfilabel = Label(master, text='tfi [mm] =', height=1).grid(row=4, column=4)
        self.tfitext = Entry(master, textvariable=var_tfi, width=10)
        self.tfitext.grid(row=4, column=5)

        self.label_vazio4 = Label(master, text='\t', height=1).grid(row=1, column=6)        

        self.button = Button(master, text="OK", command=lambda :fechar_tramo_box(self, r, c))
        self.button.grid(row=5, column=5)

        def fechar_tramo_box(self, r, c):
            master = self.master  # master do box do tramo
            global root
            master1 = root  #  master da GUI Principal
            global root_box
            
            indice = var_indice.get()
            vao = var_vao.get()
            binf = var_binf.get()
            alma = var_alma.get()
            mesa = var_mesa.get()
            fi = var_fi.get()
            nb = var_nb.get()
            tw = var_tw.get()
            tfs = var_tfs.get()
            tfi = var_tfi.get()

            try:
                butao = find_in_grid(container_tramos, r, c)
                butao['text'] = "%.0f \nVão=%.2fm \nb inf=%.2fm \n%.1fx%.1f \n%.2fx%.2fx%.2f\n %.0f # %.2f" % (indice, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi)
                datab.insert_data(db, 'novo', indice, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi)

##                datab.print_data(db)
            except Exception as e:
                print(e)
                True
            root_box.destroy()
            
#######################################################################
#######################################################################

class RetornoBox:
    def __init__(self, masterr, retorno):
        self.master = masterr
        self.master.title('Viga Mista Semi-Continua - Resumo Verificações')
        master = self.master

        fontsize1 = 10
        fontsize2 = 12

        Label(master, text='Nº tramo', height=2, font=("Arial", fontsize2)).grid(row=1, column=1)
        Label(master, text='1 Verificação', height=2, font=("Arial", fontsize2)).grid(row=2, column=1)
        Label(master, text='2 Verificação\nMesa\nAlma', height=5, font=("Arial", fontsize2)).grid(row=3, column=1)
        Label(master, text='3 Verificação', height=2, font=("Arial", fontsize2)).grid(row=4, column=1)
        Label(master, text='4 Verificação', height=2, font=("Arial", fontsize2)).grid(row=5, column=1)
        Label(master, text='5 Verificação', height=2, font=("Arial", fontsize2)).grid(row=6, column=1)
        Label(master, text='6 Verificação', height=2, font=("Arial", fontsize2)).grid(row=7, column=1)
        Label(master, text='7 Verificação', height=2, font=("Arial", fontsize2)).grid(row=8, column=1)
        Label(master, text='8 Verificação', height=2, font=("Arial", fontsize2)).grid(row=9, column=1)
##        Label(master, text='9 Verificação', height=1).grid(row=10, column=1)
        Label(master, text='10 Verificação\nAsl\nBfi', height=5, font=("Arial", fontsize2)).grid(row=10, column=1)
        Label(master, text='11 Verificação\nFlecha', height=2, font=("Arial", fontsize2)).grid(row=11, column=1)
        Label(master, text='12 Verificação\nVibração', height=2, font=("Arial", fontsize2)).grid(row=12, column=1)
        Label(master, text='13 Verificação\nFissuração', height=2, font=("Arial", fontsize2)).grid(row=13, column=1)
        Label(master, text='Peso perfil', height=2, font=("Arial", fontsize2)).grid(row=15, column=1)
        Label(master, text='Peso Barras', height=2, font=("Arial", fontsize2)).grid(row=16, column=1)
        Label(master, text='Peso cantoneiras', height=2, font=("Arial", fontsize2)).grid(row=17, column=1)
        Label(master, text='Peso Conjunto', height=2, font=("Arial", fontsize2)).grid(row=18, column=1)

        for i in range(len(retorno)):
            fg1="black"
            fg2="black"
            fg3="black"
            fg4="black"
            fg5="black"
            fg6="black"
            fg7="black"
            fg8="black"
            fg10="black"
            fg11="black"
            fg12="black"
            fg13="black"
            Label(master, text=retorno[i][0].n,height=2).grid(row=1, column=2+i)
            if retorno[i][1][0] > 1.03 or retorno[i][1][1]> 1.03:
                fg1="red"
            if float(retorno[i][2][0]) > float(retorno[i][2][1]) or float(retorno[i][2][2]) > float(retorno[i][2][3]):
                fg2="red"
            if float(retorno[i][3][0]) > 1.03:
                fg3="red"
            if float(retorno[i][4][2]) > 1.03:
                fg4="red"
            if float(retorno[i][5][2]) > 1.03:
                fg5="red"
            if float(retorno[i][6][2]) > 1.03:
                fg6="red"
            if float(retorno[i][7][2]) > 1.03:
                fg7="red"
            if float(retorno[i][8][2]) > 1.03:
                fg8="red"
            if float(retorno[i][10][0]) > 1.03 or float(retorno[i][10][1]) > 1.03 or float(retorno[i][10][2]) > 1.03:
                fg10="red"
            if float(retorno[i][11][0]) > 1.03:
                fg11="red"
            if float(retorno[i][12][0]) > 1.03:
                fg12="red"
            if float(retorno[i][13][0]) > 1.03:
                fg13="red"
                
            Label(master, text='{:.2%} / {:.2%}'.format(retorno[i][1][0],retorno[i][1][1]),height=2,width=15, fg=fg1).grid(row=2, column=2+i)
            Label(master, text='\n{:.4} / {:.4}\n{:.4} / {:.4}'.format(retorno[i][2][0],retorno[i][2][1],retorno[i][2][2],retorno[i][2][3]),height=5,width=15, fg=fg2).grid(row=3, column=2+i)
            Label(master, text='{:.2%}'.format(float(retorno[i][3][0])),height=2,width=15, fg=fg3).grid(row=4, column=2+i)
            Label(master, text='{:.2%}'.format(float(retorno[i][4][2])),height=2,width=15, fg=fg4).grid(row=5, column=2+i)
            Label(master, text='{:.2%}'.format(float(retorno[i][5][2])),height=2,width=15, fg=fg5).grid(row=6, column=2+i)
            Label(master, text='{:.2%}'.format(float(retorno[i][6][2])),height=2,width=15, fg=fg6).grid(row=7, column=2+i)
            Label(master, text='{:.2%}'.format(float(retorno[i][7][2])),height=2,width=15, fg=fg7).grid(row=8, column=2+i)
            Label(master, text='{:.2%}'.format(float(retorno[i][8][2])),height=2,width=15, fg=fg8).grid(row=9, column=2+i)
            Label(master, text='\n{:.2%}\n{:.2%}\n{:.2%}'.format(float(retorno[i][10][0]),
                                                                 float(retorno[i][10][1]),
                                                                 float(retorno[i][10][2])),height=5,width=15, fg=fg10).grid(row=10, column=2+i)
            Label(master, text='{:.2%}'.format(float(retorno[i][11][0])),height=2,width=15).grid(row=11, column=2+i)
            Label(master, text='{:.2%}'.format(float(retorno[i][12][0])),height=2,width=15).grid(row=12, column=2+i)
            Label(master, text='{:.2%}'.format(float(retorno[i][13][0])),height=2,width=15).grid(row=13, column=2+i)
            Label(master, text='\t',height=2,width=15).grid(row=14, column=2+i)
            Label(master, text='{:.2f}kg'.format(float(retorno[i][14][0])),height=2,width=15).grid(row=15, column=2+i)
            Label(master, text='{:.2f}kg'.format(float(retorno[i][14][1])),height=2,width=15).grid(row=16, column=2+i)
            Label(master, text='{:.2f}kg'.format(float(retorno[i][14][2])),height=2,width=15).grid(row=17, column=2+i)
            Label(master, text='{:.2f}kg'.format(float(retorno[i][14][0])+float(retorno[i][14][1])+float(retorno[i][14][2])),height=2,width=15).grid(row=18, column=2+i)
            

        Label(master, text="\t", height=2).grid(row=2, column=0)
        Label(master, text="\t", height=2).grid(row=0, column=0)
        Label(master, text="\t", height=2).grid(row=1, column=len(retorno)+3)
        Label(master, text="\t", height=2).grid(row=19, column=len(retorno)+3)

        self.button_about = Button(master, text="?", command=lambda :mostrar_verification_box())
        self.button_about.grid(row=1, column=0)


        self.button_salvar = Button(master, text="Salvar", command=lambda :self.Salvar())
        self.button_salvar.config(width=12)
        self.button_salvar.grid(row=0, column=1)

    def Salvar(self):
        currdir = os.getcwd()
        tempdir = filedialog.asksaveasfilename(parent=root,
                                               initialdir=currdir,
                                               title='Please select a directory',
                                               filetypes = (("Arquivos doc","*.doc"),("Toudos","*.*")))

        if (tempdir[-4:-1]+tempdir[-1]) != '.doc':
            tempdir += '.doc'
            
        if len(tempdir) > 0:
            print("You chose %s" % tempdir)

        if salvar.relatorio(tempdir):
            messagebox.showinfo("Salvar Relatorio", "Relatorio Criado com sucesso.")
        else:
            messagebox.showinfo("Mensagem de ERRO!","Erro ao salvar Relatorio.")


#######################################################################

class JanelaSalvar():
    def __init__(self, master, q_sc, q_cp, q_cpsd, hdeck, steeldeck_str):
        self.master = master
        self.master.title('Salvar Dados')
        master = self.master

        self.var_nome = StringVar(master)
        
        self.nomelabel = Label(master, text='Nome =', height=1).grid(row=1, column=1)
        self.nometext = Entry(master, textvariable=self.var_nome, width=10)
        self.nometext.grid(row=1, column=2)

        self.button_about = Button(master, text="Salvar", command=lambda :self.salvar_obra(q_sc, q_cp, q_cpsd, hdeck, steeldeck_str))
        self.button_about.grid(row=2, column=2)


    def salvar_obra(self, q_sc, q_cp, q_cpsd, hdeck, steeldeck_str):
        nome = self.var_nome.get()        
        global n_vaos

        print('Dados gerais')
        try:
            fy =  datab_gerais.get_data(dbg, 'novo', 'fy')
            fck = datab_gerais.get_data(dbg, 'novo', 'fck')
            fys = datab_gerais.get_data(dbg, 'novo', 'fys')
            ha =  datab_gerais.get_data(dbg, 'novo', 'ha')
            es =  datab_gerais.get_data(dbg, 'novo', 'es')
            e =   datab_gerais.get_data(dbg, 'novo', 'e')
            g =   datab_gerais.get_data(dbg, 'novo', 'G')
            classe_agressividade = datab_gerais.get_data(dbg,'novo', 'classe_agressividade')
        
            datab_gerais.insert_data(dbg, nome, 'fy', fy)
            datab_gerais.insert_data(dbg, nome, 'fck', fck)
            datab_gerais.insert_data(dbg, nome, 'fys', fys)
            datab_gerais.insert_data(dbg, nome, 'ha', ha)
            datab_gerais.insert_data(dbg, nome, 'es', es)
            datab_gerais.insert_data(dbg, nome, 'e', e)
            datab_gerais.insert_data(dbg, nome, 'G', g)
            datab_gerais.insert_data(dbg, nome, 'classe_agressividade', classe_agressividade)

            datab_gerais.insert_data(dbg, nome, 'q_cpsd', q_cpsd)      # kg/m2
            datab_gerais.insert_data(dbg, nome, 'q_cp', q_cp)          # kg/m2
            datab_gerais.insert_data(dbg, nome, 'q_sc', q_sc)          # kg/m2
            datab_gerais.insert_data(dbg, nome, 'hdeck', hdeck)        # cm
            datab_gerais.insert_data(dbg, nome, 'deck', steeldeck_str)        # cm

            datab_gerais.insert_data(dbg, nome, 'n_vaos', n_vaos)
            
        except Exception as e:
            print(e, 'salvar gerais')
            
        print('Dados tramos', nome)
        try:
            for i in range(n_vaos):
                retorno = datab.get_data(db,'novo',i)
                vao = float(retorno[2])                
                binf = float(retorno[3])

                d = float(retorno[4])
                bf = float(retorno[5])
                tw = float(retorno[6])
                tfs = float(retorno[7])
                tfi = float(retorno[8])

                nb = float(retorno[9])
                fi = float(retorno[10])

                inserir = datab.insert_data(db, nome,
                                  i,
                                  vao,
                                  binf,
                                  d,
                                  bf,
                                  tw,
                                  tfs,
                                  tfi,
                                  nb,
                                  fi)

##                print(inserir)
        except Exception as e:
            print(e, 'salvar tramos')

        self.master.destroy()
        


class JanelaCarregar():
    def __init__(self, master):
        self.master = master
##        global container_tramos
        self.master.title('Carregar Dados')
        master = self.master

        retorno = datab_gerais.get_obras(dbg)

        self.var_nome = StringVar(master)

        self.label_n_vaos = Label(master, text='Obras Salvas:', height=1).pack()  # .grid(row=0, column=1)


        n_vaos = 5
        self.w = OptionMenu(master, self.var_nome, *retorno)
        self.w.pack()
        self.w.config(width=9)
        
        self.button_about = Button(master, text="Carregar", command=lambda :self.carregar_obra(self.var_nome.get()))
        self.button_about.pack()

    def carregar_obra(self, nome):
        print('Carregar', nome)
        global my_gui
        global n_vaos

        labeu = find_in_grid(my_gui.container_calculo, 11, 1)
        labeu['text'] = nome
        
        try:
            
            n =   datab_gerais.get_data(dbg, nome, 'n_vaos')
            fy =  datab_gerais.get_data(dbg, nome, 'fy')
            fck = datab_gerais.get_data(dbg, nome, 'fck')
            fys = datab_gerais.get_data(dbg, nome, 'fys')
            ha =  datab_gerais.get_data(dbg, nome, 'ha')
            es =  datab_gerais.get_data(dbg, nome, 'es')
            e =   datab_gerais.get_data(dbg, nome, 'e')
            g =   datab_gerais.get_data(dbg, nome, 'G')
            classe_agressividade = datab_gerais.get_data(dbg, nome, 'classe_agressividade')

            q_cpsd = datab_gerais.get_data(dbg, nome, 'q_cpsd')      # kg/m2
            q_cp = datab_gerais.get_data(dbg, nome, 'q_cp')          # kg/m2
            q_sc = datab_gerais.get_data(dbg, nome, 'q_sc')          # kg/m2
            hdeck = datab_gerais.get_data(dbg, nome, 'hdeck')        # cm
            steeldeck_str = datab_gerais.get_data(dbg, nome, 'deck')

            n_vaos = int(n)

            datab_gerais.insert_data(dbg,'novo', 'fy', fy)
            datab_gerais.insert_data(dbg,'novo', 'fck', fck)
            datab_gerais.insert_data(dbg,'novo', 'fys', fys)
            datab_gerais.insert_data(dbg,'novo', 'ha', ha)
            datab_gerais.insert_data(dbg,'novo', 'es', es)
            datab_gerais.insert_data(dbg,'novo', 'e', e)
            datab_gerais.insert_data(dbg,'novo', 'G', g)
            datab_gerais.insert_data(dbg,'novo', 'classe_agressividade', classe_agressividade)

            label = find_in_grid(container_gerais, 1, 3)
            label['text'] = 'fy = %.1f kN/cm2' % fy
            label = find_in_grid(container_gerais, 1, 4)
            label['text'] = 'fys = %.1f kN/cm2' % fys
            label = find_in_grid(container_gerais, 1, 5)
            label['text'] = ('fck = %.1f kN/cm2' % fck)
            label = find_in_grid(container_gerais, 1, 6)
            label['text'] = ('ha = %.1f cm' % ha)
            label = find_in_grid(container_gerais, 2, 4)
            label['text'] = ('C.A. = %s' % classe_agressividade)

            label = find_in_grid(container_cargas, 4, 4)
            label.delete(0, END)
            label.insert(0, hdeck)

            label = find_in_grid(container_cargas, 4, 5)
            label.delete(0, END)
            label.insert(0, str(round(q_cp*100,2)))
##            print(q_cp)

            label = find_in_grid(container_cargas, 4, 6)
            label.delete(0, END)
            label.insert(0, str(round(q_sc*100,2)))
            
        except Exception as e:
            print(e,'carregar gerais')


        for i in range(11):
            if i > 4:
                c = i + 2 - 5
                r = 9
            else:
                c = i+2
                r = 8
            butao = find_in_grid(container_tramos, r, c)
            if butao != None:
                butao.grid_forget()
               
        for i in range(int(n)):
            if datab.get_data(db, nome, i) != None:
                retorno = datab.get_data(db, nome,i)
                vao = float(retorno[2])
                binf = float(retorno[3])

                alma = float(retorno[4])
                mesa = float(retorno[5])
                
                tw = float(retorno[6])
                tfs = float(retorno[7])
                tfi = float(retorno[8])
                nb = float(retorno[9])
                fi = float(retorno[10])
  
            if i > 4:
                c = i + 2 - 5
                r = 9
            else: 
                c = i+2
                r = 8

            x = 0
            global root

            my_gui.variable.set(n)
            text = "%.0f\nVão=%.2fm \nb inf=%.2fm \n%.2fx%.2f\n%.2fx%.2fx%.2f\n%.0f # %.2f" % (i, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi)
            botao = Button(container_tramos, text=text, command=lambda r=r,c=c: my_gui.modificar_tramos(r,c))
            botao.grid(row=r, column=c)
            botao.config(width=15)
            datab.insert_data(db, 'novo', i, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi)

            try:
                butao = find_in_grid(container_tramos, r, c)
                butao['text'] = "%.0f \nVão=%.2fm \nb inf=%.2fm \n%.1fx%.1f \n%.2fx%.2fx%.2f\n %.0f # %.2f" % (i, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi)
                datab.insert_data(db, 'novo', i, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi)
            except Exception as e:
                print(e,'carregar tramos')
                
        for i in range(int(n), 11):
            if i > 4:
                c = i + 2 - 5
                r = 9
            else:
                c = i+2
                r = 8
            butao = find_in_grid(container_tramos, r, c)
            if butao != None:
                print('botao esquecido')
                butao.grid_forget()
   

        self.master.destroy()


        
#######################################################################

def mostrar_about_box():
    messagebox.showinfo("About Box", """Programa desenvolvido para calculo de vigas mistas semi-continuas
Informações sobre o programa:
    - Numero maximo de 10 vãos;
    - Separador decimal '.'(ponto)
    - Vigas com mesas de mesma largura
    - Calculo de vigas secundárias, com cargas distribuidas uniformemente.
    - Método de calculo: Metodo dos deslocamentos

-Botão 'Calcular' realiza as verificações e apresenta os resultados
 das verificações.

-Botão 'Salvar' realiza as verificações e salva em um arquivo de texto.

-Botão 'Curta' Apresenta os diagramas de Momento e Cortante, para o
 carregamento de curta duração (Sobrecarga de utilidade depois da Cura)

-Botão 'Longa' Apresenta os diagramas de Momento e Cortante, para o
 carregamento de Longa duração (Carga Permanente depois da Cura)

-Botão 'MD' Apresenta os diagramas de Momento e Cortante, para a
 combinação de carregamento depois da cura
 ((1.2 * (cp + cpsd) + 1.6 * sc) * infl + 1.2 * pp)
 onde:
     infl: largura de influência
     pp: peso próprio da viga
     cp: carga permanente
     cpsd: carga permanente do steel deck
     sc: sobrecarga

Bibliografia:
QUEIROZ, Gilson; PIMENTA, Roberval J; MARTINS, Alexander J. Estruturas mistas
Volume 2. Rio de Janeiro: CBCA, 2010.

ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. NBR 8800. Projeto de estruturas de
aço e de estruturas mistas de aço e concreto de edifícios. Rio de Janeiro, 2008.

CHRISTOFORO, André; LAHR, Francisco A. R.; Avaliação da Rigidez Rotacional em
Estruturas Planas de Madeira Concebidas por Elementos Unidimensionais com dois
Parafusos por nó. São Carlos, 2003. 
    """)

def mostrar_verification_box():
    messagebox.showinfo("Box das Verificações", """Programa desenvolvido para calculo de vigas mistas semi-continuas
Os cálculos são realizados utilizando o metodo dos deslocamentos.


Informações sobre as verificações realizadas:
    - 1 Verificação: Cargas antes da cura
    - 2 Verificação: Esbeltez da seção
                     (NBR8800/2008 O.1.1.2.d)
    - 3 Verificação: Momento Positivo Reduzido
                     (NBR8800/2008 O.2.3)
    - 4 Verificação: Cortante
                     (NBR8800/2008 O.3)
    - 5 Verificação: Capacidade de Rotação x Rotação Necessária
                     (NBR8800/2008 Tabela R.3)
    - 6 Verificação: Flambagem lateral com distorção da
      Seção Transversal (NBR8800/2008 O.2.5)
    - 7 Verificação: Numero de Conectores
                     (NBR8800/2008 O.2.4.3)
    - 8 Verificação: Cisalhamento Longitudinal da Laje
                     (NBR8800/2008 O.1.3.4)
    - 9 Verificação: Relação entre Momento Resistivo Negativo/Positivo
    - 10 Verificação: Limitação das tensões de serviço
      (combinação rara de ações)
    - 11 Verificação: Flecha/Deslocamentos
    - 12 Verificação: Estado Limite de Vibração Excessiva
    - 13 Verificação: Fissuração do Concreto sobre os Apoios
    """)



try: 
    root = Tk()
    my_gui = Interface(root)

##    center(root)
    root.mainloop()
except Exception as e:
    print('loop da GUI', e)


