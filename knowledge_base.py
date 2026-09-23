ERROR_RULES = [

    # ---------------- NETWORK ----------------

    {
        "contains": ["SSL", "HANDSHAKE"],
        "title": "SSL Handshake Failure",
        "category": "NETWORK",
        "priority": "HIGH",
        "meaning": "Secure HTTPS connection could not be established.",
        "possible_cause": "Internet instability or certificate validation failed.",
        "qa_action": "Verify Wi-Fi and retry HTTPS request."
    },

    {
        "contains": ["INTERFACENETWORKLINUX"],
        "title": "Network Interface Status",
        "category": "NETWORK",
        "priority": "LOW",
        "meaning": "Linux virtual interface status could not be read.",
        "possible_cause": "Kernel virtual interface inactive.",
        "qa_action": "Ignore unless primary interface also fails."
    },

    {
        "contains": ["NOT CONNECT AND RETURN"],
        "title": "Socket Connection Failed",
        "category": "NETWORK",
        "priority": "MEDIUM",
        "meaning": "Remote socket connection was unavailable.",
        "possible_cause": "Server unreachable.",
        "qa_action": "Check network connectivity."
    },

    {
        "contains": ["FAILED TO FETCH"],
        "title": "HTTP Fetch Failed",
        "category": "NETWORK",
        "priority": "HIGH",
        "meaning": "HTTP resource download failed.",
        "possible_cause": "Network timeout.",
        "qa_action": "Reproduce with stable internet."
    },

    # ---------------- SYSTEM ----------------

    {
        "contains": ["MI_SYS_GETCONFIGDATA"],
        "title": "System Configuration Failure",
        "category": "SYSTEM",
        "priority": "MEDIUM",
        "meaning": "Configuration service failed.",
        "possible_cause": "Middleware initialization issue.",
        "qa_action": "Check boot sequence."
    },

    {
        "contains": ["OPAPPKEYHANDLER"],
        "title": "Application Key Handler Error",
        "category": "SYSTEM",
        "priority": "MEDIUM",
        "meaning": "Key event handler reported an invalid state.",
        "possible_cause": "Application state mismatch.",
        "qa_action": "Reproduce using the same key sequence."
    },

    {
        "contains": ["UPGRADESTATUS"],
        "title": "Upgrade Status Error",
        "category": "SYSTEM",
        "priority": "LOW",
        "meaning": "Unexpected firmware upgrade state detected.",
        "possible_cause": "Background OTA process.",
        "qa_action": "Verify OTA status."
    },

    {
        "contains": ["NO_ERR"],
        "title": "False Error Flag",
        "category": "SYSTEM",
        "priority": "LOW",
        "meaning": "Error log contains NO_ERR state.",
        "possible_cause": "Informational message.",
        "qa_action": "Can usually be ignored."
    },

    # ---------------- DRM ----------------

    {
        "contains": ["WIDEVINE", "CERT1.BIN"],
        "title": "Widevine Certificate Missing",
        "category": "DRM",
        "priority": "HIGH",
        "meaning": "Required Widevine certificate file is missing.",
        "possible_cause": "DRM provisioning incomplete.",
        "qa_action": "Verify Widevine certificates."
    },

    {
        "contains": ["WIDEVINE", "LICENSE"],
        "title": "Widevine License Failure",
        "category": "DRM",
        "priority": "HIGH",
        "meaning": "DRM license validation failed.",
        "possible_cause": "License server communication failed.",
        "qa_action": "Check DRM provisioning."
    },

    {
        "contains": ["DRM"],
        "title": "DRM Runtime Error",
        "category": "DRM",
        "priority": "MEDIUM",
        "meaning": "Protected playback encountered an error.",
        "possible_cause": "Content protection issue.",
        "qa_action": "Reproduce using DRM content."
    },

    # ---------------- PLAYBACK ----------------

    {
        "contains": ["SENDTOUCS FAILED"],
        "title": "Audio Playback Pipeline Failure",
        "category": "PLAYBACK",
        "priority": "HIGH",
        "meaning": "Audio pipeline failed to send data.",
        "possible_cause": "Audio framework communication failure.",
        "qa_action": "Verify playback and audio HAL."
    },

    {
        "contains": ["DECODER"],
        "title": "Video Decoder Error",
        "category": "PLAYBACK",
        "priority": "HIGH",
        "meaning": "Video decoder encountered an error.",
        "possible_cause": "Corrupted stream.",
        "qa_action": "Replay the same video."
    },

    {
        "contains": ["BUFFER"],
        "title": "Playback Buffer Underflow",
        "category": "PLAYBACK",
        "priority": "MEDIUM",
        "meaning": "Playback buffer emptied unexpectedly.",
        "possible_cause": "Slow streaming.",
        "qa_action": "Check bandwidth."
    },

    {
        "contains": ["MANIFEST"],
        "title": "Streaming Manifest Error",
        "category": "PLAYBACK",
        "priority": "HIGH",
        "meaning": "Manifest parsing failed.",
        "possible_cause": "Invalid DASH/HLS manifest.",
        "qa_action": "Verify streaming URL."
    },

    # ---------------- AUDIO ----------------

    {
        "contains": ["SETVOLUME"],
        "title": "Audio Volume Event",
        "category": "AUDIO",
        "priority": "LOW",
        "meaning": "Volume controller received an update.",
        "possible_cause": "User or system volume change.",
        "qa_action": "Informational only."
    },

    {
        "contains": ["AAC"],
        "title": "AAC Decode Error",
        "category": "AUDIO",
        "priority": "MEDIUM",
        "meaning": "AAC decoder failed.",
        "possible_cause": "Unsupported audio stream.",
        "qa_action": "Verify audio codec."
    },

    {
        "contains": ["PCM"],
        "title": "PCM Audio Error",
        "category": "AUDIO",
        "priority": "MEDIUM",
        "meaning": "PCM pipeline encountered an error.",
        "possible_cause": "Audio routing issue.",
        "qa_action": "Check speaker output."
    },

    # ---------------- HDMI ----------------

    {
        "contains": ["HDMI", "EDID"],
        "title": "HDMI EDID Failure",
        "category": "HDMI",
        "priority": "HIGH",
        "meaning": "TV failed to read HDMI capabilities.",
        "possible_cause": "EDID negotiation failed.",
        "qa_action": "Reconnect HDMI source."
    },

    {
        "contains": ["HDCP"],
        "title": "HDCP Authentication Failed",
        "category": "HDMI",
        "priority": "HIGH",
        "meaning": "Copy protection handshake failed.",
        "possible_cause": "HDCP mismatch.",
        "qa_action": "Reconnect HDMI cable."
    },

    # ---------------- AIRPLAY ----------------

    {
        "contains": ["AIRPLAY"],
        "title": "AirPlay Session Error",
        "category": "AIRPLAY",
        "priority": "MEDIUM",
        "meaning": "AirPlay session failed.",
        "possible_cause": "Wireless instability.",
        "qa_action": "Reconnect iPhone."
    }

]