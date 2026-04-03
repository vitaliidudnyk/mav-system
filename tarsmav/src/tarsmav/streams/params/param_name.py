def normalize_param_name(name: str | bytes) -> str:
    if isinstance(name, bytes):
        raw = name
    else:
        raw = str(name).encode("utf-8")

    return raw[:16].decode("utf-8", errors="ignore").rstrip("\x00")