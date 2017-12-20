from html.parser import HTMLParser
from bs4 import BeautifulSoup


def openAndGetAsText(file):
    t = ""
    with open(file, encoding="UTF-8") as tekst:
        for i in tekst.readlines():
            t += str(i)
    return t


def cleanMe(html):
    soup = BeautifulSoup(html) # create a new bs4 object from the html data loaded
    for script in soup(["style"]): # remove all javascript and stylesheet code
        script.extract()
    return soup
    # get text
    #text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    #lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    #chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    #text = '\n'.join(chunk for chunk in chunks if chunk)
    #return text



class MyHTMLParser(HTMLParser):

    foundAuthor = False
    foundText = False
    foundAuthorFindText = False
    authorsAndText = []

    def handle_starttag(self, tag, attrs):

        if attrs == [('class', 'user')]:
            self.foundAuthor = True
            self.foundAuthorFindText = True
            print("KEK")

        if tag == 'p' and self.foundAuthorFindText:
            self.foundText = True
            print("KEK 2")

    def handle_endtag(self, tag):

        self.foundText = False

    def handle_data(self, data):

        if self.foundAuthor:
            self.authorsAndText.append([data])
            self.foundAuthor = False
            print("KEK 3")

        if self.foundText and self.foundAuthorFindText:
            print(data)
            self.authorsAndText[-1].append(data)
            print("KEK 4")

        print("Encountered some data  :", data)


x = openAndGetAsText("tekst1.html")
m = MyHTMLParser()
m.feed(str(cleanMe(x)))
print(m.authorsAndText)

for i in m.authorsAndText:
    if len(i) != 2:
        m.authorsAndText.remove(i)


# for i in range(len(m.authorsAndText) - 1):
#     if len(m.authorsAndText[i]) >= 3:
#         print(m.authorsAndText[i])
#
#
# with open("Output.txt", "w", encoding="UTF-8") as text_file:
#     for i in range(len(m.authorsAndText) - 1):
#         print(f"{m.authorsAndText[i]} \n", file=text_file)

