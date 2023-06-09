import requests
import xmltodict
import json
import pandas as pd
from itertools import count

'''
서울시 지정·인증업소 현황
'''

accessToken = '684374574864627737337579584f63'  # 인증키
totallist = list()  # 모든 데이터가 저장될 list ( 대괄호만 적어도됨, 정석이 list() 이다)
pageSize = 1000 # 한번에 읽어 올 데이터 개수

print('크롤링을 시작합니다. 잠시만 기다려 주세요.')

for pageNumber in count(): # while True 구문과 유사한 개념의 문법
    beginRow = str(pageNumber * pageSize + 1)
    endRow = str((pageNumber+1) * pageSize)

    url = 'http://openapi.seoul.go.kr:8088/' + accessToken + '/xml/CrtfcUpsoInfo/' +beginRow + '/' + endRow + '/'


    message = '범위 : ' + beginRow + '~' + endRow
    print(message)

    response = requests.get(url)  #response : 응답 객체

    content = response.content
    xml_data = xmltodict.parse(content)  # xml 데이터를 파싱하여 dictionary 형식으로 변환
    json_data = json.loads(json.dumps(xml_data))  # JSON 형식으로 변환

    try:
        datalist = json_data['CrtfcUpsoInfo']['row']
        for data in datalist:
            totallist.append(data)

    except Exception as err:
        print('더 이상 데이터가 없어 오류가 발생하였습니다.')
        print(err)
        break

print('크롤링이 종료 되었습니다.')

filename = './../park/CrtfcUpsoInfo.csv'
myframe = pd.DataFrame(totallist)
myframe.to_csv(filename)
print(filename + '파일이 저장되었습니다.')
