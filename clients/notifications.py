from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTPException
import smtplib, yaml, json
from os import path
from pushbullet import Pushbullet
import urllib.request
import requests
from pprint import pprint
import pystache

class Notification:
    def __init__(self, email, contact):
        self.email = email
        self.contact = contact

        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "..", ".config.yml"))
        with open(filepath, 'r') as ymlfile:
            self.cfg = yaml.safe_load(ymlfile)

        filepath = path.abspath(path.join(basepath, "templates.json"))
        with open(filepath, 'r') as templates:
            self.templates = json.load(templates)

    def definitive(self, unidade, nota):
        subject = "Nova nota definitiva recente"

        html = pystache.render(self.templates["email"]["definitive"], {"unidade": unidade, "nota": nota})
        text = "Nova nota parcial.\r\nUnidade: %s\r\nNota: %s" % (unidade, nota)

        if self.email == "magalhaes1915@gmail.com":
            self.send_push(self.email, 3, unidade=unidade, nota=nota)

        self.send(html, text, subject)
        self.send_sms(text)

    def partial(self, unidade, elemento, nota):
        subject = "Nova nota parcial"

        html = pystache.render(self.templates["email"]["partial"], {"unidade": unidade, "elemento": elemento, "nota": nota})
        text = "Nova nota parcial.\r\nUnidade: %s\r\nElemento: %s\r\nNota: %s" % (unidade, elemento, nota)

        if self.email == "magalhaes1915@gmail.com":
            self.send_push(self.email, 1, unidade=unidade,elemento=elemento, nota=nota)

        self.send(html, text, subject)
        self.send_sms(text)

    def welcome(self):
        subject = "Bem vindo! 💥"
        html = self.templates["email"]["welcome"]
        text = "Bem vindo.\n"
        self.send(html, text, subject)

    def provisional(self, unidade, epoca, ex_oral, ex_escrito, nota, consula, data_oral):
        subject = "Nova nota final provisória"

        html = pystache.render(self.templates["email"]["provisional"], {"unidade": unidade, "epoca": epoca, "ex_oral": ex_oral, "ex_escrito": ex_escrito, "nota": nota, "consula": consula, "data_oral": data_oral})
        text = "Nova nota provisória.\r\nUnidade: %s\r\nEpoca: %s\r\nExame Oral: %s\r\nExame Escrito: %s\r\nNota: %s\r\nConsulta: %s\r\nData Oral: %s" % (unidade, epoca, ex_oral, ex_escrito, nota, consula, data_oral)

        if self.email == "magalhaes1915@gmail.com":
            self.send_push(self.email, 2, unidade=unidade, epoca=epoca, ex_oral=ex_oral, ex_escrito=ex_escrito, nota=nota, consula=consula, data_oral=data_oral)

        self.send(html, text, subject)
        self.send_sms(text)

    def send(self, html, text, subject):

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = str(Header('Grades Bot <' + self.cfg['stmp']['username'] + '>'))
        msg['To'] = self.email
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        try:
            smtpObj = smtplib.SMTP(self.cfg['stmp']['server'] + ':' + str(self.cfg['stmp']['port']))
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(self.cfg['stmp']['username'], self.cfg['stmp']['password'])
            smtpObj.sendmail(msg['From'], msg['To'], msg.as_string())
        except SMTPException as e:
            with open('email.log', 'a') as out:
                out.write(e)

    def send_push (self, email, type, unidade=None, elemento=None, epoca=None, ex_oral=None, ex_escrito=None, nota=None, consula=None, data_oral=None):

        if self.cfg['others']['pushbullet'] == None or len(self.cfg['others']['pushbullet']) == 0:
            return

        notifier = Pushbullet(self.cfg["others"]["pushbullet"])

        device = None

        for chat in notifier.chats:
            if email in str(chat):
                device = chat
                break

        if device == None:
            print("Unable to find device.\nExiting...")
            return

        if type == 1:
            notifier.push_note("Nova nota parcial 💥", self.build_nota_parcial(unidade, elemento, nota), chat=device)
        elif type == 2:
            notifier.push_note("Nova nota final 💥", self.build_nota_final(unidade, epoca, ex_oral, ex_escrito, nota, consula, data_oral), chat=device)
        else:
            notifier.push_note("Nova nota provisória 💥", self.build_nota_provisória(unidade, nota), chat=device)


    def build_nota_parcial(self, unidade, elemento, nota):
        return self.templates["pushbullet"]["partial"] % (unidade, elemento, nota)

    def build_nota_final(self, unidade, epoca, ex_oral, ex_escrito, nota, consula, data_oral):
        return self.templates["pushbullet"]["provisional"] % (unidade, epoca, ex_oral, ex_escrito, nota, consula, data_oral)

    def build_nota_provisória(self, unidade, nota):
        return self.templates["pushbullet"]["definitive"] % (unidade, nota)

    def send_sms(self, body):
        if self.contact == None or len(self.contact) == 0 or self.cfg['others']['BulkSMS'] == None or len(self.cfg['others']['BulkSMS']) == 0:
            print("Empty")
            return

        msg = self.templates["sms"]["normal"] % (body)

        if len(msg) > 200:
            if len(body) <= 200:
                msg = body
            else:
                msg = self.templates["sms"]["short"]


        data = json.dumps({"to": self.contact, "body": msg, "encoding": "UNICODE"})
        headers = { 'Content-Type': 'application/json', 'Authorization': self.cfg['others']['BulkSMS'] }

        requests.post('https://api.bulksms.com/v1/messages', data=data, headers=headers)