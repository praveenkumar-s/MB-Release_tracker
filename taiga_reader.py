from taigacomm import taiga_comm as coms
import requests
import pprint
import urlparse
class TaigaReader(coms.TaigaCommunicator):
    
    def getStoryByRef(self,refid):
        return requests.get(self.config['APIHost']+'/api/v1/userstories/by_ref',params={'ref':refid,'project':self.project_id},headers=self.AuthorizationHeader).json()

    def getTasksbyStory(self,user_story_id):
        return requests.get('https://api.taiga.io/api/v1/tasks',headers=self.AuthorizationHeader, params={'project':self.project_id,'user_story':user_story_id}).json()
    
    def getIssuesByStory(self,refid):
        return requests.get('https://api.taiga.io/api/v1/issues',headers=self.AuthorizationHeader, params={'order_by':'status','project':self.project_id,'q':refid}).json()

    def getIssueById(self,refid):
        return requests.get('https://api.taiga.io/api/v1/issues/by_ref',headers=self.AuthorizationHeader,params={'ref':refid,'project':self.project_id}).json()

    def getEpicByid(self,refid):
        return requests.get('https://api.taiga.io/api/v1/epics/by_ref',headers=self.AuthorizationHeader,params={'ref':refid,'project':self.project_id}).json()

    def getStoriesByEpic(self,epic_id):
        return requests.get('https://api.taiga.io/api/v1/epics/'+epic_id +'/related_userstories',headers=self.AuthorizationHeader).json()

    def set_Auth_token(self,user,password):
        datatemplate="""{
            "password": "{PASS}",
            "type": "normal",
            "username": "{USER}"
            }"""
        data=datatemplate.replace("{PASS}",password).replace("{USER}",user)
        response=requests.post(url=urlparse.urljoin(self.config["APIHost"],self.config["AuthEndpoint"]),data=data,headers={"Content-Type":"application/json"})
        if(response.status_code==200):
            return response.json()['auth_token']
        else:
            return None