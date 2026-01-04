import numpy as np
from scipy.optimize import differential_evolution

# Constants from the brief
X_GEAR_COST = 7.0
Y_AREA_COST = 0.1
Z_SLOT_PENALTY = 10.0
TARGET_RATIO = 8.0

# Fixed hole positions (H1 at 0cm to H13 at 24cm)
HOLES = np.arange(0, 26, 2)

def objective_function(params):
    """
    Objective function for a 3-shaft compound train (4 gears).
    params: [shaft2_idx, r1, r3, lr]
    """
    s2_idx, r1, r3, lr = params
    
    # Map index to physical hole position (H2 to H13)
    # s2_idx is continuous, so we cast to int
    s2_pos = HOLES[int(s2_idx)]
    
    # H14 is at 26cm + adjustment lr
    s3_pos = 26.0 + lr 
    
    # Shaft 1 is fixed at H1 (0cm)
    s1_pos = 0.0
    
    # Derived radii to satisfy mesh constraints
    # Mesh 1: Shaft 1 -> Shaft 2
    # r1 + r2 = dist(S1, S2)
    dist1 = abs(s2_pos - s1_pos)
    r2 = dist1 - r1
    
    # Mesh 2: Shaft 2 -> Shaft 3
    # r3 + r4 = dist(S2, S3)
    dist2 = abs(s3_pos - s2_pos)
    r4 = dist2 - r3
    
    # Soft Constraints
    penalty = 0
    
    # 1. Physical Realism: Radii must be positive
    # Penalize if any radius is too small (< 0.1)
    for r in [r1, r2, r3, r4]:
        if r < 0.1:
            penalty += 1000 * (0.1 - r)**2
            
    # 2. Ratio Constraint: Must be exactly 8.0
    current_ratio = (r2/r1) * (r4/r3)
    ratio_error = abs(current_ratio - TARGET_RATIO)
    penalty += 10000 * ratio_error**2
        
    # Calculate Base Objective Function P
    N = 4 # 4 gears
    area_sum = np.pi * (r1**2 + r2**2 + r3**2 + r4**2)
    
    P_base = (X_GEAR_COST * N) + (Y_AREA_COST * area_sum) + (Z_SLOT_PENALTY * abs(lr)**3)
    
    return P_base + penalty

def evaluate_simple_train():
    print("\nEvaluating Simple Train (5 Gears)...")
    # Configuration from Chat: H1, H4, H7, H10, H14
    # Gaps: 6, 6, 6, 8 (approx)
    # r1 + r2 = 6
    # r2 + r3 = 6
    # r3 + r4 = 6
    # r4 + r5 = 8
    # Ratio = r5 / r1 = 8
    
    # Constraints:
    # r5 = 8 * r1
    # r2 = 6 - r1
    # r3 = 6 - r2 = r1
    # r4 = 6 - r3 = 6 - r1
    # r5 = 8 - r4 = 2 + r1
    
    # Solve for r1:
    # 8 * r1 = 2 + r1 => 7 * r1 = 2 => r1 = 2/7
    r1 = 2/7
    r2 = 6 - r1
    r3 = r1
    r4 = 6 - r1
    r5 = 8 * r1
    
    radii = [r1, r2, r3, r4, r5]
    N = 5
    area_sum = np.pi * sum([r**2 for r in radii])
    
    # Check H14 slot
    # Last gap is H10(18) to H14(26). Dist = 8.
    # r4 + r5 = (6 - 2/7) + (16/7) = (42-2+16)/7 = 56/7 = 8.
    # Exact match at 26cm. lr = 0.
    lr = 0
    
    P = (X_GEAR_COST * N) + (Y_AREA_COST * area_sum) + (Z_SLOT_PENALTY * abs(lr)**3)
    
    print(f"  Radii: {[f'{r:.4f}' for r in radii]}")
    print(f"  Area Sum: {area_sum:.4f} cm^2")
    print(f"  Cost: ${P:.2f}")
    return P

def run_optimization():
    print("Starting Optimization for 4-Gear Compound Train...")
    
    # Bounds:
    # shaft2_idx: 1 to 12 (H2 to H13)
    # r1: 0.1 to 10 cm
    # r3: 0.1 to 10 cm
    # lr: -1.51 to 1.51 cm
    bounds = [(1, 12.99), (0.1, 10), (0.1, 10), (-1.51, 1.51)]
    
    result = differential_evolution(objective_function, bounds, seed=42, strategy='best1bin', popsize=15)
    
    print("\nOptimization Complete!")
    print(f"Optimal Score (Cost): ${result.fun:.2f}")
    
    # Decode best parameters
    s2_idx, r1, r3, lr = result.x
    s2_pos = HOLES[int(s2_idx)]
    s3_pos = 26.0 + lr
    
    r2 = abs(s2_pos - 0) - r1
    r4 = abs(s3_pos - s2_pos) - r3
    
    ratio = (r2/r1) * (r4/r3)
    
    print("\nDesign Details:")
    print(f"  Shaft 1 Position: 0.0 cm (H1)")
    print(f"  Shaft 2 Position: {s2_pos} cm (H{int(s2_idx)+1})")
    print(f"  Shaft 3 Position: {s3_pos:.4f} cm (H14 + {lr:.4f} cm)")
    print(f"  Slot Displacement (lr): {lr:.4f} cm")
    print("-" * 30)
    print(f"  Gear 1 Radius (r1): {r1:.4f} cm")
    print(f"  Gear 2 Radius (r2): {r2:.4f} cm")
    print(f"  Gear 3 Radius (r3): {r3:.4f} cm")
    print(f"  Gear 4 Radius (r4): {r4:.4f} cm")
    print("-" * 30)
    print(f"  Total Ratio: {ratio:.4f}")
    
    evaluate_simple_train()
    
    return result.fun

if __name__ == "__main__":
    run_optimization()
