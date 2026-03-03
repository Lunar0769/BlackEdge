"""
Feedback Memory Manager - Stores and retrieves past mistakes
"""
import json
import os
from datetime import datetime
from typing import List, Dict

class FeedbackManager:
    def __init__(self, log_path: str = "memory/error_log.json"):
        self.log_path = log_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                json.dump([], f)
    
    def log_failure(self, evaluation: dict):
        """Store evaluation when score < threshold"""
        with open(self.log_path, 'r') as f:
            logs = json.load(f)
        
        logs.append(evaluation)
        
        with open(self.log_path, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def get_recent_mistakes(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent failures for prompt injection"""
        with open(self.log_path, 'r') as f:
            logs = json.load(f)
        
        return logs[-limit:] if logs else []
    
    def get_common_weaknesses(self) -> List[str]:
        """Extract most common weakness patterns"""
        with open(self.log_path, 'r') as f:
            logs = json.load(f)
        
        if not logs:
            return []
        
        weakness_counts = {}
        for log in logs:
            for weakness in log.get('weaknesses', []):
                weakness_counts[weakness] = weakness_counts.get(weakness, 0) + 1
        
        # Return top 5 most common
        sorted_weaknesses = sorted(weakness_counts.items(), key=lambda x: x[1], reverse=True)
        return [w[0] for w in sorted_weaknesses[:5]]
    
    def generate_adaptive_prompt(self) -> str:
        """Generate prompt injection based on past mistakes"""
        mistakes = self.get_recent_mistakes(5)
        common_weaknesses = self.get_common_weaknesses()
        
        if not mistakes and not common_weaknesses:
            return ""
        
        prompt = "\n CRITICAL: Learn from past mistakes:\n\n"
        
        if common_weaknesses:
            prompt += "Common errors to avoid:\n"
            for i, weakness in enumerate(common_weaknesses, 1):
                prompt += f"{i}. {weakness}\n"
        
        if mistakes:
            prompt += "\nRecent failures:\n"
            for mistake in mistakes[-3:]:
                prompt += f"- Query: {mistake.get('query', 'N/A')[:100]}...\n"
                prompt += f"  Issue: {mistake.get('summary', 'N/A')}\n"
        
        prompt += "\nEnsure your analysis addresses these gaps.\n"
        return prompt
    
    def clear_logs(self):
        """Clear all logs (use with caution)"""
        with open(self.log_path, 'w') as f:
            json.dump([], f)
