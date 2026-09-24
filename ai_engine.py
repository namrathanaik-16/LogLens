from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Fast embedding model
model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

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
        "text": "ipv6 interface unavailable network adapter initialization",
        "meaning": "IPv6 interface could not be initialized.",
        "impact": "Network discovery may be unstable.",
        "qa": "Check network adapter initialization."
    },
    {
        "title": "FAST Channel Playback Error",
        "category": "PLAYBACK",
        "text": "fast channel playback stream manifest onplaybackevent",
        "meaning": "Playback pipeline entered an invalid streaming state.",
        "impact": "Video may freeze or fail to start.",
        "qa": "Validate playback events and MPD manifest."
    },
    {
        "title": "Source Detection Error",
        "category": "PLAYBACK",
        "text": "unexpected source type hdmi tuner current source",
        "meaning": "TV failed to determine the active source.",
        "impact": "Incorrect source selection or black screen.",
        "qa": "Verify HDMI/source switching."
    },
    {
        "title": "Channel List Buffer Error",
        "category": "SYSTEM",
        "text": "channel list internal buffer null getallchannels",
        "meaning": "Channel database returned a null buffer.",
        "impact": "Channel list cannot load.",
        "qa": "Rescan channels and validate database."
    },
    {
        "title": "Widevine DRM License Error",
        "category": "DRM",
        "text": "widevine drm license certificate provisioning",
        "meaning": "Widevine license acquisition failed.",
        "impact": "Protected content cannot play.",
        "qa": "Verify DRM certificate and license server."
    },
    {
        "title": "AAC Decode Error",
        "category": "AUDIO",
        "text": "aac decoder audio pcm codec failed",
        "meaning": "AAC decoder failed during playback.",
        "impact": "Playback may continue without audio.",
        "qa": "Validate AAC audio track."
    }
]

kb_vectors = model.encode(
    [k["text"] for k in KB],
    normalize_embeddings=True
)

def enrich_issue(message):
    """
    AI enrichment for ONE grouped issue.
    """

    vec = model.encode(
        [message],
        normalize_embeddings=True
    )

    scores = cosine_similarity(vec, kb_vectors)[0]
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
        "priority": "HIGH" if score > 0.82 else "MEDIUM"
    }