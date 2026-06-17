# Step 1: Basic Logic Gates

def and_gate(a, b):
    """Outputs 1 only if both inputs are 1."""
    return 1 if (a == 1 and b == 1) else 0

def or_gate(a, b):
    """Outputs 1 if at least one input is 1."""
    return 1 if (a == 1 or b == 1) else 0

def not_gate(a):
    """Flips the input (1 becomes 0, 0 becomes 1)."""
    return 1 if a == 0 else 0

def xor_gate(a, b):
    """Outputs 1 only if the inputs are different from each other."""
    return 1 if a != b else 0


# Step 2: The Half-Adder

def half_adder(a, b):
    """
    A half-adder adds two binary bits together.
    Returns a tuple containing the (Sum, Carry).
    """
    # Use XOR function to calculate the Sum
    sum_bit = xor_gate(a, b)
    
    # Use AND function to calculate the Carry
    carry_bit = and_gate(a, b)
    
    return sum_bit, carry_bit


# Step 3: Test the Circuit

def main():
    test_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    print("--- Testing Basic Logic Gates ---")
    
    print("\nAND Gate:")
    for a, b in test_cases:
        print(f"{a} AND {b}  ->  {and_gate(a, b)}")
        
    print("\nOR Gate:")
    for a, b in test_cases:
        print(f"{a} OR {b}   ->  {or_gate(a, b)}")
        
    print("\nXOR Gate:")
    for a, b in test_cases:
        print(f"{a} XOR {b}  ->  {xor_gate(a, b)}")
        
    print("\nNOT Gate:")
    for a in [0, 1]:
        print(f"NOT {a}    ->  {not_gate(a)}")

    print("\n" + "="*30)
    print("--- Testing Half-Adder ---")
    print("="*30)
    print(" A  |  B  | Sum | Carry")
    print("-" * 27)
    
    # Using a list comprehension to efficiently pass test cases through the half_adder
    # and format the results into strings for printing
    adder_results = [
        f" {a}  |  {b}  |  {half_adder(a, b)[0]}  |   {half_adder(a, b)[1]}" 
        for a, b in test_cases
    ]
    
    for result in adder_results:
        print(result)
    
    print("-" * 27)

if __name__ == "__main__":
    main()
