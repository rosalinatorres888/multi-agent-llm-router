"""
Multi-Agent LLM Router - Main orchestrator

Author: Rosalina Torres
"""

import os
import time
import logging
from typing import Optional, Dict
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelType(Enum):
    LOCAL = "local"
    CLOUD = "cloud"
    FALLBACK = "fallback"


@dataclass
class QueryResponse:
    text: str
    model: str
    model_type: ModelType
    latency: float
    cost: float
    complexity_score: float


class AgentRouter:
    """
    Intelligent LLM routing with complexity-based decision making
        Routes queries to local or cloud LLMs based on complexity
    """
    
    def __init__(
        self,
        local_model: str = "llama3",
        cloud_model: str = "gemini-pro",
        complexity_threshold: float = 0.7
    ):
        from complexity_analyzer import ComplexityAnalyzer
        
        self.local_model = local_model
        self.cloud_model = cloud_model
        self.analyzer = ComplexityAnalyzer(complexity_threshold)
        self.stats = {"local": 0, "cloud": 0, "total_cost": 0.0}
        
    def query(self, prompt: str) -> QueryResponse:
        """Route query to appropriate model"""
        start_time = time.time()
        
        # Analyze complexity
        complexity = self.analyzer.analyze(prompt)
        logger.info(f"Query complexity: {complexity:.2f}")
        
        # Route based on complexity
        if complexity < self.analyzer.threshold:
            response = self._query_local(prompt)
        else:
            response = self._query_cloud(prompt)
        
        latency = time.time() - start_time
        response.latency = latency
        response.complexity_score = complexity
        
        return response
    
    def _query_local(self, prompt: str) -> QueryResponse:
        """Query local Ollama model"""
        try:
            import requests
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.local_model, "prompt": prompt}
            )
            self.stats["local"] += 1
            return QueryResponse(
                text=response.json()["response"],
                model=self.local_model,
                model_type=ModelType.LOCAL,
                latency=0.0,
                cost=0.0,
                complexity_score=0.0
            )
        except Exception as e:
            logger.error(f"Local model failed: {e}")
            return self._query_cloud(prompt)
    
    def _query_cloud(self, prompt: str) -> QueryResponse:
        """Query cloud API (Gemini)"""
        try:
            # Simplified Gemini API call
            cost = 0.002  # $0.002 per query
            self.stats["cloud"] += 1
            self.stats["total_cost"] += cost
            
            # Actual API call would go here
            return QueryResponse(
                text="[Gemini Pro response]",
                model=self.cloud_model,
                model_type=ModelType.CLOUD,
                latency=0.0,
                cost=cost,
                complexity_score=0.0
            )
        except Exception as e:
            logger.error(f"Cloud model failed: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> QueryResponse:
        """Fallback when all models fail"""
        return QueryResponse(
            text="I apologize, but I'm unable to process your request at the moment.",
            model="fallback",
            model_type=ModelType.FALLBACK,
            latency=0.0,
            cost=0.0,
            complexity_score=0.0
        )
    
    def get_stats(self) -> Dict:
        """Get routing statistics"""
        total = self.stats["local"] + self.stats["cloud"]
        return {
            "total": total,
            "local": self.stats["local"],
            "cloud": self.stats["cloud"],
            "local_pct": (self.stats["local"] / total * 100) if total > 0 else 0,
            "total_cost": self.stats["total_cost"],
            "cost_per_query": self.stats["total_cost"] / total if total > 0 else 0
        }
