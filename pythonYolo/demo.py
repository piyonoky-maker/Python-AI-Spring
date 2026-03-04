from fastapi import FastAPI
from fastapi import Query
from typing import Optional
# FastAPI 객체 생성
app = FastAPI(
  title = 'Demo FastAPI App',
  description = '간단한 FastAPI 어플리케이션'
)
'''
uvicorn demo:app
Uvicorn이 하는 일
1. demp.py 로딩
2. app 객체 찾기( 생성 - 초기화 )
3. HTTP서버 생성
4. 8000 포트 열기
5. 요청 대기
결론: async기반 서버임
비동기 와 동기
동시요청 처리 가능
사용자 100명 동시 요청
기존(구) 서버 - 동기서버 ( WSGI )
요청1 -> 처리 -> 요청2 -> 처리 -> 요청3

Uvicorn
요청1
요청2
요청3
동시에 처리
'''

# 서버 실행
# uvicorn demo:app --reload
# demo: 파이썬 파일 이름( demo.py )
# app: FastAPI 객체 이름
# --reload: 코드 변경 시 서버 자동 재시작( 개발모드 )
# URL 라우팅 -> 함수 실행 -> {'Hello': 'World'} -> JSON응답 변환
# 브라우저 테스트 URL: http://localhost:8000/
# FastAPI는 기본적으로 문서화 API를 제공함
# http://127.0.0.1:8000/docs    -> swagger
# http://localhost:8000/redoc   -> redoc


@app.get('/')
async def read_root():
  return {'Hello': 'World'}

@app.get('/items/{item_id}')
async def read_item(item_id: int, q: str = None):
  return {'item_id': item_id, 'q': q}



# Optional( 선택 )파라미터 + Query() 검증
'''
- GET /search -> q=None, category=None(둘 다 생략)
- GET /search?q=ai -> OK 200 -> 왜냐면 길이가 2 
- GET /search?q=a -> 422 -> 왜냐면 길이가 2
'''
@app.get('/search')
async def search(
  q: Optional[str] = Query(None, min_length=2, max_length=50),
  category: Optional[str] = None
):
  results = {'query': q, 'category': category}
  return results


'''
호출 예시
- GET /tags                           -> tags=[] ( 빈 리스트 )
- GET /tags?tag=python                -> tags=['python']
- GET /tags?tag=python&tag=fastapi    -> tags=['python', 'fastapi']
'''
# 리스트 쿼리 파라미터 ( 같은 키를 여러번 보내는 패턴 )
# fastapi는 각 요소를 str로 받으며, 요소 타입에 검증도 가능함
@app.get('/tag')
def get_by_tags(tag: list[str] = Query(default=[])):        # list[str]는 python 3.9+ 이상에서는 에러코드 발생
  return {'tags': tag}

'''
Path 파라미터: /items/3 처럼 URL 경로 안에 있는 값

Query 파라미터: /item?skip=0&limit=10



'''

