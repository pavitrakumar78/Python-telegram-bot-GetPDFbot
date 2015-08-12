import json
import webapp2
import telegram
import logging
from getPDF import bookInfo
from getPDF import getPDF
import re
from google.appengine.api import urlfetch
import urllib2
from urllib2 import HTTPError, URLError
import telegram.error
from telegram.error import TelegramError

bot = telegram.Bot('100911342:AAGE50CfxEqpsWErNlIlARd7ycUCtlY69mw')
bot.setWebhook('https://getpdf-project.appspot.com/100911342:AAGE50CfxEqpsWErNlIlARd7ycUCtlY69mw')

class getPDFBotWebhookPage(webapp2.RequestHandler):

    MESSAGE_INVALID = "Sorry, the format you entered is wrong!"
    MESSAGE_START = "Hello! I am getPDF Bot, I can get you the links of any book you want. What book would you like to search for?\n\nYou can control me by sending these commands:[Note: \'x\' is the number of search results that will be displyed]\n\n/BN:<bookname>{x} - Search for a book by its name.\n/AN:<author name>{x} - Search books written by the given author.\n"
    MESSAGE_NORESULT = "Sorry, No results!"
    MESSAGE_SMALL = "Query too small!"

    def post(self):
        urlfetch.set_default_fetch_deadline(60)

        logging.debug('Request: %s' % self.request.body)
        body = json.loads(self.request.body)
        update = telegram.Update.de_json(body)

        chat_id = update.message.chat.id
        message = update.message.text
        error_message = ""
        logging.debug('message text: %s' % message)
        req_message = False
        send_message = ""
        if message is not None:
            if '/start' in message or '/help' in message:
                self.sendMessageFn(chat_id,getPDFBotWebhookPage.MESSAGE_START)
                #try:
                #    bot.sendMessage(chat_id=chat_id,text='Hello! I am getPDF Bot, I can get you the links of any book you want. What book would you like to search for?\n\nYou can control me by sending these commands:[Note: \'x\' is the number of search results that will be displyed]\n\n/BN:<bookname>{x} - Search for a book by its name.\n/AN:<author name>{x} - Search books written by the given author.\n')
                #except TelegramError as e:
                #    print "telegram error",e
                #except URLError as e:
                #    print "URL  error",e
            printList = list()
            no_of_res = 5 # default, max = 21
            name = None
            if '/BN:' in message or '/bn:' in message:
                req_message = True
                if len(message) >= 8: #(4[an or bn] + 4[query])
                    name,no_of_res,format = self.checkInput(message[4:])
                    if name is not None:
                        book = getPDF(name,"title")
                        bookList = book.connect()
                        printList = book.formatList(bookList)
                    elif format == 0:
                        req_message = False
                        self.sendMessageFn(chat_id,getPDFBotWebhookPage.MESSAGE_INVALID)
                else:
                    req_message = False
                    self.sendMessageFn(chat_id,getPDFBotWebhookPage.MESSAGE_SMALL)
                #else:
                #    req_message = False
                #    self.sendMessageFn(chat_id,getPDFBotWebhookPage.MESSAGE_INVALID)
                #print name,no_of_res
                #if name is not None:
                #    book = getPDF(name,"title")
                #    bookList = book.connect()
                #    printList = book.formatList(bookList)
                #elif format == 0:
                #    req_message = False
                #    self.sendMessageFn(chat_id,getPDFBotWebhookPage.MESSAGE_INVALID)

            if '/AN:' in message or '/an:' in message:
                req_message = True
                if len(message) >= 8: #(4[an or bn] + 4[query])
                    name,no_of_res,format = self.checkInput(message[4:])
                    if name is not None:
                        book = getPDF(name,"author")
                        bookList = book.connect()
                        printList = book.formatList(bookList)
                    elif format == 0:
                        req_message = False
                        self.sendMessageFn(chat_id,getPDFBotWebhookPage.MESSAGE_INVALID)
                else:
                    req_message = False
                    self.sendMessageFn(chat_id,getPDFBotWebhookPage.MESSAGE_SMALL)  
                #name,no_of_res,format = self.checkInput(message[4:])
                #print name,no_of_res
                #if name is not None:
                #    book = getPDF(name,"author")
                #    bookList = book.connect()
                #    printList = book.formatList(bookList)
                #elif format == 0:
                #    req_message = False
                #    self.sendMessageFn(chat_id,getPDFBotWebhookPage.MESSAGE_INVALID)

            if len(printList) > 0 and req_message == True:
                for i,eachBook in enumerate(printList,1):
                    if i <= no_of_res:
                        self.sendMessageFn(chat_id,eachBook)
                        #try:
                        #    bot.sendMessage(chat_id=chat_id, text=eachBook)
                        #except TelegramError as e:
                        #    print "telegram error",e
                        #except URLError as e:
                        #    print "URL  error",e
            elif len(printList) == 0 and req_message == True:
                self.sendMessageFn(chat_id,getPDFBotWebhookPage.MESSAGE_NORESULT)
                #try:
                #    bot.sendMessage(chat_id=chat_id, text ="Sorry, No results!")
                #except TelegramError as e:
                #    print "telegram error",e
                #except URLError as e:
                #    print "URL  error",e
        self.response.write(json.dumps(body))

    def sendMessageFn(self,id,message):
        try:
            bot.sendMessage(chat_id=id, text =message)
        except TelegramError as e:
             print "telegram error",e
        except URLError as e:
            print "URL  error",e

    def checkInput(self,s): 
        name = None
        format_matched = 0 #0 - error(none matched), 1 - match1 is matched, 2 - match2 is matched
        no_of_res = 0
        if len(s) is 0:
            return None,0
        match1 = re.search('^([A-Za-z0-9_@./#-+\"\'&*$ ]+)*( )*({[0-9]+}$)',s)
        match2 = re.search('^([A-Za-z0-9_@./#-+\"\'&*$ ]+)$',s)
        if match1 is not None:
            format_matched = 1
            name = match1.group(1)
            no_of_res = match1.group(3)
            no_of_res = no_of_res[1:len(no_of_res)-1]
        if match2 is not None:
            format_matched = 2
            name = match2.group(1)
            no_of_res = 5 #default
        return name,int(no_of_res),format_matched


app = webapp2.WSGIApplication([
    ('/100911342:AAGE50CfxEqpsWErNlIlARd7ycUCtlY69mw', getPDFBotWebhookPage),
], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    webapp.util.run_wsgi_app(app)

if __name__ == '__main__':
    main()
