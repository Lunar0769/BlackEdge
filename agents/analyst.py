from langchain_google_genai import ChatGoogleGenerativeAI
from config import MODEL_NAME, GOOGLE_API_KEY


def analyst_node(state):
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3,
    )
    
    adaptive_prompt = state.get('adaptive_prompt', '')
    
    prompt = f"""You are a financial analyst.

{adaptive_prompt}

Research:
{state['research']}

Provide comprehensive analysis covering:
- Risk-adjusted reasoning
- Valuation awareness
- Time horizon considerations
- Conflicting signals reconciliation
- Missing factors identification

Be specific and avoid overconfidence."""

    response = llm.invoke(prompt)

    state["analysis"] = response.content
    return state