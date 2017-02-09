from mwclient import Site
import re

FileOut = open('PagesBUSList.txt', 'w')
UserAgent = 'Wiki_parser/0.1 run by DremSama'
site = Site(('http', 'wiki.support.veeam.local'), path='/', clients_useragent=UserAgent)
PagesList = []
PagesBUSList = []
for page in site.allpages():
    PagesList.append(page)
    if page.name.startswith('Bug') or page.name.startswith('bug'):
        BugID = re.match(r'[A-z,a-z]ug\b.(\d*)[-|\s]*(.*)', page.page_title)
        if BugID:
            BugID_NUM = BugID.group(1)
            BugID_SUBJECT = BugID.group(2)
            print(BugID_NUM, BugID_SUBJECT)
        textALL = page.text(0)
        if not textALL:
            print(page.name)
            print('Page has no text')
        else:
            #print(page.name)
            #print(textALL)
            print('----------------------------------')
            BugCaseID = re.findall(r"'''Case ID: '''(\d*)", textALL)
            BugToBeFixedIn = re.findall(r"'''To be fixed in: '''(.*)", textALL)
            BugPrivateFix = re.findall(r"'''Private fix: '''(.*)", textALL)
            BugAdded = re.findall(r"'''Added: '''(.*) by", textALL)
            BugAddedBy = re.findall(r"by \[\[User:.*\|(.*)\]\]", textALL)
            BugComponents = re.findall(r"'''Components: '''(.*)", textALL)
            if not BugCaseID:
                print('BugCaseID was not found')
            elif not BugToBeFixedIn:
                print('BugToBeFixedIn was not found')
            elif not BugPrivateFix:
                print('BugPrivateFix was not found')
            elif not BugAdded:
                print('BugPrivateFix was not found')
            elif not BugAddedBy:
                print('BugAddedBy was not found')
            elif not BugComponents:
                print('BugComponents was not found')
            else:
                print('BugCaseID = ' + BugCaseID[0])
                print('BugToBeFixedIn = ' + BugToBeFixedIn[0])
                print('BugPrivateFix = ' + BugPrivateFix[0])
                print('BugAdded = ' + BugAdded[0])
                print('BugAddedBy = ' + BugAddedBy[0])
                print('BugComponents = ' + BugComponents[0])

        """
        textDescription = page.text(1)
        # print(textDescription)
        textSolution = page.text(2)
        print(textSolution)
        print(page._info)
        for image in page.images():
            print(image)
        for link in page.backlinks():
            print(link)
        for category in page.categories():
            print(category)
        """
        PagesBUSList.append(page)
        exit()

print(len(PagesBUSList))
# print(PagesList)
