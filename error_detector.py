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
NOISE_PATTERNS=[
    "/assets/",
    ".js(#)",
    ".css(#)",
    "sourceMappingURL"
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
    if "WARN" == upper_line:
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
def categorize_error(message):
    """
    Categorise smart TV errors into subsystem
    """
    msg=message.upper() 

    #network
    if any(word in msg for word in[
        "SSL","HTTP","FETCH","SOCKET","NETWORK",
        "HANDSHAKE","DNS","CONNECT"
    ]):
        return "NETWORK"
    #playback
    if any(word in msg for word in[
        "BUFFER","BITRATE","MANIFEST","DASH",
        "PLAYBACK","SEGMENT","VAST"
    ]):
        return "PLAYBACK"
    
    #Audio
    if any(word in msg for word in[
        "AUDIO","AAC","PCM","SPEAKER","VOLUME"
    ]):
        return "AUDIO"

    #DRM
    if any(word in msg for word in[
        "DRM","WIDEVINE","LICENSE","ISSUER"
    ]):
        return "DRM"
    
    #bluetooth
    if any(word in msg for word in[
        "BLUETOOTH","BT_","BLUEDROID"
    ]):
        return "BLUETOOTH"
    return "System"

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

        #Normal thread IDs
        msg=re.sub(r'tid\d+', 'tid', msg)

        #Normalize process IDs
        msg=re.sub(r'pid\d+', 'pid', msg)

        #Normalize ERR values
        msg=re.sub(r'ERR=\d+', 'ERR=#', msg)

        #Normalize numbers inside brackets only
        msg=re.sub(r'\[\d+\]', '[#]', msg)

        #Normalize standalone file indexes like (123)
        msg=re.sub(r'\(\d+\)', '(#)', msg)

        #clean spaces
        msg=re.sub(r'\s+', ' ', msg).strip()

        print(type(msg),msg)
        key = (error["severity"], str(msg))

        if any(pattern in msg for pattern in NOISE_PATTERNS):
            continue

        if key not in groups:
            groups[key] = {
                "severity": error["severity"],
                "pattern": error["pattern"],
                "category":categorize_error(msg),
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

def generate_summary(grouped_errors):

    categories = {}

    for issue in grouped_errors:
        cat = issue["category"]
        categories[cat] = categories.get(cat, 0) + 1

    top_issues = []

    for i, issue in enumerate(grouped_errors[:10], start=1):
        top_issues.append({
            "id": i,
            "category": issue["category"],
            "severity": issue["severity"],
            "message": issue["message"],
            "occurrences": issue["occurrences"],
            "first_line": issue["first_line"],
            "last_line": issue["last_line"]
        })

    return {
        "unique_issues": len(grouped_errors),
        "categories": categories,
        "top_issues": top_issues
    }