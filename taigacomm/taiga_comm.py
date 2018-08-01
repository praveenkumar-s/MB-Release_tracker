import requests
import json
import os
import urlparse

class TaigaCommunicator:
    
    #! Authorization Header for all Taiga Requests
    Userdata=None
    AuthorizationHeader=None
    config=None
    def __init__(self,ApplicationToken=None, project_id=None):
        self.config=json.load(open(os.getcwd()+'/TaigaConfig.json'))
        if(ApplicationToken != None):
            self.AuthorizationHeader={"Authorization":"Application "+ApplicationToken}
        if(project_id!= None):
            self.project_id=project_id

    #!CreateIssue - Used for creating an Issue in Taiga.
    #!Example CreateIssue(projectid=92046, type="Bug" ,subject="subject", description=desc , priority = "Normal", severity="Normal" , status="Level 1" , tags=["Bot","bugbin"])
    def CreateIssue(self,projectid, **kwargs):
        datamodel={
        "assigned_to": None,
        "blocked_note": "",
        "description": "",
        "is_blocked": "false",
        "is_closed": "false",
        "milestone": None,
        "priority": 3,
        "project": 1,
        "severity": 2,
        "status": 3,
        "subject": "",
        "tags": [
            "Bugbin"
        ],
        "type": 1,
        "watchers": []
        }

        for args in kwargs:
            datamodel[args]=kwargs[args]
        self.AuthorizationHeader["Content-Type"]="application/json"
        #region Translations of status, priority, severity
        datamodel["project"]=projectid
        datamodel["status"]= self.getIssueStatusid(projectid,datamodel["status"])
        datamodel["priority"]= self.getPriorityStatusId(projectid,datamodel["priority"])
        datamodel["severity"]= self.getSeverityStatusId(projectid,datamodel["severity"])
        datamodel["type"]=self.getIssueTypeId(projectid, datamodel["type"])
        #endregion
        response=requests.post(url=urlparse.urljoin(self.config["APIHost"],self.config["issueEndpoint"]), data=json.dumps(datamodel), headers=self.AuthorizationHeader)
        if(response.status_code==201):
            return {"status_code":response.status_code, "content":response.content, "transaction_status":"OK"}
        else:
            return {"status_code":response.status_code, "content":response.content, "transaction_status":"FAILED"}    
        

    #!Authenticate User.
    #!Used to Authenticate Users with Taiga System to preform operations
    #!parameters --> username:{Taiga_User_Name}  password:{Taiga_Password}
    #! Retruns OK if fine. Else Retruns "ERROR"
    def AuthUser(self, username,password):
        #*Data Template for POST Request for Authorization
        datatemplate="""{
        "password": "{PASS}",
        "type": "normal",
        "username": "{USER}"
        }"""
        data=datatemplate.replace("{PASS}",password).replace("{USER}",username)
        response=requests.post(url=urlparse.urljoin(self.config["APIHost"],self.config["AuthEndpoint"]),data=data,headers={"Content-Type":"application/json"})
        if(response.status_code==200):
            self.Userdata=json.loads(response.content)
            self.AuthorizationHeader={"Authorization":"Bearer "+self.Userdata["auth_token"]}
            return "OK"
        else:
            return "ERROR: "+str(json.loads(response.content)["_error_message"])





    #!Get Details about the Issue by Issue Id
    #! GetIssue("974279")
    def GetIssue(self, issueId ):
        response=requests.get(urlparse.urljoin(self.config['APIHost'],self.config['issueEndpoint']+'/'+issueId), headers=self.AuthorizationHeader)
        if(response.status_code==200):
            return {"status_code":response.status_code,"content":json.loads(response.content),"transaction_status":"OK"}
        else:
            return {"status_code":response.status_code,"content":json.loads(response.content),"transaction_status":"FAIL"}


    
    #!Edit an Issue in Taiga
    #! Parameters issueId= {Taiga issue's ID}
    def EditIssue(self, issueId , **kwargs):
        data={}
        for args in kwargs:
            data[args]=kwargs[args]
        issue=self.GetIssue(issueId)
        data["version"]=issue["version"]    
        self.AuthorizationHeader["Content-Type"]="application/json"    
        response = requests.patch(url=urlparse.urljoin(self.config['APIHost'],self.config['issueEndpoint']+'/'+issueId), data=json.dumps(data), headers=self.AuthorizationHeader)
        if(response.status_code==200):
            return {"status_code":response.status_code,"content":json.loads(response.content),"transaction_status":"OK"}
        else:
            return {"status_code":response.status_code,"content":json.loads(response.content),"transaction_status":"FAIL"}



    #! Get information about the projects assigned  for an user
    def getAssociatedProjects(self):
        params={'member':self.Userdata['id']}
        response=requests.get(urlparse.urljoin(self.config['APIHost'],self.config['projects']),params=params,headers=self.AuthorizationHeader)
        if(response.status_code==200):
            return {"status_code":response.status_code,"content":json.loads(response.content),"transaction_status":"OK"}
        else:
            return {"status_code":response.status_code,"content":json.loads(response.content),"transaction_status":"FAIL"}



    #! Get Projects simplified
    #! Returns a simplified version of the projects
    #! Eg. [{u'Justickets': 144110}, {u'Moviebuff': 92046}, {u'Moviepass and QubeID': 29888}, {u'Slydes': 167933}]
    def getAssociatedProjectssimplified(self):
        x=self.getAssociatedProjects()['content']
        if(x==None):
            return None
        arr=[]
        for items in x:
            arr.append({items["name"]:items["id"]})
        return arr
    
    #! Internal Translation method to change status name to Id
    def getIssueStatusid(self, projectId,status):
        response = requests.get(url= urlparse.urljoin(self.config['APIHost'],self.config['issue_status']),params={"project":projectId}, headers=self.AuthorizationHeader)
        if(response.status_code==200):
            content= json.loads(response.content)
            for items in content:
                if items["name"]==status:
                    return items["id"]

    #! Internal Translation method to change priority name to Id                
    def getPriorityStatusId(self, projectId,priority):
        response = requests.get(url= urlparse.urljoin(self.config['APIHost'],self.config['priority']),params={"project":projectId}, headers=self.AuthorizationHeader)
        if(response.status_code==200):
            content= json.loads(response.content)
            for items in content:
                if items["name"]==priority:
                    return items["id"]
    
    #! Internal Translation method to change priority name to Id
    def getSeverityStatusId(self, projectId,severity):
        response = requests.get(url= urlparse.urljoin(self.config['APIHost'],self.config['severity']),params={"project":projectId}, headers=self.AuthorizationHeader)
        if(response.status_code==200):
            content= json.loads(response.content)
            for items in content:
                if items["name"]==severity:
                    return items["id"]

    #! Internal Translation method to change priority name to Id
    def getIssueTypeId(self, projectId,issueType):
        response = requests.get(url= urlparse.urljoin(self.config['APIHost'],self.config['issue_types']),params={"project":projectId}, headers=self.AuthorizationHeader)
        if(response.status_code==200):
            content= json.loads(response.content)
            for items in content:
                if items["name"]==issueType:
                    return items["id"]

    #! Return the issue status id based on issue names
    def open_issue(self,product_name):
        statuses= self.config["issue_status_names"]
        for items in statuses:
            if items["product_name"]==product_name:
                return self.getIssueStatusid(projectId=items["project_id"],status= items["issue_open_status_name"])
                
    def close_issue(self,product_name):
        statuses= self.config["issue_status_names"]
        for items in statuses:
            if items["product_name"]==product_name:
                return self.getIssueStatusid(projectId=items["project_id"],status=items["issue_close_status_name"])
