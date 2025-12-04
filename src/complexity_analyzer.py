"""
Complexity Analyzer - Determines query routing based on complexity

Author: Rosalina Torres
"""

from typing import List


class ComplexityAnalyzer:
    """Analyzes query complexity to determine optimal LLM routing"""
    
    COMPLEX_KEYWORDS = [
        "explain", "analyze", "compare", "evaluate", "describe",
        "quantum", "theoretical", "philosophical", "comprehensive",
        "step-by-step", "detailed", "elaborate", "reasoning",
        "implications", "contrast", "synthesize", "critique"
    ]
    
    SIMPLE_KEYWORDS = [
        "what is", "define", "who is", "when", "where",
        "list", "name", "yes or no"
    ]
    
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
        
    def analyze(self, query: str) -> float:
        """
        Calculate complexity score (0.0 - 1.0)
        
        Higher score = more complex query requiring cloud LLM
        Lower score = simple query suitable for local LLM
        """
        score = 0.0
        
        # Length-based scoring (30% weight)
        score += self._length_score(query) * 0.3
        
        # Keyword-based scoring (40% weight)
        score += self._keyword_score(query) * 0.4
        
        # Structure-based scoring (30% weight)
        score += self._structure_score(query) * 0.3
        
        return min(score, 1.0)
    
    def _length_score(self, query: str) -> float:
        """Score based on query length"""
        length = len(query)
        if length < 50:
            return 0.2
        elif length < 150:
            return 0.5
        else:
            return 1.0
    
    def _keyword_score(self, query: str) -> float:
        """Score based on keyword presence"""
        query_lower = query.lower()
        
        # Check for simple keywords (reduces score)
        simple_matches = sum(1 for kw in self.SIMPLE_KEYWORDS if kw in query_lower)
        if simple_matches > 0:
            return 0.3
        
        # Check for complex keywords (increases score)
        complex_matches = sum(1 for kw in self.COMPLEX_KEYWORDS if kw in query_lower)
        return min(complex_matches / 3, 1.0)
    
    def _structure_score(self, query: str) -> float:
        """Score based on query structure"""
        # Multiple questions indicate complexity
        question_marks = query.count('?')
        if question_marks > 2:
            return 0.9
        elif question_marks > 1:
            return 0.6
        
        # Check for comparison structure
        if " vs " in query.lower() or " versus " in query.lower():
            return 0.8
        
        return 0.3
    
    def is_complex(self, query: str) -> bool:
        """Returns True if query exceeds complexity threshold"""
        return self.analyze(query) >= self.threshold


if __name__ == "__main__":
    # Test the analyzer
    analyzer = ComplexityAnalyzer(threshold=0.7)
    
    test_queries = [
        "What is Python?",
        "Explain quantum entanglement and its implications for quantum computing",
        "Compare supervised vs unsupervised learning approaches"
    ]
    
    for query in test_queries:
        score = analyzer.analyze(query)
        is_complex = analyzer.is_complex(query)
        print(f"Query: {query[:50]}...")
        print(f"Score: {score:.2f} | Complex: {is_complex}")
        print()
