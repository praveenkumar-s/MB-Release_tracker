from taiga_reader import TaigaReader
import os

class EpicTree():
    """
        Given an epic's ref, get the following 

        epic id
        epic status
        total stories in epic
        total stories that are closed
        total stories that are open
    """
    epic_id=None
    epic_ref=None
    epic_status=None
    epic_desc=None
    epic_total_stories=None
    epic_closed_stories=None
    epic_open_stories=None

    def __init__(self, ref_id, project_id):
        TR=TaigaReader(project_id=project_id)
        TR.AuthUser(os.environ["TAIGA_UN"],os.environ["TAIGA_PWD"])
        epic=TR.getEpicByid(ref_id)
        self.epic_id=epic['id']
        self.epic_ref=ref_id
        self.epic_status=epic['status_extra_info']['name']
        self.epic_desc=epic['subject']
        self.epic_total_stories=epic['user_stories_counts']['total']
        self.epic_closed_stories=epic['user_stories_counts']['progress']
        self.epic_open_stories=self.epic_total_stories-self.epic_closed_stories
    
    def get(self):
        return{
            '  Epic: '+self.epic_status: { self.epic_ref+' ' + self.epic_desc:{
            'stories':{
                'Total':self.epic_total_stories,
                'Closed':self.epic_closed_stories,
                'Open': self.epic_open_stories
            }} 
        }}