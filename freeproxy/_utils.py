from typing import Dict, Optional


def build_headers(api_key: str, user_agent: Optional[str] = None) -> Dict[str, str]:
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    if user_agent:
        headers["User-Agent"] = user_agent
    return headers


def extract_error_message(body_text: str, json_body: Optional[Dict] = None) -> str:
    if json_body:
        if isinstance(json_body, dict):
            if "error" in json_body:
                return str(json_body.get("error"))
            if "message" in json_body:
                return str(json_body.get("message"))
            for k in ("detail", "code"):
                if k in json_body:
                    return str(json_body.get(k))
    return body_text or "Unknown error"
