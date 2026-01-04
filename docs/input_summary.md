# Synthesis Challenge 1 Input Summary

## Overview
The challenge involves designing a gear train to transmit rotation from an Input-Shaft to an Output-Shaft.

## Functional Requirements
1.  **Transmission**: Rotation from Input-Shaft to Output-Shaft using gears.
2.  **Ratio**: Speed Reduction Ratio of exactly **8:1** (8 turns of input = 1 turn of output).
    *   *Note*: The original text mentions "81" but clarifies "8 turns... result in 1 turn", implying 8:1.
3.  **Direction**: Direction of rotation must be maintained (e.g., CCW -> CCW).

## Constraints
*   **Max Shafts**: 8.
*   **Hole Positions**:
    *   H1 to H13 are fixed at 2cm intervals (H1=0cm, H2=2cm, ..., H13=24cm).
    *   H14 is a slot centered at 26cm.
    *   H14 Movement Range: +/- 1.51cm (24.49cm to 27.51cm).

## Objective Function
Minimize the cost function $P$:

$$ P = x \cdot N + y \cdot \sum (\pi \cdot r_n^2) + z \cdot lr^3 $$

Where:
*   $N$: Overall number of gears.
*   $r_n$: Radius of each gear [cm].
*   $lr$: Distance of repositioning the output gear (H14) from its nominal position [cm].
*   $x$: Cost per gear (Estimated: $7).
*   $y$: Cost per gear area (Estimated: $0.1/cm^2$).
*   $z$: Cost per displacement (Estimated: $10/cm^3$).

*Note*: Coefficients $x, y, z$ are inferred from OCR text and need verification.
