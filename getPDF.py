import urllib2
import BeautifulSoup
import bitly_api

from itertools import islice


class bookInfo:
	def __init__(self,book_author,book_name):
		self.name = book_name
		self.author = book_author
		self.publisher = None
		self.pages = None
		self.format = None
		self.year = None
		self.dlink = list()
	def setAuthor(self,book_author):
		self.author = book_author
	def setPublisher(self,book_pub):
		self.publisher = book_pub
	def setFormat(self,book_format):
		self.format = book_format
	def setPages(self,book_pages):
		self.pages = book_pages
	def setYear(self,book_year):
		self.year = book_year
	def addDlink(self,link):
		self.dlink.append(link)
	def disp(self):
		print self.name
		print self.author
		print self.publisher
		print self.pages
		print self.dlink
		print self.format
		print "\n\n\n"


class getPDF:
	URL = 'http://gen.lib.rus.ec/search.php?req=%s&open=0&view=simple&phrase=1&column=%s'
	API_USER = "pavitrakumar"
	API_KEY = "<YOUR-API-KEY>"
	def __init__(self,search_query,search_type):
		self.query = search_query.strip().replace(" ","+")
		self.type = search_type
		print self.query," is the query"

	def getBooksList(self,tableRows):
		bookList = list()
		lst = iter(tableRows)
		for row in lst:
			if row is not None:
				try:
					if str(row).startswith("<td><a href=\"search.php?"):
						author = row.contents[0].contents[0]
						k = next(lst,None).findAll('a')[0]
						bookname = k.text
						book = bookInfo(author,bookname) #init with author name,book name
						book.setPublisher(next(lst,None).text)

						book.setYear(next(lst,None))
						book.setPages(next(lst,None).contents[0])
						book.setFormat(next(islice(lst, 2, 3), '').contents[0])
						for i in range(3):
							link = next(lst,None).contents[0].get('href')
							book.addDlink(link)
						#book = (row,next(islice(lst, 2, 3), ''),next(lst,None),next(lst,None),next(lst,None),next(lst,None),next(lst,None),next(lst,None))
						bookList.append(book)
				except IndexError,e:
					continue
		return bookList

	def connect(self):
		request = urllib2.Request(getPDF.URL % (self.query,self.type))
		response = urllib2.urlopen(request)
		soup = BeautifulSoup.BeautifulSoup(response)
		tableRows = list()
		for a in soup.findAll('td'):
			tableRows.append(a)
		return self.getBooksList(tableRows)

	def formatList(self,bookList):
		formattedList = list()
		b = bitly_api.Connection(login=getPDF.API_USER, api_key=getPDF.API_KEY)
		for book in bookList:
			#m = "Book Name:%s\nAuthor Name:%s\nFormat: %s\nDL1:%s\nDL2:%s\nDL3:%s\n" % (book.name.encode('utf8'),book.author.encode('utf8'),book.format,shortenUrl(b,book.dlink[0]),shortenUrl(b,book.dlink[1]),shortenUrl(b,book.dlink[2]))
			#use this if bitly has expired
			m = "Book Name:%s\nAuthor Name:%s\nFormat: %s\nDL1:%s\nDL2:%s\nDL3:%s\n" % (book.name.encode('utf8'),book.author.encode('utf8'),book.format.encode('utf8'),book.dlink[0].encode('utf8'),book.dlink[1].encode('utf8'),book.dlink[2].encode('utf8'))
			formattedList.append(m)

		return formattedList
	
	def shortenUrl(self,b,URL):
		return b.shorten(uri=URL)['url']

	def printList(self,bookList):
		for book in bookList:
			print book













