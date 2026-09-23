from analyzers.knowledge_base import ERROR_RULES
import re


# -------------------- Knowledge Base --------------------

def explain_error(message):
    upper_msg = message.upper()

    for rule in ERROR_RULES:
        if any(keyword in upper_msg for keyword in rule["contains"]):
            return {
                "title": rule["title"],
                "meaning": rule["meaning"],
                "possible_cause": rule["possible_cause"],
                "qa_action": rule["qa_action"],
                "priority": rule["priority"],
                "category": rule["category"]
            }

    return {
        "title": "Unknown System Error",
        "meaning": "No explanation available yet.",
        "possible_cause": "Unknown",
        "qa_action": "Inspect the original log.",
        "priority": "LOW",
        "category": "SYSTEM"
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
        line
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
            errors.append({
                "line_number": line_number,
                "timestamp": extract_timestamp(line),
                "severity": detect_severity(line),
                "pattern": matched,
                "message": line.strip()
            })

    return errors


# -------------------- Group Errors --------------------

def group_errors(errors):

    groups = {}

    for error in errors:

        original_msg = error["message"].strip()

        # Ignore unwanted frontend asset logs
        if any(p.lower() in original_msg.lower() for p in NOISE_PATTERNS):
            continue

        # Message used ONLY for grouping
        clean_msg = original_msg

        # Remove timestamps
        clean_msg = re.sub(
            r'^(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s+\d{2}:\d{2}:\d{2}\.\d+\s+',
            '',
            clean_msg
        )

        clean_msg = re.sub(
            r'^\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+\s+',
            '',
            clean_msg
        )

        # Remove thread IDs / process IDs
        clean_msg = re.sub(r'<\d+>', '<#>', clean_msg)
        clean_msg = re.sub(r'\(\d+\.\d+\)', '(#)', clean_msg)
        clean_msg = re.sub(r'\(\d+\)', '(#)', clean_msg)

        # Normalize values
        clean_msg = re.sub(r'ERR=\d+', 'ERR=#', clean_msg)
        clean_msg = re.sub(r'0x[0-9A-Fa-f]+', '0x#', clean_msg)
        clean_msg = re.sub(r'\b\d+\b', '#', clean_msg)
        
        clean_msg = re.sub(r'\s+', ' ', clean_msg).strip()

        key = (error["severity"], clean_msg)      # Used for grouping
        info = explain_error(original_msg)  

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

            # Show the ORIGINAL log text in the UI
                "message": original_msg,

                "occurrences": 0,
                "first_line": error["line_number"],
                "last_line": error["line_number"],
                "timestamps": [],
                "line_numbers": [],
                "log_lines": []
            }

        group = groups[key]

        group["occurrences"] += 1
        group["last_line"] = error["line_number"]

        if error["timestamp"]:
            group["timestamps"].append(error["timestamp"])

        group["line_numbers"].append(error["line_number"])

        # Original log lines for Log Inspector
        group["log_lines"].append({
            "line_number": error["line_number"],
            "timestamp": error["timestamp"],
            "message": original_msg
        })

    return sorted(
        groups.values(),
        key=lambda x: x["occurrences"],
        reverse=True
    )


# -------------------- Summary --------------------

def generate_summary(grouped_errors):

    categories = {}

    for issue in grouped_errors:
        cat = issue["category"]
        categories[cat] = categories.get(cat, 0) + 1

    issues = []

    for i, issue in enumerate(grouped_errors, start=1):
        issues.append({
            "id": i,
            "category": issue["category"],
            "severity": issue["severity"],
            "title": issue["title"],
            "meaning": issue["meaning"],
            "possible_cause": issue["possible_cause"],
            "qa_action": issue["qa_action"],
            "priority": issue["priority"],
            "message": issue["message"],
            "occurrences": issue["occurrences"],
            "first_line": issue["first_line"],
            "last_line": issue["last_line"],
            "log_lines": issue["log_lines"]
        })

    return {
        "unique_issues": len(grouped_errors),
        "categories": categories,
        "top_issues": issues
    }