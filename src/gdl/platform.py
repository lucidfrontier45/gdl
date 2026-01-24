"""Platform detection and synonym mappings."""

import platform

os_synonyms: dict[str, tuple[str, ...]] = {
    "windows": ("windows", "win32"),
    "linux": ("linux",),
    "macos": ("macos", "mac", "darwin"),
}

arch_synonyms: dict[str, tuple[str, ...]] = {
    "x86_64": ("x86_64", "x64", "amd64"),
    "aarch64": ("aarch64", "arm64"),
}


def get_host_os() -> str:
    """Return normalized host OS: one of 'linux', 'windows', 'macos'."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system in ("windows", "linux"):
        return system
    else:
        raise ValueError(f"Unsupported OS: {system}")


def get_host_arch() -> str:
    """Return normalized host architecture: 'x86_64' or 'aarch64'."""
    machine = platform.machine().lower()
    arch_map = {
        "amd64": "x86_64",
        "x86_64": "x86_64",
        "x64": "x86_64",
        "aarch64": "aarch64",
        "arm64": "aarch64",
    }
    if machine in arch_map:
        return arch_map[machine]
    else:
        raise ValueError(f"Unsupported architecture: {machine}")
