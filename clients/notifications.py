from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTPException
import smtplib, yaml
from os import path


class Notification:
    def __init__(self, email):
        self.email = email

    def definitive(self, unidade, nota):
        subject = "Nova nota definitiva recente"
        html = '<!doctype html><html> <head> <meta name="viewport" content="width=device-width"/> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> <title>Nova nota</title> <style>/* ------------------------------------- GLOBAL RESETS ------------------------------------- */ img{border: none; -ms-interpolation-mode: bicubic; max-width: 100%;}body{background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;}table{border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;}table td{font-family: sans-serif; font-size: 14px; vertical-align: top;}/* ------------------------------------- BODY & CONTAINER ------------------------------------- */ .body{background-color: #f6f6f6; width: 100%;}/* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */ .container{display: block; Margin: 0 auto !important; /* makes it centered */ max-width: 580px; padding: 10px; width: 580px;}/* This should also be a block element, so that it will fill 100% of the .container */ .content{box-sizing: border-box; display: block; Margin: 0 auto; max-width: 580px; padding: 10px;}/* ------------------------------------- HEADER, FOOTER, MAIN ------------------------------------- */ .main{background: #ffffff; border-radius: 3px; width: 100%;}.wrapper{box-sizing: border-box; padding: 20px;}.content-block{padding-bottom: 10px; padding-top: 10px;}.footer{clear: both; Margin-top: 10px; text-align: center; width: 100%;}.footer td, .footer p, .footer span, .footer a{color: #999999; font-size: 12px; text-align: center;}/* ------------------------------------- TYPOGRAPHY ------------------------------------- */ h1, h2, h3, h4{color: #000000; font-family: sans-serif; font-weight: 400; line-height: 1.4; margin: 0; Margin-bottom: 30px;}h1{font-size: 35px; font-weight: 300; text-align: center; text-transform: capitalize;}p, ul, ol{font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;}p li, ul li, ol li{list-style-position: inside; margin-left: 5px;}a{color: #3498db; text-decoration: underline;}/* ------------------------------------- BUTTONS ------------------------------------- */ .btn{box-sizing: border-box; width: 100%;}.btn > tbody > tr > td{padding-bottom: 15px;}.btn table{width: auto;}.btn table td{background-color: #ffffff; border-radius: 5px; text-align: center;}.btn a{background-color: #ffffff; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; color: #3498db; cursor: pointer; display: inline-block; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-decoration: none; text-transform: capitalize;}.btn-primary a{background-color: #3498db; border-color: #3498db; color: #ffffff;}/* ------------------------------------- OTHER STYLES THAT MIGHT BE USEFUL ------------------------------------- */ .last{margin-bottom: 0;}.first{margin-top: 0;}.align-center{text-align: center;}.align-right{text-align: right;}.align-left{text-align: left;}.clear{clear: both;}.mt0{margin-top: 0;}.mb0{margin-bottom: 0;}.preheader{color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;}.powered-by a{text-decoration: none;}hr{border: 0; border-bottom: 1px solid #f6f6f6; Margin: 20px 0;}/* ------------------------------------- RESPONSIVE AND MOBILE FRIENDLY STYLES ------------------------------------- */ @media only screen and (max-width: 620px){table[class=body] h1{font-size: 28px !important; margin-bottom: 10px !important;}table[class=body] p, table[class=body] ul, table[class=body] ol, table[class=body] td, table[class=body] span, table[class=body] a{font-size: 16px !important;}table[class=body] .wrapper, table[class=body] .article{padding: 10px !important;}table[class=body] .content{padding: 0 !important;}table[class=body] .container{padding: 0 !important; width: 100% !important;}table[class=body] .main{border-left-width: 0 !important; border-radius: 0 !important; border-right-width: 0 !important;}table[class=body] .btn table{width: 100% !important;}table[class=body] .btn a{width: 100% !important;}table[class=body] .img-responsive{height: auto !important; max-width: 100% !important; width: auto !important;}}/* ------------------------------------- PRESERVE THESE STYLES IN THE HEAD ------------------------------------- */ @media all{.ExternalClass{width: 100%;}.ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div{line-height: 100%;}.apple-link a{color: inherit !important; font-family: inherit !important; font-size: inherit !important; font-weight: inherit !important; line-height: inherit !important; text-decoration: none !important;}.btn-primary table td:hover{background-color: #34495e !important;}.btn-primary a:hover{background-color: #34495e !important; border-color: #34495e !important;}}</style> </head> <body class=""> <table border="0" cellpadding="0" cellspacing="0" class="body"> <tr> <td>&nbsp;</td><td class="container"> <div class="content"> <span class="preheader">Nova nota definitiva recente.</span> <table class="main"> <tr> <td class="wrapper"> <table border="0" cellpadding="0" cellspacing="0"> <tr> <td> <p>Hello 💣</p><p>Venho por este meio informar que foi lançada uma nova nota.</p><p>Detalhes em baixo 👇🏻, boa sorte 🤷‍♂️<table border="0" cellpadding="0" cellspacing="0" class="btn btn-primary"> <tbody> <tr> <td> <table border="0" cellpadding="0" cellspacing="0" style="width:100%;"> <tr style="border: 1px solid black;"> <th>Unidade Curricular</th><th>Nota</th></tr><tr> <td>' + unidade +'</td><td>' + nota + '</td></tr></table> </td></tr></tbody> </table><br><p>I know, I am awesome ❤️</p></td></tr></table> </td></tr></table> <div class="footer"> <table border="0" cellpadding="0" cellspacing="0"> <tr> <td class="content-block powered-by"> Powered by <a href="http://htmlemail.io">HTMLemail</a>. </td></tr></table> </div></div></td><td>&nbsp;</td></tr></table> </body></html>'
        text = "Nova nota.\n"
        self.send(html, text, subject)

    def partial(self, unidade, elemento, nota):
        subject = "Nova nota parcial"
        html = '<!doctype html><html> <head> <meta name="viewport" content="width=device-width"/> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> <title>Nova nota</title> <style>/* ------------------------------------- GLOBAL RESETS ------------------------------------- */ img{border: none; -ms-interpolation-mode: bicubic; max-width: 100%;}body{background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;}table{border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;}table td{font-family: sans-serif; font-size: 14px; vertical-align: top;}/* ------------------------------------- BODY & CONTAINER ------------------------------------- */ .body{background-color: #f6f6f6; width: 100%;}/* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */ .container{display: block; Margin: 0 auto !important; /* makes it centered */ max-width: 580px; padding: 10px; width: 580px;}/* This should also be a block element, so that it will fill 100% of the .container */ .content{box-sizing: border-box; display: block; Margin: 0 auto; max-width: 580px; padding: 10px;}/* ------------------------------------- HEADER, FOOTER, MAIN ------------------------------------- */ .main{background: #ffffff; border-radius: 3px; width: 100%;}.wrapper{box-sizing: border-box; padding: 20px;}.content-block{padding-bottom: 10px; padding-top: 10px;}.footer{clear: both; Margin-top: 10px; text-align: center; width: 100%;}.footer td, .footer p, .footer span, .footer a{color: #999999; font-size: 12px; text-align: center;}/* ------------------------------------- TYPOGRAPHY ------------------------------------- */ h1, h2, h3, h4{color: #000000; font-family: sans-serif; font-weight: 400; line-height: 1.4; margin: 0; Margin-bottom: 30px;}h1{font-size: 35px; font-weight: 300; text-align: center; text-transform: capitalize;}p, ul, ol{font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;}p li, ul li, ol li{list-style-position: inside; margin-left: 5px;}a{color: #3498db; text-decoration: underline;}/* ------------------------------------- BUTTONS ------------------------------------- */ .btn{box-sizing: border-box; width: 100%;}.btn > tbody > tr > td{padding-bottom: 15px;}.btn table{width: auto;}.btn table td{background-color: #ffffff; border-radius: 5px; text-align: center;}.btn a{background-color: #ffffff; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; color: #3498db; cursor: pointer; display: inline-block; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-decoration: none; text-transform: capitalize;}.btn-primary a{background-color: #3498db; border-color: #3498db; color: #ffffff;}/* ------------------------------------- OTHER STYLES THAT MIGHT BE USEFUL ------------------------------------- */ .last{margin-bottom: 0;}.first{margin-top: 0;}.align-center{text-align: center;}.align-right{text-align: right;}.align-left{text-align: left;}.clear{clear: both;}.mt0{margin-top: 0;}.mb0{margin-bottom: 0;}.preheader{color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;}.powered-by a{text-decoration: none;}hr{border: 0; border-bottom: 1px solid #f6f6f6; Margin: 20px 0;}/* ------------------------------------- RESPONSIVE AND MOBILE FRIENDLY STYLES ------------------------------------- */ @media only screen and (max-width: 620px){table[class=body] h1{font-size: 28px !important; margin-bottom: 10px !important;}table[class=body] p, table[class=body] ul, table[class=body] ol, table[class=body] td, table[class=body] span, table[class=body] a{font-size: 16px !important;}table[class=body] .wrapper, table[class=body] .article{padding: 10px !important;}table[class=body] .content{padding: 0 !important;}table[class=body] .container{padding: 0 !important; width: 100% !important;}table[class=body] .main{border-left-width: 0 !important; border-radius: 0 !important; border-right-width: 0 !important;}table[class=body] .btn table{width: 100% !important;}table[class=body] .btn a{width: 100% !important;}table[class=body] .img-responsive{height: auto !important; max-width: 100% !important; width: auto !important;}}/* ------------------------------------- PRESERVE THESE STYLES IN THE HEAD ------------------------------------- */ @media all{.ExternalClass{width: 100%;}.ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div{line-height: 100%;}.apple-link a{color: inherit !important; font-family: inherit !important; font-size: inherit !important; font-weight: inherit !important; line-height: inherit !important; text-decoration: none !important;}.btn-primary table td:hover{background-color: #34495e !important;}.btn-primary a:hover{background-color: #34495e !important; border-color: #34495e !important;}}</style> </head> <body class=""> <table border="0" cellpadding="0" cellspacing="0" class="body"> <tr> <td>&nbsp;</td><td class="container"> <div class="content"> <span class="preheader">Nova nota parcial.</span> <table class="main"> <tr> <td class="wrapper"> <table border="0" cellpadding="0" cellspacing="0"> <tr> <td> <p>Hello 💣</p><p>Venho por este meio informar que foi lançada uma nova nota.</p><p>Detalhes em baixo 👇🏻, boa sorte 🤷‍♂️<table border="0" cellpadding="0" cellspacing="0" class="btn btn-primary"> <tbody> <tr> <td> <table border="0" cellpadding="0" cellspacing="0" style="width:100%;"> <tr style="border: 1px solid black;"> <th>Unidade Curricular</th> <th>Elemento</th> <th>Nota</th></tr><tr> <td>' + unidade +'</td><td>' + elemento + '</td><td>' + nota + '</td></tr></table> </td></tr></tbody> </table><br><p>I know, I am awesome ❤️</p></td></tr></table> </td></tr></table> <div class="footer"> <table border="0" cellpadding="0" cellspacing="0"> <tr> <td class="content-block powered-by"> Powered by <a href="http://htmlemail.io">HTMLemail</a>. </td></tr></table> </div></div></td><td>&nbsp;</td></tr></table> </body></html>'
        text = "Nova nota.\n"
        self.send(html, text, subject)

    def welcome(self):
        subject = "Bem vindo! 💥"
        html = '<html><head> <meta name="viewport" content="width=device-width"> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> <title>Nova nota</title> <style>/* ------------------------------------- GLOBAL RESETS ------------------------------------- */ img{border: none; -ms-interpolation-mode: bicubic; max-width: 100%;}body{background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;}table{border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;}table td{font-family: sans-serif; font-size: 14px; vertical-align: top;}/* ------------------------------------- BODY & CONTAINER ------------------------------------- */ .body{background-color: #f6f6f6; width: 100%;}/* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */ .container{display: block; Margin: 0 auto !important; /* makes it centered */ max-width: 580px; padding: 10px; width: 580px;}/* This should also be a block element, so that it will fill 100% of the .container */ .content{box-sizing: border-box; display: block; Margin: 0 auto; max-width: 580px; padding: 10px;}/* ------------------------------------- HEADER, FOOTER, MAIN ------------------------------------- */ .main{background: #ffffff; border-radius: 3px; width: 100%;}.wrapper{box-sizing: border-box; padding: 20px;}.content-block{padding-bottom: 10px; padding-top: 10px;}.footer{clear: both; Margin-top: 10px; text-align: center; width: 100%;}.footer td, .footer p, .footer span, .footer a{color: #999999; font-size: 12px; text-align: center;}/* ------------------------------------- TYPOGRAPHY ------------------------------------- */ h1, h2, h3, h4{color: #000000; font-family: sans-serif; font-weight: 400; line-height: 1.4; margin: 0; Margin-bottom: 30px;}h1{font-size: 35px; font-weight: 300; text-align: center; text-transform: capitalize;}p, ul, ol{font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;}p li, ul li, ol li{list-style-position: inside; margin-left: 5px;}a{color: #3498db; text-decoration: underline;}/* ------------------------------------- BUTTONS ------------------------------------- */ .btn{box-sizing: border-box; width: 100%;}.btn > tbody > tr > td{padding-bottom: 15px;}.btn table{width: auto;}.btn table td{background-color: #ffffff; border-radius: 5px; text-align: center;}.btn a{background-color: #ffffff; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; color: #3498db; cursor: pointer; display: inline-block; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-decoration: none; text-transform: capitalize;}.btn-primary a{background-color: #3498db; border-color: #3498db; color: #ffffff;}/* ------------------------------------- OTHER STYLES THAT MIGHT BE USEFUL ------------------------------------- */ .last{margin-bottom: 0;}.first{margin-top: 0;}.align-center{text-align: center;}.align-right{text-align: right;}.align-left{text-align: left;}.clear{clear: both;}.mt0{margin-top: 0;}.mb0{margin-bottom: 0;}.preheader{color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;}.powered-by a{text-decoration: none;}hr{border: 0; border-bottom: 1px solid #f6f6f6; Margin: 20px 0;}/* ------------------------------------- RESPONSIVE AND MOBILE FRIENDLY STYLES ------------------------------------- */ @media only screen and (max-width: 620px){table[class=body] h1{font-size: 28px !important; margin-bottom: 10px !important;}table[class=body] p, table[class=body] ul, table[class=body] ol, table[class=body] td, table[class=body] span, table[class=body] a{font-size: 16px !important;}table[class=body] .wrapper, table[class=body] .article{padding: 10px !important;}table[class=body] .content{padding: 0 !important;}table[class=body] .container{padding: 0 !important; width: 100% !important;}table[class=body] .main{border-left-width: 0 !important; border-radius: 0 !important; border-right-width: 0 !important;}table[class=body] .btn table{width: 100% !important;}table[class=body] .btn a{width: 100% !important;}table[class=body] .img-responsive{height: auto !important; max-width: 100% !important; width: auto !important;}}/* ------------------------------------- PRESERVE THESE STYLES IN THE HEAD ------------------------------------- */ @media all{.ExternalClass{width: 100%;}.ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div{line-height: 100%;}.apple-link a{color: inherit !important; font-family: inherit !important; font-size: inherit !important; font-weight: inherit !important; line-height: inherit !important; text-decoration: none !important;}.btn-primary table td:hover{background-color: #34495e !important;}.btn-primary a:hover{background-color: #34495e !important; border-color: #34495e !important;}}</style> </head> <body class=""> <table border="0" cellpadding="0" cellspacing="0" class="body"> <tbody><tr> <td>&nbsp;</td><td class="container"> <div class="content"> <span class="preheader">Bem vindo!</span> <table class="main"> <tbody><tr> <td class="wrapper"> <table border="0" cellpadding="0" cellspacing="0"> <tbody><tr> <td> <p>Hello 😆</p><p>Venho por este meio informar que foi inscrito com sucesso no sistema.</p><p>Sempre que for lançada uma nota irá recebe-la por aqui. Verifique sempre a caixa de spam.</p><br><p>I know, I am awesome ❤️</p></td></tr></tbody></table> </td></tr></tbody></table> <div class="footer"> <table border="0" cellpadding="0" cellspacing="0"> <tbody><tr> <td class="content-block powered-by"> Powered by <a href="http://htmlemail.io">HTMLemail</a>. </td></tr></tbody></table> </div></div></td><td>&nbsp;</td></tr></tbody></table> </body></html>'
        text = "Bem vindo.\n"
        self.send(html, text, subject)

    def provisional(self, unidade, epoca, ex_oral, ex_escrito, nota, consula, data_oral):
        subject = "Nova nota final provisória"
        html = '<!doctype html><html> <head> <meta name="viewport" content="width=device-width"/> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> <title>Nova nota</title> <style>/* ------------------------------------- GLOBAL RESETS ------------------------------------- */ img{border: none; -ms-interpolation-mode: bicubic; max-width: 100%;}body{background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;}table{border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;}table td{font-family: sans-serif; font-size: 14px; vertical-align: top;}/* ------------------------------------- BODY & CONTAINER ------------------------------------- */ .body{background-color: #f6f6f6; width: 100%;}/* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */ .container{display: block; Margin: 0 auto !important; /* makes it centered */ max-width: 580px; padding: 10px; width: 580px;}/* This should also be a block element, so that it will fill 100% of the .container */ .content{box-sizing: border-box; display: block; Margin: 0 auto; max-width: 580px; padding: 10px;}/* ------------------------------------- HEADER, FOOTER, MAIN ------------------------------------- */ .main{background: #ffffff; border-radius: 3px; width: 100%;}.wrapper{box-sizing: border-box; padding: 20px;}.content-block{padding-bottom: 10px; padding-top: 10px;}.footer{clear: both; Margin-top: 10px; text-align: center; width: 100%;}.footer td, .footer p, .footer span, .footer a{color: #999999; font-size: 12px; text-align: center;}/* ------------------------------------- TYPOGRAPHY ------------------------------------- */ h1, h2, h3, h4{color: #000000; font-family: sans-serif; font-weight: 400; line-height: 1.4; margin: 0; Margin-bottom: 30px;}h1{font-size: 35px; font-weight: 300; text-align: center; text-transform: capitalize;}p, ul, ol{font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;}p li, ul li, ol li{list-style-position: inside; margin-left: 5px;}a{color: #3498db; text-decoration: underline;}/* ------------------------------------- BUTTONS ------------------------------------- */ .btn{box-sizing: border-box; width: 100%;}.btn > tbody > tr > td{padding-bottom: 15px;}.btn table{width: auto;}.btn table td{background-color: #ffffff; border-radius: 5px; text-align: center;}.btn a{background-color: #ffffff; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; color: #3498db; cursor: pointer; display: inline-block; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-decoration: none; text-transform: capitalize;}.btn-primary a{background-color: #3498db; border-color: #3498db; color: #ffffff;}/* ------------------------------------- OTHER STYLES THAT MIGHT BE USEFUL ------------------------------------- */ .last{margin-bottom: 0;}.first{margin-top: 0;}.align-center{text-align: center;}.align-right{text-align: right;}.align-left{text-align: left;}.clear{clear: both;}.mt0{margin-top: 0;}.mb0{margin-bottom: 0;}.preheader{color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;}.powered-by a{text-decoration: none;}hr{border: 0; border-bottom: 1px solid #f6f6f6; Margin: 20px 0;}/* ------------------------------------- RESPONSIVE AND MOBILE FRIENDLY STYLES ------------------------------------- */ @media only screen and (max-width: 620px){table[class=body] h1{font-size: 28px !important; margin-bottom: 10px !important;}table[class=body] p, table[class=body] ul, table[class=body] ol, table[class=body] td, table[class=body] span, table[class=body] a{font-size: 16px !important;}table[class=body] .wrapper, table[class=body] .article{padding: 10px !important;}table[class=body] .content{padding: 0 !important;}table[class=body] .container{padding: 0 !important; width: 100% !important;}table[class=body] .main{border-left-width: 0 !important; border-radius: 0 !important; border-right-width: 0 !important;}table[class=body] .btn table{width: 100% !important;}table[class=body] .btn a{width: 100% !important;}table[class=body] .img-responsive{height: auto !important; max-width: 100% !important; width: auto !important;}}/* ------------------------------------- PRESERVE THESE STYLES IN THE HEAD ------------------------------------- */ @media all{.ExternalClass{width: 100%;}.ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div{line-height: 100%;}.apple-link a{color: inherit !important; font-family: inherit !important; font-size: inherit !important; font-weight: inherit !important; line-height: inherit !important; text-decoration: none !important;}.btn-primary table td:hover{background-color: #34495e !important;}.btn-primary a:hover{background-color: #34495e !important; border-color: #34495e !important;}}</style> </head> <body class=""> <table border="0" cellpadding="0" cellspacing="0" class="body"> <tr> <td>&nbsp;</td><td class="container"> <div class="content"> <span class="preheader">Nova nota final provisória.</span> <table class="main"> <tr> <td class="wrapper"> <table border="0" cellpadding="0" cellspacing="0"> <tr> <td> <p>Hello 💣</p><p>Venho por este meio informar que foi lançada uma nova nota.</p><p>Detalhes em baixo 👇🏻, boa sorte 🤷‍♂️<table border="0" cellpadding="0" cellspacing="0" class="btn btn-primary"> <tbody> <tr> <td> <table border="0" cellpadding="0" cellspacing="0" style="width:100%;"> <tr style="border: 1px solid black;"> <th>Unidade Curricular</th> <th>Epoca</th> <th>Exame Oral</th> <th>Exame Escrito</th> <th>Nota</th> <th>Consulta</th> <th>Data Oral</th></tr><tr> <td>' + unidade +'</td><td>' + epoca + '</td><td>' + ex_oral + '</td><td>' + ex_escrito + '</td><td>' + nota + '</td><td>' + consula + '</td><td>' + data_oral + '</td></tr></table> </td></tr></tbody> </table><br><p>I know, I am awesome ❤️</p></td></tr></table> </td></tr></table> <div class="footer"> <table border="0" cellpadding="0" cellspacing="0"> <tr> <td class="content-block powered-by"> Powered by <a href="http://htmlemail.io">HTMLemail</a>. </td></tr></table> </div></div></td><td>&nbsp;</td></tr></table> </body></html>'
        text = "Nova nota.\n"
        self.send(html, text, subject)

    def send(self, html, text, subject):
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "..", ".config.yml"))
        with open(filepath, 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = str(Header('Grades Bot <' + cfg['stmp']['username'] + '>'))
        msg['To'] = self.email
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        try:
            smtpObj = smtplib.SMTP(cfg['stmp']['server'] + ':' + str(cfg['stmp']['port']))
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(cfg['stmp']['username'], cfg['stmp']['password'])
            smtpObj.sendmail(msg['From'], msg['To'], msg.as_string())         
        except SMTPException as e:
            with open('email.log', 'a') as out:
                out.write(e)