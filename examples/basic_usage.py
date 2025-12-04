"""
Basic usage example for Multi-Agent LLM Router
"""

from src.agent_router import AgentRouter

def main():
    router = AgentRouter(complexity_threshold=0.7)
    
    # Simple query → Routes to Llama 3
    response = router.query("What is Python?")
    print(f"Model: {response.model} | Cost: ${response.cost}")
    
    # Complex query → Routes to Gemini
    response = router.query("Explain quantum entanglement implications")
    print(f"Model: {response.model} | Cost: ${response.cost}")
    
    # Show stats
    stats = router.get_stats()
    print(f"\nLocal routing: {stats['local_pct']:.1f}%")
    print(f"Total cost: ${stats['total_cost']:.4f}")

if __name__ == "__main__":
    main()
