import logging, utils, json, time
from config import IGLOO_BASE_URL, IGLOO_PASSWORD, IGLOO_USER

import const

import requests
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

class ApiIgloo:
    
    @classmethod
    def get_dps_score(cls, doc_mrz=const.MRZ, 
    doc_picture=const.PHOTOBASE64):
        
        tic = time.time()
        url = IGLOO_BASE_URL
        auth=(IGLOO_USER, IGLOO_PASSWORD)
        headers = {
            'user-agent': 'innoteam',
            'Content-Type': 'application/json',
            'mode':'norm'
            }
        payload = {
            'docAlpha': doc_mrz,
            'photoBase64': doc_picture,
            'x':57, 'y':328, 'w':695, 'h':867
            }

        logging.info('PAYLOAD docAlpha: {}'.format(doc_mrz))
        logging.info('PAYLOAD photoBase64: {}'.format(doc_picture[:15]))
        
        response = requests.post(url, auth=auth, headers=headers, json=payload) # data=json.dumps(payload)) #json=payload)  # 
        response_body = response.json()
    
        logging.info('URL: {}'.format(response.url))
        logging.info('Headers: {}'.format(response.headers))
        logging.info('----------'*5)
        logging.info('DPS Distance: {}'.format( response_body['distance'] ))
        logging.info('----------'*5)
        logging.info('x:{}, y:{}, w:{}, h:{}'.format( response_body['x'],response_body['y'],response_body['w'],response_body['h'] ))
        logging.info('----------'*5)
        logging.info('raise_for_status: {}'.format( response.raise_for_status() ))
        logging.info('status_code: {}'.format(response.status_code))
        logging.info('elpased time: {}'.format(time.time() - tic))
        
        return response_body['distance']