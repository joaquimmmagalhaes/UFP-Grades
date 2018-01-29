#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helpers.definitive import definitive
from helpers.partial import partial
from helpers.provisional import provisional
from clients.aes256 import AESCipher
from helpers import login_test
from helpers import wait_until_page_is_loaded
from pymysql import DatabaseError
import pymysql, sys, yaml
import threading
from os import path
from clients.database import create_database

semaphore = threading.Semaphore(value=5)

class Analisys (threading.Thread):
    def __init__(self, db, url, user, password, cfg):
      threading.Thread.__init__(self)
      self.db = pymysql.connect(cfg['mysql']['host'], cfg['mysql']['user'], cfg['mysql']['password'], cfg['mysql']['db'])
      self.url = url
      self.user = user
      self.password = password
      self.driver = webdriver.PhantomJS()

    def login(self):
        self.driver.get('https://portal.ufp.pt/authentication.aspx')
        wait_until_page_is_loaded(self.driver)

        number = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_AccordionPane1_content_txtLogin")
        number.send_keys(self.user[1])
        pwd = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_AccordionPane1_content_txtPassword")
        pwd.send_keys(self.password + Keys.ENTER)
        wait_until_page_is_loaded(self.driver)

        if self.driver.current_url == "https://portal.ufp.pt/default.aspx":
            return True

        self.driver.quit()
        return False

    def run(self):
        semaphore.acquire()
        partial(self.db, self.url, self.user, self.password)

        if self.login():
            definitive(self.db, self.user, self.driver)
            provisional(self.db, self.user, self.driver)
            self.driver.quit()

        self.db.close()
        semaphore.release()

def verify_user(db, number, email):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email='%s'" , (email))
    users = cursor.fetchall()
    if len(users) > 0:
        return False

    cursor.execute("SELECT * FROM users WHERE number='%s'" , (number))
    users = cursor.fetchall()
    if len(users) > 0:
        return False

    return True

def add_user(db, number, password, password_cipher, email, url):
    cursor = db.cursor()
    sql = "INSERT INTO users (number, password, email) VALUES (%s, %s, %s)"

    if verify_user(db, number, email) is False:
        return False

    if login_test(number, password, url) is False:
        return False

    try:
        cursor.execute(sql, (number, str(password_cipher), email))
        db.commit()
    except DatabaseError as e:
        db.rollback()
        print(e)

    return True

if __name__ == "__main__":
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, ".config.yml"))
    with open(filepath, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    cipher = AESCipher(cfg['others']['key'])
    url = cfg['others']['api']

    try:
        db = pymysql.connect(cfg['mysql']['host'], cfg['mysql']['user'], cfg['mysql']['password'], cfg['mysql']['db'])
    except DatabaseError as e:
        if e.args[0] == 1045:
            print("Access denied. Check username and password.")
            sys.exit(1)
        elif e.args[0] == 1049:
            db = pymysql.connect(cfg['mysql']['host'], cfg['mysql']['user'], cfg['mysql']['password'])
            create_database(db, cfg, cipher)

            print("Inserting new user: ")
            number = input("Number: ")
            password = input("Password: ")
            email = input("Email: ")

            if add_user(db, number, password ,cipher.encrypt(password).decode('UTF-8'), email, url) is False:
                print("Error inserting new user.")
                sys.exit(0)
            else:
                print("Inserted user with number: " + number)
        else:
            print("Unknown error. Details: " + e)
            sys.exit(1)

    if len(sys.argv) > 1:
        if sys.argv[1] == "-a" or sys.argv[1] == "--add" and len(sys.argv) == 5:
            if add_user(db, sys.argv[2], sys.argv[3] ,cipher.encrypt(sys.argv[3]).decode('UTF-8'), sys.argv[4], url) is False:
                print("Invalid user. Number/email already registered or invalid credentials.")
        else:
            print("Usage: -a or --add <number> <password> <email>")
            sys.exit(0)

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    db.close()
    threads = []

    for user in users:
        password = cipher.decrypt(user[2].encode('UTF-8'))
        analisys = Analisys(db, url, user, password, cfg)
        threads.append(analisys)
        analisys.start()

    for thread in threads:
        thread.join()
