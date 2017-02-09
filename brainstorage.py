#brainstorage.dev.amust.local

from mwclient import Site
import re
FileOut = open('PagesBUSList.txt', 'w')
UserAgent = 'Wiki_parser/0.1 run by DremSama'
site = Site(('http', 'brainstorage.dev.amust.local'), path='/', clients_useragent=UserAgent)
PagesList = []
PagesBUSList = []
for page in site.allpages():
    PagesList.append(page)
    if page.name.startswith('Bug') or page.name.startswith('bug'):
       #print(page.name)
        BugID = re.match(r'[A-z,a-z]ug\b.(\d*)[-|\s]*(.*)', page.page_title)
        BugID_NUM = BugID.group(1)
        BugID_SUBJECT = BugID.group(2)
        print(BugID_NUM, BugID_SUBJECT)
        print(page._info)
        PagesBUSList.append(page)
        exit()


print(len(PagesBUSList))
# print(PagesList)
