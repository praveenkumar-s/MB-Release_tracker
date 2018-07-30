from taiga_reader import TaigaReader
import os



class StorytTree():
    """
    Given a Story ID:
        get the status of the story 
        get the total number of tasks under the story 
        get the number of closed tasks in the story 
        get the number of open tasks in the story 
        get the issues and associated status under that story
    
    data_structure will be :
        story_id:
        description:
        link:
        status:
        total_tasks:
        closed_tasks:
        pending_tasks:
        total_issues:
        closed_issues:
        pending_issues:
        issues:
            - issue id
            - title
            - status
    """
    story_ref=None
    story_id=None
    description=None
    status=None
    total_tasks=None
    closed_tasks=None
    pending_tasks=None
    total_issues=None
    closed_issues=None
    Pending_issues=None


    def __init__(self, story_ref , project_id):
        TR=TaigaReader(project_id=project_id)
        TR.AuthUser(os.environ["TAIGA_UN"],os.environ["TAIGA_PWD"])
        story=TR.getStoryByRef(story_ref)
        self.story_ref=story_ref
        self.story_id=story['id']
        self.description=story['subject']
        self.status=story['status_extra_info']['name']
        tasks=TR.getTasksbyStory(self.story_id)
        self.total_tasks=len(tasks)
        
        ct=0
        for items in tasks:
            if(items['is_closed']==True):
                ct=ct+1
        self.closed_tasks=ct
        self.pending_tasks=self.total_tasks-self.closed_tasks

        issues=TR.getIssuesByStory(story_ref)
        self.total_issues=len(issues)
        ci=0
        for items in issues:
            if(items['is_closed']==True):
                ci=ci+1
        self.closed_issues=ci
        self.Pending_issues=self.total_issues-self.closed_issues

    def get(self):
        return {
            "  Story: "+self.status: {self.story_ref+': '+self.description:{
            "Tasks":{
                "Total":self.total_tasks,
                "Closed":self.closed_tasks,
                "Open":self.pending_tasks,
            },
            "Issues":{
                "Total":self.total_issues,
                "Closed":self.closed_issues,
                "Open":self.Pending_issues
            }
            
        
        }}}

"""
x=StorytTree('4500')

y=x.get()

status={'31-July-2018':[y]}

import pprint
from json2html import *

pprint.pprint( json2html.convert(json=status, table_attributes=" id=\"info-table\" class=\"table table-bordered table-hover\"")   ) 
"""