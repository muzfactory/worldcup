<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>월드컵</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f8f9fa; color: #333; padding: 20px; }
    #container { max-width: 400px; margin: auto; text-align: center; }
    input[type=text] { width: calc(100% - 90px); padding: 8px; margin-right: 5px; }
    button { padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; background: #007bff; color: white; cursor: pointer; }
    button:hover:not(:disabled) { background: #0056b3; }
    button:disabled { background: #6c757d; cursor: not-allowed; }
    .btn-group { display: flex; flex-wrap: wrap; gap: 5px; justify-content: center; margin: 10px 0; }
    .btn-select { flex: 1 1 30%; }
    .btn-select.selected { background: #28a745; }
    .option-btn { width: 100%; margin: 10px 0; }
    #itemList { list-style: none; padding: 0; max-height: 150px; overflow-y: auto; text-align: left; margin: 10px 0; }
    #itemList li { padding: 4px 8px; border-bottom: 1px solid #ddd; }
    #modalOverlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; visibility: hidden; }
    #modalOverlay.show { visibility: visible; }
    #modal { background: white; padding: 20px; border-radius: 8px; text-align: center; max-width: 80%; }
    .confetti-piece { position: fixed; width: 8px; height: 8px; opacity: 0; animation: confetti-fall linear forwards; }
    @keyframes confetti-fall { 0% { transform: translateY(-10px) rotate(0deg); opacity: 1; } 100% { transform: translateY(100vh) rotate(360deg); opacity: 0; } }
    #history { text-align: left; margin-top: 20px; }
    #history h2 { font-size: 1.2em; margin-bottom: 10px; }
    #historyList { list-style: none; padding: 0; }
    #historyList li { padding: 6px 8px; border-bottom: 1px solid #ccc; display: flex; align-items: center; }
    #historyList img { width: 40px; height: 40px; object-fit: cover; margin-right: 10px; border-radius: 4px; }
    #historyList .info { flex: 1; }
    #historyList .time { font-size: 0.8em; color: #666; }
  </style>
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#007bff">
</head>
<body>
  <div id="container">
    <h1>월드컵</h1>
    <section id="setup">
      <div class="btn-group" id="listSelector">
        <button class="btn-select selected" data-list="new">NEW</button>
        <button class="btn-select" data-list="1">리스트1</button>
        <button class="btn-select" data-list="2">리스트2</button>
      </div>
      <p>항목 개수 선택:</p>
      <div class="btn-group" id="sizeSelector">
        <button class="btn-select selected" data-size="4">4</button>
        <button class="btn-select" data-size="8">8</button>
        <button class="btn-select" data-size="16">16</button>
        <button class="btn-select" data-size="32">32</button>
        <button class="btn-select" data-size="64">64</button>
        <button class="btn-select" data-size="128">128</button>
      </div>
      <p id="itemCountInfo">0/4 항목 추가됨 (NEW)</p>
      <div>
        <input type="text" id="singleInput" placeholder="항목명 입력">
        <button id="addBtn">추가</button>
      </div>
      <ul id="itemList"></ul>
      <div>
        <button id="startBtn" disabled>시작</button>
        <button id="resetBtn">초기화</button>
        <button id="shareLinkBtn">링크 공유</button>
      </div>
      <div id="saveButtons">
        <button id="saveList1Btn" disabled>리스트1 저장</button>
        <button id="saveList2Btn" disabled>리스트2 저장</button>
      </div>
    </section>
    <section id="round" style="display:none;">
      <p id="roundInfo"></p>
      <button class="option-btn" id="optA"></button>
      <button class="option-btn" id="optB"></button>
    </section>
    <section id="result" style="display:none;">
      <p id="finalText"></p>
      <button id="homeBtn">처음으로 가기</button>
    </section>
    <section id="history">
      <h2>최근 결과</h2>
      <ul id="historyList"></ul>
    </section>
  </div>
  <div id="modalOverlay">
    <div id="modal">
      <h2>축하합니다!</h2>
      <p id="modalText"></p>
      <button id="shareModalBtn">결과 저장</button>
      <button id="closeModal">닫기</button>
    </div>
  </div>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  <script defer>
    document.addEventListener('DOMContentLoaded', () => {
      const storageKey = 'worldcupstorage';
      const historyKey = 'worldcupHistory';
      const wsData = JSON.parse(localStorage.getItem(storageKey) || '{}');
      let currentList = 'new'; let bracketSize = 4;
      let items = [], current = [], nextRound = [];
      let idx = 0, roundNum = 1;

      const listGroup = document.getElementById('listSelector');
      const sizeGroup = document.getElementById('sizeSelector');
      const itemCountInfo = document.getElementById('itemCountInfo');
      const singleInput = document.getElementById('singleInput');
      const addBtn = document.getElementById('addBtn');
      const resetBtn = document.getElementById('resetBtn');
      const shareLinkBtn = document.getElementById('shareLinkBtn');
      const save1Btn = document.getElementById('saveList1Btn');
      const save2Btn = document.getElementById('saveList2Btn');
      const startBtn = document.getElementById('startBtn');
      const itemList = document.getElementById('itemList');
      const setupSec = document.getElementById('setup');
      const roundSec = document.getElementById('round');
      const resultSec = document.getElementById('result');
      const roundInfoElem = document.getElementById('roundInfo');
      const optA = document.getElementById('optA');
      const optB = document.getElementById('optB');
      const finalText = document.getElementById('finalText');
      const homeBtn = document.getElementById('homeBtn');
      const modalOverlay = document.getElementById('modalOverlay');
      const modalText = document.getElementById('modalText');
      const closeModalBtn = document.getElementById('closeModal');
      const shareModalBtn = document.getElementById('shareModalBtn');
      const historyList = document.getElementById('historyList');

      const saveStorage = () => localStorage.setItem(storageKey, JSON.stringify(wsData));
      const getHistory = () => JSON.parse(localStorage.getItem(historyKey) || '[]');
      const renderHistory = () => {
        const history = getHistory().slice(0, 10);
        historyList.innerHTML = '';
        history.forEach(entry => {
          const li = document.createElement('li');
          li.innerHTML = `<img src="${entry.image}" alt="결과"><div class="info"><div>${entry.result}</div><div class="time">${new Date(entry.time).toLocaleString()}</div></div>`;
          historyList.appendChild(li);
        });
      };

      function updateUI() {
        itemList.innerHTML = ''; items.forEach(v => itemList.insertAdjacentHTML('beforeend', `<li>${v}</li>`));
        itemCountInfo.textContent = `${items.length}/${bracketSize} 항목 추가됨 (${currentList.toUpperCase()})`;
        const isNew = currentList === 'new';
        [singleInput, addBtn, resetBtn, save1Btn, save2Btn].forEach(el => el.disabled = !isNew);
        startBtn.disabled = items.length !== bracketSize;
        save1Btn.disabled = !isNew || items.length !== bracketSize;
        save2Btn.disabled = !isNew || items.length !== bracketSize;
      }

      function loadItems() {
        const listData = wsData[currentList] || {};
        items = Array.isArray(listData[bracketSize]) ? [...listData[bracketSize]] : [];
        updateUI(); toggleGroup(listGroup, 'list', currentList); toggleGroup(sizeGroup, 'size', `${bracketSize}`);
      }

      function toggleGroup(group, key, val) { Array.from(group.children).forEach(btn => btn.classList.toggle('selected', btn.dataset[key] === val)); }

      listGroup.addEventListener('click', e => { if (!e.target.dataset.list) return; currentList = e.target.dataset.list; if (currentList === 'new') wsData.new = wsData.new || {}; toggleGroup(listGroup, 'list', currentList); loadItems(); });
      sizeGroup.addEventListener('click', e => { if (!e.target.dataset.size) return; bracketSize = +e.target.dataset.size; toggleGroup(sizeGroup, 'size', `${bracketSize}`); loadItems(); });
      addBtn.addEventListener('click', () => { const v = singleInput.value.trim(); if (!v || items.length >= bracketSize) return; items.push(v); wsData[currentList] = wsData[currentList] || {}; wsData[currentList][bracketSize] = [...items]; saveStorage(); singleInput.value = ''; updateUI(); });
      resetBtn.addEventListener('click', () => { localStorage.removeItem(storageKey); localStorage.removeItem(historyKey); Object.keys(wsData).forEach(k=>delete wsData[k]); currentList='new'; bracketSize=4; toggleGroup(listGroup,'list','new'); toggleGroup(sizeGroup,'size','4'); loadItems(); setupSec.style.display=''; roundSec.style.display='none'; resultSec.style.display='none'; });
      [save1Btn, save2Btn].forEach((btn,i)=>btn.addEventListener('click',()=>{ const key=`${i+1}`; wsData[key]=wsData[key]||{}; wsData[key][bracketSize]=[...items]; saveStorage(); alert(`리스트${key}에 저장되었습니다.`); }));
      const shuffle=a=>a.sort(()=>Math.random()-0.5);
      startBtn.addEventListener('click',()=>{ current=[...items]; shuffle(current); setupSec.style.display='none'; roundSec.style.display=''; idx=0;roundNum=1;nextRound=[]; showPair(); });
      function showPair(){ if(current.length===1) return showResult(current[0]); roundInfoElem.textContent=`Round ${roundNum}: ${current.length} → ${current.length/2}`; optA.textContent=current[idx]; optB.textContent=current[idx+1]; }
      [optA,optB].forEach(btn=>btn.addEventListener('click',()=>{ nextRound.push(btn.textContent); idx+=2; if(idx>=current.length){ current=[...nextRound]; nextRound=[]; idx=0; roundNum++; } showPair(); }));
      function showResult(final){ roundSec.style.display='none'; resultSec.style.display=''; finalText.textContent=`최종 선택된 항목: ${final}`; modalText.textContent=finalText.textContent; modalOverlay.classList.add('show'); launchConfetti(); }
      homeBtn.addEventListener('click',()=>{ modalOverlay.classList.remove('show'); resultSec.style.display='none'; setupSec.style.display=''; }); closeModalBtn.addEventListener('click',()=>modalOverlay.classList.remove('show'));
      shareLinkBtn.addEventListener('click', async()=>{ try{ if(navigator.share){ await navigator.share({ title: '월드컵 토너먼트', url: location.href }); } else { await navigator.clipboard.writeText(location.href); alert('링크가 클립보드에 복사되었습니다.'); }}catch(e){ console.error(e); alert('공유에 실패했습니다.'); }});
      shareModalBtn.addEventListener('click',async()=>{ try{ const canvas=await html2canvas(document.getElementById('modal')); const dataURL=canvas.toDataURL('image/png'); const history=getHistory(); history.unshift({ time:new Date().toISOString(), result:modalText.textContent, image:dataURL }); localStorage.setItem(historyKey,JSON.stringify(history)); const link=document.createElement('a'); link.href=dataURL; link.download=`월드컵_결과_${new Date().toISOString()}.png`; document.body.appendChild(link); link.click(); document.body.removeChild(link); renderHistory(); }catch(err){ console.error(err); alert('결과 저장 중 오류가 발생했습니다.'); }});
      function launchConfetti(){ for(let i=0;i<50;i++){ const conf=document.createElement('div'); conf.className='confetti-piece'; conf.style.backgroundColor=`hsl(${Math.random()*360},100%,50%)`; conf.style.left=`${Math.random()*100}vw`; conf.style.animationDuration=`${2+Math.random()*2}s`; document.body.appendChild(conf); conf.addEventListener('animationend',()=>conf.remove()); }}
      function getHistory(){ return JSON.parse(localStorage.getItem(historyKey)||'[]'); }
      renderHistory(); loadItems();
    });
  </script>
  <script>
    if('serviceWorker' in navigator){ window.addEventListener('load',()=>{ navigator.serviceWorker.register('/sw.js').catch(console.error); }); }
  </script>
</body>
</html>
