from taiga_reader import TaigaReader
import os

class IssueTree():
    """
        Given an issue id, get the following details:
        -issue status
    """
    issue_ref=None
    issue_id=None
    issue_status=None
    issue_desc=None
    def __init__(self,issue_ref, project_id):
        TR=TaigaReader(project_id=project_id)
        TR.AuthUser(os.environ["TAIGA_UN"],os.environ["TAIGA_PWD"])
        issue=TR.getIssueById(issue_ref)
        self.issue_ref=issue_ref
        self.issue_id=issue['id']
        self.issue_status=issue['status_extra_info']['name']
        self.issue_desc=issue['subject']
    
    def get(self):
        return{
            'Issue: ':self.issue_ref+' '+self.issue_desc,
            'Status':self.issue_status
        }