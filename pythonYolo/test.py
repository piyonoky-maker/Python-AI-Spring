import requests 
from multipart import file_path

url = 'http://localhost:8000/detect'
message = 'test message'
file_path = '../bus01.jpg'


with open(file_path, 'rb') as file:
  response = requests.post(url, data={'message': message}, files={'file': file})

print(response.json())

# 이미지 파일 위치, 이름 확인
# yolo.py 가 실행중인 상태에서 test.py 를 실행한다\
# 터미널 창에서 json형식의 메시지와 이미지 그러니까 긴 base64인코딩된 문자열이 촐력됨