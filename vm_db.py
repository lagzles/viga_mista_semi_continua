################# -*- coding: utf-8 -*-
import sqlite3
import os

##db = r'caminhos.db'


db = r'vmsc.db'


def create_db(db):
    try:
        if not os.path.isfile(db):
            conn = sqlite3.connect(db)
            c = conn.cursor()

            # Create table
            c.execute('''CREATE TABLE vmsc
                        (
                         obra text, 
                         indice real,
                         vao real,
                         binf real,
                         alma real,
                         mesa real,
                         tw real,
                         tfs real,
                         tfi real,
                         nb real,
                         fi real,
                         v1a real,
                         v1b real,
                         v2almaa real,
                         v2almab real,
                         v2mesaa real,
                         v2mesab real,
                         v3 real,
                         v4 real,
                         v5 real,
                         v6 real,
                         v7 real,
                         v8 real,
                         v10a real,
                         v10b real,
                         v10c real)''')
            # Save (commit) the changes
            conn.commit()

            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()
        
            
    except Exception as e:
        print(e, 'Criar table vmsc')

    try:
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        conn.execute("delete from vmsc WHERE obra='novo'")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e, 'Limpar table vmsc')
      
        
def insert_data(db, obra, indice, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi):
    try:
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        
        # Insert a row of data        
        c.execute('SELECT * FROM vmsc WHERE indice=? AND obra=?', (indice, obra,))
##        print(obra)
        if c.fetchone() == None:
            c.execute("INSERT INTO vmsc VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (obra, indice, vao, binf,
                       alma, mesa, tw, tfs, tfi,
                       nb, fi,'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'))
##            print('Tramo %.0f Criado' % indice)

            conn.commit()
            conn.close()
            return True
    
        else:
            t = ( vao, binf, alma, mesa, tw, tfs, tfi, nb, fi, indice, obra,)
            c.execute('''UPDATE vmsc SET vao = ?,
                             binf = ?,
                             alma = ?,
                             mesa = ?,
                             tw = ?,
                             tfs = ?,
                             tfi = ?,
                             nb = ?,
                             fi = ?,
                         v1a = 0,
                         v1b = 0,
                         v2almaa = 0,
                         v2almab = 0,
                         v2mesaa = 0,
                         v2mesab = 0,
                         v3 = 0,
                         v4 = 0,
                         v5 = 0,
                         v6 = 0,
                         v7 = 0,
                         v8 = 0,
                         v10a = 0,
                         v10b = 0,
                         v10c = 0                           
                            WHERE indice=? AND obra=?''', t)
##            print('Tramo %.0f Atualizado' % indice)
            
            conn.commit()
            conn.close()

            db = r'vmsc.db'

            conn = sqlite3.connect(db)
            ##conn.text_factory = str
            c = conn.cursor()

##            for row in c.execute('SELECT * FROM vmsc ORDER BY vao'):
##                print(row)

            conn.close()
            return None
            
    except Exception as e:
        print(e, 'inserir dados vmsc')
        return ('Error', 'inserir dados')

def print_data(db):
    try:
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
       
        # Insert a row of data        
        for row in c.execute('SELECT * FROM vmsc ORDER BY indice'):
            print(row)
        
        conn.commit()
        conn.close()
            
    except Exception as e:
        print(e)
        return ('Error', 'inserir dados')

    

def get_data(db, obra, item):
    # inserir nome do banco de dados e item a buscar
    # retorna o valor do caminho relacionado ao item
    t = (obra,item,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute("SELECT *FROM vmsc WHERE obra=? AND indice=?", t)    
        caminho = c.fetchone()
        conn.commit()
        conn.close()
        return caminho
    
    except Exception as e:
        print(e)
        print('Erro em buscar ', item)
        return ('Error', 'pegar tramo')


def count_data(db, obra):    
    conn = sqlite3.connect(db)
    conn.text_factory = str
    c = conn.cursor()

    contador = 0
    try:
        for row in c.execute('SELECT * FROM vmsc WHERE obra=? ORDER BY vao', (obra,)):
            contador += 1

        return contador
    except Exception as e:
        print(e)
        return 0

def delete_data(db, item):
    t = (item,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str        
        c.execute('DELETE FROM vmsc WHERE indice=?', t) 
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em deletar ', item)
        return ('Error', 'deletar tramo')

##########
########db = r'vmsc.db'
########
########conn = sqlite3.connect(db)
##########conn.text_factory = str
########c = conn.cursor()
########
########for row in c.execute('SELECT * FROM vmsc ORDER BY vao'):
########    print(row)
########
########conn.close()
