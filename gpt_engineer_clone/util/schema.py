from typing import Dict, List, TypedDict
from dataclasses import dataclass

class FilePlan(TypedDict):
    path: str
    description: str

class FileDraft(TypedDict):
    path: str
    content: str

class BuildState(TypedDict, total=False):
    user_prompt: str                    # raw user brief
    clarified_requirements: str         # interpreted/expanded brief
    file_plan: List[FilePlan]           # planned files
    drafts: List[FileDraft]             # generated file contents
    out_dir: str                        # output folder
    meta: Dict[str, str]                # misc telemetry

@dataclass
class Settings:
    model: str = "gpt-4.1"
    temperature: float = 0.2