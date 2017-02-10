from mwclient import Site
from PythonConfluenceAPI import ConfluenceAPI
import re
from simple_salesforce import Salesforce
api = ConfluenceAPI('admin', '123@qwe', 'http://127.0.0.1:8090')
FileOut = open('PagesBUSList.txt', 'w')
UserAgent = 'Wiki_parser/0.1 run by DremSama'
site = Site(('http', 'wiki.support.veeam.local'), path='/', clients_useragent=UserAgent)
sf = Salesforce(username='dmitriy.rozhdestvenskiy@veeam.com', password='I^C92!T!!27j',
                security_token='dNr44yHsFXaSuRmKXunWPlzS')
PagesList = []
PagesBUGSList = []
page = site.Pages['Bug 44540 - Download from EM FLR doesn\'t work with long paths more than 260 symbols']
print('----------------------------------')
BugID = re.match(r'[A-z,a-z]ug\b.(\d*)[-|\s]*(.*)', page.page_title)
if BugID:
    BugID_NUM = BugID.group(1)
    BugID_SUBJECT = BugID.group(2)
textALL = page.text(0)
if not textALL:
    print('ERROR: Page "' + page.name + '" has no text')
elif textALL.startswith('#REDIRECT'):
    print('Page "' + page.name + '" is only a redirect page, skipping')
else:
    print(page.name)
    BugCaseID = re.findall(r"'''Case ID: '''(\d*)", textALL)
    BugToBeFixedIn = re.findall(r"'''To be fixed in: '''(.*)", textALL)
    if not BugToBeFixedIn:
        BugToBeFixedIn = re.findall(r"'''Fixed in: '''(.*)", textALL)
    BugPrivateFix = re.findall(r"'''Private fix: '''(.*)", textALL)
    BugAdded = re.findall(r"'''Added: '''(.*) by", textALL)
    BugAddedBy = re.findall(r"by \[\[User:.*\|(.*)\]\]", textALL)
    BugComponents = re.findall(r"'''Components: '''(.*)", textALL)
    if not BugCaseID:
        print('ERROR: Page' + page.name + ' BugCaseID was not found')
        print(textALL)
    elif not BugToBeFixedIn:
        print('ERROR: Page' + page.name + ' BugToBeFixedIn was not found')
        print(textALL)
    elif not BugPrivateFix:
        print('ERROR: Page' + page.name + ' BugPrivateFix was not found')
        print(textALL)
    elif not BugAdded:
        print('ERROR: Page' + page.name + ' BugPrivateFix was not found')
        print(textALL)
    elif not BugAddedBy:
        print('ERROR: Page' + page.name + ' BugAddedBy was not found')
        print(textALL)
    elif not BugComponents:
        print('ERROR: Page' + page.name + ' BugComponents was not found')
        print(textALL)
    else:
        if int(BugCaseID[0]) > 0:
            request = str(
                sf.query(
                    "SELECT Version__c, Versionselect__c, Hypervisor_c__c FROM case where CaseNumber ='" + BugCaseID[0] + "'"))
            CaseVersionHypervisor = re.findall(r"'VersionSelect__c', '([\d.]*)'\), \('Hypervisor_c__c', '(.*)'",
                                               request)
            if CaseVersionHypervisor:
                print(CaseVersionHypervisor[0][0] + ' ' + CaseVersionHypervisor[0][1])
            else:
                CaseVersionHypervisor = ['NONE', 'NONE']
                print('ERROR: CaseVersionHypervisor wasn\'t found due SF lags, let it be NONE')
                print(request)
        else:
            CaseVersionHypervisor = ['NONE', 'NONE']
            print('WARNING: Unable to check case number ' + BugCaseID[0])
        if BugPrivateFix[0] != 'n/a':
            StatusMacro = '<ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Green' \
                          '</ac:parameter><ac:parameter ac:name="title">fixed</ac:parameter><ac:parameter ac:name="subtle">true</ac:parameter></ac:structured-macro>'
        else:
            StatusMacro = '<ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Red' \
                          '</ac:parameter><ac:parameter ac:name="title">not fixed</ac:parameter><ac:parameter ac:name="subtle">true</ac:parameter></ac:structured-macro>'
        textDescription = page.text(1)
        # print(textDescription)
        textSolution = page.text(2)
        # print(textSolution)
        PagesBUGSList.append(page)
        # submitting bug to EE
        DictPage = {
            'PageBugID_NUM': BugID_NUM,
            'BugID_SUBJECT': BugID_SUBJECT,
            'PageCaseID': BugCaseID[0],
            'PageCaseVersion': CaseVersionHypervisor[0][0],
            'PageCaseHypervisor': CaseVersionHypervisor[0][1],
            'PageToBeFixedIn': BugToBeFixedIn[0],
            'PageStatusMacro': StatusMacro,
            'PageAdded': BugAdded[0],
            'PageAddedBy': BugAddedBy[0],
            'PageComponents': BugComponents[0]
        }