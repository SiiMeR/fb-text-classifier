from html.parser import HTMLParser
from bs4 import BeautifulSoup




class MyHTMLParser(HTMLParser):

    foundAuthor = False
    foundText = False
    foundAuthorFindText = False
    authorsAndText = []

    def handle_starttag(self, tag, attrs):

        if attrs == [('class', 'user')]:
            self.foundAuthor = True
            self.foundAuthorFindText = True

        if tag == 'p' and self.foundAuthorFindText:
            self.foundText = True

    def handle_endtag(self, tag):

        self.foundText = False

    def handle_data(self, data):
        if self.foundAuthor:
            self.authorsAndText.append([data])
            self.foundAuthor = False

        if self.foundText and self.foundAuthorFindText:
            self.authorsAndText[-1].append(data)


      #  print("Encountered some data  :", data) left in for debugging

    def cleanHTML(self, html):
        soup = BeautifulSoup(html, "lxml")  # create a new bs4 object from the html data loaded
        for script in soup(["style"]):  # remove all javascript and stylesheet code
            script.extract()
        return soup

    def fileToString(self, file):
        t = ""
        with open(file, encoding="UTF-8") as text:
            for i in text.readlines():
                t += str(i)
        return t


    def parseChat(self, file):
        fileString = self.fileToString(file)
        self.feed(str(self.cleanHTML(fileString)))

        for i in self.authorsAndText:
            if len(i) != 2:
                self.authorsAndText.remove(i)

        return self.authorsAndText




#print(m.authorsAndText)

