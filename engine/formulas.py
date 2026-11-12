# engine/formulas.py
import math

def create_cost_formula(curve_type="geometric", base_cost=50.0, **kwargs):
    """
    Generalized function factory supporting arithmetic (sequential), 
    geometric (exponential), polynomial, logarithmic, and multivariable scaling.
    """
    
    if curve_type in ["arithmetic", "sequential"]:
        # Arithmetic / Sequential: Cost increases by a flat increment per level
        # Formula: Cost = Base + (Increment * Level)
        increment = kwargs.get("increment", 25.0)
        return lambda level: base_cost + (increment * level)
        
    elif curve_type in ["geometric", "exponential"]:
        # Geometric / Exponential: Cost multiplies by a constant ratio per level
        # Formula: Cost = Base * (Ratio ^ Level)
        ratio = kwargs.get("ratio", 1.15)
        return lambda level: base_cost * (ratio ** level)
        
    elif curve_type == "polynomial":
        # Polynomial / Power Law: Cost scales with level raised to an exponent
        # Formula: Cost = Base * (Level ^ Exponent)
        exponent = kwargs.get("exponent", 2.0)
        return lambda level: base_cost * (max(1, level) ** exponent)
        
    elif curve_type == "logarithmic":
        # Logarithmic / Diminishing Returns: Costs rise sharply at first, then flatten (soft cap)
        # Formula: Cost = Base + (Scale * ln(Level))
        scale = kwargs.get("scale", 50.0)
        return lambda level: base_cost + (scale * math.log(max(1, level)))
        
    elif curve_type == "multivariable":
        # Multivariable: Cost depends on both the upgrade level and the player's current map zone
        # Formula: Cost = Base * (Level^Alpha * Zone^Beta)
        alpha = kwargs.get("alpha", 1.5)
        beta = kwargs.get("beta", 0.5)
        return lambda level, zone: base_cost * ((max(1, level) ** alpha) * max(1, zone ** beta))
        
    else:
        # Default fallback to geometric
        ratio = kwargs.get("ratio", 1.15)
        return lambda level: base_cost * (ratio ** level)