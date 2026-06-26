def get_contextualizer(strategy="memory"):
    if strategy == "memory":
        from .memory_manager import create_session, add_message, format_history_for_prompt, contextualize_query
        return create_session, add_message, format_history_for_prompt, contextualize_query
    else:
        raise ValueError(f"Unknown contextualization strategy: {strategy}")
