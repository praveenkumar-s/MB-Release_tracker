import storytree
import issuetree
import epictree
from json2html import *
from collections import OrderedDict
import json



#release_date=json.load(open("release_dates_sample.json"), object_pairs_hook=OrderedDict)

def processor(release_date_json):
    config=json.load(open('TaigaConfig.json'))
    output=OrderedDict()
    for items in release_date_json['dates']:
        output[items]=[]
        for subitems in release_date_json['dates'].get(items):
            if(subitems['kind']=='story'):
                operation=storytree.StorytTree(subitems['ref'], config['project_ids'][release_date_json['product']])
                output[items].append(operation.get())
            if(subitems['kind']=='issue'):
                operation=issuetree.IssueTree(subitems['ref'], config['project_ids'][release_date_json['product']])
                output[items].append(operation.get())
            if(subitems['kind']=='epic'):
                operation=epictree.EpicTree(subitems['ref'], config['project_ids'][release_date_json['product']])
                output[items].append(operation.get())
    return json.dumps(output)


def plan2html(plan):
    return json2html.convert(json = plan, table_attributes="align=\"center\" border=\"3\" id=\"info-table\" class=\"table table-bordered table-hover\"")


