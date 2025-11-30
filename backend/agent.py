from typing import TypedDict, List, Any, Dict

class AgentState(TypedDict):
    file_path: str
    data: Any
    preprocessing_steps: List[str]
    info: List[Dict[str,Any]]
    error_message: str
    anomalies: Any
    correlations: Any
    explanation: str