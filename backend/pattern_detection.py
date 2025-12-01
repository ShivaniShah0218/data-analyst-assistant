from .agent import AgentState

def pattern_detection_node(state):
    df=state["data"].select_dtypes(include="number")
    correlation=df.corr()
    state["correlations"]=correlation
    state["preprocessing_steps"].append("pattern_detection")
    return state