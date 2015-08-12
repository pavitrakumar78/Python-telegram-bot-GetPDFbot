#Telegram GetPDFBot 

A Telegram bot to get links to download various formats of books according to user query.
[uses libgen.ru as the search site]

This bot uses the python telegram-bot-API wrapper made by leandrotoledo
(https://github.com/leandrotoledo/python-telegram-bot)

I have used Google App Engine as the server to host the files.

To deploy files and run the application:

1. Create a project on Google App Engine console [assume <PROJECT-ID> will be your project ID].
2. Update the application field in the .yaml to <PROJECT-ID>.
3. Update <TELEGRAM API KEY> and <PROJECT-ID>  in `main.py`.
4. Create a directory named 'lib' in the same folder.  
    `$ mkdir lib`
5. Install all necessary libraries into that directory.  
    `$ pip install -t lib python-telegram-bot BeautifulSoup bitly_api`
6. To deploy the files to your server, use the command below or install GAE Launcher and put your directory in it and click 'Deploy'.  
    `$ appcfg.py -A <PROJECT-ID> update .`
