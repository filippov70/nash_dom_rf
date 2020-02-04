#!/usr/bin/env python3

import json
import os.path
import time

# from urllib.request import urlopen
import requests

# from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

jsfile = open("houses.json", "rt")

json_data = json.load(jsfile)

mp_file = open('new_buildings.mp', 'w')
header = '''
; Generated by GPSMapEdit 1.24.2.0ASu
[IMG ID]
CodePage=65001
LblCoding=9
Locale=0x409
ID=
Name=
TypeSet=Navitel
Elevation=M
Preprocess=F
TreSize=511
TreMargin=0.000000
RgnLimit=127
POIIndex=Y
PAI5=Y
Levels=2
Level0=26
Level1=8
Zoom0=0
Zoom1=1
[END-IMG ID]

'''

poi_begin = '''
[POI]
Type=0x2c00
'''
poi_end = '''
[END]
'''

script = '''
var callback = arguments[arguments.length - 1]; // https://electrictower.ru/webdriver-executescript-i-executeasyncscript/
var xcsrf = document.getElementById('csrf-token').value;
//console.log('current xcsrf=' + xcsrf);
var oReq = new XMLHttpRequest();
oReq.onload = function() {
  if (this.status == 200 && this.readyState == 4) {
    //console.log(this);
    //console.log(JSON.stringify(this.response));
    var data = JSON.stringify(this.response);
    //console.log('this.response = ' + data);
    callback(data);
  } else {
    console.log('status != 200, status is '+this.status);
    callback(null);
  }
};
oReq.responseType = 'json';
oReq.open("GET", "https://наш.дом.рф/каталог_объектов/grapi/v1/housingUnderConstruction/houseCard/_ID_", true);
oReq.setRequestHeader('content-type', 'application/json');
oReq.setRequestHeader('x-csrf', xcsrf);
oReq.send();
'''
request_counter = 0
mp_file.write(header)
options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(
    '/home/filippov/software/firefox/', options=options)  # options=options

driver.get('https://наш.дом.рф/каталог_объектов/новостройки/карта')


def get_attribute_ajax(obj):
  global request_counter
  request_counter += 1
  #print('request_counter=' + str(request_counter))
  if request_counter == 100:
    request_counter = 0
    driver.refresh()
    print('F5')
    time.sleep(10)
    print('refreshed')
  uid = obj['b2c_object_id']
  run_script = script.replace('_ID_', uid)
  # print (run_script)
  time.sleep(1)
  response = driver.execute_async_script(run_script)
  if response is not None:
    response_json = json.loads(response)
    print('return ' + response_json['address'])
    adres = response_json['address']
    date = response_json['readyDateString']
    developer = response_json['developer']['name']
    returned_data = ''
    if adres is not None:
      returned_data += ';ADDR=' + adres
    if date is not None:
      returned_data += '\n;DATE=' + date
    if developer is not None:
      returned_data += '\n;DEV=' + developer
    return returned_data
  else:
    return ''


time.sleep(10)
# n-1708521001-l-4914
for obj in json_data['data']['houses']['hits']:
  atrib = get_attribute_ajax(obj)
  if atrib != '':
    mp_file.write(atrib)
    mp_file.write(poi_begin)
    mp_file.write('Data0=(' + str(obj['latitude']) + ',' + str(obj['longitude']) + ')')
    mp_file.write(poi_end)
    done = True
    done_count = 0
    print('Done')
  else:
    done_count = 10
    request_counter = 0
    driver.refresh()
    print('F5')
    time.sleep(10)
    print('refreshed')
    while done_count > 0:
      if atrib != '':
        mp_file.write(atrib)
        mp_file.write(poi_begin)
        mp_file.write('Data0=(' + str(obj['latitude']) + ',' + str(obj['longitude']) + ')')
        mp_file.write(poi_end)
        done_count = 0
        print('Done')
        break
      else:
        done_count -= 1
        print('repeated request ' + str(done_count))
        atrib = get_attribute_ajax(obj)

driver.close()
print('stop requests')
