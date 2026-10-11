"""麦当劳 MCP 通用客户端 (Streamable HTTP JSON-RPC)."""
import json
import os
import urllib.request

MCP_URL = os.environ.get("MCD_MCP_URL", "https://mcp.mcd.cn")
TOKEN = os.environ.get("MCD_MCP_TOKEN", "")


def rpc(method, params=None, session=None, timeout=30):
    body = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    ).encode()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": f"Bearer {TOKEN}",
    }
    if session:
        headers["Mcp-Session-Id"] = session
    req = urllib.request.Request(MCP_URL, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", "replace")
        new_session = resp.headers.get("Mcp-Session-Id") or session
    try:
        return json.loads(raw), new_session
    except json.JSONDecodeError:
        for line in raw.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                try:
                    return json.loads(line[5:].strip()), new_session
                except json.JSONDecodeError:
                    continue
    raise RuntimeError(f"无法解析 MCP 返回: {raw[:200]}")


def extract_payload(result):
    """从 tools/call 结果里抠出业务 JSON (兼容"说明文字+JSON"混排)."""
    if isinstance(result, dict) and "structuredContent" in result:
        return result["structuredContent"]
    texts = []
    if isinstance(result, dict):
        for p in result.get("content", []):
            if isinstance(p, dict) and p.get("type") == "text":
                texts.append(p.get("text", ""))
    text = "".join(texts)
    for marker in ('{"success"', '{"code"', '"data"'):
        i = text.find(marker)
        if i >= 0:
            start = text.rfind("{", 0, i + 1)
            try:
                return json.loads(text[start if start >= 0 else i:])
            except json.JSONDecodeError:
                continue
    return json.loads(text)


def connect():
    if not TOKEN:
        raise RuntimeError("缺少 MCD_MCP_TOKEN 环境变量")
    _, session = rpc("initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "mcd-maimen-trial", "version": "0.1.0"},
    })
    try:
        rpc("notifications/initialized", {}, session)
    except Exception:
        pass
    return session


def call_tool(session, name, arguments):
    data, session = rpc("tools/call",
                        {"name": name, "arguments": arguments}, session)
    if "error" in data:
        raise RuntimeError(f"工具 {name} 报错: {data['error']}")
    return extract_payload(data.get("result", {})), session
