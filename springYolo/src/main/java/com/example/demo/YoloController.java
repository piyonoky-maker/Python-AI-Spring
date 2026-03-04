package com.example.demo;

import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.client.WebClient;

@Log4j2
@RestController
@RequestMapping("/yolo")
@RequiredArgsConstructor
public class YoloController {
    private final WebClient webClient;
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
        String result = "{'message':'test hello', 'base64이미지':''}";
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
