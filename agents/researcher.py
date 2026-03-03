from langchain_google_genai import ChatGoogleGenerativeAI
from config import MODEL_NAME, GOOGLE_API_KEY


def researcher_node(state):
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
    )
    
    adaptive_prompt = state.get('adaptive_prompt', '')
    
    prompt = f"""You are a market researcher.

{adaptive_prompt}

Context:
{state['context']}

Query: {state['query']}

Summarize key insights with focus on:
- Macro factors
- Sector dynamics
- Risk factors
- Contradictory signals"""

    response = llm.invoke(prompt)

    state["research"] = response.content
    return state