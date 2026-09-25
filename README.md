# 🔍 LogLens

<p align="center">
  <b>AI-Assisted Playback Log Analysis Platform</b><br>
  Analyze large TV playback logs, automatically detect failures, group similar errors using AI, and investigate playback issues faster.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge\&logo=react\&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge\&logo=sqlite\&logoColor=white)
![AI](https://img.shields.io/badge/AI-Log%20Investigation-8A2BE2?style=for-the-badge)

</p>

---

## 📖 About LogLens

**LogLens** is an AI-assisted playback log analysis platform designed for playback QA engineers and streaming developers.

Modern televisions generate thousands of log lines during playback testing, making manual debugging slow and repetitive. LogLens automates this investigation by detecting failures, grouping similar errors using AI, and providing an interactive log inspection interface.

Instead of searching through massive log files manually, engineers can identify **what failed, where it failed, and inspect the exact evidence** within seconds.

---

## 🎯 Problem

A typical playback debugging workflow:

```text
PR Raised
     ↓
Flash Software to TV
     ↓
Run Playback Test
     ↓
TV Generates Log File
     ↓
Thousands of Log Lines
     ↓
Manual Error Search
     ↓
Find Timestamp
     ↓
Investigate Failure
```

### LogLens simplifies it into:

```text
Upload Log
     ↓
AI Log Processing
     ↓
Error Detection
     ↓
Semantic Error Grouping
     ↓
Interactive Log Inspector
     ↓
Investigation Summary
```

---

## ✨ Features

### 📂 Log Upload

* Upload `.log` and `.txt` playback logs
* FastAPI-powered backend processing
* Supports large playback log files

### 🤖 AI Log Analysis

* Detects Errors & Warnings
* Extracts timestamps and line numbers
* Identifies affected components
* Groups similar log messages using AI embeddings
* Categorizes issues into Playback, Network, Audio, DRM and System

### 🔎 Interactive Log Viewer

* Search detected issues
* Click any issue to inspect matching log lines
* View timestamps and line numbers
* Preserve original log messages
* Investigation-ready interface

### 📊 Investigation Summary

Every analysis provides:

* Total log lines
* Error count
* Unique issue groups
* Error categories
* AI-generated explanation for each issue

---

## 🖥️ Interface

```text
┌──────────────────────────────┬──────────────────────────────────┐
│                              │                                  │
│        ISSUE PANEL           │        LOG INSPECTOR             │
│                              │                                  │
│ 🔴 Playback Failure          │ #184729                          │
│ 🟡 Network Timeout           │ 10:42:24                         │
│ 🔵 Audio Decoder             │ ERROR Playback Failed            │
│                              │                                  │
│ Search Issues...             │ Original matching log lines      │
│                              │                                  │
└──────────────────────────────┴──────────────────────────────────┘
```

---

## 🏗️ Architecture

```text
                    LogLens
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
 React Frontend                FastAPI Backend
        │                             │
        │                      Log Processing
        │                             │
        │                      Error Detection
        │                             │
        │                  AI Error Grouping
        │                             │
        └──────────────┬──────────────┘
                       │
                       ▼
              Investigation Results
                       │
              ┌────────┴────────┐
              ▼                 ▼
        Issue Panel       Log Inspector
```

---

## 🛠️ Tech Stack

| Layer           | Technology            |
| --------------- | --------------------- |
| Frontend        | React + Vite          |
| Styling         | CSS                   |
| Backend         | FastAPI               |
| Language        | Python 3.13           |
| AI              | Sentence Transformers |
| Log Processing  | Regex + Custom Parser |
| Server          | Uvicorn               |
| Database        | SQLite                |
| Version Control | Git & GitHub          |

---

## 📂 Project Structure

```text
LogLens/
│
├── Backend/
│   ├── analyzers/
│   ├── routes/
│   ├── models/
│   ├── services/
│   └── main.py
│
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── api.js
│
├── .venv/
├── README.md
└── .gitignore
```

---

## 🚀 Development Progress

### Phase 1 — Backend Foundation

* [x] Python environment
* [x] Virtual environment
* [x] FastAPI setup
* [x] Uvicorn setup
* [x] Log Upload API

### Phase 2 — Log Processing

* [x] Log validation
* [x] Timestamp extraction
* [x] Log-level detection
* [x] Error detection
* [x] Warning detection
* [x] Line number tracking
* [x] Component identification
* [x] AI semantic error grouping

### Phase 3 — Interactive Log Viewer

* [x] Searchable issue list
* [x] Interactive Log Inspector
* [x] Line numbers
* [x] Timestamp viewer
* [x] AI investigation summary

### Phase 4 — Storage & Reporting *(Upcoming)*

* [ ] SQLite session history
* [ ] Export investigation report
* [ ] Previous analysis history

---

## 🔄 Investigation Workflow

```text
Upload Playback Log
          │
          ▼
Log Validation
          │
          ▼
Error Detection
          │
          ▼
AI Similarity Grouping
          │
          ▼
Issue Categorization
          │
          ▼
Interactive Log Inspector
          │
          ▼
Investigation Summary
```

---

## 🎯 Project Goal

LogLens reduces the time required to investigate playback failures by combining:

* Traditional log processing
* AI semantic error grouping
* Interactive log inspection
* Searchable investigation workflow

The objective is to help engineers quickly determine **what failed, when it failed, and inspect the exact log evidence** without manually searching thousands of log lines.

---

## 👩‍💻 Author

**Namratha V Naik**

Software Engineer • AI/ML • Streaming Technologies • Web Development

---

<p align="center">

⭐ If you found LogLens interesting, consider giving the repository a star.

</p>
