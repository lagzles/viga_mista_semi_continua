################# -*- coding: utf-8 -*-
import sqlite3
import os

db = r'vmsc_relatorio.db'
 
def create_db(db):
    try:
        if not os.path.isfile(db):
            conn = sqlite3.connect(db)
            c = conn.cursor()

            # Create table
            c.execute('''CREATE TABLE vmsc_relatorio
                        (metodo TEXT, tramo TEXT, texto TEXT)''')
            # Save (commit) the changes
            conn.commit()

            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()
##            print(' ')
            
    except Exception as e:
        print(e)

    try:
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        conn.execute("delete from vmsc_relatorio")
        conn.commit()
        conn.close()
    except Exception as e:        
        print("Erro em: Limpar caso ja exista ",e)


        
def insert_data(db, metodo, tramo, valor):
    try:
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        
        # Insert a row of data        
        c.execute('SELECT * FROM vmsc_relatorio WHERE metodo=? AND tramo=?', (metodo, tramo,))
        if c.fetchone() == None:
            c.execute("INSERT INTO vmsc_relatorio VALUES (?,?,?)", (metodo, tramo, valor))

##            print('Criado')
            conn.commit()
            conn.close()
    
        else:
            t = ( valor, metodo, tramo,)
            c.execute('''UPDATE vmsc_relatorio SET texto = ? WHERE metodo=? AND tramo=?''', t)
##            print('Atualizado')
            conn.commit()
            conn.close()
            
    except Exception as e:
        print(e, metodo, tramo)
        return ('Error', ' inserir dados', (e, metodo, tramo))
    

def get_data(db, metodo, tramo):
    # inserir nome do banco de dados e item a buscar
    # retorna o valor do caminho relacionado ao item
    t = (metodo, tramo,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('SELECT *FROM vmsc_relatorio WHERE metodo=? AND tramo=?', t)    
        caminho = c.fetchone()[2]
        conn.commit()
        conn.close()
        return caminho
    except Exception as e:
        print(e)
        print('Erro em buscar ', metodo, " ", tramo)
        return ('Error', 'valores do metodo e tramo', e)

db = r'vmsc_relatorio.db'

######conn = sqlite3.connect(db)
######conn.text_factory = str
######c = conn.cursor()
######
########print(get_data(db, "Calculo do C","1"))
######
######for row in c.execute('SELECT * FROM vmsc_relatorio ORDER BY metodo'):
######    print(row[0], row[1], row[2])
######
######print(get_data(db, "Veriricacao", '1'))
######print(insert_data(db, "Veriricacao", '1', "dauisdhuiashduihasuidhiuahsd"))
######print(get_data(db, "Veriricacao", '1'))
##print(conn.execute("delete from vmsc").rowcount)
##conn.execute("delete from vmsc")
##conn.commit()
##conn.close()
