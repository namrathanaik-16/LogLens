ERROR_RULES = [

    # ---------- NETWORK ----------
    {
        "contains": ["MONITOR_NEW_SESSION", "NETWORK CURL FAIL"],
        "title": "Network Connectivity Failure",
        "meaning": "Device failed the internet connectivity check.",
        "possible_cause": "DNS, gateway, or internet unavailable.",
        "qa_action": "Verify Ethernet/Wi-Fi and retry connectivity test.",
        "priority": "HIGH",
        "category": "NETWORK"
    },
    {
        "contains": ["IPV6", "INTERFACE NOT FOUND"],
        "title": "IPv6 Interface Missing",
        "meaning": "Requested network interface could not be found.",
        "possible_cause": "Network adapter unavailable.",
        "qa_action": "Check interface initialization.",
        "priority": "MEDIUM",
        "category": "NETWORK"
    },

    # ---------- PLAYBACK ----------
    {
        "contains": ["UNEXPECTED SOURCE TYPE"],
        "title": "Source Detection Error",
        "meaning": "TV failed to identify the current playback source.",
        "possible_cause": "Invalid HDMI or input state.",
        "qa_action": "Reconnect source and verify input selection.",
        "priority": "MEDIUM",
        "category": "PLAYBACK"
    },
    {
        "contains": ["FAST CHANNEL", "STREAM_ERROR"],
        "title": "FAST Channel Stream Failure",
        "meaning": "Streaming channel entered an error state.",
        "possible_cause": "Manifest or stream unavailable.",
        "qa_action": "Validate stream URL and playback.",
        "priority": "HIGH",
        "category": "PLAYBACK"
    },
    {
        "contains": ["WEBVTT", "UNKNOWN CODEC"],
        "title": "Subtitle Codec Unsupported",
        "meaning": "Adaptive streaming subtitle codec is unsupported.",
        "possible_cause": "Invalid WebVTT subtitle track.",
        "qa_action": "Validate subtitle codec in MPD/HLS manifest.",
        "priority": "LOW",
        "category": "PLAYBACK"
    },

    # ---------- AUDIO ----------
    {
        "contains": ["AAC DECODER FAILED", "AAC"],
        "title": "AAC Decode Error",
        "meaning": "AAC decoder failed during playback.",
        "possible_cause": "Corrupted audio stream.",
        "qa_action": "Verify AAC track and playback.",
        "priority": "HIGH",
        "category": "AUDIO"
    },

    # ---------- DRM ----------
    {
        "contains": ["WIDEVINE", "LICENSE"],
        "title": "Widevine DRM License Error",
        "meaning": "Widevine license acquisition failed.",
        "possible_cause": "License server unavailable.",
        "qa_action": "Verify DRM certificate and license server.",
        "priority": "HIGH",
        "category": "DRM"
    },

    # ---------- SYSTEM ----------
    {
        "contains": ["UPGRADESTATUS"],
        "title": "Firmware Upgrade Status Error",
        "meaning": "Firmware upgrade process returned an unexpected state.",
        "possible_cause": "Upgrade state machine mismatch.",
        "qa_action": "Validate firmware update sequence.",
        "priority": "MEDIUM",
        "category": "SYSTEM"
    },
    {
        "contains": ["MXTVR_CHANNELLIST_GETALLCHANNELSFORLIST", "INTERNAL BUFFER NULL"],
        "title": "Channel List Buffer Error",
        "meaning": "TV failed to retrieve the channel list because the internal buffer was null.",
        "possible_cause": "Channel database was not initialized correctly.",
        "qa_action": "Rescan channels and verify channel database.",
        "priority": "HIGH",
        "category": "SYSTEM"
    },

    {
        "contains": ["ONPLAYBACKEVENT", "TTUI_FASTCHANNEL"],
        "title": "FAST Channel Playback Event Error",
        "meaning": "Playback event failed while handling FAST channel streaming.",
        "possible_cause": "Streaming state transition failed.",
        "qa_action": "Validate playback event flow and FAST channel manifest.",
        "priority": "HIGH",
        "category": "PLAYBACK"
    },

    {
        "contains": ["TTUI_PICTURE_GETCURRENTSOURCE", "UNEXPECTED SOURCE TYPE"],
        "title": "Current Source Detection Failed",
        "meaning": "The TV could not determine the active input source.",
        "possible_cause": "Invalid HDMI or tuner source state.",
        "qa_action": "Verify source switching and TTUI Picture module.",
        "priority": "MEDIUM",
        "category": "PLAYBACK"
    },
]