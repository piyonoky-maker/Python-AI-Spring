package com.example.demo;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;
/*
WebClientConfig
- Spring(WebFlux)에서 HTTP요청을 보내는 WebClient를 공통 설정으로 만들어주는 클래스
- RestTemplate(구버전)대신 WebClient(신버전/비동기)를 많이 사용함.
언제 쓰니?
- Spring Boot(8080) -> FastAPI(파이썬)같은 외부 API 서버 호출할 때
- implementation 'org.springframework.boot:spring-boot-starter-webflux'
- 예)파일 업로드/다운로드, AI추론 요청, 이미지/대용량 JSON응답 받기 등.

 */
@Configuration
public class WebClientConfig {
    //WebClient 빈 등록 - 스프링 컨테이너가 WebClient 싱글턴 관리해줌
    //YoloController에서 생성자 객체 주입법으로 재사용이 가능함.
    //프로젝트 전역규칙을 한 곳에서 관리
    @Bean
    public WebClient webClient() {
        //ExchangeStrategies: WebClient가 응답을 읽고(디코딩) 요청을 쓰는(인코딩)규칙을 모아둔 설정
        //codecs설정은 왜 필요한가?
        //WebClient는 기본적으로 응답 데이터를 메모리에 담아서 처리하는데
        //큰 데이터(대용량 JSON,큰이미지 Base64, 큰 파일 응답)를 받으면
        //DataBufferLimitException 같은 에러가 날 수 있음.
        ExchangeStrategies strategies = ExchangeStrategies.builder()
                .codecs(clientCodecConfigurer -> clientCodecConfigurer.defaultCodecs()
                        .maxInMemorySize(-1)).build();

        return WebClient.builder().exchangeStrategies(strategies)//위에서 만든 codec/전략 적용
                .baseUrl("http://localhost:8000")//기본 호출 대상 서버 주소 - uvicorn서버
                .build();//WebClient생성됨
    }//end of webClient
}
