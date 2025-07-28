import re
from datetime import datetime

class WordlistGenerator:
    def __init__(self):
        self.leetspeak_map = {
            'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7', 'l': '1'
        }
        
        self.common_years = []
        current_year = datetime.now().year
        for year in range(1950, current_year + 10):
            self.common_years.extend([str(year), str(year)[2:]])

    def clean_input(self, text):
        if not text:
            return []
        
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if len(word) >= 2]

    def apply_leetspeak(self, word):
        variations = [word]
        
        leet_word = word
        for char, replacement in self.leetspeak_map.items():
            leet_word = leet_word.replace(char, replacement)
        if leet_word != word:
            variations.append(leet_word)
        
        partial_leet = word
        for char, replacement in self.leetspeak_map.items():
            if char in partial_leet:
                temp_word = partial_leet.replace(char, replacement, 1)
                variations.append(temp_word)
        
        return list(set(variations))

    def generate_variations(self, word):
        variations = [word]
        
        variations.append(word.capitalize())
        variations.append(word.upper())
        
        if len(word) > 3:
            variations.append(word[:-1])
            variations.append(word[1:])
        
        return list(set(variations))

    def combine_words(self, words):
        combinations = []
        
        for i, word1 in enumerate(words):
            for j, word2 in enumerate(words):
                if i != j:
                    combinations.append(word1 + word2)
                    combinations.append(word1 + word2.capitalize())
        
        return combinations

    def parse_date(self, date_string):
        date_variations = []
        
        date_patterns = [
            r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})',
            r'(\d{4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})',
            r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2})',
            r'(\d{2})[\/\-\.](\d{2})[\/\-\.](\d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_string)
            if match:
                groups = match.groups()
                for group in groups:
                    if len(group) >= 2:
                        date_variations.append(group)
                
                date_variations.append(''.join(groups))
                date_variations.append(groups[0] + groups[1])
                if len(groups) >= 3:
                    date_variations.append(groups[1] + groups[2])
        
        numbers = re.findall(r'\d+', date_string)
        date_variations.extend(numbers)
        
        return list(set(date_variations))

    def generate(self, name='', birthdate='', pet_names='', custom_words='', include_leetspeak=False, include_years=False):
        base_words = []
        
        if name:
            base_words.extend(self.clean_input(name))
        
        if pet_names:
            base_words.extend(self.clean_input(pet_names))
        
        if custom_words:
            base_words.extend(self.clean_input(custom_words))
        
        if birthdate:
            base_words.extend(self.parse_date(birthdate))
        
        if not base_words:
            return []
        
        all_words = set()
        
        for word in base_words:
            all_words.add(word)
            variations = self.generate_variations(word)
            all_words.update(variations)
        
        if len(base_words) > 1:
            combinations = self.combine_words(base_words[:5])
            all_words.update(combinations)
        
        if include_leetspeak:
            leet_words = set()
            for word in list(all_words):
                if word.isalpha():
                    leet_variations = self.apply_leetspeak(word)
                    leet_words.update(leet_variations)
            all_words.update(leet_words)
        
        if include_years:
            year_words = set()
            for word in list(all_words):
                for year in self.common_years[:20]:
                    year_words.add(word + year)
                    year_words.add(year + word)
            all_words.update(year_words)
        
        filtered_words = [word for word in all_words if len(word) >= 3 and len(word) <= 50]
        
        return sorted(list(set(filtered_words)))
