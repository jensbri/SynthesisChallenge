import numpy as np

# Constants
X_COST = 7.0
Y_COST = 0.1
Z_COST = 10.0

def calculate_cost(name, gears, shafts, slot_shift=0):
    """
    gears: list of radii
    shafts: number of shafts
    slot_shift: displacement of output shaft
    """
    area_sum = sum([np.pi * r**2 for r in gears])
    cost = (X_COST * shafts) + (Y_COST * area_sum) + (Z_COST * abs(slot_shift)**3)
    return cost, area_sum

def analyze_brute_force():
    print("\n--- Brute Force (8 Shafts) ---")
    # Configuration: 8 shafts. 7 intervals.
    # First 6 intervals are 2cm gaps (bridging). Last interval is 14cm (reduction).
    # S1..S7 are 2cm apart. S7..S8 is 14cm.
    # Total distance: 6*2 + 14 = 26cm.
    # Ratio: 8:1.
    # Last stage (S7-S8) does the heavy lifting, but constrained by S6-S7.
    
    # Equations:
    # r8 / r1 = 8 (Simple train)
    # r7 + r8 = 14
    # r6 + r7 = 2
    # r5 + r6 = 2
    # ...
    # r1 + r2 = 2
    
    # From r8/r1 = 8 => r8 = 8*r1.
    # r7 = 14 - r8 = 14 - 8*r1.
    # r6 = 2 - r7 = 2 - (14 - 8*r1) = 8*r1 - 12.
    # r5 = 2 - r6 = 2 - (8*r1 - 12) = 14 - 8*r1.
    # Pattern: Odd gears (r1, r3, r5, r7) = r1 (Wait, let's check)
    
    # r7 = 14 - 8*r1.
    # r5 = 14 - 8*r1.
    # r3 = 14 - 8*r1.
    # r1 = 14 - 8*r1 => 9*r1 = 14 => r1 = 1.555...
    
    # Let's verify:
    # r1 = 14/9 (~1.56)
    # r2 = 2 - r1 = 2 - 1.56 = 0.44
    # r3 = 2 - r2 = 1.56
    # r4 = 0.44
    # r5 = 1.56
    # r6 = 0.44
    # r7 = 2 - r6 = 1.56
    # r8 = 14 - r7 = 12.44
    # Ratio = r8/r1 = 12.44 / 1.56 = 8.0. Correct.
    
    gears = [14/9, 4/9, 14/9, 4/9, 14/9, 4/9, 14/9, 112/9] # r8 = 8 * 14/9 = 112/9
    
    cost, area = calculate_cost("Brute Force", gears, 8)
    print(f"Radii: {[round(r, 2) for r in gears]}")
    print(f"Total Area: {area:.2f}")
    print(f"Cost: ${cost:.2f}")

def analyze_three_gears():
    print("\n--- Three Gears (3 Shafts) ---")
    # S1(0), S_mid, S3(26).
    # r1 + r2 = d1
    # r2 + r3 = d2
    # r3 = 8*r1
    # d1 + d2 = 26
    
    best_cost = float('inf')
    best_config = None
    
    # Iterate through possible middle holes (H2 to H13, i.e., 2cm to 24cm)
    for d1 in range(2, 26, 2):
        d2 = 26 - d1
        
        # r1 + r2 = d1 => r2 = d1 - r1
        # r2 + 8*r1 = d2 => (d1 - r1) + 8*r1 = d2 => 7*r1 = d2 - d1
        
        if d2 <= d1:
            # If d2 - d1 <= 0, r1 would be negative or zero (impossible)
            continue
            
        r1 = (d2 - d1) / 7
        r3 = 8 * r1
        r2 = d1 - r1
        
        if r1 <= 0 or r2 <= 0 or r3 <= 0:
            continue
            
        gears = [r1, r2, r3]
        cost, area = calculate_cost(f"3-Gear (Mid={d1})", gears, 3)
        
        print(f"Mid Hole {d1}cm: r={np.round(gears, 2)}, Cost=${cost:.2f}")
        
        if cost < best_cost:
            best_cost = cost
            best_config = (d1, gears, area)

    print(f"\nBest 3-Gear Config: Mid Hole at {best_config[0]}cm")
    print(f"Radii: {[round(r, 2) for r in best_config[1]]}")
    print(f"Total Area: {best_config[2]:.2f}")
    print(f"Cost: ${best_cost:.2f}")

if __name__ == "__main__":
    analyze_brute_force()
    analyze_three_gears()
