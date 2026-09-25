import { useState } from "react";
import Sidebar from "./components/Sidebar";
import { uploadLog } from "./api";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [selectedIssueId, setSelectedIssueId] = useState(null);
  const [search, setSearch] = useState("");

  async function handleUpload() {
    if (!file) return;

    try {
      const data = await uploadLog(file);
      setResult(data);
      setSelectedIssueId(null);
    } catch (err) {
      console.error(err);
      alert("Failed to analyze log.");
    }
  }

  const filteredIssues =
    result?.top_issues?.filter((issue) => {
      const text = (
        issue.title +
        " " +
        issue.message +
        " " +
        issue.category
      ).toLowerCase();

      return text.includes(search.toLowerCase());
    }) || [];

  const selectedIssue =
    filteredIssues.find((issue) => issue.id === selectedIssueId) || null;

  return (
    <div className="layout">
      <Sidebar />

      <main className="main">
        {/* ================= TOP BAR ================= */}

        <div className="topbar">
          <div>
            <h2>{file ? file.name : "No Log Uploaded"}</h2>
            <p>
              {file
                ? "Ready for analysis"
                : "Upload a TV log to begin analysis"}
            </p>
          </div>

          <div className="top-actions">
            <label className="upload-btn">
              Upload
              <input
                hidden
                type="file"
                accept=".txt,.log"
                onChange={(e) => setFile(e.target.files[0])}
              />
            </label>

            <button className="analyze-btn" onClick={handleUpload}>
              Analyze
            </button>
          </div>
        </div>

        {/* ================= SUMMARY ================= */}

        <div className="cards">
          <div className="card">
            <span>Total Lines</span>
            <h1>{result?.summary?.total_lines || 0}</h1>
          </div>

          <div className="card">
            <span>Error Lines</span>
            <h1>{result?.summary?.total_errors || 0}</h1>
          </div>

          <div className="card">
            <span>Error Groups</span>
            <h1>{result?.summary?.unique_issues || 0}</h1>
          </div>

          <div className="card">
            <span>Categories</span>
            <h1>{Object.keys(result?.categories || {}).length}</h1>
          </div>
        </div>

        {/* ================= MAIN CONTENT ================= */}

        <div className="content">
          {/* -------- LEFT PANEL -------- */}

          <section className="issues">
            <h3>Issues ({filteredIssues.length})</h3>

            <div className="search-bar">
              <input
                type="text"
                placeholder="Search issues..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            <div className="issues-list">
              {filteredIssues.map((issue) => (
                <div
                  key={issue.id}
                  className={`issue-card ${
                    selectedIssueId === issue.id ? "active" : ""
                  }`}
                  onClick={() => setSelectedIssueId(issue.id)}
                >
                  <div className="issue-left">
                    <span className="badge">{issue.category}</span>

                    <div className="issue-content">
                      <h4>
                        {issue.title === "Unknown System Error"
                          ? issue.message
                          : issue.title}
                      </h4>

                      <p className="issue-subtitle">
                        {issue.title === "Unknown System Error"
                          ? `Lines ${issue.first_line} – ${issue.last_line}`
                          : issue.meaning}
                      </p>
                    </div>
                  </div>

                  <span className="count">{issue.occurrences}</span>
                </div>
              ))}
            </div>
          </section>

          {/* -------- RIGHT PANEL -------- */}

          <section className="viewer">
            <h3>Log Inspector</h3>

            {!selectedIssue ? (
              <div className="empty">
                Click an issue to view matching log lines
              </div>
            ) : (
              <>
                <div className="inspector-header">
                  <span className="badge large">
                    {selectedIssue.category}
                  </span>

                  <h2>
                    {selectedIssue.title === "Unknown System Error"
                      ? selectedIssue.message
                      : selectedIssue.title}
                  </h2>

                  <p className="inspector-subtitle">
                    {selectedIssue.title === "Unknown System Error"
                      ? `Lines ${selectedIssue.first_line} – ${selectedIssue.last_line}`
                      : selectedIssue.meaning}
                  </p>
                </div>

                <div className="stats">
                  <div>
                    <small>Occurrences</small>
                    <strong>{selectedIssue.occurrences}</strong>
                  </div>

                  <div>
                    <small>First Line</small>
                    <strong>{selectedIssue.first_line}</strong>
                  </div>

                  <div>
                    <small>Last Line</small>
                    <strong>{selectedIssue.last_line}</strong>
                  </div>
                </div>

                <div className="logs">
                  {selectedIssue.log_lines?.map((log, index) => (
                    <div className="log-line" key={index}>
                      <div className="log-top">
                        <span className="line-no">
                          #{log.line_number}
                        </span>

                        <span className="time">
                          {log.timestamp || "--"}
                        </span>
                      </div>

                      <div className="msg">{log.message}</div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;