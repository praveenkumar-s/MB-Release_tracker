import storytree
import issuetree
import epictree
from collections import OrderedDict
import json
from taiga_reader import TaigaReader
import os
import html_templates
import data_struct_utils
container_class='container right'

def swap_container_class():
    global container_class
    if (container_class== 'container left'):
        container_class= 'container right'
    else:
        container_class= 'container left'
    return container_class

#release_date=json.load(open("release_dates_sample.json"), object_pairs_hook=OrderedDict)

def processor(release_date_json):
    Highlight_start='<span style="background-color: #FFFF00"><b>'
    Highlight_end='</span></b>'
    TR=TaigaReader(project_id=release_date_json['product'])
    os.environ['auth_token']= TR.set_Auth_token(os.environ["TAIGA_UN"],os.environ["TAIGA_PWD"])
    config=json.load(open('TaigaConfig.json'))
    contents=""
    for items in release_date_json['dates']:
        contents_per_date=""
        for subitems in release_date_json['dates'].get(items):
            if(subitems['kind']=='story'):
                operation=storytree.StorytTree(subitems['ref'], config['project_ids'][release_date_json['product']])
                contents_per_date= contents_per_date + html_templates.story_container.format('Story: '+operation.story_ref+': '+operation.description,'Status: '+Highlight_start+operation.status+Highlight_end ,  'Issues: Open: {0} | Closed: {1}'.format(operation.Pending_issues,operation.closed_issues), 'Tasks:   Open: {0} | Closed: {1}'.format(operation.pending_tasks,operation.closed_tasks))
            if(subitems['kind']=='issue'):
                operation=issuetree.IssueTree(subitems['ref'], config['project_ids'][release_date_json['product']])
                contents_per_date= contents_per_date + html_templates.issue_containter.format('Issue: '+operation.issue_ref+': '+ operation.issue_desc,'Status: '+Highlight_start+operation.issue_status+Highlight_end)                
            if(subitems['kind']=='epic'):
                operation=epictree.EpicTree(subitems['ref'], config['project_ids'][release_date_json['product']])
                contents_per_date= contents_per_date + html_templates.epic_container.format('Epic: '+operation.epic_ref+': '+operation.epic_desc , 'Status: '+ Highlight_start+operation.epic_status+Highlight_end ,'Stories: Open:{0} | Closed: {1}'.format(int(operation.epic_open_stories),int(operation.epic_closed_stories)))
            
        contents= contents + html_templates.data_container.format(Release_date=items, stories_or_Issues_or_epics= contents_per_date, container_class=swap_container_class())
    contents=html_templates.base_page.replace('{ELEMENTS_OF_TIMELINE}',contents)    
    return contents

def process_historical_releases(product_name,product_id=None):
    if(product_id==None):
        config=json.load(open('TaigaConfig.json'))
        product_id=config['project_ids'][product_name]    
    TR=TaigaReader(project_id=product_id)
    os.environ['auth_token']= TR.set_Auth_token(os.environ["TAIGA_UN"],os.environ["TAIGA_PWD"])
    TR.AuthUser(os.environ["TAIGA_UN"],os.environ["TAIGA_PWD"])
    releasedStories=None
    releaseIssues=None
    release_data=None
    releasedStories= TR.getReleasedStories()
    releaseIssues=TR.getReleasedIssues()
    release_data=data_struct_utils.groupby_year_month(releasedStories)
    release_data=data_struct_utils.groupby_year_month(releaseIssues,release_data)
    return release_data