## FastAPI 설치

```sh
# uvicorn은 python 웹서버 프로그램
# FastAPI 코드를 실제 웹 서비스로 실행해주는 엔진임
pip install fastapi uvicorn
```

#### ASGI
- 파이썬에서 비동기 웹 서버와 웹 어플리케이션 간의 인터페이스 표준.
- 기존 WSGI(Web Server Gateway Interface)의 비동기 버전
- 파이썬에서 비동기 처리를 지원한느 웹 어플리케이션 구축을 위해 설계되었음.

#### ASGI 주요 특징
- 비동기 지원 : 높은 성능과 동시성을 제공. 비동기 통신이 필요한 곳에 유용
- 범용성 : ASGI는 HTTP뿐만 아니라 WebSocket, gRPC와 같은 다른 프로토콜도 지원
- 유연성 : 다양한 서버 및 프레임워크와 호환됨. 모듈식으로 구성 가능.

#### FastAPI와 ASGI
- FastAPI는 ASGI 표준을 따르는 웹 프레임워크
- 비동기를 기본으로 하며, uvicorn과 같은 ASGI서버를 사용하여 높은 성능 제공.