################# -*- coding: utf-8 -*-
import sqlite3
import os

##db = r'caminhos.db'


db = r'vmsc.db'
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



####def create_db(db):
####    try:
####        if not os.path.isfile(db):
####            conn = sqlite3.connect(db)
####            c = conn.cursor()
####
####            # Create table
####            c.execute('''CREATE TABLE vmsc
####                        (
####                         indice real,
####                         vao real,
####                         binf real,
####                         alma real,
####                         mesa real,
####                         tw real,
####                         tfs real,
####                         tfi real,
####                         nb real,
####                         fi real)''')
####            # Save (commit) the changes
####            conn.commit()
####
####            # We can also close the connection if we are done with it.
####            # Just be sure any changes have been committed or they will be lost.
####            conn.close()
####            print('DB tramos criado com sucesso')
####        else:
####            print('DB tramos ok')
####            
####    except Exception as e:
####        print(e)
####
####    try:
####        conn = sqlite3.connect(db)
####        conn.text_factory = str
####        c = conn.cursor()
####        conn.execute("delete from vmsc")
####        conn.commit()
####        conn.close()
####    except Exception as e:
####        print(e)


def create_db(db):
    try:
        if not os.path.isfile(db):
            conn = sqlite3.connect(db)
            c = conn.cursor()

            # Create table
            c.execute('''CREATE TABLE vmsc
                        (
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
            print('DB tramos criado com sucesso')
        else:
            print('DB tramos ok')
            
    except Exception as e:
        print(e, 'Criar table vmsc')

    try:
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        conn.execute("delete from vmsc")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print(e, 'Limpar table vmsc')
        



        
def insert_data(db, indice, vao, binf, alma, mesa, tw, tfs, tfi, nb, fi):
    try:
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        
        # Insert a row of data        
        c.execute('SELECT * FROM vmsc WHERE indice=?', (indice,))
        if c.fetchone() == None:
            c.execute("INSERT INTO vmsc VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (indice, vao, binf,
                                                        alma, mesa, tw, tfs, tfi,
                                                        nb, fi,
                                                                        '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'))
            print('Tramo %.0f Criado' % indice)

            conn.commit()
            conn.close()
    
        else:
            t = ( vao, binf, alma, mesa, tw, tfs, tfi, nb, fi, indice,)
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
                            WHERE indice=?''', t)
            print('Tramo %.0f Atualizado' % indice)
            
            conn.commit()
            conn.close()
            
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

    

def get_data(db, item):
    # inserir nome do banco de dados e item a buscar
    # retorna o valor do caminho relacionado ao item
    t = (item,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('SELECT *FROM vmsc WHERE indice=?', t)    
        caminho = c.fetchone()
        conn.commit()
        conn.close()
        return caminho
    
    except Exception as e:
        print(e)
        print('Erro em buscar ', item)
        return ('Error', 'pegar tramo')

def count_data(db):    
    conn = sqlite3.connect(db)
    conn.text_factory = str
    c = conn.cursor()

    contador = 0
    try:
        for row in c.execute('SELECT * FROM vmsc ORDER BY vao'):
    ##        print(row)
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

def update_v1a(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
##        conn.text_factory = str
        c.execute('UPDATE vmsc SET v1a=? WHERE indice=?', (str(valor), str(indice)))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v1a',  valor, type(valor), type(indice))
        return ('Error', 'update valor tramo', indice)


def update_v1b(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
##        conn.text_factory = str
        valor = str(valor)
        c.execute('UPDATE vmsc SET v1b=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v1b',  valor, type((valor)) )
        return ('Error', 'update valor tramo', indice)

def update_v2almaa(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
##        conn.text_factory = str
        c.execute('UPDATE vmsc SET v2almaa=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v2almaa',  valor, )
        return ('Error', 'update valor tramo', indice)

def update_v2almab(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
##        conn.text_factory = str
        c.execute('UPDATE vmsc SET v2almab=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v2almab',  valor, )
        return ('Error', 'update valor tramo', indice)
    
def update_v2mesaa(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
##        conn.text_factory = str
        c.execute('UPDATE vmsc SET v2mesaa=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v2mesaa',  valor, )
        return ('Error', 'update valor tramo', indice)

def update_v2mesab(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('UPDATE vmsc SET v1a=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update ',  valor, )
        return ('Error', 'update valor tramo', indice)

def update_v3(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('UPDATE vmsc SET v3=? WHERE indice=?', (str(valor), indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v3',  valor, )
        return ('Error', 'update valor tramo', indice)

def update_v4(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('UPDATE vmsc SET v4=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v4',  valor, )
        return ('Error', 'update valor tramo', indice)

def update_v5(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('UPDATE vmsc SET v5=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v5',  valor, )
        return ('Error', 'update valor tramo', indice)

def update_v6(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('UPDATE vmsc SET v6=? WHERE indice=?', (str(valor), indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v6',  valor, )
        return ('Error', 'update valor tramo', indice)

def update_v7(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('UPDATE vmsc SET v7=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v7',  valor, )
        return ('Error', 'update valor tramo', indice)

def update_v8(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('UPDATE vmsc SET v8=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v8',  valor, )
        return ('Error', 'update valor tramo', indice)

def update_v10a(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('UPDATE vmsc SET v10a=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v10a',  valor, )
        return ('Error', 'update valor tramo', indice)

def update_v10b(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('UPDATE vmsc SET v10b=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v10b',  valor, )
        return ('Error', 'update valor tramo', indice)

def update_v10c(db, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        conn.text_factory = str
        c.execute('UPDATE vmsc SET v10c=? WHERE indice=?', (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update v10c',  valor, )
        return ('Error', 'update valor tramo', indice)
    
def update_data(db, coluna, indice, valor):
    t = (valor,)
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('UPDATE vmsc SET {}=? WHERE indice=?'.format(coluna), (valor, indice))
        conn.commit()
        conn.close()
        return None
    
    except Exception as e:
        print(e)
        print('Erro em update vmsc', coluna ,  valor, )
        return ('Error', 'update valor tramo', indice, coluna)


##
####db = r'vmsc.db'
####
####conn = sqlite3.connect(db)
######conn.text_factory = str
####c = conn.cursor()
####
####for row in c.execute('SELECT * FROM vmsc ORDER BY vao'):
####    print(row)
####
####
####print()
####c.execute('update vmsc set {}=? where indice=?'.format('v1b'),(0.631231231231333123,1))
####print()
####
####for row in c.execute('SELECT * FROM vmsc ORDER BY vao'):
####    print(row)
####
######update_v1a(db, '1', .5)
########
########print("update")
########print_data(db)
########    
########print(conn.execute("delete from vmsc").rowcount)
########conn.execute("delete from vmsc")
########conn.commit()
####conn.close()
