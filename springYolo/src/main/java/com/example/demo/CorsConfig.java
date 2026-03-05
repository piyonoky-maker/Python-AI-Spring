package com.example.demo;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

// 스프링이 시작할 때 이 클래스를 설정 빈으로 등록
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    //특정 컨트롤러에 붙이는 방법 보다는 전역으로 잡아서
    //모든 API에 일괄 적용한다.
    @Override
    public void addCorsMappings(CorsRegistry registry){
        registry.addMapping("/**")
                .allowedOrigins("http://localhost:8080","http://localhost:5173")
                .allowedMethods("GET","POST","PUT","DELETE","OPTIONS","PATCH")
                .allowedHeaders("*")
                .exposedHeaders("Authorization","Location")
                .allowCredentials(true)//true이면 allowedOrigins는 와일드카드 사용불가함
                .maxAge(3600);//3600초동안 캐시에 유지-> 네트워크 요청 감소, 체감 성능 향상
    }//end of addCorsMappings
}//end of CorsConfig