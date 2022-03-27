from utils.logger import log
from requests import get

def database_fixer(cwd: str) -> None:
    """Re-downloads the database if it is corrupt.

    Args:
        cwd (str): The current working directory.
        
    Returns:
        None
    """
    
    log(None, "WARNING", "Database file is corrupted. Re-downloading now.")
    
    req = get("https://raw.githubusercontent.com/didlly/grank/main/src/database.json", allow_redirects=True).content
    
    log(None, "DEBUG", "Retreived new database file.")
    
    with open(f"{cwd}database.json", "wb") as db:
        log(None, "DEBUG", f"Opened `{cwd}database.json`.")
        db.write(req)
        log(None, "DEBUG", f"Wrote new database to `{cwd}database.json`.")
        
    log(None, "DEBUG", f"Closed `{cwd}database.json`.")