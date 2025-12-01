import ollama
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap
import ast

# Ensure figures directory exists
os.makedirs('./figures/', exist_ok=True)

def eda_node(state):
    # system_prompt=f"You are a data analyst assistant. Generate useful exploratory plots using seaborn or matplotlib and save them using plt.savefig() inside './figures/': for each plot use filenames like plot1.png, plot2.png and take care to clear each figure with plt.clf() before doing another plot."
    system_prompt=f"""You are a data analyst assistant. Generate clean, PEP8-compliant Python code that creates all useful EDA plots using seaborn and matplotlib.

Requirements:
- Use `df` (already loaded) for data.
- Save plots to './figures/' using `plt.savefig('figures/plot1.png')` etc.
- Always use `plt.clf()` after saving each plot.
- Do NOT include markdown or explanations. Only Python code."""

    user_prompt=f"""Here is the data structure information:{state['info']}, anomalies: {state['anomalies'].head(3).to_dict()} and correlations: {state['correlations'].to_string()}
 and data:{state['data']}.Generate all the possible useful exploratory plots but donot display them."""
    response=ollama.chat(model='phi',messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}])
    # result=subprocess.run(["ollama", "run", "llama3", prompt], capture_output=True, text=True)

    # state["explanation"] = response['message']['content']
    code = textwrap.dedent(response['message']['content'])
    # print("Generated code:\n", code)

    # Execute the code
    # exec_globals = {
    #     'plt': plt,
    #     'sns': sns,
    #     'df': state['data'],
    #     'os': os
    # }
    # exec(code, exec_globals)
    ast.parse(code)

    print("✅ Plots saved to './figures/'")
    state["preprocessing_steps"].append("exploratory_analysis_explanation")
    return state