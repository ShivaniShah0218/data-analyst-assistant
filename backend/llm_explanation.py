import ollama


def llm_explanation_node(state):
    system_prompt="""You are a data analyst assistant.

Given the structure of a dataset, anomalies, correlations, suggest the following:

1. A list of useful **visualizations** for creating a data dashboard. Include:
   - the chart type (e.g., bar, line, heatmap),
   - the relevant columns,
   - the insight each visualization is intended to reveal.

2. Potential **predictive analysis tasks** that could be built on this dataset. Include:
   - the target variable,
   - the type of ML task (e.g., classification, regression),
   - the business question it answers.

Respond in structured JSON format like:

{
  "visualizations": [
    {
      "type": "bar chart",
      "columns": ["department", "total_sales"],
      "insight": "Compare total sales across departments"
    },
    ...
  ],
  "predictive_analysis": [
    {
      "target": "churn",
      "task_type": "classification",
      "question": "Which customers are likely to churn?"
    },
    ...
  ]
}

"""
    user_prompt=f"""Here is the data structure information:{state['info']}, anomalies: {state['anomalies'].head(3).to_dict()} and correlations: {state['correlations'].to_string()}.Based on this, suggest:
1. Useful visualizations for building an interactive dashboard.
2. Predictive analysis tasks (classification/regression) and target columns.
Return the output as JSON with two keys: 'visualizations' and 'predictive_analysis'(No code No explanation)."""
    response=ollama.chat(model='phi',messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}])
    # result=subprocess.run(["ollama", "run", "llama3", prompt], capture_output=True, text=True)

    state["explanation"] = response['message']['content']
    state["preprocessing_steps"].append("dataanalyst_agent_explanation")
    return state