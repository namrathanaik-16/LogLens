from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# -------------------- AI MODEL --------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------- KNOWLEDGE BASE --------------------

KB = [
    {
        "title": "Network Connectivity Failure",
        "category": "NETWORK",
        "text": "network curl fail internet dns gateway ethernet wifi connectivity",
        "meaning": "Device failed internet connectivity validation.",
        "impact": "Streaming apps and FAST channels may fail.",
        "qa": "Verify Ethernet/Wi-Fi, DNS and gateway."
    },
    {
        "title": "IPv6 Interface Missing",
        "category": "NETWORK",
        "text": "ipv6 interface unavailable network adapter initialization interface not found p2p1",
        "meaning": "Requested network interface could not be found.",
        "impact": "Network discovery and streaming may fail.",
        "qa": "Check IPv6 adapter initialization and network configuration."
    },
    {
        "title": "FAST Channel Playback Event Error",
        "category": "PLAYBACK",
        "text": "fast channel playback onplaybackevent streaming event",
        "meaning": "Playback event failed while handling FAST channel streaming.",
        "impact": "Video may freeze or fail to start.",
        "qa": "Validate playback events and MPD manifest."
    },
    {
        "title": "FAST Channel Stream Failure",
        "category": "PLAYBACK",
        "text": "fast channel receive stream status stream error stream_state",
        "meaning": "Streaming channel entered an error state.",
        "impact": "FAST channel playback becomes unavailable.",
        "qa": "Inspect stream status, manifest and CDN connectivity."
    },
    {
        "title": "Channel List Buffer Error",
        "category": "SYSTEM",
        "text": "channel list internal buffer null getallchannels mxtvr channel list",
        "meaning": "Channel database returned a null buffer.",
        "impact": "TV failed to retrieve the channel list.",
        "qa": "Rescan channels and validate channel database."
    },
    {
        "title": "Source Detection Error",
        "category": "PLAYBACK",
        "text": "unexpected source type getcurrentsource hdmi tuner picture source",
        "meaning": "TV failed to determine the active source.",
        "impact": "Incorrect source selection or black screen.",
        "qa": "Verify HDMI/source switching."
    },
    {
        "title": "AAC Decode Error",
        "category": "AUDIO",
        "text": "aac decoder audio pcm codec failed",
        "meaning": "AAC decoder failed during playback.",
        "impact": "Playback may continue without audio.",
        "qa": "Validate AAC audio track."
    },
    {
        "title": "Widevine DRM License Error",
        "category": "DRM",
        "text": "widevine drm license provisioning certificate",
        "meaning": "Widevine license acquisition failed.",
        "impact": "Protected content cannot play.",
        "qa": "Verify DRM certificate and license server."
    }
]

# -------------------- PRECOMPUTE EMBEDDINGS --------------------

EMBEDDINGS = model.encode(
    [item["text"] for item in KB],
    normalize_embeddings=True
)

# -------------------- AI CLASSIFICATION --------------------

def enrich_issue(message):
    query = model.encode(
        [message],
        normalize_embeddings=True
    )

    scores = cosine_similarity(query, EMBEDDINGS)[0]

    idx = int(np.argmax(scores))
    score = float(scores[idx])

    best = KB[idx]

    return {
        "title": best["title"],
        "category": best["category"],
        "meaning": best["meaning"],
        "possible_cause": best["impact"],
        "qa_action": best["qa"],
        "confidence": round(score * 100, 1),
        "priority": "HIGH" if score >= 0.80 else "MEDIUM"
    }