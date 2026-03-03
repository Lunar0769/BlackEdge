"""
Rate Limiter - Enforces 30-minute cooldown between analyses
"""
import json
import os
from datetime import datetime, timedelta

RATE_LIMIT_FILE = "rate_limit.json"
COOLDOWN_MINUTES = 30

class RateLimiter:
    def __init__(self):
        self.limit_file = RATE_LIMIT_FILE
    
    def _load_last_usage(self):
        """Load last usage timestamp"""
        if not os.path.exists(self.limit_file):
            return None
        
        try:
            with open(self.limit_file, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data['last_usage'])
        except:
            return None
    
    def _save_usage(self):
        """Save current timestamp"""
        with open(self.limit_file, 'w') as f:
            json.dump({
                'last_usage': datetime.now().isoformat()
            }, f)
    
    def can_proceed(self):
        """Check if user can make a request"""
        last_usage = self._load_last_usage()
        
        if last_usage is None:
            return True, 0
        
        time_passed = datetime.now() - last_usage
        cooldown = timedelta(minutes=COOLDOWN_MINUTES)
        
        if time_passed >= cooldown:
            return True, 0
        
        remaining = cooldown - time_passed
        remaining_minutes = int(remaining.total_seconds() / 60)
        
        return False, remaining_minutes
    
    def record_usage(self):
        """Record that a request was made"""
        self._save_usage()
    
    def reset(self):
        """Reset rate limit (admin only)"""
        if os.path.exists(self.limit_file):
            os.remove(self.limit_file)
