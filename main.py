import boto3
from fastapi import FastAPI,Form,File,UploadFile
import json
from random import randint
#import pprin
from parsers import(
    extract_text,
    map_word_id,
    extract_table_info,
    get_key_map,
    get_value_map,
    get_kv_map,
) 
# import logging
# from botocore.exceptions import ClientError



app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# s3 = boto3.resource(
#     service_name='s3',
#     region_name='ap-south-1',
#     aws_access_key_id='AKIAUB4VE3EDLJ254MJL',
#     aws_secret_access_key='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'
# )
# #Print out bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)


# @app.post("/upload")
# def upload():
#     s3_client=boto3.client('s3')
#     response=s3_client.upload_file('C:/Users/User/Downloads/table.pdf','textract-infeon-demo','table.pdf')
#     return({response:"sucefully upload"})


import uuid  
# boto3 client
client = boto3.client(
    'textract', 
    region_name='ap-south-1', 
    aws_access_key_id='AKIAUB4VE3EDLJ254MJL', 
    aws_secret_access_key='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'
)

# Read image


@app.post("/file/")
async def create_upload_file(file: UploadFile = File(...)):
            img = await file.read()

        # Call Amazon Textract
            response = client.detect_document_text(
                Document={'Bytes': img}
                )
    
            response = client.detect_document_text(
                Document={'Bytes': img}
                )
            raw_text =extract_text(response,extract_by="LINE")
            word_map = map_word_id(response)
            table = extract_table_info(response, word_map)
            key_map = get_key_map(response, word_map)
            value_map = get_value_map(response, word_map)
            final_map = get_kv_map(key_map, value_map)
     
        
            # print(json.dumps(table))
            # print(json.dumps(final_map))
            # print(raw_text)
  
            value=dict()
            value['table']=json.dumps(table)
            value['final_map']=final_map
            value['raw_text']=raw_text  
            value['key_map']=key_map
            return(value)        
            # metadaat=[json.dumps(table),json.dumps(final_map),raw_text]
            # return metadaat
        
            #return {"statusCode": 200, "body": json.dumps("Thanks from Srce Cde!")}
        

