def get_generator(strategy="ollama"):
    if strategy == "ollama":
        from .ollama_generator import generate_response
        return generate_response
    else:
        raise ValueError(f"Unknown generation strategy: {strategy}")
