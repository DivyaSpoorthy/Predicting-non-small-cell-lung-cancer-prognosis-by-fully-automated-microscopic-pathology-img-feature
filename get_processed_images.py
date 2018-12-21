import requests
import json
import PIL
import openslide
import os

GDC_POST_URL = 'https://api.gdc.cancer.gov/files'

GDC_DOWNLOAD_URL = 'https://api.gdc.cancer.gov/data/'

payload = {
    "filters":{
        "op":"and",
        "content":[
            {
                "op":"in",
                "content":{
                    "field":"cases.disease_type",
                    "value":["Adenomas and Adenocarcinomas",
                             "Squamous Cell Neoplasms"]
                }
            },
            {
                "op": "in",
                "content":{
                    "field": "cases.project.project_id",
                    "value": ["TCGA-LUAD",
                               "TCGA-LUSC"]
                }
            },
            {
                "op": "in",
                "content":{
                    "field": "files.data_format",
                    "value": ["SVS"]
                }
            }
        ]
    },
    "size": 100
}

zoom_dim = 40

#Zoom and save and preprocess using bftools
def preprocess(filename):
    im_svs = openslide.OpenSlide(filename)
    tup = im_svs.level_dimensions[zoom_dim]
    img = im_svs.read_region(zoom_dim, tup) #Get image at x40
    img.save(filename + '-snap', "TIFF") #Save TIFF image


result_count = 0
max_results = 99999999

start = 1
while result_count < max_results:
    headers = {'Content-type': 'application/json'}
    payload['from'] = start
    response = requests.post(GDC_POST_URL, json.dumps(payload), headers=headers)

    d = dict(response.json())

    partial_res = d['data']

    pag_inf = partial_res['pagination']
    total = int(pag_inf['total'])

    if max_results is 99999999:
        max_results = total

    partial_res_cnt = int(pag_inf['count'])
    start += partial_res_cnt
    result_count += partial_res_cnt

    for result in partial_res['hits']:
        file_id = result['file_id']

        link = GDC_DOWNLOAD_URL + str(file_id)
        dst = file_id
        r = requests.get(link, stream=True) #Download and stream in chunks
        with open(dst, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        preprocess(dst)
        os.remove(dst) #Delete the big svs file


