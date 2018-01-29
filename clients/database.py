import pymysql, sys, yaml

def create_database(db, cfg, cipher):
    print("Creating database and tables...")
    
    cursor = db.cursor()
    sql = 'CREATE DATABASE ' + cfg['mysql']['db']
    cursor.execute(sql)
    cursor.execute('USE ' + cfg['mysql']['db'])
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    number TEXT,
    password TEXT,
    token TEXT,
    email TEXT)""")
    db.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS recent_definitive(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id TEXT,
    unidade TEXT,
    nota TEXT)""")
    db.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS provisional(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id TEXT,
    unidade TEXT,
    epoca TEXT,
    ex_oral TEXT,
    ex_escrito TEXT,
    nota TEXT,
    consula TEXT,
    data_oral TEXT)""")
    db.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS partial_grades(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id TEXT,
    unidade TEXT,
    elemento TEXT,
    nota TEXT)""")
    db.commit()
    print("Created database and tables.")
