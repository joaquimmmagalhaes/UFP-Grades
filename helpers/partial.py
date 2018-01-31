import requests, sys
from helpers import login
from clients.notifications import Notification
from pymysql import DatabaseError

def exists(unidade, elemento, nota, all_grades):
    for grade in all_grades:
        if (grade[2].encode('utf-8').strip() == unidade and
        grade[3].encode('utf-8').strip() == elemento and
        grade[4].encode('utf-8').strip() == nota):
            return True
    return False


def partial(db, url, data, password):
    if data[3] == None or len(data[3]) == 0:
        token_json = login(data[1], str(password), db, data, url)

        if token_json == False or token_json["token"] == "Check your credentials":
            print("Unable to login. Check username and password")
            sys.exit(1)
    else:
        token_json = data[3]


    grades = requests.get(url + "grades/detailed", token_json)

    if grades.status_code == 403 or grades.status_code == "403":
        token_json = login(data[1], password, db, data, url)

        if token_json == False:
            print("Unable to login. Check username and password")
            sys.exit(1)

        grades = requests.get(url + "grades/detailed", token_json)

    all_grades = grades.json()["message"]["2017/18"]
    cursor = db.cursor()
    cursor.execute("SELECT * FROM partial_grades WHERE user_id=%s", (str(data[0])))
    all_db_grades = cursor.fetchall()

    notifier = Notification(data[4], data[6])

    for grade in all_grades:
        for details in all_grades[grade]:
            if exists(details["unidade"].encode('utf-8').strip(), details["elemento"].encode('utf-8').strip(), details["nota"].encode('utf-8').strip(), all_db_grades) is False:
                sql = "INSERT INTO partial_grades(user_id, unidade, elemento, nota) VALUES (%s, %s, %s, %s)"
                try:
                    cursor.execute(sql, (data[0] ,details["unidade"], details["elemento"], details["nota"]))
                    db.commit()

                    if data[5] is 0:
                        notifier.partial(details["unidade"], details["elemento"], details["nota"])

                except DatabaseError as e:
                    db.rollback()
                    print(e)