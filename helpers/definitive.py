from clients.notifications import Notification
from helpers import wait_until_page_is_loaded
from pymysql import DatabaseError

def exists(unidade, nota, all_grades):
    for grade in all_grades:
        if (grade[2] == unidade and grade[3] == nota):
            return True
    return False

def definitive(db, data, driver):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM recent_definitive WHERE user_id=%s", (str(data[0])))
    all_db_grades = cursor.fetchall()

    driver.get('https://portal.ufp.pt/Notas/Recente.aspx')
    wait_until_page_is_loaded(driver)

    table = driver.find_elements_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_AccordionPane1_content_GridView1"]/tbody/tr')

    if len(table) == 0:
        return

    del table[0]

    notifier = Notification(data[4], data[6])

    for row in table:
        col = row.find_elements_by_tag_name("td")
        unidade = col[0].get_attribute('innerText')
        nota = col[2].get_attribute('innerText')

        if exists(unidade, nota, all_db_grades) is False:
            sql = "INSERT INTO recent_definitive (user_id, unidade, nota) VALUES (%s, %s, %s)"

            try:
                cursor.execute(sql, (data[0], unidade, nota))
                db.commit()

                if data[5] is 0:
                    notifier.definitive(unidade, nota)

            except DatabaseError as e:
                db.rollback()
                print(e)
