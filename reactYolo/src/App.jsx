import { useRef, useState } from "react";

const App = () => {
  //useRef Hook: DOM에 직접 접근할 때 사용
  //상태가 변하더라도 기존에 정보를 유지해줌
  const formRef = useRef(null);
  //result: 서버 응답(JSON)을 저장해서 화면에 출력하기 위한 state
  const [result, setResult] = useState(null);
  //loading: 요청이 진행 중인지 여부 -> true이면 버튼을 disabled시켜서 중복 요청 방지
  const [loading, setLoading] = useState(false);
  //버튼 클릭시 실행되는 함수
  //폼 데이터를 만들어서 Spring Boot서버로 POST요청을 보냄
  //파일 업로드 + 텍스트 메시지 동시에 전송
  const handleClick = () => {
    //폼 상태값이 null(폼(form)이 아직 렌더링 안 되었거나 참조 실패)이면 종료
    if (!formRef.current) return;
    //여기까지 진행이 되었다면 화면이 정상적으로 렌더링이 되었다
    //이종간에 연계(연동) - FormData - 서로 다른 장치에서도 웹 요청 처리 가능
    //폼 안에 있는 input 들의 name기준으로 값을 자동 수집
    //결과적으로 서버로 전송(multipart/form-data)
    //file은 사용자가 선택한 파일 바이너리
    const formData = new FormData(formRef.current);
    // 요청 시작 -> 로딩 상태 (버튼 비활성화)
    setLoading(true);
    //fetch(), axios
    const xhr = new XMLHttpRequest(); //비동기통신객체 -> 서로 맞추지 않아도 돼 -> 너가 해줄때까지 나는 다른일을 할 수 있어
    //상태값을 추적 -> 0 -> 1 -> 2 -> 3 -> 4(204)
    xhr.open("POST", "http://localhost:8080/yolo/reactService", true);
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        //responseText(text/plain) or responseXML(text/xml)-> application/json(표준)
        const response = JSON.parse(xhr.responseText);
        //useState훅에 초기화 하기 null -> {"message":"test hello", "image":sfsdfsdfsdfsdfsdfsd}
        setResult(response);
        //로딩 종료
        setLoading(false);
      } else {
        //서버가 응답은 했지만 4xx/5xx 같은 에러 상태 코드
        console.error("Error: " + xhr.statusText);
        setLoading(false);
      }
    }; //end of onload
    //네트워크 오류(서버 다운, CORS 차단, 연결 불가 등)로 요청 자체가 실패한 경우
    //이 경우는 onload로 안 들어온다.
    xhr.onerror = () => {
      console.error("Error: " + xhr.statusText);
      setLoading(false);
    };
    //여기까지 정상적으로 도착하였다면
    xhr.send(formData);
  }; //end of handleClick
  return (
    <>
      <h2>객체탐지 - 이미지 처리</h2>
      <form
        ref={formRef}
        method="post"
        id="fileUploadForm"
        enctype="multipart/form-data"
      >
        데이터 : <input type="text" name="message" value="test hello" />
        <p></p>
        파일 : <input type="file" name="file" />
        <p></p>
        <input type="button" onClick={handleClick} value="비동기 요청" />
      </form>
      {/* FastAPI가 응답으로 보내준 JSON파일에서 message정보와 image정보 출력하기 */}
      <div id="result" style={{ marginTop: "20px" }}>
        {result ? (
          <div>
            {/* 서버가 준 message출력 */}
            <span>{result.message}</span>
            <br />
            {/* base64 이미지를 바로 화면에 표시하는 방법
              data:image/png;base64, ...형태의 Data URL 사용
              서버는 image필드에 base64문자열만 보내고
              프론트에서 앞부분을 붙여 img src로 사용하면 사진이 됨.
            */}
            <img
              src={`data:image/png;base64, ${result.image}`}
              alt="객체탐지 끝난 이미지"
              width={"80%"}
            />
          </div>
        ) : (
          //결과가 없을
          "여기에 요청 결과가 출력 됩니다."
        )}
      </div>
    </>
  );
};

export default App;
