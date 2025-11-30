from pyod.models.iforest import IForest
from .agent import AgentState

def anomaly_detection_node(state):
    df=state["data"].select_dtypes(include="number")
    clf=IForest()
    clf.fit(df)
    labels=clf.predict(df)
    df['anomaly']=labels
    state["anomalies"]=df[df['anomaly']==1]
    state["preprocessing_steps"].append("anomaly_detected")
    return state