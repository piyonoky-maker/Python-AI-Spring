# REST API서버를 구성하고 파일 및 폼 데이터를 처리하는데 사용됨. 
from fastapi import FastAPI, File, Form, UploadFile
# JSON형태의 응답을 변환할 때 사용
from fastapi.responses import JSONResponse
# BaseModel을 상속하여 데이터 모델을 정의함.
# 이 모델은 API의 응답 데이터 검증 및 직렬화 하는데 도움
from pydantic import BaseModel
# io와 base64는 이미지 데이터를 메모리에서 처리하고 base64로
# 인코딩하여 전송하는데 사용됨
import io
import base64
# 이미지를 열고 조작할 때 사용
from PIL import Image
# 배열이나 행렬 연산시 사용
import numpy as np
from ultralytics import YOLO # YOLO v8모델중 나노 버전을 불러와 객체 탐지 수행
# OpenCV이미지 처리 및 도형 그리기(사각형, 텍스트 삽입)에 사용됨
import cv2
# FastAPI인스턴스를 생성하여 REST API서버를 구성함.
app = FastAPI()
# YOLO v8버전에 나노 모델을 불러와 객체 탐지에 사용할 준비하기
model = YOLO('yolov8n.pt') # 욜로8안에 나노 모델 가져오기

# pydantic모델 정의 - API 응답에 사용될 데이터 모델
class DetectionResult(BaseModel):
  message: str 
  image: str

# 객체를 탐지 하는 함수 만들기
# 입력 : PIL의 Image 객체
# 처리 과정 :
def detect_objects(image: Image.Image):
  # 이미지 배열 변환 - PIL 이미지를 numpy 배열로 변환함. 
  img = np.array(image)  
  # 객체 탐지 수행 - YOLO 모델에 이미지를 전달해 탐지 결과를 받아옴.
  results = model(img) #result에는 객체 탐지한 결과가 담김.
  class_names = model.names #모델에 있는 클래스 이름을 가져와서 화면에 출력할 예정임
  # 탐지 결과 반복 처리
  # 각 탐지 결과(result)에서 탐지된 객체의 경계 상자(boxes.xyxy), 신뢰도(boxes.conf), 클래스 이름(boxes.cls)를 가져옴.
  # 각 객체에 대해 좌표를 정수형으로 변환하고 클래스 이름(model.names)을 매핑합니다. 
  for result in results:
    # xyxy는 두 개의 점 정보를 의미 시작점과 가로세로끝점
    boxes = result.boxes.xyxy
    confidences = result.boxes.conf
    class_ids = result.boxes.cls #cls는 클래스 이름을 가짐.
    for box, confidence, class_id in zip(boxes, confidences, class_ids):
      #왼쪽 상단좌표(x1,y1), 우측하단좌표(x2, y2)
      x1, y1, x2, y2 = map(int, box)
      label = class_names[int(class_id)]
      # 결과 시각화: cv2.rectangle을 사용해 객체 위치에 사각형을 그림.
      # cv2.putText를 통해 객체의 클래스 이름과 신뢰도를 이미지에 텍스트로 표시함.
      #cv2는 색상이 bgr(255,0,0)-파랑색으로 굵기 2만큼
      cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,0), 2)
      cv2.putText(img, f'{label} {confidence:.2f}', (x1,y1),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
    # 결과를 이미지 객체로 만들기
    # OpenCV로 처리된 Numpy 배열을 Image.fromarray(img)를 통해 PIL 이미지 객체로 변환
    result_image = Image.fromarray(img) #rgb로 변경해서 처리해줌
    # 객체 탐지가* 완료된 결과 이미지(PIL Image객체체)
    return result_image

@app.post("/detect")
async def dectected_service(message: str = Form(...), file: UploadFile = Form(...)):
  #파일 데이터를 읽은 후 Image.open으로 PIL이미지 객체 생성함.
  image = Image.open(io.BytesIO(await file.read()))
  # 이미지 모드 변환 : 만일 이미지 모드가 RGBA 혹은 RGB가 아닌 경우 conver('RGB')를 통해
  # RGB모드로 변환하여 호환성을 보장함.
  if image.mode == 'RGBA':
    image = image.convert('RGB')
  elif image.mode == 'RGB':
    image = image.convert('RGB')
  # 이미지 내 객체들을 탐지하고 결과 이미지를 반환 받음.
  result_image = detect_objects(image)
  # 결과 이미지를 메모리 버퍼에 JPEG형식으로 저장 후 base64.b64encode로 인코딩함.
  buffered = io.BytesIO()
  result_image.save(buffered, format='JPEG')#로컬에 저장하기. 즉 파일에 저장하는 것임.
  img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
  return DetectionResult(message=message, image=img_str)

# 이 코드는 FastAPI를 사용하여 이미지 업로드 및 객체 탐지를 수행하는 REST API 서버를 구현함.
# 1. 클라이언트가 이미지 파일과 메시지를 폼 데이터로 전송하면
# 2. 서버는 YOLO모델을 활용해 이미지 내 객체를 탐지하고 
# 3. 객체 탐지 결과를 시각적으로 표시한 후 base64 문자열로 인코딩하여 클라이언트에게 반환함.