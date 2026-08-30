import sys
from pathlib import Path

REPO_PATH: Path = Path(__file__).parent.parent
SCRIPTS_PATH: Path = REPO_PATH / "scripts"

sys.path.append(str(SCRIPTS_PATH))

COMMENT_USER = "github-actions"
