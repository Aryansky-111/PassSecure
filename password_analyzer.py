import re
import math
import string
import hashlib
from collections import Counter

class PasswordAnalyzer:
    def __init__(self):
        self.common_patterns = [
            r'(.)\1{2,}',
            r'(012|123|234|345|456|567|678|789|890)',
            r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)',
            r'(qwe|wer|ert|rty|tyu|yui|uio|iop|asd|sdf|dfg|fgh|ghj|hjk|jkl|zxc|xcv|cvb|vbn|bnm)'
        ]
        
        self.common_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123', 'password123',
            'admin', 'letmein', 'welcome', 'monkey', '1234567890', 'login',
            'guest', 'hello', 'welcome123', 'admin123', 'root', 'test'
        ]
        
        self.strength_levels = [
            {'min_score': 0, 'max_score': 25, 'level': 'Very Weak', 'color': 'danger'},
            {'min_score': 26, 'max_score': 45, 'level': 'Weak', 'color': 'warning'},
            {'min_score': 46, 'max_score': 65, 'level': 'Fair', 'color': 'info'},
            {'min_score': 66, 'max_score': 85, 'level': 'Good', 'color': 'primary'},
            {'min_score': 86, 'max_score': 100, 'level': 'Strong', 'color': 'success'}
        ]

    def calculate_entropy(self, password):
        if not password:
            return 0
        
        charset_size = 0
        
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += len(string.punctuation)
        
        if charset_size == 0:
            return 0
        
        entropy = len(password) * math.log2(charset_size)
        return entropy

    def check_common_patterns(self, password):
        patterns_found = []
        
        for pattern in self.common_patterns:
            if re.search(pattern, password.lower()):
                if 'repeat' not in [p['type'] for p in patterns_found]:
                    patterns_found.append({'type': 'repeat', 'description': 'Repeated characters'})
                if 'sequence' not in [p['type'] for p in patterns_found]:
                    patterns_found.append({'type': 'sequence', 'description': 'Sequential characters'})
                if 'keyboard' not in [p['type'] for p in patterns_found]:
                    patterns_found.append({'type': 'keyboard', 'description': 'Keyboard patterns'})
        
        if password.lower() in self.common_passwords:
            patterns_found.append({'type': 'common', 'description': 'Common password'})
        
        return patterns_found

    def calculate_score(self, password):
        score = 0
        length = len(password)
        
        if length >= 8:
            score += 10
        if length >= 12:
            score += 10
        if length >= 16:
            score += 10
        
        if any(c.islower() for c in password):
            score += 5
        if any(c.isupper() for c in password):
            score += 5
        if any(c.isdigit() for c in password):
            score += 5
        if any(c in string.punctuation for c in password):
            score += 10
        
        entropy = self.calculate_entropy(password)
        if entropy >= 50:
            score += 15
        elif entropy >= 35:
            score += 10
        elif entropy >= 25:
            score += 5
        
        patterns = self.check_common_patterns(password)
        score -= len(patterns) * 5
        
        char_variety = len(set(password.lower()))
        if char_variety >= length * 0.8:
            score += 10
        elif char_variety >= length * 0.6:
            score += 5
        
        score = max(0, min(100, score))
        return score

    def get_strength_level(self, score):
        for level in self.strength_levels:
            if level['min_score'] <= score <= level['max_score']:
                return level
        return self.strength_levels[0]

    def get_suggestions(self, password):
        suggestions = []
        
        if len(password) < 8:
            suggestions.append("Use at least 8 characters")
        if len(password) < 12:
            suggestions.append("Consider using 12 or more characters for better security")
        
        if not any(c.islower() for c in password):
            suggestions.append("Add lowercase letters")
        if not any(c.isupper() for c in password):
            suggestions.append("Add uppercase letters")
        if not any(c.isdigit() for c in password):
            suggestions.append("Add numbers")
        if not any(c in string.punctuation for c in password):
            suggestions.append("Add special characters (!@#$%^&*)")
        
        patterns = self.check_common_patterns(password)
        if patterns:
            suggestions.append("Avoid common patterns and repeated characters")
        
        if password.lower() in self.common_passwords:
            suggestions.append("Avoid common passwords")
        
        char_variety = len(set(password.lower()))
        if char_variety < len(password) * 0.6:
            suggestions.append("Use a wider variety of characters")
        
        return suggestions

    def create_sha256_hash(self, password):
        password_bytes = password.encode('utf-8')
        hash_object = hashlib.sha256(password_bytes)
        hex_hash = hash_object.hexdigest()
        return hex_hash

    def analyze(self, password):
        if not password:
            return {
                'score': 0,
                'strength': self.get_strength_level(0),
                'entropy': 0,
                'patterns': [],
                'suggestions': ['Please enter a password to analyze']
            }
        
        score = self.calculate_score(password)
        strength = self.get_strength_level(score)
        entropy = self.calculate_entropy(password)
        patterns = self.check_common_patterns(password)
        suggestions = self.get_suggestions(password)
        sha256_hash = self.create_sha256_hash(password)
        
        return {
            'score': score,
            'strength': strength,
            'entropy': round(entropy, 2),
            'patterns': patterns,
            'suggestions': suggestions,
            'sha256_hash': sha256_hash
        }
