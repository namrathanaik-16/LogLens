import re
ERROR_PATTERNS=[
    "ERROR",
    "FAILED",
    "FAILURE",
    "CRITICAL",
    "FATAL",
    "EXCEPTION"
    "HANDSHAKE FAILED",
    "CONNECTION BROKEN",
    "FAILED TO FETCH",
]
def extract_timestamp(line):
    """
    Extract timestamp from LinuxTV log format.

    Example:
    Jun 17 07:32:12.847 LinuxTV ...
    """

    match=re.search(
         r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
         r"\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\.\d{3}",
         line
    )
    if match:
        return match.group(0)
    
    return None

def detect_severity(line):
    """
    Determine the severity of a log line.
    """

    upper_line=line.upper()
    if "CRITICAL" in upper_line:
        return "CRITICAL"
    if "FATAL" in upper_line:
        return "FATAL"
    if "ERROR" in upper_line:
        return "ERROR"
    if "FAILED" in upper_line or "FAILURE" in upper_line:
        return "ERROR"
    if "EXCEPTION" in upper_line:
        return "ERROR"
    if "WARN" is upper_line:
        return "WARNING"
    return None

def detect_errors(lines):
    """
    Scan the complete log and return structured error information.
    """
    errors=[]
    for line_number, line in enumerate(lines, start=1):
        upper_line=line.upper()
        matched_pattern=None
        for pattern in ERROR_PATTERNS:
            if pattern in upper_line:
                matched_pattern=pattern
                break
        if matched_pattern:
            errors.append({
                "line_number":line_number,
                "timestamp":extract_timestamp(line),
                "severity":detect_severity(line),
                "pattern":matched_pattern,
                "message":line.strip()
            })
    return errors
def group_errors(errors):
    groups = {}

    for error in errors:

        msg = error["message"]

        # Remove ANSI colors
        msg = re.sub(r'\x1b\[[0-9;]*m', '', msg)

        # Remove timestamp
        msg = re.sub(
            r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s+\d{2}:\d{2}:\d{2}\.\d{3}\s+',
            '',
            msg
        )

        # Keep only the actual message after the last colon
        if ":" in msg:
            msg = msg.split(":")[-1].strip()

        # Remove numbers
        msg = re.sub(r'\d+', '#', msg)

        # Remove multiple spaces
        msg = re.sub(r'\s+', ' ', msg).strip()

        key = (error["severity"], msg)

        if key not in groups:
            groups[key] = {
                "severity": error["severity"],
                "pattern": error["pattern"],
                "message": msg,
                "occurrences": 0,
                "first_line": error["line_number"],
                "last_line": error["line_number"],
                "timestamps": [],
                "line_numbers": []
            }

        group = groups[key]
        group["occurrences"] += 1
        group["last_line"] = error["line_number"]

        if error["timestamp"]:
            group["timestamps"].append(error["timestamp"])

        group["line_numbers"].append(error["line_number"])

    return sorted(
        groups.values(),
        key=lambda x: x["occurrences"],
        reverse=True
    )