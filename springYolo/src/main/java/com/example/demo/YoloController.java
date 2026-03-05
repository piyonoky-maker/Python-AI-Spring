package com.example.demo;

import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

@Log4j2
@RestController
@RequestMapping("/yolo")
@RequiredArgsConstructor
public class YoloController {
    // 브라우저에서 파이썬 서버를 요청해야 하는데
    // implementation 'org.springframework.boot:spring-boot-starter-webflux' 추가 할것
    // 자바코드로 이것을 하려면 추가 API가 필요하다
    private final WebClient webClient; // 불변객체
    /*****************************************************************************
     * 톰캣 서버의 템플릿 엔진으로 화면을 받아올 때
     * @param file
     * @param message - test hello
     * @return result
     *****************************************************************************/
    @PostMapping("/javaService")
    public String javaService(@RequestParam("file") MultipartFile file
            , @RequestParam("message") String message) {
        log.info("javaService");
        //=======1) 화면으로 부터 들어오는 값 확인(디버깅 로그)
        log.info("file:{} ", file);//파일 객체 자체 확인
        log.info("message:{} ", message);//함께 전송할 문자열 확인
        //=======2) python서버로 보내기 위해 multipart/form-data 바디 구성
        //브라우저에서 <form enctype="multipart/form-data">로 보내는 것과 같은
        //형태를 서버 코드에서 직접 만들어서 요청해야 함.
        MultipartBodyBuilder bodyBuilder = new  MultipartBodyBuilder();
        //문자열 폼 필드 추가
        bodyBuilder.part("message", message);
        //파일 폼 필드 추가
        //file자체는 파일을 객체화한 주소번지이므로 자원을 WebClient가
        //파일 리소스로 읽어서 전송하도록 해야 함.
        bodyBuilder.part("file", file.getResource());
        //=======3) WebClient로 python서버에 POST요청
        //POST http://localhost:8000/detect
        String result = webClient.post()
                .uri("/detect")
                .contentType(MediaType.MULTIPART_FORM_DATA)
                .body(BodyInserters.fromMultipartData(bodyBuilder.build()))
                //=======4) 응답 처리(실제 처리는 파이썬에서 하고 결과처리는 스프링으로 전달함)
                //요청 실행 후 응답을 가져옴.
                .retrieve()
                .bodyToMono(String.class)
                //=======5) 응답이 올때까지 기다렸다가 결과를 string 꺼냄
                //WebClient는 원래 비동기 인데 block을 사용하면 현재 스레드가
                //응답 올 때 까지 기다렸다가 결과를 String으로 꺼냄.
                .block();
        return result;
    }//end of javaService
    /*****************************************************************************
     * 리액트 서버의 Yolo.jsx로 부터 요청을 받았올 때
     * @param file
     * @param message
     * @return result
     *****************************************************************************/
    @PostMapping("/reactService")
    public ResponseEntity<String> reactService(MultipartFile file, String message) {
        log.info("reactService");
        String result = "{'message':'test hello', 'base64이미지':''}";
        //파이썬 서버로 부터 받은 JSON문자열을 React 클라이언트 전달
        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_JSON)
                .body(result);
    }
}