<!DOCTYPE html>

<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Сенсей AI — Личный тренер</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {
  --red:#C0392B;--red-dark:#922B21;--red-glow:rgba(192,57,43,0.25);
  --white:#F5F0EB;--off:#D8D2C8;--black:#0D0D0D;
  --d1:#141414;--d2:#1C1C1C;--d3:#262626;--d4:#333;
  --gray:#777;--gold:#C9A84C;
  --safe:env(safe-area-inset-bottom,0px);
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{height:100%;overflow:hidden;}
body{background:var(--black);color:var(--white);font-family:'Inter',sans-serif;display:flex;flex-direction:column;position:fixed;inset:0;}
body::before{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 15% 0%,rgba(192,57,43,0.1) 0%,transparent 55%),radial-gradient(ellipse at 85% 100%,rgba(192,57,43,0.07) 0%,transparent 50%);}

/* HEADER */
header{position:relative;z-index:20;flex-shrink:0;display:flex;align-items:center;justify-content:space-between;padding:12px 16px;background:rgba(13,13,13,0.97);border-bottom:1px solid rgba(255,255,255,0.07);backdrop-filter:blur(12px);}
.logo{display:flex;align-items:center;gap:10px;}
.logo-kanji{font-family:‘Noto Serif JP’,serif;font-size:30px;font-weight:900;color:var(–red);line-height:1;text-shadow:0 0 16px var(–red-glow);}
.logo-text h1{font-family:‘Noto Serif JP’,serif;font-size:16px;font-weight:700;color:var(–white);}
.logo-text p{font-size:10px;color:var(–gray);letter-spacing:.12em;text-transform:uppercase;margin-top:1px;}
.hbtns{display:flex;gap:8px;}
.ibtn{width:34px;height:34px;border-radius:9px;border:1px solid rgba(255,255,255,0.1);background:var(–d3);color:var(–off);font-size:15px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .15s;}
.ibtn:hover{background:var(–d4);border-color:rgba(255,255,255,0.2);}
.ibtn.del:hover{background:var(–red-dark);border-color:var(–red);}

/* DRAWER */
.ov{position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:100;opacity:0;pointer-events:none;transition:opacity .25s;backdrop-filter:blur(4px);}
.ov.open{opacity:1;pointer-events:all;}
.drawer{position:fixed;top:0;right:0;bottom:0;width:min(340px,92vw);background:var(–d1);border-left:1px solid rgba(255,255,255,0.08);z-index:101;transform:translateX(100%);transition:transform .3s cubic-bezier(.4,0,.2,1);display:flex;flex-direction:column;overflow-y:auto;padding-bottom:calc(20px + var(–safe));}
.drawer.open{transform:translateX(0);}
.dhead{padding:16px;border-bottom:1px solid rgba(255,255,255,0.07);display:flex;align-items:center;justify-content:space-between;}
.dhead h2{font-family:‘Noto Serif JP’,serif;font-size:16px;color:var(–white);}
.dbody{padding:16px;display:flex;flex-direction:column;gap:13px;}
.fg label{display:block;font-size:11px;color:var(–gray);letter-spacing:.1em;text-transform:uppercase;margin-bottom:5px;}
.fg input,.fg select{width:100%;padding:9px 12px;background:var(–d3);border:1px solid rgba(255,255,255,0.1);border-radius:9px;color:var(–white);font-size:14px;font-family:‘Inter’,sans-serif;outline:none;transition:border-color .15s;}
.fg input:focus,.fg select:focus{border-color:var(–red);}
.fg select option{background:var(–d2);}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.sbtn{padding:11px;border-radius:10px;background:var(–red);border:none;color:#fff;font-size:14px;font-weight:600;cursor:pointer;transition:background .15s;}
.sbtn:hover{background:var(–red-dark);}
.pcard{background:var(–d3);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:12px 14px;font-size:13px;color:var(–off);line-height:1.8;display:none;}
.pcard.on{display:block;}
.pcard strong{color:var(–gold);}

/* TABS */
.tabs{flex-shrink:0;position:relative;z-index:10;display:flex;overflow-x:auto;scrollbar-width:none;background:rgba(13,13,13,0.85);border-bottom:1px solid rgba(255,255,255,0.06);padding:0 8px;}
.tabs::-webkit-scrollbar{display:none;}
.tab{flex-shrink:0;padding:10px 14px;font-size:12.5px;font-weight:500;color:var(–gray);cursor:pointer;border-bottom:2px solid transparent;transition:all .2s;white-space:nowrap;}
.tab:hover{color:var(–white);}
.tab.active{color:var(–red);border-bottom-color:var(–red);}

/* CHIPS */
.chips{flex-shrink:0;display:flex;gap:7px;padding:9px 12px;overflow-x:auto;scrollbar-width:none;background:rgba(18,18,18,0.7);border-bottom:1px solid rgba(255,255,255,0.04);}
.chips::-webkit-scrollbar{display:none;}
.chip{flex-shrink:0;padding:6px 13px;border-radius:18px;font-size:12px;font-weight:500;background:var(–d3);border:1px solid rgba(255,255,255,0.08);color:var(–off);cursor:pointer;transition:all .2s;white-space:nowrap;-webkit-tap-highlight-color:transparent;}
.chip:hover,.chip:active{background:var(–red-dark);border-color:var(–red);color:#fff;}

/* MESSAGES */
.msgwrap{flex:1;min-height:0;display:flex;flex-direction:column;position:relative;}
.msgs{flex:1;overflow-y:auto;padding:16px 12px;display:flex;flex-direction:column;gap:16px;-webkit-overflow-scrolling:touch;}
.msgs::-webkit-scrollbar{width:3px;}
.msgs::-webkit-scrollbar-thumb{background:var(–d4);border-radius:2px;}

/* Welcome */
.welcome{text-align:center;padding:28px 16px;animation:fi .6s ease;}
.wk{font-family:‘Noto Serif JP’,serif;font-size:58px;font-weight:900;color:var(–red);text-shadow:0 0 30px var(–red-glow);display:block;margin-bottom:12px;animation:pulse 3s ease-in-out infinite;}
@keyframes pulse{0%,100%{text-shadow:0 0 30px var(–red-glow);}50%{text-shadow:0 0 50px rgba(192,57,43,.45);}}
.welcome h2{font-family:‘Noto Serif JP’,serif;font-size:20px;color:var(–white);margin-bottom:8px;}
.welcome p{font-size:13px;color:var(–gray);max-width:400px;margin:0 auto;line-height:1.6;}
.pp{margin-top:14px;padding:9px 16px;display:inline-flex;align-items:center;gap:8px;background:var(–d3);border:1px solid rgba(255,255,255,0.1);border-radius:20px;font-size:12px;color:var(–gold);cursor:pointer;transition:all .2s;}
.pp:hover{background:var(–d4);}

/* Messages */
.msg{display:flex;gap:10px;animation:si .3s ease;}
@keyframes si{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:translateY(0);}}
@keyframes fi{from{opacity:0;}to{opacity:1;}}
.msg.u{flex-direction:row-reverse;}
.av{width:32px;height:32px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:14px;font-family:‘Noto Serif JP’,serif;font-weight:900;}
.av.ai{background:var(–red-dark);color:#fff;border:1px solid var(–red);box-shadow:0 0 10px var(–red-glow);}
.av.u{background:var(–d4);color:var(–white);border:1px solid rgba(255,255,255,0.12);}
.bub{max-width:80%;padding:11px 14px;border-radius:14px;font-size:13.5px;line-height:1.75;word-break:break-word;}
.msg.ai .bub{background:var(–d2);border:1px solid rgba(255,255,255,0.07);border-top-left-radius:4px;color:var(–off);}
.msg.u .bub{background:var(–red-dark);border:1px solid var(–red);border-top-right-radius:4px;color:#fff;}
.bub h3{color:var(–gold);font-size:12.5px;font-weight:700;margin:10px 0 5px;text-transform:uppercase;letter-spacing:.06em;}
.bub strong{color:var(–gold);}
.bub em{color:#e8b4a0;font-style:normal;}
.bub ul,.bub ol{padding-left:18px;margin:7px 0;}
.bub li{margin:4px 0;line-height:1.6;}
.bub hr{border:none;border-top:1px solid rgba(255,255,255,0.1);margin:10px 0;}
.bub p{margin:5px 0;}
.bub p:first-child{margin-top:0;}
.bub p:last-child{margin-bottom:0;}

/* Typing */
.tw{display:flex;gap:10px;animation:si .3s ease;}
.typ{display:flex;align-items:center;gap:4px;padding:12px 14px;background:var(–d2);border:1px solid rgba(255,255,255,0.07);border-radius:14px;border-top-left-radius:4px;}
.typ span{width:6px;height:6px;border-radius:50%;background:var(–red);animation:bo 1.2s infinite;}
.typ span:nth-child(2){animation-delay:.2s;}
.typ span:nth-child(3){animation-delay:.4s;}
@keyframes bo{0%,60%,100%{transform:translateY(0);opacity:.35;}30%{transform:translateY(-5px);opacity:1;}}

/* Scroll btn */
.scb{position:absolute;right:12px;bottom:8px;z-index:15;width:32px;height:32px;border-radius:50%;background:var(–d3);border:1px solid rgba(255,255,255,0.15);color:var(–white);font-size:15px;cursor:pointer;display:none;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,0.4);transition:all .2s;}
.scb.on{display:flex;}
.scb:hover{background:var(–red-dark);border-color:var(–red);}

/* INPUT */
.inparea{flex-shrink:0;position:relative;z-index:20;padding:10px 12px calc(10px + var(–safe));background:rgba(13,13,13,0.97);border-top:1px solid rgba(255,255,255,0.07);}
.inprow{display:flex;gap:8px;align-items:flex-end;}
.inpbox{flex:1;display:flex;align-items:flex-end;gap:8px;background:var(–d2);border:1px solid rgba(255,255,255,0.1);border-radius:13px;padding:9px 12px;transition:border-color .2s;}
.inpbox:focus-within{border-color:var(–red);box-shadow:0 0 0 3px var(–red-glow);}
textarea{flex:1;background:transparent;border:none;outline:none;color:var(–white);font-family:‘Inter’,sans-serif;font-size:14px;line-height:1.5;resize:none;max-height:100px;min-height:21px;}
textarea::placeholder{color:#4a4a4a;}
.sndbtn{width:36px;height:36px;border-radius:10px;background:var(–red);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .15s;color:white;font-size:17px;flex-shrink:0;-webkit-tap-highlight-color:transparent;}
.sndbtn:hover{background:var(–red-dark);transform:scale(1.05);}
.sndbtn:disabled{background:var(–d4);cursor:not-allowed;transform:none;}
.hint{text-align:center;font-size:10px;color:#3a3a3a;margin-top:6px;}

/* TOAST */
.toast{position:fixed;bottom:86px;left:50%;transform:translateX(-50%) translateY(10px);background:var(–d3);border:1px solid rgba(255,255,255,0.15);color:var(–white);padding:8px 18px;border-radius:20px;font-size:13px;z-index:200;opacity:0;transition:all .3s;pointer-events:none;white-space:nowrap;}
.toast.on{opacity:1;transform:translateX(-50%) translateY(0);}

@media(min-width:600px){
.msgs{padding:20px;}
.bub{max-width:72%;font-size:14px;}
.inparea{padding:12px 20px calc(12px + var(–safe));}
header{padding:14px 20px;}
}
</style>

</head>
<body>

<header>
  <div class="logo">
    <div class="logo-kanji">柔道</div>
    <div class="logo-text"><h1>Сенсей AI</h1><p>Тренер · Дзюдо · Фитнес · Питание</p></div>
  </div>
  <div class="hbtns">
    <button class="ibtn" onclick="openD()" title="Мой профиль">👤</button>
    <button class="ibtn del" onclick="clearChat()" title="Очистить чат">🗑</button>
  </div>
</header>

<div class="tabs" id="tabs">
  <div class="tab active" data-m="general">🎯 Общее</div>
  <div class="tab" data-m="judo">🥋 Дзюдо</div>
  <div class="tab" data-m="fitness">💪 Фитнес</div>
  <div class="tab" data-m="nutrition">🥗 Питание</div>
  <div class="tab" data-m="competition">🏆 Соревнования</div>
</div>

<div class="chips" id="chips"></div>

<div class="msgwrap">
  <div class="msgs" id="msgs">
    <div class="welcome" id="welcome">
      <span class="wk">道</span>
      <h2>Приветствую, спортсмен!</h2>
      <p>Я твой персональный тренер по дзюдо и фитнесу. Знаю правила IJF, помогу с тренировками, питанием и подготовкой к соревнованиям.</p>
      <div class="pp" onclick="openD()">👤 Заполни профиль для персональных советов</div>
    </div>
  </div>
  <button class="scb" id="scb" onclick="stb()">↓</button>
</div>

<div class="inparea">
  <div class="inprow">
    <div class="inpbox">
      <textarea id="inp" placeholder="Задай вопрос сенсею…" rows="1"
        onkeydown="onK(event)" oninput="rs(this)"></textarea>
    </div>
    <button class="sndbtn" id="sndbtn" onclick="send()">➤</button>
  </div>
  <div class="hint">Enter — отправить · Shift+Enter — новая строка</div>
</div>

<!-- PROFILE DRAWER -->

<div class="ov" id="ov" onclick="closeD()"></div>
<div class="drawer" id="drawer">
  <div class="dhead">
    <h2>👤 Мой профиль</h2>
    <button class="ibtn" onclick="closeD()">✕</button>
  </div>
  <div class="dbody">
    <div class="pcard" id="pcard"></div>
    <div class="fg"><label>Имя</label><input id="pN" placeholder="Как тебя зовут?"/></div>
    <div class="row2">
      <div class="fg"><label>Возраст</label><input id="pA" type="number" placeholder="лет" min="5" max="80"/></div>
      <div class="fg"><label>Пол</label>
        <select id="pG"><option value="">—</option><option>Мужской</option><option>Женский</option></select>
      </div>
    </div>
    <div class="row2">
      <div class="fg"><label>Вес (кг)</label><input id="pW" type="number" placeholder="кг"/></div>
      <div class="fg"><label>Рост (см)</label><input id="pH" type="number" placeholder="см"/></div>
    </div>
    <div class="fg"><label>Уровень дзюдо</label>
      <select id="pL">
        <option value="">Выбери уровень</option>
        <option>Новичок (нет пояса)</option><option>Белый пояс</option><option>Жёлтый пояс</option>
        <option>Оранжевый пояс</option><option>Зелёный пояс</option><option>Синий пояс</option>
        <option>Коричневый пояс</option><option>Чёрный пояс 1–2 дан</option><option>Чёрный пояс 3+ дан</option>
      </select>
    </div>
    <div class="fg"><label>Цель</label>
      <select id="pGoal">
        <option value="">Выбери цель</option>
        <option>Освоить базовую технику дзюдо</option><option>Подготовиться к соревнованиям</option>
        <option>Набрать мышечную массу</option><option>Сбросить / согнать вес</option>
        <option>Повысить выносливость</option><option>Общая физическая форма</option>
        <option>Восстановление после травмы</option>
      </select>
    </div>
    <div class="fg"><label>Тренировок в неделю</label>
      <select id="pF">
        <option value="">—</option><option>1–2 раза</option><option>3–4 раза</option>
        <option>5–6 раз</option><option>Каждый день</option>
      </select>
    </div>
    <div class="fg"><label>Травмы / ограничения</label><input id="pI" placeholder="Например: колено, спина…"/></div>
    <button class="sbtn" onclick="saveP()">💾 Сохранить профиль</button>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const CHIPS={
  general:["Составь план тренировок","С чего начать дзюдо?","Как похудеть и набрать форму?","Разминка перед татами","Советы для новичка"],
  judo:["Правила IJF 2024","Техника O-soto-gari","Что такое иппон?","Запрещённые приёмы","Система наказаний","Как выбрать дзюдоги?","Весовые категории"],
  fitness:["ОФП для дзюдо","Упражнения для захвата","Взрывная сила","Кардио для борца","Тренировка кора","Гибкость и растяжка"],
  nutrition:["Рацион дзюдоиста","Сгонка веса перед турниром","Что есть до тренировки?","Восстановление после нагрузок","Гидратация","Спортивные добавки"],
  competition:["Подготовка за неделю до турнира","Разминка перед схваткой","Психологический настрой","Тактика в матче","Разбор поражения","День соревнований"]
};

const SYS=`Ты — Сенсей AI, профессиональный тренер с чёрным поясом 6-го дана по дзюдо, лицензированный тренер по фитнесу и спортивный нутрициолог.

ЗНАНИЯ:
🥋 Дзюдо: правила IJF 2024, броски (нагэ-вадза: 67 техник Годокё), удержания (осаэ-вадза), болевые (кансэцу-вадза), удушающие (симэ-вадза). Оценки: иппон (победа), вадза-ари (2=иппон). Голдэн скор — доп. время до первого очка. Наказания: сидо×3=хансоку-маке (поражение). Весовые категории: мужчины −60,−66,−73,−81,−90,−100,+100кг; женщины −48,−52,−57,−63,−70,−78,+78кг. Форма: белый и синий дзюдоги. Принципы Дзигоро Кано: максимальная эффективность, взаимное процветание.
💪 Фитнес: периодизация, ОФП/СФП для единоборств, взрывная сила, выносливость.
🥗 Питание: макросы, микросы, тайминг, сгонка веса, гидратация, восстановление.
🏆 Соревнования: тактика, психология, разминка, пик формы.

СТИЛЬ: отвечай на русском, используй ### заголовки, списки -, **жирный**, *курсив*. Японские термины — с переводом. Конкретные советы. Строгий, но заботливый сенсей. Учитывай профиль пользователя если он заполнен.`;

let mode='general', hist=[], busy=false;
let P=JSON.parse(localStorage.getItem('sp')||'{}');

// Profile
function saveP(){
  P={name:$('pN').value.trim(),age:$('pA').value,gender:$('pG').value,weight:$('pW').value,height:$('pH').value,level:$('pL').value,goal:$('pGoal').value,freq:$('pF').value,injury:$('pI').value.trim()};
  localStorage.setItem('sp',JSON.stringify(P));
  renderPC(); closeD(); showToast('Профиль сохранён ✓');
}
function loadPF(){
  if(!P.name)return;
  $('pN').value=P.name||'';$('pA').value=P.age||'';$('pG').value=P.gender||'';
  $('pW').value=P.weight||'';$('pH').value=P.height||'';$('pL').value=P.level||'';
  $('pGoal').value=P.goal||'';$('pF').value=P.freq||'';$('pI').value=P.injury||'';
}
function renderPC(){
  const c=$('pcard');
  if(!P.name){c.classList.remove('on');return;}
  const r=[];
  if(P.name)r.push('<strong>Спортсмен:</strong> '+P.name);
  if(P.age||P.gender)r.push('<strong>Данные:</strong> '+[P.age&&P.age+' лет',P.gender].filter(Boolean).join(', '));
  if(P.weight||P.height)r.push('<strong>Параметры:</strong> '+[P.weight&&P.weight+' кг',P.height&&P.height+' см'].filter(Boolean).join(' / '));
  if(P.level)r.push('<strong>Уровень:</strong> '+P.level);
  if(P.goal)r.push('<strong>Цель:</strong> '+P.goal);
  if(P.injury)r.push('<strong>Ограничения:</strong> '+P.injury);
  c.innerHTML=r.join('<br>');c.classList.add('on');
}
function pCtx(){
  if(!P.name)return'';
  const r=[];
  if(P.name)r.push('Имя: '+P.name);
  if(P.age)r.push('Возраст: '+P.age+' лет');
  if(P.gender)r.push('Пол: '+P.gender);
  if(P.weight)r.push('Вес: '+P.weight+' кг');
  if(P.height)r.push('Рост: '+P.height+' см');
  if(P.level)r.push('Уровень дзюдо: '+P.level);
  if(P.goal)r.push('Цель: '+P.goal);
  if(P.freq)r.push('Тренировок/нед: '+P.freq);
  if(P.injury)r.push('Ограничения: '+P.injury);
  return r.length?'\n\nПРОФИЛЬ:\n'+r.join('\n'):'';
}
function openD(){loadPF();renderPC();$('drawer').classList.add('open');$('ov').classList.add('open');}
function closeD(){$('drawer').classList.remove('open');$('ov').classList.remove('open');}

// Tabs
$('tabs').addEventListener('click',e=>{
  const t=e.target.closest('.tab');if(!t)return;
  document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
  t.classList.add('active');mode=t.dataset.m;renderChips();
});
function renderChips(){
  $('chips').innerHTML=CHIPS[mode].map(c=>`<div class="chip" onclick="useChip('${c.replace(/'/g,"\\'")}')"> ${c}</div>`).join('');
}
function useChip(t){$('inp').value=t;send();}

// Markdown
function md(t){
  return t
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/^### (.+)$/gm,'<h3>$1</h3>')
    .replace(/^## (.+)$/gm,'<h3>$1</h3>')
    .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
    .replace(/\*(.+?)\*/g,'<em>$1</em>')
    .replace(/^[-•] (.+)$/gm,'<li>$1</li>')
    .replace(/^(\d+)\. (.+)$/gm,'<li>$2</li>')
    .replace(/(<li>[\s\S]*?<\/li>)/g,'<ul>$1</ul>')
    .replace(/<\/ul>\s*<ul>/g,'')
    .replace(/---+/g,'<hr>')
    .replace(/\n{2,}/g,'</p><p>')
    .replace(/\n/g,'<br>')
    .replace(/^/,'<p>').replace(/$/,'</p>');
}

// Chat
function addMsg(role,html){
  const m=$('msgs'),w=$('welcome');if(w)w.remove();
  const d=document.createElement('div');d.className='msg '+(role==='user'?'u':'ai');
  const av=document.createElement('div');av.className='av '+(role==='user'?'u':'ai');av.textContent=role==='user'?'👤':'師';
  const b=document.createElement('div');b.className='bub';b.innerHTML=html;
  d.appendChild(av);d.appendChild(b);m.appendChild(d);stb();
}
function showTyp(){
  const m=$('msgs'),d=document.createElement('div');d.className='tw';d.id='typ';
  const av=document.createElement('div');av.className='av ai';av.textContent='師';
  const t=document.createElement('div');t.className='typ';t.innerHTML='<span></span><span></span><span></span>';
  d.appendChild(av);d.appendChild(t);m.appendChild(d);stb();
}
function hideTyp(){$('typ')?.remove();}
function stb(){const m=$('msgs');m.scrollTop=m.scrollHeight;}
$('msgs').addEventListener('scroll',()=>{
  const m=$('msgs'),atB=m.scrollHeight-m.scrollTop-m.clientHeight<80;
  $('scb').classList.toggle('on',!atB);
});

function clearChat(){
  if(!confirm('Очистить историю чата?'))return;
  hist=[];
  $('msgs').innerHTML=`<div class="welcome" id="welcome"><span class="wk">道</span><h2>Новый диалог</h2><p>История очищена. Задай новый вопрос!</p><div class="pp" onclick="openD()">👤 Профиль спортсмена</div></div>`;
  showToast('Чат очищен');
}

// Send
async function send(){
  if(busy)return;
  const inp=$('inp'),text=inp.value.trim();if(!text)return;
  inp.value='';inp.style.height='auto';
  busy=true;$('sndbtn').disabled=true;
  addMsg('user',text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'));
  const mHint={general:'Универсальный тренер.',judo:'Фокус: дзюдо, техника, правила IJF.',fitness:'Фокус: физподготовка.',nutrition:'Фокус: питание.',competition:'Фокус: соревнования.'}[mode];
  hist.push({role:'user',content:text});
  showTyp();
  try{
    const r=await fetch('https://api.anthropic.com/v1/messages',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({model:'claude-sonnet-4-20250514',max_tokens:1000,system:SYS+pCtx()+'\nРежим: '+mHint,messages:hist})});
    const d=await r.json();
    const reply=d.content?.[0]?.text||'Попробуй ещё раз.';
    hist.push({role:'assistant',content:reply});
    hideTyp();addMsg('ai',md(reply));
  }catch(e){hideTyp();addMsg('ai','⚠️ Ошибка соединения. Проверь интернет.');}
  busy=false;$('sndbtn').disabled=false;inp.focus();
}
function onK(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}}
function rs(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,100)+'px';}

// Toast
function showToast(msg){const t=$('toast');t.textContent=msg;t.classList.add('on');setTimeout(()=>t.classList.remove('on'),2200);}

// Util
function $(id){return document.getElementById(id);}

// Init
renderChips();$('inp').focus();
</script>

</body>
</html>