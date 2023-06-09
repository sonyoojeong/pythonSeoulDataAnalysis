dataInFolder = './../seoul/'
filename = dataInFolder + 'store.txt'

speech = open(filename, encoding='UTF-8').read()
#print(speech)

# url : https://konlpy.org/ko/latest/

from konlpy.tag import Komoran



komo = Komoran()  # 객체생성 (생성자)
token_list = komo.nouns(speech)  # nouns : 명사 추출
print('토큰 목록')
print(token_list)


import nltk  # 자연어 처리해주는 툴킷 : nltk (national language toolkit)

nltk_token = nltk.Text(tokens=token_list)
bindo_size = 500  # 빈도 수가 많은 500개
token_data = nltk_token.vocab().most_common(bindo_size)  # 빈도 수가 제일 많은거 500개 보여 달라는 것
print('토큰과 빈도수 확인')
print(token_data)

wordlist = list() # 튜플 (단어, 빈도수) 를 저장할 리스트

# 빈도가 1번인 글자 빼고, 한 글자만 추출된 글자도 빼자!  (아래랑 동일한 말)
# 단어의 길이가 1 이상, 빈도수가 2이상인 데이터만 추출하기
for word,bindo in token_data:
    if (len(word) >= 2 and bindo >=2):
        wordlist.append((word,bindo))

# token_data 파일로 저장하기
print('단어의 길이가 1 이상, 빈도수가 2이상인 데이터만 추출하기')
print(wordlist)

import pandas as pd

savewordFile = dataInFolder + 'word_list2.csv'
dataframe = pd.DataFrame(wordlist, columns=['단어','빈도수'])
dataframe.to_csv(savewordFile, encoding='cp949', index=False)
print(savewordFile + ' 파일 저장 완료')

print('상위 top 10개 막대 그래프')
barcount = 10
chartdata = dataframe.set_index('단어').iloc[0:barcount]

import matplotlib.pyplot as plt
plt.rc('font', family = 'malgun gothic')

chartdata.plot(kind='bar', rot=30, grid = True, use_index=True, legend=False)

plt.title('빈도 '+ str(barcount) + '개 상위 단어', size =20)
plt.xlabel('주요 키워드', size=12)
plt.ylabel('빈도 수', size=12)

barFileName = dataInFolder + 'bar_chart2.png'
plt.savefig(barFileName)   # savefig : 하드디스크에다가 직접 저장하는 것

# plt.show()  # 실행하면 팝업창으로 떠지게 함, 그림이 너무 많으면 번거로워서 1개 정도일 때 확인할 겸 사용하면 된다.
print(barFileName + ' 그래프가 생성되었습니다.')

print('빈도를 이용한 워드 클라우드')

# 참조 url : https://amueller.github.io/word_cloud/index.html


import numpy as np
from PIL import Image #PIL : Python Image Library
from wordcloud import WordCloud

alice_color_file = dataInFolder + 'alice_color.png'  # 워드 클라우드가 그려질 이미지
alice_color_array = np.array(Image.open(alice_color_file))  # 이미지 배열

word_dict = dict(wordlist)  # 단어 사전

font_name = 'malgun.ttf'  # 글꼴
mycloud = WordCloud(font_path=font_name, mask=alice_color_array, background_color='white')
mycloud = mycloud.generate_from_frequencies(word_dict)  # 빈도수대로 집어넣음

# ImageColorGenerator : 컬러 이미지의 색상 톤을 유지하고자 할 때 사용되는 라이브러리
from wordcloud import ImageColorGenerator
color_generator = ImageColorGenerator(alice_color_array)

mycloud = mycloud.recolor(color_func=color_generator)

plt.figure(figsize=(16,8))  # 새 도화지 준비
plt.axis('off')  # 눈금 없애주는 것
plt.imshow(mycloud)  #

cloudFileName = dataInFolder + 'word_cloud2.png'
plt.savefig(cloudFileName)

print(cloudFileName + ' 그래프가 생성되었습니다.')


print('finished')