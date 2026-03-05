import { useRef, useState } from "react";

const App = () => {
  const formRef = useRef(null);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(null);

  const handleClick = () => {
    // 폼 상태값이 null( 폼(form)이 아직렌더링 안 되었거나 참조 실패 )이면 종료
    if (!formRef.current) return;

    const formData = new FormData(formRef.current);
    // 요청 시작 -> 로딩 사애 ( 버튼 비활성화 )
    setLoading(true);
    const xhr = new XMLHttpRequest();

    // xhr.open("POST", "http://localhost:8080/yolo/reactService", true);
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        setResult(response);
        console.log(response);
        const response = JSON.parse(xhr.responsText);
      }
    };
  };
  return (
    <>
      <h2>객체탐지 - 이미지 처리</h2>
      <form method={formRef} id="fileUploadForm" enctype="multipart/form-data">
        데이터 : <input type="text" name="message" value="test hello" />
        <p></p>
        파일 : <input type="file" name="file" />
        <p></p>
        <input type="button" onClick={handleClick} value="비동기 요청" />
      </form>
    </>
  );
};

export default App;
