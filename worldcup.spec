<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>월드컵 토너먼트</title>
  <style>
    /* Reset & Base */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Arial', sans-serif; background: #f0f4f8; color: #333; line-height: 1.4; }
    #container { max-width: 600px; margin: 20px auto; padding: 10px; }
    h1 { text-align: center; font-size: 2.5em; margin-bottom: 0.5em; color: #005b96; }

    /* Button styles */
    .btn { display: inline-block; font-size: 1.2em; padding: 12px 20px; margin: 6px; border: none; border-radius: 8px;
           cursor: pointer; transition: background 0.2s; }
    .btn:disabled { background: #ccc; cursor: not-allowed; }
    .btn-primary { background: #007bff; color: #fff; }
    .btn-primary:hover:not(:disabled) { background: #0056b3; }
    .btn-success { background: #28a745; color: #fff; }
    .btn-success:hover { background: #218838; }
    .btn-secondary { background: #6c757d; color: #fff; }
    .btn-secondary:hover { background: #5a6268; }
    #shareLinkBtn, #shareModalBtn { background: #17a2b8; }
    #shareLinkBtn:hover, #shareModalBtn:hover { background: #117a8b; }

    /* Layout */
    .section { background: #fff; border-radius: 10px; padding: 15px; margin-bottom: 20px;
               box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .section p { font-size: 1.1em; margin: 10px 0; }
    .btn-group { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; }
    input[type=text] { width: calc(100% - 140px); padding: 10px; font-size: 1.1em; border: 2px solid #ccc; border-radius: 8px; }

    /* List & History */
    ul { list-style: none; margin-top: 10px; }
    ul li { background: #fafafa; border: 1px solid #e0e0e0; padding: 10px; margin-bottom: 6px; border-radius: 6px; font-size: 1.1em; }
    .history-item { display: flex; align-items: center; }
    .history-item img { width: 48px; height: 48px; border-radius: 6px; margin-right: 12px; }
    .history-item .info { flex: 1; }
    .history-item .time { font-size: 0.9em; color: #666; }
  </style>
</head>
<body>
  <div id="container">
    <h1>월드컵 토너먼트</h1>

    <section class="section" id="setup">
      <div class="btn-group">
        <button class="btn btn-success" data-list="new">NEW</button>
        <button class="btn btn-primary" data-list="1">리스트1</button>
        <button class="btn btn-primary" data-list="2">리스트2</button>
      </div>
      <p>항목 개수 선택:</p>
      <div class="btn-group" id="sizeSelector">
        <button class="btn btn-success" data-size="4">4</button>
        <button class="btn btn-primary" data-size="8">8</button>
        <button class="btn btn-primary" data-size="16">16</button>
        <button class="btn btn-primary" data-size="32">32</button>
        <button class="btn btn-primary" data-size="64">64</button>
        <button class="btn btn-primary" data-size="128">128</button>
      </div>
      <p id="itemCountInfo">0/4 항목 추가됨 (NEW)</p>
      <div class="btn-group">
        <input type="text" id="singleInput" placeholder="항목명을 입력하세요">
        <button id="addBtn" class="btn btn-primary">추가</button>
      </div>
      <div class="btn-group">
        <button id="startBtn" class="btn btn-primary" disabled>시작</button>
        <button id="resetBtn" class="btn btn-secondary">초기화</button>
        <button id="shareLinkBtn" class="btn">링크 공유</button>
      </div>
      <div class="btn-group">
        <button id="saveList1Btn" class="btn btn-primary" disabled>리스트1 저장</button>
        <button id="saveList2Btn" class="btn btn-primary" disabled>리스트2 저장</button>
      </div>
    </section>

    <section class="section" id="round" style="display:none;">
      <p id="roundInfo"></p>
      <div class="btn-group">
        <button class="btn btn-primary option-btn" id="optA"></button>
        <button class="btn btn-primary option-btn" id="optB"></button>
      </div>
    </section>

    <section class="section" id="result" style="display:none;">
      <p id="finalText" style="font-size:1.3em; font-weight:bold;"></p>
      <button id="homeBtn" class="btn btn-success">처음으로 가기</button>
    </section>

    <section class="section" id="history">
      <h2>최근 결과</h2>
      <ul id="historyList"></ul>
    </section>
  </div>

  <!-- 모달 오버레이 -->
  <div id="modalOverlay" style="display:none;">
    <div id="modal" class="section" style="max-width:300px; margin:auto;">
      <h2>축하합니다!</h2>
      <p id="modalText" style="font-size:1.2em;"></p>
      <div class="btn-group">
        <button id="shareModalBtn" class="btn">결과 저장</button>
        <button id="closeModal" class="btn btn-secondary">닫기</button>
      </div>
    </div>
  </div>

  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  <script>
    // (기존 자바스크립트 로직 유지)
  </script>
</body>
</html>
