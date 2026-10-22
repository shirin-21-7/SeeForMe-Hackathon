
import os
import logging
import re
from io import BytesIO
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from google import genai
from PIL import Image

load_dotenv()
logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemma-4-26b-a4b-it"
client = genai.Client(api_key=API_KEY) if API_KEY else None

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#fff8ec">
<title>SeeForMe | Shop with confidence</title>
<style>
:root {
  --orange:#f47721; --yellow:#ffd45c; --cream:#fff8ec;
  --ink:#29251f; --muted:#777168; --line:#eee5d8;
  --white:#fff; --green:#237b53;
  --shadow:0 14px 42px rgba(75,46,16,.075);
}
* { box-sizing:border-box; }
html { scroll-behavior:smooth; }
body {
  margin:0; background:var(--cream); color:var(--ink);
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
}
button,input { font:inherit; }
button { cursor:pointer; }
button:focus-visible,label:focus-visible,input:focus-visible {
  outline:3px solid #2468b4; outline-offset:4px;
}
.topbar {
  min-height:76px; padding:12px 6%; background:white;
  border-bottom:1px solid var(--line); display:flex;
  align-items:center; justify-content:space-between; gap:12px;
}
.brand { display:flex; align-items:center; gap:11px; }
.brand-mark {
  width:43px;height:43px;border-radius:15px;
  background:linear-gradient(145deg,#ffad36,var(--orange));
  display:grid;place-items:center;color:white;font-size:23px;font-weight:900;
  box-shadow:0 6px 15px #f4772133;
}
.brand-name { font-size:23px;font-weight:850;letter-spacing:-1px; }
.brand-name span { color:var(--orange); }
.brand-caption { font-size:10px;color:var(--muted);margin-top:2px; }
.status-pill {
  display:flex;align-items:center;gap:8px;border:1px solid var(--line);
  background:white;border-radius:30px;padding:10px 13px;
  font-size:12px;font-weight:700;
}
.dot { width:8px;height:8px;background:#32a66a;border-radius:50%; }
main { max-width:1100px;margin:auto;padding:35px 24px 55px; }
.hero {
  position:relative;overflow:hidden;border-radius:30px;padding:39px;color:#34240f;
  background:linear-gradient(115deg,#ffe9ad 0%,#ffce72 53%,#ffb15e 100%);
  display:grid;grid-template-columns:1.25fr .75fr;align-items:center;gap:22px;
}
.hero:after {
  content:"";position:absolute;width:260px;height:260px;border-radius:50%;
  border:40px solid #ffffff28;right:-85px;top:-100px;pointer-events:none;
}
.eyebrow {
  display:inline-flex;align-items:center;gap:7px;background:#ffffff8a;
  border:1px solid #ffffff9e;border-radius:30px;padding:8px 12px;
  font-size:11px;letter-spacing:1px;text-transform:uppercase;font-weight:800;
}
h1 { font-size:clamp(35px,5.3vw,58px);line-height:1.04;
  letter-spacing:-2.5px;margin:19px 0 15px;max-width:570px; }
.hero p { font-size:16px;line-height:1.65;max-width:480px;color:#634c2c; }
.hero-art { display:grid;place-items:center;min-height:200px;position:relative; }
.orbit {
  width:210px;height:210px;border:1px solid #ffffffa8;border-radius:50%;
  display:grid;place-items:center;background:#ffffff30;
}
.orbit-inner {
  width:145px;height:145px;border-radius:42px;transform:rotate(-8deg);
  display:grid;place-items:center;font-size:65px;background:#fffaf0;
  box-shadow:0 18px 35px #93500b26;
}
.float-chip {
  position:absolute;background:white;border-radius:15px;padding:11px 14px;
  font-size:12px;font-weight:800;box-shadow:var(--shadow);
}
.chip-one { top:18px;right:0; }
.chip-two { bottom:16px;left:0; }
.section-heading {
  display:flex;align-items:end;justify-content:space-between;gap:12px;
  margin:34px 0 16px;
}
.section-heading h2 { margin:0;font-size:24px;letter-spacing:-.7px; }
.section-heading p { margin:6px 0 0;font-size:13px;color:var(--muted); }
.grid { display:grid;grid-template-columns:1fr 1fr;gap:19px; }
.card {
  background:white;border:1px solid var(--line);border-radius:25px;
  padding:25px;box-shadow:var(--shadow);min-width:0;
}
.card-heading { display:flex;gap:13px;align-items:center;margin-bottom:18px; }
.icon-box {
  width:47px;height:47px;flex-shrink:0;border-radius:16px;
  background:#fff0d9;display:grid;place-items:center;font-size:23px;
}
.card h3 { margin:0;font-size:19px;letter-spacing:-.4px; }
.card-heading p { margin:5px 0 0;color:var(--muted);font-size:12px;line-height:1.45; }
.mic-area {
  min-height:180px;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:13px;background:#fff9ed;
  border:1px dashed #f2d7a8;border-radius:22px;padding:18px;text-align:center;
}
.mic-button {
  border:0;width:86px;height:86px;border-radius:29px;color:white;font-size:34px;
  background:linear-gradient(145deg,#ff9b37,var(--orange));
  box-shadow:0 9px 25px #f4772142;transition:transform .2s;
}
.mic-button:hover { transform:translateY(-3px); }
.mic-button.listening { animation:pulse 1.5s infinite; }
@keyframes pulse {
  0%,100% { box-shadow:0 0 0 0 #f4772155,0 9px 25px #f4772142; }
  50% { box-shadow:0 0 0 13px #f4772100,0 9px 25px #f4772142; }
}
.mic-title { font-weight:800;font-size:15px; }
.mic-hint { color:var(--muted);font-size:12px;line-height:1.5; }
#message { color:#76502c;font-size:12px;min-height:18px;margin:14px 0 0; }
.commands { display:flex;flex-wrap:wrap;gap:7px;margin-top:13px; }
.command-chip {
  border:1px solid var(--line);background:white;color:#5f5142;
  border-radius:30px;padding:8px 11px;font-size:11px;
}
.upload-zone {
  border:1.5px dashed #edc99b;border-radius:20px;background:#fffbf5;
  min-height:155px;padding:22px 14px;text-align:center;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:8px;cursor:pointer;
}
.upload-symbol {
  width:46px;height:46px;display:grid;place-items:center;
  background:#ffedcf;border-radius:16px;font-size:23px;
}
.upload-zone strong { font-size:14px; }
.upload-zone small { font-size:12px;color:var(--muted);line-height:1.5; }
.upload-zone:hover { border-color:var(--orange);background:#fff6e8; }
#photoInput {
  position:absolute;width:1px;height:1px;overflow:hidden;
  clip:rect(0,0,0,0);white-space:nowrap;
}
#preview {
  display:none;width:100%;max-height:230px;object-fit:contain;
  background:#fffaf2;border-radius:16px;margin-top:15px;
}
.button-row { display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px; }
.btn {
  border:0;border-radius:14px;padding:14px 12px;min-height:49px;
  font-size:13px;font-weight:800;transition:transform .15s,opacity .15s;
}
.btn:hover { transform:translateY(-1px); }
.btn:disabled { opacity:.45;cursor:not-allowed;transform:none; }
.btn-primary { background:var(--orange);color:white; }
.btn-secondary { background:#fff0d9;color:#63380f; }
.camera-note { color:var(--muted);font-size:11px;line-height:1.5;margin:13px 0 0; }
.result-card { margin-top:19px; }
.result-top { display:flex;align-items:center;gap:12px; }
.result-badge {
  background:#e6f5eb;color:var(--green);border-radius:30px;
  padding:7px 10px;font-size:10px;font-weight:850;letter-spacing:.4px;
}
.result-placeholder {
  margin-top:18px;background:#fffaf3;border:1px solid #f2e8d9;
  border-radius:18px;padding:23px;text-align:center;
}
.big-icon { font-size:31px; }
.result-placeholder p { color:var(--muted);font-size:13px;line-height:1.6;margin-bottom:0; }
#result { white-space:pre-wrap;line-height:1.75;font-size:14px;overflow-wrap:anywhere; }
#result:not(:empty) { margin-top:18px; }
.result-actions { display:flex;flex-wrap:wrap;gap:9px;margin-top:15px; }
.result-actions .btn { flex:1; }
#helpText {
  display:none;padding:13px;border-radius:14px;background:#fff8e9;
  font-size:12px;line-height:1.7;
}
footer { text-align:center;padding:24px 16px;color:var(--muted);font-size:11px;line-height:1.7; }
.footer-mark { color:var(--orange);font-weight:900; }
@media(max-width:720px) {
  .topbar { padding:12px 16px; }
  main { padding:19px 14px 35px; }
  .hero { padding:26px 22px;grid-template-columns:1fr;border-radius:25px; }
  .hero-art { min-height:155px; }
  .orbit { width:150px;height:150px; }
  .orbit-inner { width:105px;height:105px;border-radius:32px;font-size:48px; }
  .chip-one { right:9%;top:2px; }
  .chip-two { left:8%;bottom:0; }
  h1 { font-size:40px; }
  .grid { grid-template-columns:1fr; }
  .section-heading { margin-top:27px; }
  .card { padding:20px; }
}
@media(max-width:390px) {
  .brand-name { font-size:20px; }
  .brand-caption { font-size:8px; }
  .status-pill { font-size:10px;padding:8px; }
}
@media(prefers-reduced-motion:reduce) {
  *,*::before,*::after { animation:none!important;transition:none!important;scroll-behavior:auto!important; }
}
</style>
</head>
<body>
<header class="topbar">
  <div class="brand" aria-label="SeeForMe shopping assistant">
    <div class="brand-mark" aria-hidden="true">S</div>
    <div>
      <div class="brand-name">See<span>ForMe</span></div>
      <div class="brand-caption">SHOPPING, MADE MORE INDEPENDENT</div>
    </div>
  </div>
  <div class="status-pill"><span class="dot"></span><span id="voiceStatus">Ready to help</span></div>
</header>

<main>
  <section class="hero" aria-labelledby="heroTitle">
    <div>
      <div class="eyebrow">✦ YOUR AI SHOPPING COMPANION</div>
      <h1 id="heroTitle">Shop with more <span style="color:#a84708">confidence.</span></h1>
      <p>Identify products, understand packaging, and hear the details that matter — with help from your voice assistant.</p>
    </div>
    <div class="hero-art" aria-hidden="true">
      <div class="orbit"><div class="orbit-inner">🛍️</div></div>
      <div class="float-chip chip-one">✦ AI-powered</div>
      <div class="float-chip chip-two">♡ Made for accessibility</div>
    </div>
  </section>

  <div class="section-heading">
    <div><h2>How can I help?</h2><p>Choose a way to get started.</p></div>
  </div>

  <div class="grid">
    <section class="card voice-card" aria-labelledby="voiceHeading">
      <div class="card-heading">
        <div class="icon-box" aria-hidden="true">🎙️</div>
        <div><h3 id="voiceHeading">Talk to SeeForMe</h3><p>Your voice is your shortcut.</p></div>
      </div>
      <div class="mic-area">
        <button id="voiceButton" class="mic-button" type="button"
          aria-label="Start voice assistant" aria-pressed="false">🎙</button>
        <div class="mic-title" id="micTitle">I'm ready when you are</div>
        <div class="mic-hint">Tap the microphone, then speak naturally.</div>
      </div>
      <p id="message" role="status" aria-live="polite">Voice assistant is ready.</p>
      <div class="commands" aria-label="Example voice commands">
        <button class="command-chip" data-command="help" type="button">Help</button>
        <button class="command-chip" data-command="choose a photo" type="button">Choose a photo</button>
        <button class="command-chip" data-command="scan this" type="button">Scan this</button>
        <button class="command-chip" data-command="read that again" type="button">Read again</button>
      </div>
      <div id="helpText">
        <strong>Try saying:</strong> “Choose a photo”, “Open camera”, “Scan this”, “Read that again”, or “Stop speaking”.
      </div>
    </section>

    <section class="card" aria-labelledby="scanHeading">
      <div class="card-heading">
        <div class="icon-box" aria-hidden="true">📦</div>
        <div><h3 id="scanHeading">Identify a product</h3><p>Start with a clear product photo.</p></div>
      </div>
      <label class="upload-zone" for="photoInput" tabindex="0" id="uploadLabel">
        <span class="upload-symbol" aria-hidden="true">↑</span>
        <strong>Choose a product photo</strong>
        <small>Tap to browse your device<br>JPG, PNG and other common image formats</small>
      </label>
      <input id="photoInput" type="file" accept="image/*" aria-label="Choose a product photo">
      <img id="preview" alt="Preview of the selected product photo">
      <div class="button-row">
        <button id="cameraButton" class="btn btn-secondary" type="button">📷 Camera help</button>
        <button id="scanButton" class="btn btn-primary" type="button" disabled>✦ Scan product</button>
      </div>
      <p class="camera-note">Camera unavailable? Upload a photo instead. Your image is previewed before analysis.</p>
    </section>
  </div>

  <section class="card result-card" aria-labelledby="resultHeading">
    <div class="result-top">
      <div class="icon-box" aria-hidden="true">✨</div>
      <div style="flex:1"><h3 id="resultHeading">Your product insights</h3><p style="margin:5px 0 0;color:var(--muted);font-size:12px">Clear information, read aloud when you need it.</p></div>
      <span id="resultBadge" class="result-badge">WAITING FOR PHOTO</span>
    </div>
    <div id="resultPlaceholder" class="result-placeholder">
      <div class="big-icon" aria-hidden="true">🔎</div>
      <strong>Your next discovery starts here</strong>
      <p>Choose a product photo and tap Scan product.<br>Your AI-generated product details will appear here.</p>
    </div>
    <div id="result" role="region" aria-label="Product analysis result" aria-live="polite"></div>
    <div class="result-actions">
      <button id="readButton" class="btn btn-secondary" type="button">🔊 Read result aloud</button>
      <button id="stopButton" class="btn btn-secondary" type="button">■ Stop speaking</button>
    </div>
  </section>
</main>

<footer>
  <span class="footer-mark">SeeForMe</span> · Shopping with greater independence<br>
  AI results may be incomplete. Verify important product details directly on the packaging.
</footer>

<script>
(() => {
  const $ = id => document.getElementById(id);
  const voiceButton = $("voiceButton");
  const voiceStatus = $("voiceStatus");
  const message = $("message");
  const micTitle = $("micTitle");
  const photoInput = $("photoInput");
  const preview = $("preview");
  const scanButton = $("scanButton");
  const result = $("result");
  const resultBadge = $("resultBadge");
  const resultPlaceholder = $("resultPlaceholder");
  const helpText = $("helpText");
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  let selectedFile = null;
  let lastResult = "";
  let recognition = null;
  let listening = false;
  let speaking = false;
  let welcomeDone = false;
  let pendingResume = false;
  let recognitionWanted = false;

  // Remove Markdown syntax before speech; keep the visible result unchanged.
  function cleanForSpeech(text) {
    return String(text || "")
      .replace(/```[\s\S]*?```/g, " ")
      .replace(/`([^`]+)`/g, "$1")
      .replace(/\*\*(.*?)\*\*/g, "$1")
      .replace(/__(.*?)__/g, "$1")
      .replace(/~~(.*?)~~/g, "$1")
      .replace(/^\s{0,3}#{1,6}\s*/gm, "")
      .replace(/^\s*[-*+]\s+/gm, "")
      .replace(/^\s*>\s?/gm, "")
      .replace(/[*_#~]/g, "")
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
      .replace(/https?:\/\/\S+/g, "")
      .replace(/\n{2,}/g, ". ")
      .replace(/\n/g, ". ")
      .replace(/\s+([.,!?;:])/g, "$1")
      .replace(/([.,!?;:])\1+/g, "$1")
      .replace(/\s{2,}/g, " ")
      .trim();
  }

  function setStatus(text) {
    voiceStatus.textContent = text;
    message.textContent = text;
  }

  function stopSpeech() {
    if ("speechSynthesis" in window) window.speechSynthesis.cancel();
    speaking = false;
    pendingResume = false;
  }

  function speak(text, resume = false) {
    const spokenText = cleanForSpeech(text);
    if (!spokenText) return;

    if (!("speechSynthesis" in window)) {
      setStatus("Speech output is unavailable in this browser.");
      return;
    }

    pendingResume = resume && listening;
    window.speechSynthesis.cancel();
    speaking = true;

    if (recognition && listening) {
      try { recognition.stop(); } catch (_) {}
    }

    const utterance = new SpeechSynthesisUtterance(spokenText);
    utterance.lang = "en-IN";
    utterance.rate = 0.94;

    utterance.onend = () => {
      speaking = false;
      if (pendingResume && listening) {
        pendingResume = false;
        setTimeout(startRecognition, 400);
      }
    };

    utterance.onerror = () => {
      speaking = false;
      if (pendingResume && listening) {
        pendingResume = false;
        setTimeout(startRecognition, 400);
      }
    };

    window.speechSynthesis.speak(utterance);
  }

  function announce(text) {
    setStatus(text);
    speak(text, listening);
  }

  function startRecognition() {
    if (!recognition || !listening || speaking) return;
    try { recognition.start(); } catch (_) {}
  }

  function updateVoiceUI(active) {
    voiceButton.textContent = active ? "■" : "🎙";
    voiceButton.setAttribute("aria-label", active ? "Stop voice assistant" : "Start voice assistant");
    voiceButton.setAttribute("aria-pressed", String(active));
    voiceButton.classList.toggle("listening", active);
    micTitle.textContent = active ? "Listening — speak now" : "I'm ready when you are";
  }

  function startListening() {
    if (!SpeechRecognition) {
      announce("Voice recognition is not supported here. Please use the buttons on the screen.");
      return;
    }

    if (listening) {
      listening = false;
      recognitionWanted = false;
      try { recognition.stop(); } catch (_) {}
      updateVoiceUI(false);
      setStatus("Voice assistant stopped.");
      speak("Voice assistant stopped. Tap the microphone to start again.");
      return;
    }

    recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.continuous = true;
    recognition.interimResults = false;
    recognitionWanted = true;
    listening = true;
    updateVoiceUI(true);
    setStatus("Listening. Tell me what you need.");
    speak("Voice assistant started. Say help, choose a photo, open camera, or scan this.");

    recognition.onresult = event => {
      const text = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
      setStatus("I heard: " + text);
      handleCommand(text);
    };

    recognition.onerror = event => {
      if (event.error === "not-allowed" || event.error === "service-not-allowed") {
        listening = false;
        recognitionWanted = false;
        updateVoiceUI(false);
        micTitle.textContent = "Microphone permission needed";
        announce("Microphone access was denied. Allow it in your browser settings, or use the buttons.");
      } else if (event.error === "network") {
        setStatus("Voice recognition has a network issue. Use the screen buttons instead.");
      }
    };

    recognition.onend = () => {
      if (recognitionWanted && listening && !speaking) {
        setTimeout(startRecognition, 400);
      }
    };
  }

  function handleCommand(text) {
    if (text.includes("stop speaking") || text === "be quiet" || text === "quiet") {
      stopSpeech();
      setStatus("Speech stopped.");
      return;
    }

    if (text.includes("stop listening") || text.includes("turn off voice")) {
      listening = false;
      recognitionWanted = false;
      if (recognition) try { recognition.stop(); } catch (_) {}
      updateVoiceUI(false);
      setStatus("Voice assistant stopped.");
      speak("Voice assistant stopped.");
      return;
    }

    if (text.includes("help") || text.includes("what can you do")) {
      helpText.style.display = "block";
      announce("You can say choose a photo, open camera, scan this, read that again, or stop speaking.");
      return;
    }

    if (text.includes("choose") || text.includes("upload") || text.includes("select photo")) {
      announce("The choose a product photo area is below the product heading. Select it to browse your device.");
      photoInput.click();
      return;
    }

    if (text.includes("camera")) {
      announce("The camera help button is on the right side of the product controls. If your camera is unavailable, choose a photo instead.");
      return;
    }

    if (text.includes("scan") || text.includes("identify") ||
        text.includes("analyse") || text.includes("analyze") ||
        text.includes("describe this")) {
      scanProduct();
      return;
    }

    if (text.includes("read") || text.includes("repeat") || text.includes("again")) {
      if (lastResult) speak(lastResult, listening);
      else announce("There is no product result yet. Choose a photo and say scan this.");
      return;
    }

    announce("Sorry, I did not understand that. Say help to hear the available commands.");
  }

  voiceButton.addEventListener("click", startListening);

  window.addEventListener("load", () => {
    if (welcomeDone) return;
    welcomeDone = true;
    setTimeout(() => {
      speak("Welcome to SeeForMe. Your shopping assistant is ready. The choose a product photo area is on the left, and the camera help and scan buttons are on the right. Tap the microphone to use voice commands.");
    }, 800);
  });

  photoInput.addEventListener("change", () => {
    const file = photoInput.files && photoInput.files[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      announce("That file is not an image. Please choose a product photo.");
      return;
    }

    selectedFile = file;

    if (preview.dataset.objectUrl) URL.revokeObjectURL(preview.dataset.objectUrl);
    const objectUrl = URL.createObjectURL(file);
    preview.dataset.objectUrl = objectUrl;
    preview.src = objectUrl;
    preview.style.display = "block";

    scanButton.disabled = false;
    resultBadge.textContent = "PHOTO SELECTED";
    resultPlaceholder.style.display = "none";
    result.textContent = "";

    announce("Photo selected. Say scan this to identify the product, or tap Scan product.");
  });

  $("uploadLabel").addEventListener("keydown", event => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      photoInput.click();
    }
  });

  $("cameraButton").addEventListener("click", () => {
    announce("Your camera may not be available on this device. Use Choose a product photo to upload an image.");
  });

  document.querySelectorAll("[data-command]").forEach(button => {
    button.addEventListener("click", () => handleCommand(button.dataset.command));
  });

  scanButton.addEventListener("click", scanProduct);

  $("readButton").addEventListener("click", () => {
    if (lastResult) speak(lastResult, listening);
    else announce("No product result is available yet. Choose a product photo and scan it first.");
  });

  $("stopButton").addEventListener("click", () => {
    stopSpeech();
    setStatus("Speech stopped.");
  });

  async function scanProduct() {
    if (!selectedFile) {
      announce("Please choose a product photo first.");
      photoInput.click();
      return;
    }

    scanButton.disabled = true;
    scanButton.textContent = "Analysing…";
    resultBadge.textContent = "WORKING";
    resultPlaceholder.style.display = "none";
    result.textContent = "Identifying your product. Please wait.";
    announce("Identifying the product. Please wait.");

    try {
      const form = new FormData();
      form.append("file", selectedFile);

      const response = await fetch("/analyse", {
        method: "POST",
        body: form
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || "Product analysis failed.");
      }

      lastResult = data.result;
      result.textContent = lastResult;
      resultBadge.textContent = "ANALYSIS READY";
      setStatus("Product identified. Analysis is ready.");
      speak("Product identified. I will now read the result. " + lastResult, listening);

    } catch (error) {
      lastResult = "";
      resultBadge.textContent = "TRY AGAIN";
      result.textContent =
        "I could not identify this product clearly.\n\n" +
        "Try another photo with better lighting and make sure the label is readable.\n\n" +
        "Technical detail: " + (error.message || "Unknown error");

      announce("I could not identify this product clearly. Try another photo with better lighting.");

    } finally {
      scanButton.disabled = !selectedFile;
      scanButton.textContent = "✦ Scan product";
    }
  }
})();
</script>
</body>
</html>
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("SeeForMe starting")
    yield
    logging.info("SeeForMe shutting down")


app = FastAPI(title="SeeForMe", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(HTML)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "api_key_configured": bool(API_KEY),
        "model": MODEL_NAME,
    }


@app.post("/analyse")
async def analyse(file: UploadFile = File(...)):
    if not client:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "GEMINI_API_KEY is missing. Check your .env file.",
            },
        )

    if not file.content_type or not file.content_type.startswith("image/"):
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "Please upload an image file."},
        )

    try:
        contents = await file.read()

        if not contents:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "The image file is empty."},
            )

        image = Image.open(BytesIO(contents))
        image.verify()
        image = Image.open(BytesIO(contents)).convert("RGB")
        image.thumbnail((1600, 1600))

        prompt = """
You are SeeForMe, a voice-first shopping assistant for blind and low-vision users.
Inspect the product image and respond in concise, plain English.

Use these headings:
1. Product identification
2. Brand and product name
3. Visible label details
4. Size, quantity, or variant
5. Price, if clearly visible
6. Important cautions or expiry information, if clearly visible
7. What the shopper should verify

Only report information visible or identifiable with reasonable confidence.
Clearly state when text is unreadable or identification is uncertain.
Never invent ingredients, prices, expiry dates, medical advice, or claims.
If the image is not a product, explain that and ask for a clear product photo.
Make the result easy to understand when read aloud.
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, image],
        )

        answer = (response.text or "").strip()

        if not answer:
            raise ValueError("The AI returned an empty response.")

        # Preserve Markdown for display. The frontend removes it only for speech.
        return {"success": True, "result": answer}

    except Exception as exc:
        logging.exception("Product analysis failed")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": (
                    "Analysis failed. Check internet access, API key, model access, "
                    "and image file. Details: " + str(exc)[:300]
                ),
            },
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
