from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# FastAPI 앱 생성
app = FastAPI()

# 요청 바디 스키마 정의
'''
Item 클래스는 클리이언트가 POST/ Item로 보내야 하는 JSON 형태를 정의
FastAPI 는 이 모델을 보고:
- JSON을 파싱해서 Item 객체로 만들고
- 타입이 맞는지 검증하고 ( 문자열/ 숫자등 )
- 필수/ 선택 필드를 체크함
'''


class Item( BaseModel ):
  # 필수: 문자열
  name: str
  # 선택: 문자열( 없으면 None )
  descption: Optional[ str ] = None
  # 필수: 실수 ( float )
  price: float
  # 선택: 실수 ( float ) ( 없으면 None )
  tax: Optional[ float ] = None

# http://127.0.0.1:8000/items
@app.post('/items')
def create_item(item: Item):
  # pydantic모델( Item )을 일반 dict로 변환
  # 응답으로 돌려주기 쉽게 만들기 위함
  item_dict = item.dict
  if item.tax is not None:
    price_with_tax = item.price + item.tax
    # 기존 dict에 새로운 키 추가
    item_dict.update({'price_with_tax': price_with_tax})
    # 최종 dict 반환하면 FastAPI가 JSON으로 변환해서 응답
  return item_dict


items = {}
# http://127.0.0.1:8000/items/1
@app.get('/items/{item_id}')
async def read_item (item_id:int):
  if item_id not in items:
    raise HTTPException( status_code = 404, detail='아이템을 찾을 수 없습니다.')
  return items[item_id]


'''
# 요청 예시
{
  'name': 'apple',
  'price': 1000,
  'tax': 100
}

# 응답 예시
{
  'name': 'apple',
  'descrption': null,
  'price': 1000,
  'tax': 100,
  'price_with_tax': 1100
}

여기서 모델은 요청과 응답에 사용되는 데이터 규격( 스키마 )을 정의 하는 클래스를 말함
즉, 들어오는 JSON을 검사( 검증 )하고, 필요한 타입으로 바꿔( 파싱 ) 주고
문서화 까지 자동으로 해주는 설계도 임.

왜 쓰나?
검증: 필수값 누락 타입 오류를 자동으로 잡아줌
422번 에러 상태값 잡아줌
파싱: 가능한 경우 타입도 변환 해줌
예) '12.5' -> 12.5

자동 문서화 ( OpenAPI/ Swagger ): 모델을 기반으로 API 문서에 필드가 자동 표시됨 
코드 가독성/ 유지보수: '이 API는 이러한 데이터만 받는다' 가 코드로 분명해 짐

서버 실행 하기
uvicorn requestBody:app --reload

요청 URL 
http://localhost:8000/items
주의 post방식은 URL요청으로 테스트 불가함

swagger : http://localhost:8000/docs
          http://localhost:8000/redoc

'''
























'''
요청 바디 스키마 정의( pydantic 모델 )
pydantic 이란?
파이썬 데이터 검증 라이브러리
데이터 타입 검사 ( 자동으로 검사 )
JSON <-> Python 객체 변환
FastAPI에서 요청/ 응답 모델로 사용
'''