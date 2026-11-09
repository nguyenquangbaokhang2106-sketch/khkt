import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
detail_data = json.loads((ROOT / 'data' / 'provinces_detail.json').read_text(encoding='utf-8'))

template = '''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chi tiết tỉnh thành — VietNam Explorer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
<style>
:root{
  --paper:#f5f7f2;--ink:#1a2b22;--muted:#667768;--line:#dde4d6;
  --accent:#2b593f;--card-bg:#ffffff;--soft:#eef3e8;
  font-family:'Be Vietnam Pro',system-ui,-apple-system,sans-serif;
  color:var(--ink);background:var(--paper);
}
*{box-sizing:border-box}body{margin:0;line-height:1.65;background:var(--paper)}
a{color:inherit;text-decoration:none}
button{font:inherit;cursor:pointer}

/* Top bar */
.top-nav{
  position:sticky;top:0;z-index:50;
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 5%;background:rgba(245,247,242,0.94);
  backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  border-bottom:1px solid var(--line);
}
.back-btn{
  display:inline-flex;align-items:center;gap:8px;
  background:#ffffff;border:1px solid var(--line);
  padding:8px 16px;border-radius:24px;
  font-size:16.5px;font-weight:600;color:#284330;
  transition:all .18s ease;box-shadow:0 2px 8px rgba(0,0,0,0.03);
}
.back-btn:hover{background:#e7efe0;border-color:#b9ccaf;transform:translateX(-2px)}
.top-title{font-size:17px;font-weight:700;color:#45604b;letter-spacing:1px;text-transform:uppercase}
.top-badge{display:inline-flex;align-items:center;gap:6px;font-size:15.5px;padding:6px 12px;background:#e2ebda;color:#23442a;border-radius:20px;font-weight:600}
.top-dot{width:7px;height:7px;border-radius:50%;background:#10b981}

/* Container */
.page-wrap{max-width:1200px;margin:auto;padding:28px 5% 60px}

/* Province Switcher & Region Filter */
.region-switcher{
  background:#ffffff;border:1px solid var(--line);border-radius:20px;
  padding:16px 20px;margin-bottom:28px;box-shadow:0 4px 18px rgba(35,55,35,0.04);
}
.region-tabs{
  display:flex;gap:6px;overflow-x:auto;padding-bottom:10px;margin-bottom:10px;
  border-bottom:1px solid #edf2e8;scrollbar-width:none;
}
.region-tabs::-webkit-scrollbar{display:none}
.reg-tab-btn{
  padding:5px 12px;border-radius:14px;border:1px solid #dce4d4;
  background:#f7f9f4;font-size:15px;font-weight:600;color:#546850;
  white-space:nowrap;transition:all .18s;
}
.reg-tab-btn:hover{background:#e8f0e0;color:#1e3522}
.reg-tab-btn.is-active{background:#25442f;color:#ffffff;border-color:#25442f}

.switcher-pills{display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}
.switcher-pills::-webkit-scrollbar{display:none}
.switch-pill{
  display:inline-flex;align-items:center;gap:6px;
  padding:6px 12px;border-radius:20px;
  border:1px solid #dce4d4;background:#f9fbf7;
  font-size:15.5px;font-weight:600;color:#334835;
  white-space:nowrap;transition:all .18s;
}
.switch-pill:hover{background:#edf4e6;border-color:#b7caa9;transform:translateY(-1px)}
.switch-pill.is-current{
  background:#233f2c;color:#ffffff;border-color:#233f2c;
  box-shadow:0 4px 12px rgba(35,63,44,0.25);
}
.switch-pill .p-dot{width:7px;height:7px;border-radius:50%}

/* Hero section */
.hero{
  display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:36px;
  background:#ffffff;border:1px solid var(--line);border-radius:24px;
  padding:36px;margin-bottom:32px;box-shadow:0 8px 30px rgba(35,55,35,0.04);
  position:relative;overflow:hidden;
}
.hero::before{
  content:'';position:absolute;top:0;right:0;width:340px;height:100%;
  background:radial-gradient(circle at 80% 30%, rgba(144,195,140,0.15), transparent 70%);
  pointer-events:none;
}
.hero-tag{
  display:inline-flex;align-items:center;gap:7px;
  font-size:15.5px;font-weight:650;color:#355639;
  background:#e7f0e0;padding:5px 12px;border-radius:20px;margin-bottom:14px;
}
.hero-name{
  font-family:'Playfair Display',Georgia,serif;
  font-size:clamp(36px,3.8vw,52px);font-weight:700;
  line-height:1.15;letter-spacing:-1px;margin:0 0 12px;color:#183220;
}
.hero-quote{
  font-size:18px;font-weight:550;color:#5a755d;
  font-style:italic;margin:0 0 16px;line-height:1.5;
}
.hero-desc{
  font-size:17.5px;line-height:1.85;color:#4a594d;margin:0;max-width:680px;
}
.hero-visual{
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:linear-gradient(145deg,#f3f7ee,#e7eee0);
  border:1px solid #dbe4d4;border-radius:20px;padding:24px 20px;text-align:center;
}
.silhouette-img{max-width:180px;max-height:180px;object-fit:contain;filter:drop-shadow(0 10px 14px rgba(35,55,35,0.18))}
.hero-id-tag{margin-top:14px;font-size:15px;font-weight:700;letter-spacing:1.5px;color:#5a7356;text-transform:uppercase}

/* Key Stats Grid */
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px}
.stat-card{
  background:#ffffff;border:1px solid var(--line);border-radius:18px;
  padding:20px;box-shadow:0 4px 16px rgba(35,55,35,0.03);
  transition:transform .18s,box-shadow .18s;
}
.stat-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(35,55,35,0.06)}
.stat-label{font-size:14.5px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#70826d;margin-bottom:6px}
.stat-val{font-size:25px;font-weight:750;letter-spacing:-.6px;color:#1d3926;margin-bottom:4px;line-height:1.2}
.stat-sub{font-size:15px;color:#7a8a76}

/* Content Sections */
.section-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:32px}
.card{
  background:#ffffff;border:1px solid var(--line);border-radius:20px;
  padding:26px;box-shadow:0 4px 18px rgba(35,55,35,0.03);
}
.card-header{display:flex;align-items:center;gap:10px;margin-bottom:18px;border-bottom:1px solid #edf2e8;padding-bottom:12px}
.card-icon{width:32px;height:32px;border-radius:8px;background:#e9f0e2;display:grid;place-items:center;color:#2f5337;font-size:20px}
.card-title{font-size:20px;font-weight:700;letter-spacing:-.3px;color:#1e3523;margin:0}
.info-list{margin:0;padding-left:18px;color:#445747;font-size:17px;line-height:1.85}
.info-list li{margin-bottom:10px}

/* Highlights Gallery */
.highlights-section{margin-bottom:40px}
.section-title{
  display:flex;align-items:center;gap:12px;
  font-family:'Playfair Display',Georgia,serif;
  font-size:30px;font-weight:700;color:#183220;margin:0 0 20px;
}
.section-title::after{content:'';flex:1;height:1px;background:var(--line)}
.highlights-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.highlight-card{
  background:#ffffff;border:1px solid var(--line);border-radius:20px;
  overflow:hidden;box-shadow:0 6px 22px rgba(35,55,35,0.04);
  display:flex;flex-direction:column;transition:transform .2s,box-shadow .2s;
}
.highlight-card:hover{transform:translateY(-3px);box-shadow:0 12px 30px rgba(35,55,35,0.09)}
.img-wrap{
  position:relative;width:100%;height:250px;background:#e6ede0;overflow:hidden;cursor:zoom-in;
}
.highlight-img{
  width:100%;height:100%;object-fit:cover;transition:transform .4s ease;
}
.highlight-card:hover .highlight-img{transform:scale(1.04)}
.img-badge{
  position:absolute;top:14px;left:14px;background:rgba(20,38,25,0.82);
  color:#ffffff;font-size:14px;font-weight:600;padding:4px 9px;border-radius:12px;
  backdrop-filter:blur(6px);
}
.highlight-body{padding:22px;flex:1;display:flex;flex-direction:column}
.highlight-title{font-size:21px;font-weight:700;color:#1b3622;margin:0 0 8px}
.highlight-caption{font-size:15.5px;font-weight:600;color:#5a755d;margin:0 0 10px}
.highlight-desc{font-size:16.5px;line-height:1.75;color:#4d5f50;margin:0}

/* Heritage & Links bottom cards */
.bottom-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:40px}
.badge-list{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.heritage-badge{
  display:inline-flex;align-items:center;gap:6px;font-size:16px;font-weight:600;
  padding:7px 12px;border-radius:10px;background:#edf4e7;color:#28482d;
  border:1px solid #dbe6d3;
}
.link-list{display:flex;flex-direction:column;gap:8px;margin-top:12px}
.ext-link{
  display:inline-flex;align-items:center;justify-content:space-between;
  padding:10px 14px;border-radius:10px;background:#f8faf6;border:1px solid #dce4d5;
  font-size:16.5px;font-weight:600;color:#23442a;transition:all .18s;
}
.ext-link:hover{background:#edf5e5;border-color:#b5caa6;transform:translateX(3px);color:#122918}

/* Lightbox Modal */
.modal{
  position:fixed;inset:0;z-index:100;background:rgba(12,22,15,0.92);
  backdrop-filter:blur(8px);display:none;align-items:center;justify-content:center;padding:30px;
}
.modal.is-open{display:flex}
.modal-content{max-width:92vw;max-height:88vh;border-radius:16px;overflow:hidden;position:relative}
.modal-img{max-width:100%;max-height:85vh;object-fit:contain;display:block}
.modal-caption{
  background:#1a2b1f;color:#e8f0e4;font-size:17px;padding:12px 18px;text-align:center;font-weight:500;
}
.modal-close{
  position:absolute;top:20px;right:24px;color:#ffffff;background:rgba(255,255,255,0.2);
  border:0;width:38px;height:38px;border-radius:50%;font-size:26px;display:grid;place-items:center;
}
.modal-close:hover{background:rgba(255,255,255,0.35)}

/* Bottom page navigation */
.page-nav-btns{
  display:flex;justify-content:space-between;align-items:center;gap:16px;
  margin-top:20px;padding-top:24px;border-top:1px solid var(--line);
}
.nav-link-btn{
  display:inline-flex;align-items:center;gap:8px;
  padding:10px 18px;border-radius:12px;background:#ffffff;border:1px solid var(--line);
  font-size:16.5px;font-weight:650;color:#2b4830;transition:all .18s;
}
.nav-link-btn:hover{background:#edf4e7;border-color:#b9ccaf;transform:translateY(-1px)}

/* Responsive */
@media(max-width:950px){
  .hero{grid-template-columns:1fr;padding:26px}
  .hero-visual{order:-1;padding:18px}
  .stats-grid{grid-template-columns:repeat(2,1fr)}
  .section-grid,.highlights-grid,.bottom-grid{grid-template-columns:1fr}
}
@media(max-width:600px){
  .stats-grid{grid-template-columns:1fr}
  .page-wrap{padding:20px 4% 40px}
  .hero-name{font-size:32px}
  .stat-val{font-size:23px}
  .img-wrap{height:200px}
}
</style>
</head>
<body>

<header class="top-nav">
  <a href="./index.html" class="back-btn" title="Quay lại bản đồ tương tác Việt Nam">
    <span>← Quay lại Bản đồ</span>
  </a>
  <div class="top-title">VIETNAM EXPLORER</div>
  <div class="top-badge" id="top-badge">
    <span class="top-dot" id="top-dot"></span>
    <span id="top-region-text">Bản đồ 34 tỉnh thành</span>
  </div>
</header>

<main class="page-wrap">
  <!-- Province Switcher & Region Filter -->
  <section class="region-switcher" aria-label="Chọn tỉnh thành theo vùng">
    <div class="region-tabs" id="region-tabs"></div>
    <div class="switcher-pills" id="switcher-pills"></div>
  </section>

  <!-- Hero Header -->
  <section class="hero" id="hero-section">
    <div>
      <div class="hero-tag" id="hero-tag">
        <span id="hero-tag-text">📍 VÙNG ĐẤT VIỆT NAM</span>
      </div>
      <h1 class="hero-name" id="hero-name">Tỉnh thành</h1>
      <div class="hero-quote" id="hero-quote"></div>
      <p class="hero-desc" id="hero-desc"></p>
    </div>
    <div class="hero-visual">
      <img id="silhouette-img" class="silhouette-img" src="" alt="Bản đồ đường viền tỉnh">
      <div class="hero-id-tag" id="hero-id-tag">TỈNH THÀNH #01</div>
    </div>
  </section>

  <!-- Statistics Grid -->
  <section class="stats-grid" id="stats-grid"></section>

  <!-- Section Cards Grid -->
  <section class="section-grid" id="section-grid"></section>

  <!-- Highlights & Real Photo Gallery -->
  <section class="highlights-section">
    <h2 class="section-title">Hình ảnh, Thắng cảnh & Di tích tiêu biểu</h2>
    <div class="highlights-grid" id="highlights-grid"></div>
  </section>

  <!-- Bottom Grid: Heritage & Links -->
  <section class="bottom-grid">
    <div class="card">
      <div class="card-header">
        <div class="card-icon">🏛️</div>
        <h3 class="card-title">Di sản & Điểm đến văn hóa</h3>
      </div>
      <div class="badge-list" id="heritage-list"></div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="card-icon">🔗</div>
        <h3 class="card-title">Hình ảnh tham khảo & Cổng thông tin</h3>
      </div>
      <div class="link-list" id="links-list"></div>
    </div>
  </section>

  <!-- Next / Prev Province Navigator -->
  <div class="page-nav-btns">
    <button type="button" class="nav-link-btn" id="prev-btn">← Tỉnh trước</button>
    <a href="./index.html" class="nav-link-btn" style="background:#284831;color:#fff;border-color:#284831">Bản đồ toàn quốc ↗</a>
    <button type="button" class="nav-link-btn" id="next-btn">Tỉnh tiếp theo →</button>
  </div>
</main>

<!-- Lightbox Modal -->
<div class="modal" id="image-modal" role="dialog" aria-modal="true" aria-label="Phóng to ảnh">
  <button class="modal-close" id="modal-close" aria-label="Đóng">✕</button>
  <div class="modal-content">
    <img id="modal-img" class="modal-img" src="" alt="">
    <div id="modal-caption" class="modal-caption"></div>
  </div>
</div>

<script>
'use strict';
const DATA = /* PROVINCE_DETAIL_DATA */;

const REGIONS_LIST = [
  {id: 'all', name: 'Tất cả 36 địa phương & quần đảo'},
  {id: 'vung-1', name: 'Trung Du & MN Bắc Bộ (9)'},
  {id: 'vung-2', name: 'Đồng bằng sông Hồng (6)'},
  {id: 'vung-3', name: 'Bắc Trung Bộ (5)'},
  {id: 'vung-4', name: 'Nam Trung Bộ, Tây Nguyên & Biển Đảo (8)'},
  {id: 'vung-5', name: 'Đông Nam Bộ (8)'}
];

const ALL_IDS = Object.keys(DATA).map(Number).sort((a,b)=>a-b);

function getUrlId() {
  const params = new URLSearchParams(window.location.search);
  const qId = parseInt(params.get('id'));
  if (qId && DATA[qId]) return qId;
  const qSlug = params.get('slug');
  if (qSlug) {
    const found = ALL_IDS.find(id => DATA[id] && DATA[id].slug === qSlug);
    if (found) return found;
  }
  return 5; // Default: Tuyên Quang
}

let currentId = getUrlId();
let currentRegionFilter = (DATA[currentId] && DATA[currentId].regionId) || 'all';

function renderRegionTabs() {
  const container = document.getElementById('region-tabs');
  container.replaceChildren();
  REGIONS_LIST.forEach(r => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'reg-tab-btn' + (r.id === currentRegionFilter ? ' is-active' : '');
    btn.textContent = r.name;
    btn.onclick = () => {
      currentRegionFilter = r.id;
      renderRegionTabs();
      renderSwitcherPills();
    };
    container.append(btn);
  });
}

function renderSwitcherPills() {
  const container = document.getElementById('switcher-pills');
  container.replaceChildren();
  const list = (currentRegionFilter === 'all') 
    ? ALL_IDS 
    : ALL_IDS.filter(id => DATA[id] && DATA[id].regionId === currentRegionFilter);

  list.forEach(oId => {
    const item = DATA[oId];
    if (!item) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'switch-pill' + (oId === currentId ? ' is-current' : '');
    btn.innerHTML = `<span class="p-dot" style="background:${item.litColor}"></span><span>${item.short}</span>`;
    btn.addEventListener('click', () => {
      renderPage(oId);
      window.scrollTo({top: 0, behavior: 'smooth'});
    });
    container.append(btn);
  });
}

function renderPage(id) {
  const p = DATA[id];
  if (!p) return;
  currentId = id;
  currentRegionFilter = p.regionId;

  // Update browser URL without reload
  const url = new URL(window.location.href);
  url.searchParams.set('id', id);
  window.history.replaceState({id}, '', url.toString());

  document.title = `${p.name} — Thông tin & Hình ảnh đầy đủ · VietNam Explorer`;

  // Top badge
  document.getElementById('top-dot').style.background = p.litColor;
  document.getElementById('top-region-text').textContent = p.regionName;

  // Switchers
  renderRegionTabs();
  renderSwitcherPills();

  // Hero section
  document.getElementById('hero-tag-text').textContent = `📍 ${p.regionName.toUpperCase()}`;
  document.getElementById('hero-name').textContent = p.name;
  document.getElementById('hero-quote').textContent = p.quote || '';
  document.getElementById('hero-desc').textContent = p.overview || '';
  document.getElementById('silhouette-img').src = p.silhouette;
  document.getElementById('silhouette-img').alt = 'Bản đồ ranh giới ' + p.name;
  document.getElementById('hero-id-tag').textContent = (p.id >= 35) ? `QUẦN ĐẢO THIÊNG LIÊNG #${String(p.id).padStart(2,'0')}` : `TỈNH THÀNH #${String(p.id).padStart(2,'0')}`;

  // Key stats
  const statsGrid = document.getElementById('stats-grid');
  statsGrid.replaceChildren();
  (p.stats || []).forEach(st => {
    const card = document.createElement('div');
    card.className = 'stat-card';
    card.innerHTML = `
      <div class="stat-label">${st.label}</div>
      <div class="stat-val">${st.value}</div>
      <div class="stat-sub">${st.sub}</div>
    `;
    statsGrid.append(card);
  });

  // Section cards
  const sectionGrid = document.getElementById('section-grid');
  sectionGrid.replaceChildren();
  (p.sections || []).forEach(sec => {
    const card = document.createElement('div');
    card.className = 'card';
    const itemsHtml = (sec.content || []).map(t => `<li>${t}</li>`).join('');
    card.innerHTML = `
      <div class="card-header">
        <div class="card-icon">📌</div>
        <h3 class="card-title">${sec.title}</h3>
      </div>
      <ul class="info-list">${itemsHtml}</ul>
    `;
    sectionGrid.append(card);
  });

  // Highlights & photo gallery
  const highGrid = document.getElementById('highlights-grid');
  highGrid.replaceChildren();
  (p.highlights || []).forEach(h => {
    const card = document.createElement('article');
    card.className = 'highlight-card';
    card.innerHTML = `
      <div class="img-wrap" title="Nhấn để phóng to ảnh">
        <img class="highlight-img" src="${h.image}" alt="${h.title}" loading="lazy">
        <span class="img-badge">📷 HÌNH ẢNH / DANH THẮNG</span>
      </div>
      <div class="highlight-body">
        <h3 class="highlight-title">${h.title}</h3>
        <p class="highlight-caption">${h.caption || ''}</p>
        <p class="highlight-desc">${h.desc || ''}</p>
      </div>
    `;
    const imgWrap = card.querySelector('.img-wrap');
    imgWrap.addEventListener('click', () => openModal(h.image, `${h.title} — ${h.caption}`));
    highGrid.append(card);
  });

  // Heritage list
  const herList = document.getElementById('heritage-list');
  herList.replaceChildren();
  (p.heritage || []).forEach(h => {
    const badge = document.createElement('span');
    badge.className = 'heritage-badge';
    badge.innerHTML = `<span>★</span><span>${h}</span>`;
    herList.append(badge);
  });

  // Links list
  const linksList = document.getElementById('links-list');
  linksList.replaceChildren();
  (p.links || []).forEach(lnk => {
    const a = document.createElement('a');
    a.className = 'ext-link';
    a.href = lnk.url;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.innerHTML = `<span>${lnk.title}</span><span style="color:#7a8a76">↗</span>`;
    linksList.append(a);
  });

  // Next / Prev button setup
  const idx = ALL_IDS.indexOf(id);
  const prevId = ALL_IDS[(idx - 1 + ALL_IDS.length) % ALL_IDS.length];
  const nextId = ALL_IDS[(idx + 1) % ALL_IDS.length];
  
  const prevBtn = document.getElementById('prev-btn');
  prevBtn.textContent = `← ${DATA[prevId].short}`;
  prevBtn.onclick = () => { renderPage(prevId); window.scrollTo({top:0, behavior:'smooth'}); };

  const nextBtn = document.getElementById('next-btn');
  nextBtn.textContent = `${DATA[nextId].short} →`;
  nextBtn.onclick = () => { renderPage(nextId); window.scrollTo({top:0, behavior:'smooth'}); };
}

// Lightbox Modal
const modal = document.getElementById('image-modal');
const modalImg = document.getElementById('modal-img');
const modalCap = document.getElementById('modal-caption');
const modalClose = document.getElementById('modal-close');

function openModal(src, cap) {
  modalImg.src = src;
  modalCap.textContent = cap;
  modal.classList.add('is-open');
}

modalClose.addEventListener('click', () => modal.classList.remove('is-open'));
modal.addEventListener('click', e => { if (e.target === modal) modal.classList.remove('is-open'); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') modal.classList.remove('is-open'); });

// Initial render
renderPage(currentId);
</script>
</body>
</html>
'''

output = template.replace('/* PROVINCE_DETAIL_DATA */', json.dumps(detail_data, ensure_ascii=False))

(ROOT / 'province.html').write_text(output, encoding='utf-8')
(ROOT / 'dist' / 'province.html').write_text(output, encoding='utf-8')

print('Built province.html successfully supporting all 34 provinces!')
