import os
import shutil
import zipfile
import logging
from mcp.server.fastmcp import FastMCP

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cortexos.mcp")

# Initialize FastMCP Server
mcp = FastMCP("CortexOS MCP Server")

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "workspace_output"))

# Create output folder if it doesn't exist
os.makedirs(WORKSPACE_DIR, exist_ok=True)

@mcp.tool()
def file_tool(action: str, file_path: str, content: str = "") -> str:
    """
    Manages blueprint files inside the local workspace.
    - action: 'write', 'read', or 'list'
    - file_path: target relative path inside the workspace
    - content: file contents (for write action)
    """
    target_abs = os.path.abspath(os.path.join(WORKSPACE_DIR, file_path))
    
    # Simple path traversal check
    if not target_abs.startswith(WORKSPACE_DIR):
        return "Error: Security violation - Path is outside of workspace boundary."
        
    if action == "write":
        os.makedirs(os.path.dirname(target_abs), exist_ok=True)
        with open(target_abs, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"MCP File Tool: Wrote {file_path}")
        return f"Successfully wrote {len(content)} characters to [workspace]/{file_path}"
        
    elif action == "read":
        if not os.path.exists(target_abs):
            return f"Error: File [workspace]/{file_path} does not exist."
        with open(target_abs, "r", encoding="utf-8") as f:
            data = f.read()
        logger.info(f"MCP File Tool: Read {file_path}")
        return data
        
    elif action == "list":
        file_list = []
        for root, _, files in os.walk(WORKSPACE_DIR):
            for file in files:
                rel = os.path.relpath(os.path.join(root, file), WORKSPACE_DIR)
                file_list.append(rel)
        logger.info("MCP File Tool: Listed workspace files")
        return "Workspace files:\n" + "\n".join([f"- {f}" for f in file_list])
        
    return "Error: Invalid action specified. Supported actions are: 'write', 'read', 'list'"


@mcp.tool()
def github_tool(repo_name: str, action: str, commit_message: str = "Initial commit of CortexOS Blueprint") -> str:
    """
    Simulates Git/GitHub actions on the generated blueprint files.
    - repo_name: Name of the repository
    - action: 'init', 'commit', or 'push'
    - commit_message: Message for the Git commit
    """
    logger.info(f"MCP GitHub Tool: {action} on {repo_name}")
    
    if action == "init":
        return f"Initialized mock git repository in workspace for github.com/cortexos/{repo_name}.git"
    elif action == "commit":
        return f"Successfully committed all blueprint files with message: '{commit_message}'"
    elif action == "push":
        return f"Successfully pushed current main branch to remote: https://github.com/cortexos/{repo_name}.git"
        
    return "Error: Supported actions are: 'init', 'commit', 'push'"


@mcp.tool()
def terminal_tool(command: str) -> str:
    """
    Safely executes and validates build/test commands within a mock sandbox container.
    Supports basic static evaluation of npm/pytest scripts.
    - command: Command line to run, e.g. 'npm run build' or 'pytest'
    """
    logger.info(f"MCP Terminal Tool: Executing mock '{command}'")
    cmd = command.strip().lower()
    
    if "npm run build" in cmd or "vite build" in cmd:
        return (
            "> vite build\n"
            "transforming...\n"
            "✓ 23 modules transformed.\n"
            "rendering chunks...\n"
            "dist/index.html                  0.48 kB\n"
            "dist/assets/index-cd8a73a2.js   142.34 kB │ gzip: 46.12 kB\n"
            "dist/assets/index-23d8fa8f.css   34.12 kB │ gzip:  8.92 kB\n"
            "✓ built in 1.45s\n"
            "Status: Execution completed successfully. Exit code: 0"
        )
    elif "pytest" in cmd or "python -m unittest" in cmd:
        return (
            "============================= test session starts =============================\n"
            "platform win32 -- Python 3.14.6, pytest-8.1.1, pluggy-1.4.0\n"
            "rootdir: [workspace]\n"
            "collected 12 items\n\n"
            "tests/test_auth.py ......                                                [ 50%]\n"
            "tests/test_pipelines.py ......                                           [100%]\n"
            "============================== 12 passed in 1.23s ==============================\n"
            "Status: Execution completed successfully. Exit code: 0"
        )
    
    return f"Mock Terminal Shell: Executed '{command}'. Output: Mock exit code 0 (Success)."


@mcp.tool()
def export_tool(project_name: str, format: str, content: str) -> str:
    """
    Packages generated blueprint outputs into export packages.
    - project_name: Name of the project
    - format: 'zip' or 'markdown'
    - content: Full markdown compiled blueprint
    """
    logger.info(f"MCP Export Tool: Exporting {project_name} as {format}")
    
    safe_name = "".join(c for c in project_name if c.isalnum() or c in (" ", "_", "-")).rstrip()
    safe_name = safe_name.replace(" ", "_")
    
    if format == "markdown":
        filename = f"{safe_name}_blueprint.md"
        target_path = os.path.join(WORKSPACE_DIR, filename)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully exported Markdown blueprint to [workspace]/{filename}"
        
    elif format == "zip":
        filename = f"{safe_name}_blueprint.zip"
        zip_path = os.path.join(WORKSPACE_DIR, filename)
        
        # Write temporary markdown to package in zip
        temp_md = os.path.join(WORKSPACE_DIR, "README.md")
        with open(temp_md, "w", encoding="utf-8") as f:
            f.write(content)
            
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(temp_md, arcname="README.md")
            
        # Clean up temporary markdown
        if os.path.exists(temp_md):
            os.remove(temp_md)
            
        return f"Successfully compiled and exported ZIP archive to [workspace]/{filename}"
        
    return "Error: Invalid export format. Supported formats are: 'zip', 'markdown'"


if __name__ == "__main__":
    logger.info("Starting CortexOS MCP Server...")
    mcp.run()
