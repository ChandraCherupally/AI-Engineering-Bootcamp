from mcp.server.fastmcp import FastMCP
import os
import psutil
import platform
import shutil

# Initialize FastMCP Server
mcp = FastMCP("SystemUtility")

@mcp.tool()
def get_system_info() -> dict:
    """Gets general operating system, CPU architecture, and processor details."""
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "python_version": platform.python_version()
    }

@mcp.tool()
def get_cpu_memory_usage() -> dict:
    """Gets the current overall CPU percentage usage and system virtual memory statistics."""
    mem = psutil.virtual_memory()
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "memory_total_gb": round(mem.total / (1024**3), 2),
        "memory_available_gb": round(mem.available / (1024**3), 2),
        "memory_percent_used": mem.percent
    }

@mcp.tool()
def list_directory(path: str = ".") -> list:
    """Lists the files and folders inside the specified directory path."""
    resolved_path = os.path.abspath(path)
    if not os.path.exists(resolved_path):
        return [f"Error: Path '{path}' does not exist."]
    if not os.path.isdir(resolved_path):
        return [f"Error: Path '{path}' is not a directory."]
    
    items = []
    try:
        for entry in os.scandir(resolved_path):
            info = {
                "name": entry.name,
                "is_directory": entry.is_dir(),
                "size_bytes": entry.stat().st_size if entry.is_file() else None
            }
            items.append(info)
    except Exception as e:
        return [f"Error reading directory: {str(e)}"]
    return items

@mcp.tool()
def get_disk_usage(path: str = ".") -> dict:
    """Gets disk space statistics (total, used, free) for the volume containing the specified path."""
    resolved_path = os.path.abspath(path)
    try:
        usage = shutil.disk_usage(resolved_path)
        return {
            "total_gb": round(usage.total / (1024**3), 2),
            "used_gb": round(usage.used / (1024**3), 2),
            "free_gb": round(usage.free / (1024**3), 2),
            "percent_used": round((usage.used / usage.total) * 100, 1)
        }
    except Exception as e:
        return {"error": f"Error reading disk usage: {str(e)}"}



if __name__ == "__main__":
    mcp.run(transport="stdio")
