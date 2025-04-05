def decide_next_action(updated_offer, attorney_threshold, adjuster_flags=None, auto_approve_enabled=True):
    """
    Determine the next step based on adjuster offer and attorney-defined minimum.
    
    Parameters:
        updated_offer (float): The settlement amount offered by the adjuster.
        attorney_threshold (float): The minimum acceptable settlement set by the attorney.
        adjuster_flags (list[str], optional): Issues with adjuster response (e.g., IME, missed diagnosis).
        auto_approve_enabled (bool): If True, decision is made automatically.

    Returns:
        str: One of "ACCEPT", "TRIGGER_PROPHET", or "MANUAL_REVIEW"
    """
    adjuster_flags = adjuster_flags or []

    # Acceptable offer with no red flags
    if updated_offer >= attorney_threshold and not adjuster_flags:
        return "ACCEPT"
    
    # Low offer or issues in adjuster response
    if auto_approve_enabled:
        return "TRIGGER_PROPHET"
    
    # Manual review for edge cases
    return "MANUAL_REVIEW"
