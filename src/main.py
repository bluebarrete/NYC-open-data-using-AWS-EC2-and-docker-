from sodapy import Socrata
import requests
from requests.auth import HTTPBasicAuth
import argparse
import sys
import os
import json 
parser = argparse.ArgumentParser(description='Process data from project')
parser.add_argument('--page_size', type=int,
                    help = 'how many rows to get per page', required = True)
parser.add_argument('--num_pages', type=int,
                    help = 'how many pages to get in total')
args = parser.parse_args(sys.argv[1:])

'''
DATASET_ID="nc67-uf89"
APP_TOKEN="5lMjOivZyCXZNcza8FYif28IZ"
ES_HOST="https://search-project01-ckicdd7aebnapooogqb2iqlbbm.us-east-2.es.amazonaws.com"
ES_USERNAME="jayant"
ES_PASSWORD="Jayant@123"
INDEX_NAME ="opcv"
'''
DATASET_ID = os.environ["DATASET_ID"]
APP_TOKEN = os.environ["APP_TOKEN"]
ES_HOST = os.environ["ES_HOST"]
ES_USERNAME = os.environ["ES_USERNAME"]
ES_PASSWORD = os.environ["ES_PASSWORD"]
INDEX_NAME=os.environ["INDEX_NAME"]



if __name__ == '__main__':
    #resp = requests.get(ES_HOST, auth=HTTPBasicAuth(ES_USERNAME,ES_PASSWORD))
    #print(resp.json())
    try:
        resp = requests.put(
            f"{ES_HOST}/{INDEX_NAME}",
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
            
            json = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "mappings": {
                    "properties": {
                        "plate": {"type": "keyword"},
                        "state": {"type": "keyword"},
                        "license_type": {"type": "keyword"},
                        "summons_number": {"type": "keyword"},
                        "issue_date": {"type": "date", "format": "mm/dd/yyyy"},
                        "violation_time": {"type": "keyword"},
                        "violation": {"type": "keyword"},
                        "fine_amount": {"type": "float"},
                        "penalty_amount": {"type": "float"},
                        "interest_amount": {"type": "float"},
                        "reduction_amount": {"type": "float"},
                        "payment_amount": {"type": "float"},
                        "amount_due": {"type": "float"},
                        "precinct": {"type": "keyword"},
                        "county": {"type": "keyword"},
                        "issuing_agency": {"type": "keyword"},
                    }
                },
            })
        resp.raise_for_status()
        print(resp.json())
    except Exception:
        print("Index already exists! Skipping")
    


    client = Socrata("data.cityofnewyork.us", APP_TOKEN,)
    rows=[]
    for i in range(args.num_pages):
        rows=client.get(DATASET_ID, limit=args.page_size,offset=args.num_pages*i)
        es_rows=[]
    #print(rows)
    
        for row in rows:
            try:
                es_row={}
                es_row["issue_date"] = row["issue_date"]
                es_row["fine_amount"] = float(row["fine_amount"])
                es_row["penalty_amount"] = float(row["penalty_amount"])
                es_row["interest_amount"] = float(row["interest_amount"])
                es_row["reduction_amount"] = float(row["reduction_amount"])
                es_row["payment_amount"] = float(row["payment_amount"])
                es_row["amount_due"] = float(row["amount_due"])
                es_row["plate"] = row["plate"]
                es_row["state"] = row["state"]
                es_row["license_type"] = row["license_type"]
                es_row["summons_number"] =row["summons_number"]
                es_row["violation"] = row["violation"]
                es_row["precinct"] = row["precinct"]
                es_row["county"] = row["county"]
                es_row["issuing_agency"] = row["issuing_agency"]
            except Exception as e:
                print(f"Error!: {e}, row SKIPPED! : {row}")
                continue
            es_rows.append(es_row)
    #print(es_rows)
    #print(len(es_rows))
        bulk_upload_data = ""
        for line in es_rows:
            print(f'Handling row {line["summons_number"]}')
            action = '{"index": {"_index": "' + INDEX_NAME + '", "_type": "_doc", "_id": "' + line["summons_number"] + '"}}'
            data = json.dumps(line)
            bulk_upload_data += f"{action}\n"
            bulk_upload_data += f"{data}\n"
        #print (bulk_upload_data)
    
        try:
            
            resp = requests.post(f"{ES_HOST}/_bulk",
            
                    data=bulk_upload_data,auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD), headers = {"Content-Type": "application/x-ndjson"})
            resp.raise_for_status()
            print ('Done')
            
        
        except Exception as e:
            print(f"INSERTION FAILED in ES: {e}, skipping row: {row}")

        
        
    
    
    '''
        try:
            resp = requests.post(
                f"{ES_HOST}/project/_doc",
                json=row,
                auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD)
            )
            resp.raise_for_status()
        except Exception as e:
            print(f"Upload to ES Failed: {e}, skipping row: {row}")
            continue
        
        print(resp.json())
'''
