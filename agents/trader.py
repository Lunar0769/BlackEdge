from langchain_google_genai import ChatGoogleGenerativeAI
from config import MODEL_NAME, GOOGLE_API_KEY


def trader_node(state):
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.1,
    )
    
    adaptive_prompt = state.get('adaptive_prompt', '')
    
    prompt = f"""You are a trader making investment decisions.

{adaptive_prompt}

Analysis:
{state['analysis']}

Make a clear decision (BUY/SELL/HOLD) with:
- Specific reasoning
- Risk factors acknowledged
- Position sizing guidance
- Time horizon
- Exit conditions

Avoid overconfidence. State uncertainties explicitly."""

    response = llm.invoke(prompt)

    state["decision"] = response.content
    state["final_decision"] = response.content
    return state