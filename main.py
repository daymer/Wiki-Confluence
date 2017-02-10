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


for page in site.allpages():
    PagesList.append(page)
    if page.name.startswith('Bug') or page.name.startswith('bug'):
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
                            "SELECT Versionselect__c, Hypervisor_c__c FROM case where CaseNumber ='" + BugCaseID[0] + "'"))
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
                #print(textDescription)
                textSolution = page.text(2)
                #print(textSolution)
                PagesBUGSList.append(page)
                #submitting bug to EE
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

                def PageGen(Dict):
                    pagebody = str('<ac:layout>'
                                   '<ac:layout-section ac:type="two_equal"><ac:layout-cell>'\
                                   '<h2>General info:</h2>' \
                                   '<ac:structured-macro ac:name="details"><ac:parameter ac:name="id">1' \
                                   '</ac:parameter><ac:rich-text-body>' \
                                   '<table>' \
                                   '<tbody>' \
                                   '<tr>' \
                                   '<td><strong>Case ID:</strong></td>' \
                                   '<td colspan="1">' + Dict['PageCaseID'] + '</td></tr>' \
                                   '<tr>' \
                                   '<td><strong>Found in Version:</strong></td>' \
                                   '<td colspan="1">' + Dict['PageCaseVersion'] + '</td></tr>' \
                                   '<tr>' \
                                   '<td><strong>Hypervisor in case:</strong></td>' \
                                   '<td colspan="1">' + Dict['PageCaseHypervisor'] + '</td></tr>' \
                                   '<tr>' \
                                   '<td><strong>To be fixed in:</strong></td>' \
                                   '<td colspan="1">' + Dict['PageToBeFixedIn'] + '</td></tr>' \
                                   '<tr>' \
                                   '<td><strong>Current status:</strong></td>' \
                                   '<td colspan="1">' + Dict['PageStatusMacro'] + '</td></tr>' \
                                   '<tr>' \
                                   '<td><strong>Added:</strong></td>' \
                                   '<td colspan="1">' + Dict['PageAdded'] + '</td></tr>' \
                                   '<tr>' \
                                   '<td><strong>Added by:</strong></td>' \
                                   '<td colspan="1">' + Dict['PageAddedBy'] + '</td></tr>' \
                                   '<tr>' \
                                   '<td colspan="1"><strong>Components:&nbsp;</strong>'
                                   '</td><td colspan="1"><span>' + Dict['PageComponents'] + '</span></td></tr>' \
                                   '</tbody></table></ac:rich-text-body></ac:structured-macro></ac:layout-cell><ac:layout-cell>' \
                                   '<p><ac:structured-macro ac:name="attachments" /></p>' \
                                   '</ac:layout-cell></ac:layout-section><ac:layout-section ac:type="single">' \
                                   '<ac:layout-cell>' \
                                   '<h2><span class="mw-headline">Description</span></h2>' \
                                   '<h2><span class="mw-headline">Solution</span></h2>'\
                                   '</ac:layout-cell>'\
                                   '<p><span class="mw-headline"><br /></span></p></ac:layout-section></ac:layout>')
                                   #'<p>' + textSolution + '</p>'
                                   #'<p>' + textDescription + '</p>' \
                    title = "Bug " + Dict['PageBugID_NUM'] + " " + Dict['BugID_SUBJECT']
                    pagecontent = {
                        "type": "page",
                        "title": title,
                        "ancestors": [{"type": "page", "id": 13434925}],
                        #http://ee.support2.veeam.local/display/TKB/Found+Bugs
                        "space": {
                            "key": "TKB"
                        },
                        "body": {
                            "storage": {
                                "value": pagebody,
                                "representation": "storage"
                            }
                        }
                    }
                    return pagecontent

                PageContentGenerated = PageGen(DictPage)
                title = "Bug " + BugID_NUM + " " + BugID_SUBJECT

                #api.create_new_content(content)
                print('...migrated')


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
print('----------------------------------')
print(len(PagesBUGSList))
#print(PagesList)

'''
#'<ac:structured-macro ac:name="code"><ac:parameter ac:name="theme">Emacs</ac:parameter><ac:parameter ac:name="linenumbers">true</ac:parameter>' \
#'<ac:parameter ac:name="language">perl</ac:parameter><ac:plain-text-body>' \
#'<![CDATA[[21.11.2016 05:06:08] <20> Error    Failed to connect to agent\'s endpoint \'172.30.0.147:2504\'. Host: \'54.209.155.168\'.' \
#'[21.11.2016 05:06:08] <20> Error    A connection attempt failed because the connected party did not properly respond after a period of time, or established \r\n' \
#'connection failed because connected host has failed to respond 172.30.0.147:2504 (System.Net.Sockets.SocketException)' \
#'[21.11.2016 05:06:08] <20> Error       at System.Net.Sockets.Socket.DoConnect(EndPoint endPointSnapshot, SocketAddress socketAddress)' \
#'[21.11.2016 05:06:08] <20> Error       at System.Net.Sockets.Socket.Connect(EndPoint remoteEP)' \
#'[21.11.2016 05:06:08] <20> Error       at Veeam.Backup.AgentProvider.CAgentEndpointConnecter.ConnectToAgentEndpoint(ISocket socket, IAgentEndPoint endPoint)]]></ac:plain-text-body></ac:structured-macro></ac:layout-cell></ac:layout-section><ac:layout-section ac:type="single"><ac:layout-cell>' \

                               #'<p><span class="mw-headline"><span style="color: rgb(37,37,37);">Private fix for v.9.5.0.711 is available.</span></span></p><ac:structured-macro ac:name="panel"><ac:rich-text-body>' \
                           #'<ol>' \
                           #'<li><span style="color: rgb(37,37,37);">Make sure, that no jobs are running at the moment;</span></li>' \
                           #'<li><span style="color: rgb(37,37,37);">Stop all Veeam services;</span></li>' \
                           #'<li><span style="color: rgb(37,37,37);">Go to installation folder (default: C:\Program Files\Veeam\Backup and Replication\Backup);</span></li>' \
                           #'<li>Copy the original files somewhere before replacing them<br /><strong>veeam.backup.servicelib.dll</strong><br /><strong>veeam.backup.core.dll</strong><br /><strong>veeam.backup.CloudService.exe</strong></li>' \
                           #'<li>Copy new DLL files from the fix folder to the installation folder;</li>' \
                           #'<li>Start Veeam services;</li></ol>' \
                           #'<p>&nbsp;</p></ac:rich-text-body></ac:structured-macro>' \
                           #'<p><span class="mw-headline"><br /></span></p></ac:layout-cell></ac:layout-section></ac:layout>'



'''