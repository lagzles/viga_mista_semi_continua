################# -*- coding: utf-8 -*-
import sqlite3
import os


def create_db(db):
    try:
        if not os.path.isfile(db):
            conn = sqlite3.connect(db)
            c = conn.cursor()

            # Create table
            c.execute('''CREATE TABLE vmsc_g
                        (obra text, name TEXT, valor REAL)''')
            # Save (commit) the changes
            conn.commit()

            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()
##            print(' ')
            
    except Exception as e:
        print('criar db gerais', e)

    try:
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        conn.execute("delete from vmsc_g WHERE obra='novo'")
        conn.commit()
        conn.close()
    except Exception as e:
        print('criar db gerais', e)


        
def insert_data(db, obra, name, valor):
    try:
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        
        # Insert a row of data        
        c.execute('SELECT * FROM vmsc_g WHERE name=? AND obra=?', (name, obra,))
        if c.fetchone() == None:
            c.execute("INSERT INTO vmsc_g VALUES (?,?,?)", (obra,name, valor))

##            print('Criado')
            conn.commit()
            conn.close()
    
        else:
            t = ( valor, name,)
            c.execute('''UPDATE vmsc_g SET valor = ? WHERE name=?''', t)
##            print('Atualizado')
            conn.commit()
            conn.close()
            
    except Exception as e:
        print(e, name, valor)
        return ('Error', 'inserir dados')


def get_data(db, obra, item):
    # inserir nome do banco de dados e item a buscar
    # retorna o valor do caminho relacionado ao item
    t = (obra,item,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('SELECT *FROM vmsc_g WHERE obra =? AND name=?', t)    
        caminho = c.fetchone()[2]
        conn.commit()
        conn.close()
        return caminho
    except Exception as e:
        print(e)
        print('Erro em buscar ', item)
        return ('Error', 'pegar data')

def get_obras(db):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT obra FROM vmsc_g ")
        itens = c.fetchall()

        lista = []
        for obra in itens:
            if obra[0] not in lista and obra[0]!='novo':
                lista.append(obra[0])

        conn.commit()
        conn.close()
        return lista
    except Exception as e:
        print(e)
        return None


######db = r'vmsc_g.db'
######
######conn = sqlite3.connect(db)
######conn.text_factory = str
######c = conn.cursor()
######
######
######for row in c.execute("SELECT * FROM vmsc_g ORDER BY obra"):
######    print(row)
######
######print('*'*40)
######for row in c.execute("SELECT obra FROM vmsc_g "):
######    print(row)
######
######c.execute("SELECT obra FROM vmsc_g ")
######itens = c.fetchall()
######print(itens)
######lista = []
######
######for obra in itens:
######    if obra[0] not in lista and obra[0]!='novo':
######        lista.append(obra[0])
######
######print(lista)
############    
##################print(conn.execute("delete from vmsc").rowcount)
##################conn.execute("delete from vmsc")
######conn.commit()
######conn.close()
