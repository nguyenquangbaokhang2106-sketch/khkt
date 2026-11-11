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
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
<style>
:root{
  --paper:#ffffff;--ink:#1a2b22;--muted:#667768;--line:#e2e8f0;
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
  padding:16px 20px;margin-bottom:28px;box-shadow:0 4px 16px rgba(0,0,0,0.02);
}
.region-tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid #edf1e8}
.reg-tab-btn{
  background:#f0f4ec;border:1px solid transparent;border-radius:20px;
  padding:6px 14px;font-size:13.5px;font-weight:600;color:#35533c;
  transition:all .18s ease;
}
.reg-tab-btn:hover{background:#e1ebdb}
.reg-tab-btn.is-active{background:#23402b;color:#ffffff}
.switcher-pills{display:flex;flex-wrap:wrap;gap:8px;max-height:160px;overflow-y:auto;padding-right:4px}
.switcher-pills::-webkit-scrollbar{width:5px}
.switcher-pills::-webkit-scrollbar-thumb{background:#ccd8c4;border-radius:10px}
.switch-pill{
  display:inline-flex;align-items:center;gap:6px;
  background:#f9fbf7;border:1px solid #e1e7dc;border-radius:16px;
  padding:5px 12px;font-size:13px;color:#253d2c;
  transition:all .15s ease;
}
.switch-pill:hover{background:#e9f0e3;border-color:#b8ccaf;transform:translateY(-1px)}
.switch-pill.is-current{background:#e2eddb;border-color:#2a5033;font-weight:700;color:#183620}
.switch-pill .p-dot{width:6px;height:6px;border-radius:50%}

/* Hero Header */
.hero{
  background:linear-gradient(135deg,#ffffff 0%,#f5f8f2 100%);
  border:1px solid var(--line);border-radius:24px;
  padding:36px 40px;margin-bottom:28px;
  box-shadow:0 8px 30px rgba(0,0,0,0.03);
  display:grid;grid-template-columns:1.5fr 1fr;gap:36px;align-items:center;
}
.hero-tag{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:700;letter-spacing:1.5px;color:#45674c;margin-bottom:10px;text-transform:uppercase}
.hero-name{font-family:'Playfair Display',Georgia,serif;font-size:46px;font-weight:700;line-height:1.15;margin:0 0 14px;color:#122b1b}
.hero-quote{font-style:italic;color:#526d57;font-size:17.5px;margin-bottom:18px;border-left:3px solid #89ad8f;padding-left:14px}
.hero-desc{font-size:16px;color:#3d5242;line-height:1.75;margin:0}
.hero-visual{display:flex;flex-direction:column;align-items:center;justify-content:center;background:#edf3e8;border-radius:20px;padding:26px;border:1px dashed #cadbc2}
.silhouette-img{max-width:240px;max-height:240px;width:auto;height:auto;filter:drop-shadow(0 14px 18px rgba(20,40,25,0.18));transition:transform .3s ease}
.silhouette-img:hover{transform:scale(1.05)}
.hero-id-tag{margin-top:14px;font-size:13.5px;font-weight:700;color:#47654d;letter-spacing:1px}

/* Statistics Grid */
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px}
.stat-card{
  background:#ffffff;border:1px solid var(--line);border-radius:18px;
  padding:20px 22px;box-shadow:0 3px 12px rgba(0,0,0,0.02);
  transition:all .18s ease;
}
.stat-card:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,0.05);border-color:#b9ccaf}
.stat-label{font-size:13px;font-weight:600;color:#6d806f;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}
.stat-val{font-size:27px;font-weight:800;color:#183620;line-height:1.2}
.stat-sub{font-size:12.5px;color:#859687;margin-top:4px}

/* Section Cards Grid */
.section-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-bottom:28px}
.card{
  background:#ffffff;border:1px solid var(--line);border-radius:20px;
  padding:26px 28px;box-shadow:0 4px 16px rgba(0,0,0,0.02);
}
.card-header{display:flex;align-items:center;gap:12px;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #edf1e8}
.card-icon{font-size:24px;width:42px;height:42px;border-radius:12px;background:#eef4e8;display:flex;align-items:center;justify-content:center}
.card-title{font-size:19px;font-weight:700;margin:0;color:#183620}
.card-body{font-size:15px;color:#354d3b;line-height:1.75}
.card-body ul{margin:0;padding-left:20px}
.card-body li{margin-bottom:8px}

/* Real Photo Gallery & Highlights */
.highlights-section{margin-bottom:34px}
.section-title{font-family:'Playfair Display',Georgia,serif;font-size:27px;font-weight:700;color:#14331e;margin:0 0 18px}
.highlights-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.highlight-item{
  background:#ffffff;border:1px solid var(--line);border-radius:20px;
  overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,0.03);
  transition:all .2s ease;
}
.highlight-item:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(0,0,0,0.08);border-color:#b9ccaf}
.img-wrap{position:relative;width:100%;height:240px;overflow:hidden;background:#e1e9db;cursor:pointer}
.highlight-img{width:100%;height:100%;object-fit:cover;transition:transform .4s ease}
.highlight-item:hover .highlight-img{transform:scale(1.05)}
.img-badge{position:absolute;top:12px;left:12px;background:rgba(20,40,25,0.78);color:#ffffff;font-size:12px;font-weight:600;padding:4px 10px;border-radius:12px;backdrop-filter:blur(4px)}
.highlight-info{padding:20px 22px}
.highlight-title{font-size:17.5px;font-weight:750;color:#183620;margin:0 0 8px}
.highlight-desc{font-size:14.5px;color:#495e4d;line-height:1.6;margin:0}

/* Bottom Grid: Heritage & Links */
.bottom-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-bottom:28px}
.badge-list{display:flex;flex-wrap:wrap;gap:8px}
.badge{background:#eef4e8;border:1px solid #d5e2cc;color:#284831;padding:6px 14px;border-radius:16px;font-size:13.5px;font-weight:600}
.link-list{display:flex;flex-direction:column;gap:10px}
.ref-link{display:flex;align-items:center;justify-content:space-between;background:#f8faf6;border:1px solid #e2ebd9;padding:10px 16px;border-radius:14px;font-size:14.5px;color:#284831;font-weight:600;transition:all .15s}
.ref-link:hover{background:#eaf2e3;border-color:#b3c9a6;transform:translateX(3px)}

/* ================= KAHOOT MINI QUIZ STYLES ================= */
.kahoot-wrapper{
  margin:45px 0 35px;
  width:100%;
}
.kahoot-container{
  background: radial-gradient(circle at 50% 15%, #5c2094 0%, #3e1273 50%, #200642 100%);
  border-radius: 24px;
  box-shadow: 0 25px 60px rgba(32, 6, 66, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.12);
  overflow: hidden;
  position: relative;
  color: #ffffff;
  padding: 24px 28px 36px;
  font-family: 'Be Vietnam Pro', system-ui, -apple-system, sans-serif;
  user-select: none;
  min-height: 560px;
  display: flex;
  flex-direction: column;
}
.kahoot-top-bar{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
}
.kahoot-logo-wrap{
  display: flex;
  align-items: center;
  gap: 12px;
}
.kahoot-brand{
  font-family: 'Arial Black', Impact, sans-serif;
  font-size: 32px;
  font-weight: 900;
  color: #ffffff;
  letter-spacing: -1.5px;
  line-height: 1;
  text-shadow: 0 3px 10px rgba(0,0,0,0.3);
}
.kahoot-brand span{
  color: #ff3355;
  font-size: 36px;
  display: inline-block;
  transform: rotate(8deg);
}
.kahoot-badge-live{
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.25);
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 750;
  letter-spacing: 1px;
  color: #ffd166;
}
.kahoot-controls{
  display: flex;
  align-items: center;
  gap: 10px;
}
.k-ctrl-btn{
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.22);
  color: #ffffff;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  cursor: pointer;
  transition: all .18s ease;
}
.k-ctrl-btn:hover{
  background: rgba(255, 255, 255, 0.26);
  transform: scale(1.06);
}

/* Settings Drawer */
.kahoot-settings-panel{
  background: rgba(28, 8, 56, 0.96);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 16px;
  padding: 16px 20px;
  backdrop-filter: blur(16px);
  position: absolute;
  top: 75px;
  right: 28px;
  z-index: 40;
  min-width: 280px;
  box-shadow: 0 15px 35px rgba(0,0,0,0.45);
}
.k-set-header{
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 700;
  font-size: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  margin-bottom: 12px;
}
.k-set-row{
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  margin-bottom: 10px;
  color: #e0d6f2;
}

/* Screen Layouts */
.kahoot-screen{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  animation: kFadeIn .28s cubic-bezier(.22,.61,.36,1);
}
@keyframes kFadeIn{
  from{opacity:0; transform:scale(0.98);}
  to{opacity:1; transform:scale(1);}
}

/* Glass Start Card (exact match with image) */
.k-glass-card{
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(28px);
  -webkit-backdrop-filter: blur(28px);
  border: 1px solid rgba(255, 255, 255, 0.32);
  border-radius: 22px;
  padding: 28px 36px 34px;
  max-width: 580px;
  width: 100%;
  text-align: center;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.k-card-brand{
  font-family: 'Arial Black', Impact, sans-serif;
  font-size: 34px;
  font-weight: 900;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: -1.5px;
  margin-bottom: 16px;
}
.k-card-brand span{
  color: rgba(255, 255, 255, 0.9);
}
.k-featured-visual{
  position: relative;
  width: 100%;
  max-width: 440px;
  height: 220px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0,0,0,0.3);
  background: #1f0b38;
  margin-bottom: 22px;
}
.k-start-img{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.k-questions-badge{
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(6px);
  color: #ffffff;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13.5px;
  font-weight: 700;
  letter-spacing: 0.5px;
}
.k-start-title{
  font-size: 24px;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 16px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
  line-height: 1.35;
}
.k-mode-chips{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-bottom: 22px;
}
.k-mode-pill{
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: #f1e9ff;
  font-size: 12.5px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 20px;
  cursor: pointer;
  transition: all .16s ease;
}
.k-mode-pill:hover{
  background: rgba(255, 255, 255, 0.28);
}
.k-mode-pill.is-active{
  background: #ffffff;
  color: #3e1273;
  font-weight: 750;
  border-color: #ffffff;
  box-shadow: 0 3px 10px rgba(0,0,0,0.2);
}
.k-start-btn{
  background: #2b2b2b;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 13px 64px;
  font-size: 18px;
  font-weight: 750;
  border-radius: 32px;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(0,0,0,0.4);
  transition: all .2s cubic-bezier(.22,.61,.36,1);
}
.k-start-btn:hover{
  background: #111111;
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 10px 28px rgba(0,0,0,0.5);
}
.k-footer-caption{
  margin-top: 18px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.65);
  text-align: center;
  font-style: italic;
  max-width: 600px;
}

/* Playing Screen HUD */
.k-hud-bar{
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.k-hud-left, .k-hud-right{
  display: flex;
  align-items: center;
  gap: 8px;
}
.k-q-num-pill, .k-score-pill{
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.28);
  padding: 6px 14px;
  border-radius: 18px;
  font-size: 14px;
  font-weight: 750;
}
.k-q-part-pill{
  background: rgba(255, 215, 0, 0.2);
  border: 1px solid rgba(255, 215, 0, 0.4);
  color: #ffe680;
  padding: 6px 12px;
  border-radius: 18px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
}
.k-streak-pill{
  background: linear-gradient(135deg, #ff4d00, #ff8c00);
  color: #fff;
  padding: 6px 12px;
  border-radius: 18px;
  font-size: 13px;
  font-weight: 800;
  box-shadow: 0 2px 8px rgba(255, 77, 0, 0.4);
}
.k-timer-circle{
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.4);
  border: 3px solid #ffbe0b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 800;
  color: #ffffff;
}
.k-timer-circle.is-warning{
  border-color: #ff3355;
  color: #ff3355;
  animation: kPulse .5s infinite;
}
@keyframes kPulse{
  0%, 100%{transform: scale(1);}
  50%{transform: scale(1.15);}
}
.k-timer-bar-wrap{
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 20px;
}
.k-timer-bar-fill{
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #ffbe0b, #ff006e);
  transition: width 1s linear;
}

/* Question Box */
.k-question-box{
  background: #ffffff;
  color: #1a0833;
  width: 100%;
  padding: 24px 30px;
  border-radius: 18px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
  margin-bottom: 24px;
  text-align: center;
}
.k-question-text{
  font-size: 21px;
  font-weight: 750;
  line-height: 1.45;
  margin: 0;
}

/* Answer Blocks Grid (Kahoot Iconic 4 Blocks) */
.k-answers-area{
  width: 100%;
}
.k-grid-4{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  width: 100%;
}
.k-ans-btn{
  border: none;
  border-radius: 14px;
  padding: 20px 22px;
  color: #ffffff;
  font-size: 17px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  text-align: left;
  transition: all .16s cubic-bezier(.22,.61,.36,1);
  box-shadow: 0 6px 0 rgba(0,0,0,0.22), 0 10px 18px rgba(0,0,0,0.18);
  position: relative;
  overflow: hidden;
  min-height: 76px;
}
.k-ans-btn:hover{
  transform: translateY(-3px);
  filter: brightness(1.08);
}
.k-ans-btn:active{
  transform: translateY(3px);
  box-shadow: 0 2px 0 rgba(0,0,0,0.22);
}
.k-shape-icon{
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}
.k-btn-red{ background: #e21b3c; }
.k-btn-blue{ background: #1368ce; }
.k-btn-yellow{ background: #d89e00; }
.k-btn-green{ background: #26890c; }

/* True/False Grid */
.k-grid-tf{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
  width: 100%;
}
.k-tf-btn{
  min-height: 100px;
  font-size: 22px;
  justify-content: center;
}

/* Fill Input Form */
.k-fill-wrap{
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(16px);
  border-radius: 16px;
  padding: 20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.k-input-row{
  display: flex;
  gap: 10px;
}
.k-fill-input{
  flex: 1;
  padding: 14px 18px;
  border-radius: 12px;
  border: 2px solid rgba(255, 255, 255, 0.35);
  background: #ffffff;
  color: #1f0b38;
  font-size: 17px;
  font-weight: 600;
  outline: none;
}
.k-fill-submit{
  background: #26890c;
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 14px 28px;
  font-size: 16.5px;
  font-weight: 750;
  cursor: pointer;
}
.k-fill-hint{
  font-size: 13px;
  color: #e0d5f2;
}

/* Matching UI */
.k-match-wrap{
  background: rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  padding: 18px;
  width: 100%;
}
.k-match-grid{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}
.k-match-col{
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.k-match-item{
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 12px 14px;
  border-radius: 10px;
  font-size: 14.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all .16s;
  text-align: left;
}
.k-match-item:hover{
  background: rgba(255, 255, 255, 0.32);
}
.k-match-item.is-selected{
  background: #ffbe0b;
  color: #1f0b38;
  border-color: #ffffff;
  transform: scale(1.02);
}
.k-match-item.is-matched{
  background: #26890c;
  color: #ffffff;
  border-color: #80e66b;
  pointer-events: none;
  opacity: 0.85;
}

/* Feedback Overlay Screen */
.k-feedback-card{
  background: rgba(255, 255, 255, 0.96);
  color: #1a0833;
  border-radius: 24px;
  padding: 34px 40px;
  max-width: 540px;
  width: 100%;
  text-align: center;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4);
  animation: kPopIn .24s ease;
}
@keyframes kPopIn{
  0%{transform: scale(0.9); opacity:0;}
  100%{transform: scale(1); opacity:1;}
}
.k-feedback-card.is-correct{ border-top: 8px solid #26890c; }
.k-feedback-card.is-wrong{ border-top: 8px solid #e21b3c; }
.k-fb-icon{ font-size: 52px; margin-bottom: 8px; }
.k-fb-title{ font-size: 26px; font-weight: 850; margin: 0 0 10px; }
.is-correct .k-fb-title{ color: #26890c; }
.is-wrong .k-fb-title{ color: #e21b3c; }
.k-fb-points{ font-size: 20px; font-weight: 800; color: #1368ce; margin-bottom: 6px; }
.k-fb-streak{ font-size: 14px; font-weight: 700; color: #e65100; margin-bottom: 14px; }
.k-fb-explain{
  font-size: 15px;
  line-height: 1.5;
  color: #443355;
  background: #f4effa;
  padding: 14px 18px;
  border-radius: 12px;
  margin-bottom: 22px;
  text-align: left;
}
.k-next-btn{
  background: #3e1273;
  color: #ffffff;
  border: none;
  padding: 13px 45px;
  border-radius: 28px;
  font-size: 17px;
  font-weight: 750;
  cursor: pointer;
  transition: all .16s ease;
}
.k-next-btn:hover{
  background: #250747;
  transform: translateY(-2px);
}

/* Finish Podium Card */
.k-podium-card{
  background: rgba(255, 255, 255, 0.96);
  color: #1a0833;
  border-radius: 24px;
  padding: 36px 40px;
  max-width: 580px;
  width: 100%;
  text-align: center;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4);
}
.k-podium-trophy{ font-size: 64px; margin-bottom: 8px; }
.k-finish-heading{ font-size: 24px; font-weight: 850; color: #3e1273; margin: 0 0 16px; }
.k-final-score-box{
  background: #f3ecfb;
  border-radius: 16px;
  padding: 14px;
  margin-bottom: 20px;
}
.k-score-label{ font-size: 12px; font-weight: 750; letter-spacing: 1.5px; color: #7240a6; display: block; margin-bottom: 4px; }
.k-final-score-val{ font-size: 38px; font-weight: 900; color: #3e1273; }
.k-final-stats{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}
.k-stat-item{
  background: #faf7fd;
  border: 1px solid #e7dcf5;
  border-radius: 12px;
  padding: 10px;
}
.k-stat-sub{ font-size: 12px; color: #6b5c7e; display: block; margin-bottom: 4px; }
.k-stat-big{ font-size: 19px; font-weight: 800; color: #200642; }
.k-rank-badge{
  display: inline-block;
  background: #fff3cd;
  border: 1px solid #ffeeba;
  color: #856404;
  padding: 8px 18px;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 750;
  margin-bottom: 24px;
}
.k-finish-actions{
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.k-action-btn{
  border: none;
  border-radius: 28px;
  padding: 12px 24px;
  font-size: 15.5px;
  font-weight: 750;
  cursor: pointer;
  transition: all .16s ease;
}
.k-action-btn.primary{ background: #3e1273; color: #fff; }
.k-action-btn.secondary{ background: #1368ce; color: #fff; }
.k-action-btn.tertiary{ background: #e9e2f5; color: #3e1273; }
.k-action-btn:hover{ transform: translateY(-2px); filter: brightness(1.08); }

/* Review Panel */
.k-review-panel{
  background: #ffffff;
  color: #1a0833;
  border-radius: 20px;
  padding: 24px;
  margin-top: 20px;
  text-align: left;
  max-width: 600px;
  width: 100%;
  max-height: 380px;
  overflow-y: auto;
  box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}
.k-review-header{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0d5ec;
  padding-bottom: 10px;
  margin-bottom: 14px;
}
.k-review-item{
  font-size: 13.5px;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px dashed #e9e1f2;
}

/* Responsive */
@media(max-width:1024px){
  .hero{grid-template-columns:1fr;padding:26px}
  .hero-visual{order:-1;padding:18px}
  .stats-grid{grid-template-columns:repeat(2,1fr)}
  .section-grid,.highlights-grid,.bottom-grid{grid-template-columns:1fr}
}
@media(max-width:768px){
  .kahoot-container{ padding: 18px 16px 26px; min-height: 520px; }
  .k-glass-card{ padding: 22px 18px 26px; }
  .k-featured-visual{ height: 170px; }
  .k-start-title{ font-size: 20px; }
  .k-grid-4{ grid-template-columns: 1fr; }
  .k-grid-tf{ grid-template-columns: 1fr; }
  .k-ans-btn{ min-height: 62px; padding: 14px 16px; font-size: 15.5px; }
  .k-question-text{ font-size: 17.5px; }
}
@media(max-width:600px){
  .stats-grid{grid-template-columns:1fr}
  .page-wrap{padding:20px 4% 40px}
  .hero-name{font-size:32px}
  .stat-val{font-size:23px}
  .img-wrap{height:200px}
}

/* Page Navigator Buttons */
.page-nav-btns{display:flex;align-items:center;justify-content:space-between;margin-top:20px;padding-top:24px;border-top:1px solid var(--line)}
.nav-link-btn{
  background:#ffffff;border:1px solid var(--line);border-radius:24px;
  padding:10px 22px;font-size:15px;font-weight:600;color:#284330;
  transition:all .18s ease;box-shadow:0 2px 8px rgba(0,0,0,0.03);
}
.nav-link-btn:hover{background:#e7efe0;border-color:#b9ccaf;transform:translateY(-2px)}

/* Lightbox Modal */
.modal{position:fixed;inset:0;background:rgba(15,25,18,0.88);backdrop-filter:blur(10px);z-index:999;display:none;align-items:center;justify-content:center;padding:20px}
.modal.is-open{display:flex}
.modal-content{position:relative;max-width:90vw;max-height:90vh;display:flex;flex-direction:column;align-items:center}
.modal-img{max-width:100%;max-height:80vh;border-radius:14px;box-shadow:0 12px 40px rgba(0,0,0,0.5)}
.modal-caption{color:#ffffff;font-size:16px;margin-top:12px;text-align:center;font-weight:500}
.modal-close{position:absolute;top:-40px;right:0;background:none;border:none;color:#ffffff;font-size:30px;cursor:pointer}
</style>
</head>
<body>

<header class="top-nav">
  <a href="./index.html" class="back-btn" title="Trở về bản đồ tương tác Việt Nam">
    <span>←</span>
    <span>Trở về bản đồ</span>
  </a>
  <div class="top-title">Hồ sơ địa phương — 34 Tỉnh thành</div>
  <div class="top-badge">
    <span class="top-dot" id="top-dot"></span>
    <span id="top-region-text">Vùng kinh tế</span>
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

  <!-- KAHOOT MINI QUIZ SECTION (Underneath Province Details) -->
  <section class="kahoot-wrapper" id="kahoot-quiz-section">
    <div class="kahoot-container" id="kahoot-container">
      
      <!-- Top Bar -->
      <div class="kahoot-top-bar">
        <div class="kahoot-logo-wrap">
          <span class="kahoot-brand">Kahoot<span>!</span></span>
          <span class="kahoot-badge-live">LIVE QUIZ</span>
        </div>
        <div class="kahoot-controls">
          <button type="button" class="k-ctrl-btn" id="k-sound-btn" title="Bật/Tắt âm thanh" aria-label="Âm thanh">🔊</button>
          <button type="button" class="k-ctrl-btn" id="k-settings-btn" title="Cài đặt trò chơi" aria-label="Cài đặt">⚙️</button>
        </div>
      </div>

      <!-- Settings Dropdown -->
      <div class="kahoot-settings-panel" id="k-settings-panel" style="display:none;">
        <div class="k-set-header">
          <span>⚙️ Cài đặt Thử Thách</span>
          <button type="button" id="k-set-close" style="background:none;border:none;color:#fff;font-size:16px;">✕</button>
        </div>
        <div class="k-set-row">
          <label for="k-timer-toggle">Đếm ngược 20 giây:</label>
          <input type="checkbox" id="k-timer-toggle" checked>
        </div>
        <div class="k-set-row">
          <label for="k-sound-toggle">Âm thanh Web Audio:</label>
          <input type="checkbox" id="k-sound-toggle" checked>
        </div>
      </div>

      <!-- VIEW 1: START SCREEN (matches user photo) -->
      <div class="kahoot-screen" id="k-screen-start">
        <div class="k-glass-card">
          <div class="k-card-brand">Kahoot<span>!</span></div>
          
          <div class="k-featured-visual">
            <img id="k-start-img" class="k-start-img" src="" alt="Hình ảnh thử thách">
            <span class="k-questions-badge" id="k-questions-badge">5 Questions</span>
          </div>

          <h3 class="k-start-title" id="k-start-title">Khám Phá Bảo Tàng Đà Nẵng</h3>

          <!-- Mode selector chips -->
          <div class="k-mode-chips">
            <button type="button" class="k-mode-pill is-active" data-mode="province" id="k-mode-province">
              🎯 Thử thách tỉnh này (5 câu)
            </button>
            <button type="button" class="k-mode-pill" data-mode="random">
              🎲 5 câu ngẫu nhiên
            </button>
            <button type="button" class="k-mode-pill" data-mode="all">
              🏆 Bộ 40 câu trọn vẹn
            </button>
          </div>

          <button type="button" class="k-start-btn" id="k-start-btn">
            Start
          </button>
        </div>

        <div class="k-footer-caption" id="k-footer-caption">
          Dự án: "Bản đồ số tương tác 34 tỉnh, thành phố và 2 quần đảo Hoàng Sa – Trường Sa"
        </div>
      </div>

      <!-- VIEW 2: QUESTION SCREEN -->
      <div class="kahoot-screen" id="k-screen-question" style="display:none;">
        <div class="k-hud-bar">
          <div class="k-hud-left">
            <span class="k-q-num-pill" id="k-hud-counter">1 of 5</span>
            <span class="k-q-part-pill" id="k-hud-part">TRẮC NGHIỆM</span>
          </div>
          <div class="k-hud-center">
            <div class="k-timer-circle" id="k-timer-circle">20</div>
          </div>
          <div class="k-hud-right">
            <span class="k-score-pill" id="k-hud-score">0 pts</span>
            <span class="k-streak-pill" id="k-hud-streak" style="display:none;">🔥 0</span>
          </div>
        </div>

        <div class="k-timer-bar-wrap">
          <div class="k-timer-bar-fill" id="k-timer-bar-fill"></div>
        </div>

        <div class="k-question-box">
          <h2 class="k-question-text" id="k-question-text">Câu hỏi đang tải...</h2>
        </div>

        <div class="k-answers-area" id="k-answers-area"></div>
      </div>

      <!-- VIEW 3: FEEDBACK SCREEN (Instant Correct / Incorrect) -->
      <div class="kahoot-screen" id="k-screen-feedback" style="display:none;">
        <div class="k-feedback-card" id="k-feedback-card">
          <div class="k-fb-icon" id="k-fb-icon">🎉</div>
          <h2 class="k-fb-title" id="k-fb-title">CHÍNH XÁC!</h2>
          <div class="k-fb-points" id="k-fb-points">+1,000 pts</div>
          <div class="k-fb-streak" id="k-fb-streak" style="display:none;">🔥 Chuỗi trả lời đúng x2!</div>
          <div class="k-fb-explain" id="k-fb-explain">Giải thích chi tiết...</div>
          <button type="button" class="k-next-btn" id="k-next-btn">Tiếp theo ➔</button>
        </div>
      </div>

      <!-- VIEW 4: FINISH / PODIUM SCREEN -->
      <div class="kahoot-screen" id="k-screen-finish" style="display:none;">
        <div class="k-podium-card">
          <div class="k-podium-trophy">🏆</div>
          <h2 class="k-finish-heading">XUẤT SẮC HOÀN THÀNH!</h2>
          <div class="k-final-score-box">
            <span class="k-score-label">TỔNG ĐIỂM</span>
            <span class="k-final-score-val" id="k-final-score-val">5,000</span>
          </div>
          <div class="k-final-stats">
            <div class="k-stat-item">
              <span class="k-stat-sub">Độ chính xác</span>
              <span class="k-stat-big" id="k-stat-accuracy">100%</span>
            </div>
            <div class="k-stat-item">
              <span class="k-stat-sub">Số câu đúng</span>
              <span class="k-stat-big" id="k-stat-correct">5 / 5</span>
            </div>
            <div class="k-stat-item">
              <span class="k-stat-sub">Chuỗi cao nhất</span>
              <span class="k-stat-big" id="k-stat-max-streak">🔥 5</span>
            </div>
          </div>
          <div class="k-rank-badge" id="k-rank-badge">🥇 Bậc Thầy Địa Lý Việt Nam</div>

          <div class="k-finish-actions">
            <button type="button" class="k-action-btn primary" id="k-btn-replay">Chơi lại vòng này 🔄</button>
            <button type="button" class="k-action-btn secondary" id="k-btn-play-all">Chinh phục 40 câu trọn vẹn 🌟</button>
            <button type="button" class="k-action-btn tertiary" id="k-btn-review">Xem lại bảng đáp án 📋</button>
          </div>
        </div>

        <div class="k-review-panel" id="k-review-panel" style="display:none;">
          <div class="k-review-header">
            <h4 style="margin:0;font-size:16px;">Bảng đáp án chi tiết 40 câu hỏi</h4>
            <button type="button" id="k-review-close" style="background:none;border:none;font-size:16px;cursor:pointer;">✕</button>
          </div>
          <div class="k-review-list" id="k-review-list"></div>
        </div>
      </div>

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
const QUIZ_BANK = /* QUIZ_QUESTIONS_DATA */;

const REGIONS_LIST = [
  {id: 'all', name: 'Tất cả 36 địa phương & quần đảo'},
  {id: 'vung-1', name: 'Trung Du & MN Bắc Bộ (9)'},
  {id: 'vung-2', name: 'Đồng bằng sông Hồng (6)'},
  {id: 'vung-3', name: 'Bắc Trung Bộ (5)'},
  {id: 'vung-4', name: 'Nam Trung Bộ, Tây Nguyên & Biển Đảo (8)'},
  {id: 'vung-5', name: 'Đông Nam Bộ (3)'},
  {id: 'vung-6', name: 'Đồng bằng sông Cửu Long (5)'}
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
  return 17; // Default: Đà Nẵng
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
  document.getElementById('silhouette-img').alt = 'Bản đồ đường viền ' + p.name;
  document.getElementById('hero-id-tag').textContent = (p.id >= 35) ? `QUẦN ĐẢO THIÊNG LIÊNG #${String(p.id).padStart(2,'0')}` : `TỈNH THÀNH #${String(p.id).padStart(2,'0')}`;

  // Key stats
  const statsGrid = document.getElementById('stats-grid');
  statsGrid.replaceChildren();
  const stats = [
    {label: 'Trung tâm hành chính', val: p.capital, sub: 'Đô thị hạt nhân'},
    {label: 'Diện tích tự nhiên', val: p.area, sub: 'Quy mô địa lý'},
    {label: 'Dân số', val: p.population, sub: 'Số liệu thống kê'},
    {label: 'Số đơn vị cấp huyện', val: p.districts, sub: 'Quận, huyện, thị xã'}
  ];
  stats.forEach(s => {
    const el = document.createElement('div');
    el.className = 'stat-card';
    el.innerHTML = `<div class="stat-label">${s.label}</div><div class="stat-val">${s.val}</div><div class="stat-sub">${s.sub}</div>`;
    statsGrid.append(el);
  });

  // Section cards
  const sectionGrid = document.getElementById('section-grid');
  sectionGrid.replaceChildren();
  const cards = [
    {icon: '🧭', title: 'Vị trí địa lý & Địa hình', body: p.geo_body},
    {icon: '📜', title: 'Căn cứ lịch sử & Pháp lý', body: p.history_body},
    {icon: '🛡️', title: 'Quốc phòng & An ninh biển', body: p.defense_body},
    {icon: '🌊', title: 'Tiềm năng kinh tế biển & Phát triển', body: p.economy_body}
  ];
  cards.forEach(c => {
    const el = document.createElement('div');
    el.className = 'card';
    el.innerHTML = `
      <div class="card-header">
        <div class="card-icon">${c.icon}</div>
        <h3 class="card-title">${c.title}</h3>
      </div>
      <div class="card-body">${c.body}</div>
    `;
    sectionGrid.append(el);
  });

  // Highlights & Real Photo Gallery
  const hlGrid = document.getElementById('highlights-grid');
  hlGrid.replaceChildren();
  if (p.highlights && p.highlights.length) {
    p.highlights.forEach(h => {
      const el = document.createElement('div');
      el.className = 'highlight-item';
      el.innerHTML = `
        <div class="img-wrap" onclick="openModal('${h.image}', '${h.title.replace(/'/g, "\\'")}')">
          <img class="highlight-img" src="${h.image}" alt="${h.title}" loading="lazy">
          <span class="img-badge">Ảnh thực tế 🔍</span>
        </div>
        <div class="highlight-info">
          <h3 class="highlight-title">${h.title}</h3>
          <p class="highlight-desc">${h.desc}</p>
        </div>
      `;
      hlGrid.append(el);
    });
  }

  // Heritage list
  const heritageList = document.getElementById('heritage-list');
  heritageList.replaceChildren();
  (p.heritage || []).forEach(item => {
    const span = document.createElement('span');
    span.className = 'badge';
    span.textContent = item;
    heritageList.append(span);
  });

  // Reference links
  const linksList = document.getElementById('links-list');
  linksList.replaceChildren();
  (p.links || []).forEach(lnk => {
    const a = document.createElement('a');
    a.className = 'ref-link';
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

  // Update Kahoot game for current province
  initKahootForProvince(p);
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

/* ====================================================================
   KAHOOT MINI-QUIZ GAME LOGIC (100% Client-Side with Web Audio Synth)
==================================================================== */
let currentProvinceObj = null;
let quizMode = 'province'; // 'province' | 'random' | 'all'
let quizQuestions = [];
let currentIndex = 0;
let userScore = 0;
let currentStreak = 0;
let maxStreak = 0;
let correctCount = 0;
let timerSeconds = 20;
let timerInterval = null;
let timeRemaining = 20;
let hasAnswered = false;
let audioCtx = null;
let soundEnabled = true;
let timerEnabled = true;

// Web Audio API Sound Effects
function initAudio() {
  if (!audioCtx) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (AudioContext) audioCtx = new AudioContext();
  }
  if (audioCtx && audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
}

function playSound(type) {
  if (!soundEnabled) return;
  try {
    initAudio();
    if (!audioCtx) return;
    const now = audioCtx.currentTime;

    if (type === 'tick') {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(800, now);
      gain.gain.setValueAtTime(0.04, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.04);
    } else if (type === 'correct') {
      [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, now + i * 0.07);
        gain.gain.setValueAtTime(0.12, now + i * 0.07);
        gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.07 + 0.32);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now + i * 0.07);
        osc.stop(now + i * 0.07 + 0.32);
      });
    } else if (type === 'wrong') {
      [310, 240].forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(freq, now + i * 0.1);
        gain.gain.setValueAtTime(0.09, now + i * 0.1);
        gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.1 + 0.22);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now + i * 0.1);
        osc.stop(now + i * 0.1 + 0.22);
      });
    } else if (type === 'fanfare') {
      [523.25, 659.25, 783.99, 1046.50, 1318.51].forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now + i * 0.1);
        gain.gain.setValueAtTime(0.14, now + i * 0.1);
        gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.1 + 0.5);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now + i * 0.1);
        osc.stop(now + i * 0.1 + 0.5);
      });
    }
  } catch(e) {}
}

// Controls: Sound toggle & Settings
document.getElementById('k-sound-btn').addEventListener('click', () => {
  soundEnabled = !soundEnabled;
  document.getElementById('k-sound-btn').textContent = soundEnabled ? '🔊' : '🔇';
  document.getElementById('k-sound-toggle').checked = soundEnabled;
});
document.getElementById('k-sound-toggle').addEventListener('change', e => {
  soundEnabled = e.target.checked;
  document.getElementById('k-sound-btn').textContent = soundEnabled ? '🔊' : '🔇';
});
document.getElementById('k-timer-toggle').addEventListener('change', e => {
  timerEnabled = e.target.checked;
});

const settingsPanel = document.getElementById('k-settings-panel');
document.getElementById('k-settings-btn').addEventListener('click', () => {
  settingsPanel.style.display = settingsPanel.style.display === 'none' ? 'block' : 'none';
});
document.getElementById('k-set-close').addEventListener('click', () => {
  settingsPanel.style.display = 'none';
});

// Mode Pills on Start Screen
document.querySelectorAll('.k-mode-pill').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.k-mode-pill').forEach(b => b.classList.remove('is-active'));
    btn.classList.add('is-active');
    quizMode = btn.dataset.mode;
    updateQuestionCountBadge();
  });
});

function updateQuestionCountBadge() {
  const badge = document.getElementById('k-questions-badge');
  if (quizMode === 'all') {
    badge.textContent = `${QUIZ_BANK.length} Questions`;
  } else {
    badge.textContent = `5 Questions`;
  }
}

// Initialize Kahoot Start Card for Current Province
function initKahootForProvince(p) {
  currentProvinceObj = p;
  
  // Set Featured Visual from province highlights or silhouette
  const startImg = document.getElementById('k-start-img');
  if (p.highlights && p.highlights.length && p.highlights[0].image) {
    startImg.src = p.highlights[0].image;
  } else {
    startImg.src = p.silhouette;
  }

  // Set Title matching user's screenshot
  const startTitle = document.getElementById('k-start-title');
  if (p.id === 17) {
    startTitle.textContent = 'Khám Phá Bảo Tàng Đà Nẵng';
  } else {
    startTitle.textContent = `Khám Phá ${p.name}`;
  }

  document.getElementById('k-mode-province').textContent = `🎯 Thử thách ${p.short} (5 câu)`;
  updateQuestionCountBadge();

  // Reset to Start Screen
  showScreen('start');
}

function showScreen(name) {
  document.getElementById('k-screen-start').style.display = (name === 'start') ? 'flex' : 'none';
  document.getElementById('k-screen-question').style.display = (name === 'question') ? 'flex' : 'none';
  document.getElementById('k-screen-feedback').style.display = (name === 'feedback') ? 'flex' : 'none';
  document.getElementById('k-screen-finish').style.display = (name === 'finish') ? 'flex' : 'none';
}

// Prepare Question Pool
function prepareQuestions() {
  if (quizMode === 'all') {
    // Return all 40 questions in order
    return [...QUIZ_BANK];
  } else if (quizMode === 'random') {
    // 5 random questions
    const shuffled = [...QUIZ_BANK].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, 5);
  } else {
    // Province specific: prioritize current province, current region, then pad to 5
    const pid = currentProvinceObj ? currentProvinceObj.id : 17;
    const regId = currentProvinceObj ? currentProvinceObj.regionId : 'vung-4';
    
    // Direct province match
    const direct = QUIZ_BANK.filter(q => q.provinces && (q.provinces.includes(pid) || (q.provinces.includes(regId))));
    // Region or general match
    const others = QUIZ_BANK.filter(q => !direct.includes(q)).sort(() => 0.5 - Math.random());
    
    const combined = [...direct, ...others];
    return combined.slice(0, 5);
  }
}

// Start Game
document.getElementById('k-start-btn').addEventListener('click', () => {
  initAudio();
  quizQuestions = prepareQuestions();
  currentIndex = 0;
  userScore = 0;
  currentStreak = 0;
  maxStreak = 0;
  correctCount = 0;
  renderQuestion(currentIndex);
});

// Render a Question
function renderQuestion(index) {
  hasAnswered = false;
  if (index >= quizQuestions.length) {
    finishGame();
    return;
  }
  
  const q = quizQuestions[index];
  showScreen('question');

  // Update HUD
  document.getElementById('k-hud-counter').textContent = `${index + 1} of ${quizQuestions.length}`;
  document.getElementById('k-hud-part').textContent = q.part.replace(/PHẦN [I|V|X]+.\s*/, '');
  document.getElementById('k-hud-score').textContent = `${userScore.toLocaleString()} pts`;
  
  const streakPill = document.getElementById('k-hud-streak');
  if (currentStreak >= 2) {
    streakPill.style.display = 'inline-block';
    streakPill.textContent = `🔥 x${currentStreak}`;
  } else {
    streakPill.style.display = 'none';
  }

  // Question Text
  document.getElementById('k-question-text').textContent = q.question;

  // Answers Area
  const answersArea = document.getElementById('k-answers-area');
  answersArea.replaceChildren();

  if (q.type === 'tf') {
    // True / False: 2 blocks (Blue: Đúng, Red: Sai)
    const grid = document.createElement('div');
    grid.className = 'k-grid-tf';
    
    const btnTrue = document.createElement('button');
    btnTrue.type = 'button';
    btnTrue.className = 'k-ans-btn k-tf-btn k-btn-blue';
    btnTrue.innerHTML = `<span class="k-shape-icon">◆</span><span>ĐÚNG</span>`;
    btnTrue.onclick = () => submitAnswer('Đúng');

    const btnFalse = document.createElement('button');
    btnFalse.type = 'button';
    btnFalse.className = 'k-ans-btn k-tf-btn k-btn-red';
    btnFalse.innerHTML = `<span class="k-shape-icon">▲</span><span>SAI</span>`;
    btnFalse.onclick = () => submitAnswer('Sai');

    grid.append(btnTrue, btnFalse);
    answersArea.append(grid);

  } else if (q.type === 'fill') {
    // Fill in the blank: Input box + 4 quick-select Kahoot pills
    const wrap = document.createElement('div');
    wrap.className = 'k-fill-wrap';
    
    wrap.innerHTML = `
      <div class="k-input-row">
        <input type="text" class="k-fill-input" id="k-fill-input-field" placeholder="Nhập từ hoặc cụm từ thích hợp..." autocomplete="off">
        <button type="button" class="k-fill-submit" id="k-fill-submit-btn">Trả lời</button>
      </div>
      <div class="k-fill-hint">Hoặc chọn nhanh một trong 4 phương án dưới đây:</div>
    `;
    
    const grid = document.createElement('div');
    grid.className = 'k-grid-4';
    const classes = ['k-btn-red', 'k-btn-blue', 'k-btn-yellow', 'k-btn-green'];
    const shapes = ['▲', '◆', '●', '■'];
    
    q.options.forEach((opt, idx) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `k-ans-btn ${classes[idx % 4]}`;
      btn.innerHTML = `<span class="k-shape-icon">${shapes[idx % 4]}</span><span>${opt.text}</span>`;
      btn.onclick = () => submitAnswer(opt.text);
      grid.append(btn);
    });

    wrap.append(grid);
    answersArea.append(wrap);

    const inputField = wrap.querySelector('#k-fill-input-field');
    const submitBtn = wrap.querySelector('#k-fill-submit-btn');
    submitBtn.onclick = () => {
      if (inputField.value.trim()) submitAnswer(inputField.value.trim());
    };
    inputField.onkeydown = e => {
      if (e.key === 'Enter' && inputField.value.trim()) submitAnswer(inputField.value.trim());
    };

  } else if (q.type === 'match') {
    // Matching pairs / Column matching
    const wrap = document.createElement('div');
    wrap.className = 'k-match-wrap';

    const grid = document.createElement('div');
    grid.className = 'k-grid-4';
    const classes = ['k-btn-red', 'k-btn-blue', 'k-btn-yellow', 'k-btn-green'];
    const shapes = ['▲', '◆', '●', '■'];

    q.options.forEach((opt, idx) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `k-ans-btn ${classes[idx % 4]}`;
      btn.innerHTML = `<span class="k-shape-icon">${shapes[idx % 4]}</span><span><strong>${opt.id}.</strong> ${opt.text}</span>`;
      btn.onclick = () => submitAnswer(opt.id);
      grid.append(btn);
    });

    wrap.innerHTML = `<div style="margin-bottom:12px;font-size:14px;color:#f3e8ff;">Gợi ý cột ghép: <em>${q.answer_summary || ''}</em></div>`;
    wrap.append(grid);
    answersArea.append(wrap);

  } else {
    // Default 4 Kahoot Blocks (mc, guess, color)
    const grid = document.createElement('div');
    grid.className = 'k-grid-4';
    const classes = ['k-btn-red', 'k-btn-blue', 'k-btn-yellow', 'k-btn-green'];
    const shapes = ['▲', '◆', '●', '■'];

    q.options.forEach((opt, idx) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `k-ans-btn ${classes[idx % 4]}`;
      const colorDot = opt.color ? `<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:${opt.color};margin-right:6px;border:2px solid #fff;"></span>` : '';
      btn.innerHTML = `<span class="k-shape-icon">${shapes[idx % 4]}</span><span>${colorDot}${opt.text}</span>`;
      btn.onclick = () => submitAnswer(opt.id);
      grid.append(btn);
    });

    answersArea.append(grid);
  }

  // Timer Setup
  startTimer();
}

function startTimer() {
  clearInterval(timerInterval);
  timeRemaining = 20;
  const circle = document.getElementById('k-timer-circle');
  const bar = document.getElementById('k-timer-bar-fill');
  circle.textContent = timeRemaining;
  circle.classList.remove('is-warning');
  bar.style.width = '100%';

  if (!timerEnabled) {
    circle.textContent = '∞';
    return;
  }

  timerInterval = setInterval(() => {
    timeRemaining--;
    circle.textContent = timeRemaining;
    bar.style.width = `${(timeRemaining / 20) * 100}%`;

    if (timeRemaining <= 5) {
      circle.classList.add('is-warning');
      playSound('tick');
    }

    if (timeRemaining <= 0) {
      clearInterval(timerInterval);
      handleTimeout();
    }
  }, 1000);
}

function handleTimeout() {
  if (hasAnswered) return;
  hasAnswered = true;
  playSound('wrong');
  currentStreak = 0;
  showFeedback(false, "Hết thời gian!", quizQuestions[currentIndex].explain);
}

function submitAnswer(userChoice) {
  if (hasAnswered) return;
  hasAnswered = true;
  clearInterval(timerInterval);

  const q = quizQuestions[currentIndex];
  let isCorrect = false;

  if (q.type === 'fill') {
    const normUser = userChoice.trim().toLowerCase();
    const normAns = q.answer.trim().toLowerCase();
    const accepted = (q.accepted_answers || []).map(a => a.toLowerCase());
    isCorrect = (normUser === normAns) || accepted.includes(normUser);
  } else if (q.type === 'tf') {
    isCorrect = (userChoice.toLowerCase() === q.answer.toLowerCase());
  } else {
    isCorrect = (userChoice === q.answer);
  }

  if (isCorrect) {
    correctCount++;
    currentStreak++;
    if (currentStreak > maxStreak) maxStreak = currentStreak;
    const timeBonus = Math.max(100, timeRemaining * 40);
    const streakBonus = currentStreak >= 2 ? (currentStreak * 100) : 0;
    const pts = 1000 + timeBonus + streakBonus;
    userScore += pts;
    playSound('correct');
    showFeedback(true, `+${pts.toLocaleString()} pts`, q.explain);
  } else {
    currentStreak = 0;
    playSound('wrong');
    showFeedback(false, "+0 pts", q.explain);
  }
}

function showFeedback(isCorrect, pointsText, explainText) {
  showScreen('feedback');
  const card = document.getElementById('k-feedback-card');
  const title = document.getElementById('k-fb-title');
  const icon = document.getElementById('k-fb-icon');
  const pts = document.getElementById('k-fb-points');
  const streakEl = document.getElementById('k-fb-streak');
  const explain = document.getElementById('k-fb-explain');

  if (isCorrect) {
    card.className = 'k-feedback-card is-correct';
    icon.textContent = '🎉';
    title.textContent = 'CHÍNH XÁC!';
    pts.textContent = pointsText;
    pts.style.color = '#26890c';
    if (currentStreak >= 2) {
      streakEl.style.display = 'block';
      streakEl.textContent = `🔥 Chuỗi trả lời đúng x${currentStreak}!`;
    } else {
      streakEl.style.display = 'none';
    }
  } else {
    card.className = 'k-feedback-card is-wrong';
    icon.textContent = '❌';
    title.textContent = 'CHƯA CHÍNH XÁC';
    pts.textContent = '+0 pts';
    pts.style.color = '#e21b3c';
    streakEl.style.display = 'none';
  }

  explain.textContent = explainText || '';
}

document.getElementById('k-next-btn').addEventListener('click', () => {
  currentIndex++;
  renderQuestion(currentIndex);
});

// Finish Game Screen
function finishGame() {
  clearInterval(timerInterval);
  showScreen('finish');
  playSound('fanfare');

  const total = quizQuestions.length;
  const pct = Math.round((correctCount / total) * 100);

  document.getElementById('k-final-score-val').textContent = userScore.toLocaleString();
  document.getElementById('k-stat-accuracy').textContent = `${pct}%`;
  document.getElementById('k-stat-correct').textContent = `${correctCount} / ${total}`;
  document.getElementById('k-stat-max-streak').textContent = `🔥 ${maxStreak}`;

  const badge = document.getElementById('k-rank-badge');
  if (pct === 100) {
    badge.textContent = '🥇 Bậc Thầy Địa Lý Việt Nam (Tuyệt đối!)';
  } else if (pct >= 80) {
    badge.textContent = '🥈 Chuyên Gia Bản Đồ 34 Tỉnh Thành';
  } else if (pct >= 60) {
    badge.textContent = '🥉 Nhà Khám Phá Địa Phương Tích Cực';
  } else {
    badge.textContent = '💪 Khởi Động Tốt! Thử Lại Để Nâng Cao Điểm Số!';
  }
}

// Actions on Finish Screen
document.getElementById('k-btn-replay').addEventListener('click', () => {
  initAudio();
  quizQuestions = prepareQuestions();
  currentIndex = 0;
  userScore = 0;
  currentStreak = 0;
  maxStreak = 0;
  correctCount = 0;
  renderQuestion(0);
});

document.getElementById('k-btn-play-all').addEventListener('click', () => {
  initAudio();
  quizMode = 'all';
  document.querySelectorAll('.k-mode-pill').forEach(b => b.classList.remove('is-active'));
  document.querySelector('.k-mode-pill[data-mode="all"]').classList.add('is-active');
  updateQuestionCountBadge();
  quizQuestions = prepareQuestions();
  currentIndex = 0;
  userScore = 0;
  currentStreak = 0;
  maxStreak = 0;
  correctCount = 0;
  renderQuestion(0);
});

// Review Answers Panel
const reviewPanel = document.getElementById('k-review-panel');
document.getElementById('k-btn-review').addEventListener('click', () => {
  reviewPanel.style.display = 'block';
  const list = document.getElementById('k-review-list');
  list.replaceChildren();

  QUIZ_BANK.forEach(q => {
    const item = document.createElement('div');
    item.className = 'k-review-item';
    let ansTxt = q.answer;
    if (q.type === 'mc' || q.type === 'guess' || q.type === 'color' || q.type === 'match') {
      const found = q.options.find(o => o.id === q.answer);
      if (found) ansTxt = `${q.answer}. ${found.text}`;
    }
    item.innerHTML = `
      <div><strong>Câu ${q.id} (${q.part}):</strong> ${q.question}</div>
      <div style="color:#26890c;margin-top:4px;"><strong>✓ Đáp án:</strong> ${ansTxt}</div>
      <div style="color:#666;font-size:12.5px;margin-top:2px;">${q.explain}</div>
    `;
    list.append(item);
  });

  reviewPanel.scrollIntoView({behavior: 'smooth'});
});
document.getElementById('k-review-close').addEventListener('click', () => {
  reviewPanel.style.display = 'none';
});

// Initial render
renderPage(currentId);
</script>
</body>
</html>
'''

# Output substitution
output = template.replace('/* PROVINCE_DETAIL_DATA */', json.dumps(detail_data, ensure_ascii=False))
quiz_data = (ROOT / 'data' / 'quiz_questions.json').read_text(encoding='utf-8')
output = output.replace('/* QUIZ_QUESTIONS_DATA */', quiz_data)

(ROOT / 'province.html').write_text(output, encoding='utf-8')
(ROOT / 'dist' / 'province.html').write_text(output, encoding='utf-8')
print('Built province.html successfully with Kahoot Mini Quiz Game!')
