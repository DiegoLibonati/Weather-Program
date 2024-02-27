def add_zero(
    value: int
) -> str:
    
    if value >= 0 and value <= 10:
        return f"0{value}"
    
    return str(value)