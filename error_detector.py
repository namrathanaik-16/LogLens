from analyzers.knowledge_base import ERROR_RULES
from analyzers.ai_engine import enrich_issue
import re

# -------------------- Knowledge Base --------------------

def explain_error(message):
    upper = message.upper()

    for rule in ERROR_RULES:
        if any(keyword in upper for keyword in rule["contains"]):
            return {
                "title": rule["title"],
                "meaning": rule["meaning"],
                "possible_cause": rule["possible_cause"],
                "qa_action": rule["qa_action"],
                "priority": rule["priority"],
                "category": rule["category"],
                "confidence": 100
            }

    return {
        "title": "Unknown System Error",
        "meaning": "",
        "possible_cause": "",
        "qa_action": "",
        "priority": "LOW",
        "category": "SYSTEM",
        "confidence": 0
    }


# -------------------- Error Patterns --------------------

ERROR_PATTERNS = [
    "ERROR",
    "FAILED",
    "FAILURE",
    "CRITICAL",
    "FATAL",
    "EXCEPTION",
    "HANDSHAKE FAILED",
    "CONNECTION BROKEN",
    "FAILED TO FETCH",
]

NOISE_PATTERNS = [
    "/assets/",
    ".js(#)",
    ".css(#)",
    "sourceMappingURL"
]


# -------------------- Helpers --------------------

def extract_timestamp(line):
    match = re.search(
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\.\d{3}",
        line,
    )
    return match.group(0) if match else None


def detect_severity(line):
    upper = line.upper()

    if "CRITICAL" in upper:
        return "CRITICAL"
    if "FATAL" in upper:
        return "FATAL"
    if "ERROR" in upper:
        return "ERROR"
    if "FAILED" in upper or "FAILURE" in upper:
        return "ERROR"
    if "EXCEPTION" in upper:
        return "ERROR"
    if "WARN" in upper:
        return "WARNING"

    return None


# -------------------- Detect Errors --------------------

def detect_errors(lines):
    errors = []

    for line_number, line in enumerate(lines, start=1):
        upper = line.upper()
        matched = None

        for pattern in ERROR_PATTERNS:
            if pattern in upper:
                matched = pattern
                break

        if matched:
            errors.append(
                {
                    "line_number": line_number,
                    "timestamp": extract_timestamp(line),
                    "severity": detect_severity(line),
                    "pattern": matched,
                    "message": line.strip(),
                }
            )

    return errors


# -------------------- Group Errors --------------------

def group_errors(errors):
    groups = {}

    for error in errors:
        msg = error["message"]

        # Remove timestamps
        msg = re.sub(
            r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s+\d{2}:\d{2}:\d{2}\.\d+\s+",
            "",
            msg,
        )

        # Normalize values
        msg = re.sub(r"<\d+>", "<#>", msg)
        msg = re.sub(r"\(\d+\.\d+\)", "(#)", msg)
        msg = re.sub(r"\(\d+\)", "(#)", msg)
        msg = re.sub(r"0x[0-9A-Fa-f]+", "0x#", msg)
        msg = re.sub(r"\b\d+\b", "#", msg)
        msg = re.sub(r"\s+", " ", msg).strip()

        # Skip noisy frontend logs
        if any(x.lower() in msg.lower() for x in NOISE_PATTERNS):
            continue

        key = (error["severity"], msg)

        info = explain_error(msg)

        if key not in groups:
            groups[key] = {
                "severity": error["severity"],
                "pattern": error["pattern"],
                "category": info["category"],
                "title": info["title"],
                "meaning": info["meaning"],
                "possible_cause": info["possible_cause"],
                "qa_action": info["qa_action"],
                "priority": info["priority"],
                "confidence": info["confidence"],
                "message": msg,
                "occurrences": 0,
                "first_line": error["line_number"],
                "last_line": error["line_number"],
                "timestamps": [],
                "line_numbers": [],
                "log_lines": [],
            }

        group = groups[key]

        group["occurrences"] += 1
        group["last_line"] = error["line_number"]

        if error["timestamp"]:
            group["timestamps"].append(error["timestamp"])

        group["line_numbers"].append(error["line_number"])

        group["log_lines"].append(
            {
                "line_number": error["line_number"],
                "timestamp": error["timestamp"],
                "message": error["message"],
            }
        )

    # ---------- AI ENRICHMENT ----------
    for group in groups.values():
        ai = enrich_issue(group["message"])

        if ai["confidence"] > 55:
            group["title"] = ai["title"]
            group["category"] = ai["category"]
            group["meaning"] = ai["meaning"]
            group["possible_cause"] = ai["possible_cause"]
            group["qa_action"] = ai["qa_action"]
            group["priority"] = ai["priority"]
            group["confidence"] = ai["confidence"]

    return sorted(
        groups.values(),
        key=lambda x: x["occurrences"],
        reverse=True,
    )


# -------------------- Summary --------------------

def generate_summary(grouped_errors):
    categories = {}

    for issue in grouped_errors:
        cat = issue["category"]
        categories[cat] = categories.get(cat, 0) + 1

    issues = []

    for i, issue in enumerate(grouped_errors, start=1):
        issues.append(
            {
                "id": i,
                "category": issue["category"],
                "severity": issue["severity"],
                "title": issue["title"],
                "meaning": issue["meaning"],
                "possible_cause": issue["possible_cause"],
                "qa_action": issue["qa_action"],
                "priority": issue["priority"],
                "confidence": issue["confidence"],
                "message": issue["message"],
                "occurrences": issue["occurrences"],
                "first_line": issue["first_line"],
                "last_line": issue["last_line"],
                "log_lines": issue["log_lines"],
            }
        )

    return {
        "unique_issues": len(grouped_errors),
        "categories": categories,
        "top_issues": issues,
    }