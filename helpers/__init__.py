import requests, json, pymysql
from pymysql import DatabaseError

def wait_until_page_is_loaded(driver):
    while (driver.execute_script('return document.readyState;') != "complete"):
        continue

def login_test(username, password, url):
    login = requests.post(url + "login", json={"username": username, "password": password})

    if login.json()["status"]  != "Error":
        return True

    return False

def login(username, password, db, data, url):
    login = requests.post(url + "login", json={"username": data[1], "password": password})
    token = False
    if login.json()["status"]  != "Error":
        token = login.json()["message"]
        token_json = {"token": token}
        query = ("UPDATE users SET token='%s' WHERE id='%s'")
        try:
        # Execute the SQL command
            cursor = db.cursor()
            cursor.execute(query, (json.dumps(token_json), str(data[0])))
        # Commit your changes in the database
            db.commit()
        except DatabaseError as e:
        # Rollback in case there is any error
            db.rollback()
            print(e)
    else:
        return False

    return token_json