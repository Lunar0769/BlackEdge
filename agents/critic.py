"""
Critic Agent - Evaluates investment decisions for logical flaws and risks
"""
import google.generativeai as genai
from config import GOOGLE_API_KEY
import json
from datetime import datetime

genai.configure(api_key=GOOGLE_API_KEY)

class CriticAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def evaluate(self, query: str, decision: str, context: dict = None) -> dict:
        """
        Evaluate investment decision for flaws, risks, and overconfidence
        Returns score (1-10) and detailed feedback
        """
        prompt = f"""You are a risk auditor and investment critic. Evaluate this investment decision.

ORIGINAL QUERY:
{query}

DECISION:
{decision}

EVALUATION CRITERIA:
1. Logical contradictions or inconsistencies
2. Missing risk factors (macro, sector, company-specific)
3. Overconfidence or insufficient hedging
4. Hallucinations or unsupported claims
5. Valuation awareness
6. Time horizon clarity
7. Risk-adjusted reasoning

Provide:
- Score: 1-10 (10 = excellent, 1 = critically flawed)
- Weaknesses: List specific issues
- Missing factors: What was overlooked
- Recommendations: How to improve

Format as JSON:
{{
    "score": <number>,
    "weaknesses": [<list of issues>],
    "missing_factors": [<list of overlooked items>],
    "recommendations": [<list of improvements>],
    "summary": "<brief evaluation>"
}}
"""
        
        response = self.model.generate_content(prompt)
        
        try:
            # Extract JSON from response
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            evaluation = json.loads(text)
            evaluation['timestamp'] = datetime.now().isoformat()
            evaluation['query'] = query
            evaluation['decision'] = decision
            
            return evaluation
            
        except Exception as e:
            return {
                "score": 5,
                "weaknesses": [f"Evaluation parsing error: {str(e)}"],
                "missing_factors": [],
                "recommendations": ["Review decision manually"],
                "summary": "Could not complete evaluation",
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "decision": decision
            }
