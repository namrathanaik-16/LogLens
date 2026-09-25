# 🔍 LogLens

<p align="center">
  <b>AI-Assisted Playback Log Analysis & Investigation Platform</b><br>
  Analyze large playback logs, identify errors, trace failure timelines, and investigate potential root causes.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![AI](https://img.shields.io/badge/AI-Log%20Investigation-8A2BE2?style=for-the-badge)

</p>

---

## 📖 About LogLens

**LogLens** is an AI-assisted playback log analysis and investigation platform designed to simplify the analysis of large-scale TV playback logs.

During playback testing, televisions can generate extremely large log files containing thousands or even hundreds of thousands of lines. Manually searching through these logs to identify errors, timestamps, and the sequence of events leading to a playback failure can be time-consuming.

LogLens aims to automate this investigation process.

Users can upload a playback log file, provide the corresponding test case, and allow LogLens to process the log, identify relevant errors, correlate events, and present the investigation results alongside the original log.

---

## 🎯 Problem

A typical playback debugging workflow looks like:

```text
PR Raised
    ↓
Connect USB to TV
    ↓
Run Playback Test Case
    ↓
TV Generates Logs
    ↓
Logs Stored on USB
    ↓
Large Log File
    ↓
Manual Log Analysis
    ↓
Identify Error
    ↓
Find Timestamp
    ↓
Investigate Failure
```

Large log files make this process difficult because the relevant failure may be surrounded by thousands of unrelated events.

### LogLens aims to simplify this:

```text
Upload Log
    ↓
Enter Test Case
    ↓
Log Processing
    ↓
Error Detection
    ↓
Event Correlation
    ↓
AI Investigation
    ↓
Failure Timeline
    ↓
Root Cause Analysis
```

---

## ✨ Planned Features

### 📂 Log File Upload

Upload large playback log files directly to the platform.

Supported log formats will initially include:

- `.log`
- `.txt`
- Other text-based log formats where applicable

---

### 📄 Complete Log Viewer

Display the complete uploaded log in an interactive viewer.

The viewer will provide:

- Line numbers
- Search
- Scrolling
- Error highlighting
- Warning highlighting
- Jump-to-line functionality
- Context around detected events

---

### 🚨 Error Detection

Automatically identify important events such as:

- Errors
- Warnings
- Critical failures
- Playback failures
- Network failures
- Buffering events
- Decoder failures
- Segment download failures
- Retry attempts

Each detected event will retain its original:

- Timestamp
- Line number
- Log level
- Message
- Component

---

### 🧪 Test Case Context

Users will provide the playback test case associated with the uploaded log.

Example:

```text
Start 4K DASH playback
→ Pause playback after 30 seconds
→ Resume playback
→ Verify playback continues without buffering
```

LogLens will use the test case as context when analyzing the log.

---

### 🕒 Failure Timeline

Relevant events will be organized chronologically.

Example:

```text
10:42:05  Playback Started
10:42:17  Segment Request Timeout
10:42:18  Retry Attempt 1
10:42:19  Retry Attempt 2
10:42:21  Buffer Underrun
10:42:24  Playback Failed
```

This helps engineers understand what happened immediately before the failure.

---

### 🔗 Event Correlation

LogLens will correlate related events instead of treating every error independently.

For example:

```text
Segment Timeout
      ↓
Retry Attempt
      ↓
Retry Attempt
      ↓
Buffer Depletion
      ↓
Playback Stall
      ↓
Playback Failure
```

This allows the tool to identify the sequence of events that may have contributed to the final failure.

---

### 🤖 AI Investigation

The AI investigation layer will analyze the relevant events and provide an engineering-oriented explanation.

Example:

```text
Likely Root Cause

The playback failure appears to be associated with
a segment download timeout occurring shortly after
playback resumed.

Evidence:

• Segment request timeout at 10:42:17
• Two retry attempts followed
• Buffer level dropped at 10:42:21
• Playback failure occurred at 10:42:24

Confidence: 87%
```

The AI will work on relevant extracted log context rather than blindly sending the entire raw log file.

---

### 🎯 Interactive Error Investigation

The analysis panel and log viewer will be connected.

For example:

```text
ERROR
Playback failed

Timestamp: 10:42:24
Line: 184729
```

Clicking the error will:

1. Jump to the corresponding line.
2. Highlight the line.
3. Display surrounding log context.
4. Show the related investigation details.

---

## 🖥️ Planned Interface

```text
┌──────────────────────────────┬───────────────────────────────────┐
│                              │                                   │
│       AI INVESTIGATION       │          COMPLETE LOG             │
│                              │                                   │
│ ❌ Playback Failure          │ 184720 INFO  Segment loaded       │
│                              │ 184721 INFO  Buffer: 8.2s         │
│ Timestamp: 10:42:24         │ 184722 WARN  Retry attempt        │
│ Line: 184729                │                                   │
│                              │ ███ 184729 ERROR Playback failed ███
│ Likely Cause:                │ 184730 INFO  Player cleanup       │
│ Segment request timeout      │                                   │
│                              │                                   │
│ Evidence:                    │                                   │
│ • Timeout at 10:42:17        │                                   │
│ • Retry at 10:42:18          │                                   │
│ • Buffer underrun at 10:42:21│                                   │
│                              │                                   │
│ Confidence: 87%              │                                   │
└──────────────────────────────┴───────────────────────────────────┘
```

---

## 🏗️ Architecture

```text
                         LogLens
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
      React Frontend                  FastAPI Backend
             │                             │
             │                       Log Processing
             │                             │
             │                       Error Detection
             │                             │
             │                       Event Correlation
             │                             │
             │                       Test Case Analysis
             │                             │
             │                       AI Investigation
             │                             │
             └──────────────┬──────────────┘
                            │
                            ▼
                     Analysis Results
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
          Analysis Panel            Log Viewer
             LEFT SIDE              RIGHT SIDE
                                        │
                                        ▼
                                  Highlighted Lines
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Frontend Language | JavaScript / TypeScript |
| UI | Tailwind CSS |
| Log Viewer | Monaco Editor |
| Backend | Python |
| API Framework | FastAPI |
| Server | Uvicorn |
| Log Processing | Python |
| Pattern Detection | Regex + Custom Parsers |
| Data Processing | Pandas |
| AI Investigation | LLM API |
| Database | SQLite |
| Version Control | Git / GitHub |

---

## 📂 Planned Project Structure

```text
LogLens/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── parsers/
│   ├── analyzers/
│   └── models/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│
├── .venv/
│
├── .gitignore
└── README.md
```

---

## 🚀 Development Roadmap

### Phase 1 — Backend Foundation

- [x] Python environment
- [x] Virtual environment
- [x] FastAPI setup
- [x] Uvicorn setup
- [x] Basic API endpoint
- [x] Log upload API

### Phase 2 — Log Processing

- [x] Log file validation
- [x] Timestamp extraction
- [x] Log-level detection
- [x] Error detection
- [x] Warning detection
- [x] Line number tracking
- [x] Component identification

### Phase 3 — Interactive Log Viewer

- [x] Complete log viewer
- [x] Line numbers
- [x] Search
- [ ] Error highlighting
- [ ] Warning highlighting
- [ ] Jump-to-line
- [ ] Context viewer

### Phase 4 — Test Case Analysis

- [ ] Test case input
- [ ] Test case event mapping
- [ ] Event timeline
- [ ] Relevant event detection
- [ ] Failure point identification

### Phase 5 — AI Investigation

- [ ] AI integration
- [ ] Error explanation
- [ ] Event correlation
- [ ] Root cause hypothesis
- [ ] Evidence extraction
- [ ] Confidence scoring

### Phase 6 — Storage & Reporting

- [ ] SQLite integration
- [ ] Session history
- [ ] Previous investigation results
- [ ] Investigation report
- [ ] Export analysis

### Phase 7 — Final Product

- [ ] UI refinement
- [ ] Performance optimization
- [ ] Large-log handling
- [ ] Error handling
- [ ] Security improvements
- [ ] Documentation
- [ ] Deployment

---

## 🔄 Investigation Workflow

```text
                    Upload Playback Log
                            │
                            ▼
                    Enter Test Case
                            │
                            ▼
                     Log Validation
                            │
                            ▼
                     Log Processing
                            │
                            ▼
                    Event Extraction
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
             Errors                  Warnings
                │                       │
                └───────────┬───────────┘
                            ▼
                     Event Correlation
                            │
                            ▼
                    Test Case Analysis
                            │
                            ▼
                     AI Investigation
                            │
                            ▼
                 Root Cause Hypothesis
                            │
                            ▼
                 Evidence + Timeline
                            │
                            ▼
               Interactive Log Viewer
```

---

## 🔐 Security Considerations

Log files may contain sensitive system information.

Future versions of LogLens will consider:

- Secure file handling
- Input validation
- File size limits
- Temporary file cleanup
- API authentication
- Protection of sensitive log information
- Secure AI processing

---

## 🔮 Future Enhancements

- Support for multiple TV log formats
- Known-error knowledge base
- RAG-based investigation
- Historical session comparison
- Similar failure detection
- Automatic regression detection
- Playback failure trend analysis
- Team investigation history
- PDF investigation reports
- Cloud deployment
- Authentication and role-based access

---

## 🎯 Project Goal

The goal of LogLens is to reduce the time required to investigate large playback logs by combining:

```text
Traditional Log Processing
          +
Event Correlation
          +
Test Case Context
          +
AI Investigation
          +
Interactive Log Visualization
```

Instead of manually searching through thousands of log lines, engineers should be able to quickly identify **what failed, when it failed, what happened before the failure, and why it may have happened.**

---

## 👩‍💻 Author

**Namratha V Naik**

Software Engineer

Software Development • AI/ML • Streaming Technologies • Web Development

---

<p align="center">

⭐ If you find LogLens interesting, consider giving the project a star.

</p>
