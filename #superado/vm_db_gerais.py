################# -*- coding: utf-8 -*-
import sqlite3
import os

##db = r'vmsc_g.db'
##db = r'vmsc.db'
##
####try:
####    conn = sqlite3.connect(db)
####    conn.text_factory = str
####    c = conn.cursor()
####    conn.execute("delete from vmsc")
####    conn.commit()
####    conn.close()
####except Exception as e:
##    print(e)



def create_db(db):
    try:
        if not os.path.isfile(db):
            conn = sqlite3.connect(db)
            c = conn.cursor()

            # Create table
            c.execute('''CREATE TABLE vmsc_g
                        (name TEXT, valor REAL)''')
            # Save (commit) the changes
            conn.commit()

            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()
            print('DB Gerais criado com sucesso')
        else:
            print('DB Gerais ok')
    except Exception as e:
        print(e)

    try:
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        conn.execute("delete from vmsc_g")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)


        
def insert_data(db, name, valor):
    try:
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        
        # Insert a row of data        
        c.execute('SELECT * FROM vmsc_g WHERE name=?', (name,))
        if c.fetchone() == None:
            c.execute("INSERT INTO vmsc_g VALUES (?,?)", (name, valor))

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
    

def get_data(db, item):
    # inserir nome do banco de dados e item a buscar
    # retorna o valor do caminho relacionado ao item
    t = (item,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('SELECT *FROM vmsc_g WHERE name=?', t)    
        caminho = c.fetchone()[1]
        conn.commit()
        conn.close()
        return caminho
    except Exception as e:
        print(e)
        print('Erro em buscar ', item)
        return ('Error', 'pegar data')

##
##db = r'vmsc.db'
##
##conn = sqlite3.connect(db)
##conn.text_factory = str
##c = conn.cursor()
##
##
##for row in c.execute('SELECT * FROM vmsc ORDER BY vao'):
##    print(row)
    
##print(conn.execute("delete from vmsc").rowcount)
##conn.execute("delete from vmsc")
##conn.commit()
##conn.close()
