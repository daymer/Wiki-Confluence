from PythonConfluenceAPI import ConfluenceAPI

api = ConfluenceAPI('admin', '123@qwe', 'http://127.0.0.1:8090')
spaces = api.get_space_content('TKB')
print(spaces)
PageBody = '<ac:layout><ac:layout-section ac:type="two_equal"><ac:layout-cell>' \
            '<h2>General info:</h2>' \
            '<ac:structured-macro ac:name="details"><ac:parameter ac:name="id">1</ac:parameter><ac:rich-text-body>' \
            '<table>' \
            '<tbody>' \
            '<tr>' \
            '<td><strong>Case ID:</strong></td>' \
            '<td colspan="1">01980837</td></tr>' \
            '<tr>' \
            '<td><strong>Found in Version:</strong></td>' \
            '<td colspan="1">9.0</td></tr>' \
            '<tr>' \
            '<td><strong>To be fixed in:</strong></td>' \
            '<td colspan="1">9.5 update 1</td></tr>' \
            '<tr>' \
            '<td><strong>Current status:</strong></td>' \
            '<td colspan="1"><ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Green</ac:parameter><ac:parameter ac:name="title">fixed</ac:parameter><ac:parameter ac:name="subtle">true</ac:parameter></ac:structured-macro></td></tr>' \
            '<tr>' \
            '<td><strong>Comments:</strong></td>' \
            '<td colspan="1">none</td></tr>' \
            '<tr>' \
            '<td colspan="1"><strong>Components:&nbsp;</strong></td>' \
            '<td colspan="1"><span>Agent, Backup, Rescan</span></td></tr></tbody></table></ac:rich-text-body></ac:structured-macro></ac:layout-cell><ac:layout-cell>' \
            '<p><ac:structured-macro ac:name="attachments" /></p></ac:layout-cell></ac:layout-section><ac:layout-section ac:type="single"><ac:layout-cell>' \
            '<h2><span class="mw-headline">Description</span></h2>' \
            '<p>Server is added to Veeam using public ip, which is not listed inside guest.<br />Veeam does not have direct access to private ip on linux, so the communication should go over public ip.<br />We login to this Server via SSH using correct ip and start agent there, but agents connection goes only via private one.</p><ac:structured-macro ac:name="code"><ac:parameter ac:name="theme">Emacs</ac:parameter><ac:parameter ac:name="linenumbers">true</ac:parameter>' \
            '<ac:parameter ac:name="language">perl</ac:parameter><ac:plain-text-body>' \
            '<![CDATA[[21.11.2016 05:06:08] <20> Error    Failed to connect to agent\'s endpoint \'172.30.0.147:2504\'. Host: \'54.209.155.168\'.' \
            '[21.11.2016 05:06:08] <20> Error    A connection attempt failed because the connected party did not properly respond after a period of time, or established \r\n' \
            'connection failed because connected host has failed to respond 172.30.0.147:2504 (System.Net.Sockets.SocketException)' \
            '[21.11.2016 05:06:08] <20> Error       at System.Net.Sockets.Socket.DoConnect(EndPoint endPointSnapshot, SocketAddress socketAddress)' \
            '[21.11.2016 05:06:08] <20> Error       at System.Net.Sockets.Socket.Connect(EndPoint remoteEP)' \
            '[21.11.2016 05:06:08] <20> Error       at Veeam.Backup.AgentProvider.CAgentEndpointConnecter.ConnectToAgentEndpoint(ISocket socket, IAgentEndPoint endPoint)]]></ac:plain-text-body></ac:structured-macro></ac:layout-cell></ac:layout-section><ac:layout-section ac:type="single"><ac:layout-cell>' \
            '<h2><span class="mw-headline">Solution</span></h2>' \
            '<p><span class="mw-headline"><span style="color: rgb(37,37,37);">Private fix for v.9.5.0.711 is available.</span></span></p><ac:structured-macro ac:name="panel"><ac:rich-text-body>' \
            '<ol>' \
            '<li><span style="color: rgb(37,37,37);">Make sure, that no jobs are running at the moment;</span></li>' \
            '<li><span style="color: rgb(37,37,37);">Stop all Veeam services;</span></li>' \
            '<li><span style="color: rgb(37,37,37);">Go to installation folder (default: C:\Program Files\Veeam\Backup and Replication\Backup);</span></li>' \
            '<li>Copy the original files somewhere before replacing them<br /><strong>veeam.backup.servicelib.dll</strong><br /><strong>veeam.backup.core.dll</strong><br /><strong>veeam.backup.CloudService.exe</strong></li>' \
            '<li>Copy new DLL files from the fix folder to the installation folder;</li>' \
            '<li>Start Veeam services;</li></ol>' \
            '<p>&nbsp;</p></ac:rich-text-body></ac:structured-macro>' \
            '<p><span class="mw-headline"><br /></span></p></ac:layout-cell></ac:layout-section></ac:layout>'
content ={
    "type": "page",
    "title": "Bug test2",
    "ancestors": [{"type": "page", "id": 13434925}], #http://ee.support2.veeam.local/display/TKB/Found+Bugs
    "space": {
        "key": "TKB"
    },
    "body": {
        "storage": {
            "value": PageBody,
            "representation": "storage"
        }
    }
}

api.create_new_content(content)