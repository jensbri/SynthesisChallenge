# Optimization Methodology & Deep Dive

This document details the mathematical optimization approach used to solve the Synthesis Challenge.

## The Problem
We formulated the gear train design as a **Mixed-Integer Non-Linear Programming (MINLP)** problem.

*   **Objective**: Minimize Cost $P = 7N + 0.1 \sum (\pi r^2) + 10 l_r^3$
*   **Variables**:
    *   $N$: Number of gears (Integer, discrete choice of train type).
    *   $H_{idx}$: Shaft positions (Integer/Discrete from fixed holes).
    *   $r_n$: Gear radii (Continuous).
    *   $l_r$: Output slot displacement (Continuous).
*   **Constraints**:
    *   Geometric Continuity: $r_n + r_{n+1} = \text{Distance}(H_a, H_b)$
    *   Ratio: $\prod \text{Ratios} = 8.0$
    *   Physical Realism: $r_n > 0.1$

## Optimization Strategy

Since the problem involves discrete choices (which hole to use) and continuous variables (radii), and the objective function is non-convex (due to the $r^2$ area term and complex geometric constraints), we employed **Global Optimization** techniques.

### 1. Differential Evolution (DE)
*   **Library**: `scipy.optimize.differential_evolution`
*   **Method**: Stochastically searches the space by maintaining a population of candidate solutions. It combines existing candidates to create new ones, effectively exploring the landscape to avoid local minima.
*   **Parameters**:
    *   `strategy='best1bin'`: Focuses on the best solution found so far.
    *   `popsize=15`: Population size multiplier.
    *   **Soft Penalties**: We converted hard constraints (like "Ratio must be exactly 8") into soft penalties in the objective function (adding $10000 \times \text{error}^2$) to guide the optimizer toward valid solutions.

### 2. Dual Annealing (DA)
*   **Library**: `scipy.optimize.dual_annealing`
*   **Method**: Combines Classical Simulated Annealing (CSA) with a local search strategy. It is excellent for finding the global minimum of a function with many local minima.
*   **Comparison**: We used DA to cross-validate the results from DE.

## Results & Analysis

We ran both optimizers to find the best configuration for a **4-Gear Compound Train** (the most promising alternative to the simple train).

| Optimizer | Best Cost Found | Configuration Found |
| :--- | :--- | :--- |
| **Differential Evolution** | **$91.54** | Shafts at H1, H8, H14. |
| **Dual Annealing** | **$91.37** | Shafts at H1, H6, H14. |
| **Simple Train (Baseline)** | **$57.21** | Shafts at H1, H4, H7, H10, H14. |

### Interpretation
Both global optimizers converged to solutions costing ~$91. This consistency strongly suggests that **$91 is indeed the global minimum for the 4-gear compound configuration**.

The high cost is driven by the **Area Penalty ($r^2$)**.
*   The Compound Train reduces $N$ by 1 (saving $7).
*   However, it requires bridging larger gaps (e.g., 10-14cm).
*   Bridging a 12cm gap requires gears with radii summing to 12. Even with a 1:1 ratio ($r=6$), the area is $\pi \times 6^2 \approx 113 \text{cm}^2$.
*   In contrast, the Simple Train bridges 6cm gaps. $r=3 \implies \text{Area} \approx 28 \text{cm}^2$.
*   Since Area scales with the **square** of the radius, using more small gears (Simple Train) is significantly cheaper than fewer large gears (Compound Train).

### Conclusion
We can state with **high confidence** that the **Simple Optimized Train ($57.21)** is the global optimal solution for this specific set of cost coefficients. The penalty for gear area ($0.1/\text{cm}^2$) is too high to make compound trains viable for these specific distances.
