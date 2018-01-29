from selenium.webdriver.common.keys import Keys
from clients.notifications import Notification
from helpers import wait_until_page_is_loaded
from pymysql import DatabaseError

def exists(unidade, epoca, ex_oral, ex_escrito, nota, consula, data_oral, all_grades):
    for grade in all_grades:
        if (grade[2] == unidade and grade[3] == epoca and grade[4] == ex_oral and grade[5] == ex_escrito and grade[6] == nota):
            return True
    return False

def provisional(db, data, driver):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM provisional WHERE user_id=%s", (str(data[0])))
    all_db_grades = cursor.fetchall()

    first_usage = False
    if len(all_db_grades) == 0:
        first_usage = True

    driver.get('https://portal.ufp.pt/Notas/FinalProv.aspx')
    wait_until_page_is_loaded(driver)

    table = driver.find_elements_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_AccordionPane1_content']/table/tbody/tr[contains(@class, 'odd') or contains(@class, 'even')]")

    notifier = Notification(data[4])

    for row in table:
        col = row.find_elements_by_tag_name("td")
        unidade = col[1].get_attribute('innerText')
        epoca = col[2].get_attribute('innerText')
        ex_oral = col[3].get_attribute('innerText')
        ex_escrito = col[4].get_attribute('innerText')
        nota = col[5].get_attribute('innerText')
        consula = col[6].get_attribute('innerText')
        data_oral = col[7].get_attribute('innerText')

        if exists(unidade, epoca, ex_oral, ex_escrito, nota, consula, data_oral, all_db_grades) is False:
            sql = "INSERT INTO provisional (user_id, unidade, epoca, ex_oral, ex_escrito, nota, consula, data_oral) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            try:
                cursor.execute(sql, (data[0], unidade, epoca, ex_oral, ex_escrito, nota, consula, data_oral))
                db.commit()
                if first_usage is False:
                    notifier.provisional(unidade, epoca, ex_oral, ex_escrito, nota, consula, data_oral)
            except DatabaseError as e:
                db.rollback()
                print(e)

    driver.quit()
    