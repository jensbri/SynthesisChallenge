import plotly.graph_objects as go
import numpy as np
import os

# Ensure output directory exists
OUTPUT_DIR = "docs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_gear_plot(gears, title, filename, rail_length=26):
    """
    Generates a Plotly HTML file for a given gear configuration.
    """
    fig = go.Figure()

    # Add gears
    for g in gears:
        # Generate circle coordinates
        theta = np.linspace(0, 2*np.pi, 200)
        x_coords = g["x"] + g["r"] * np.cos(theta)
        y_coords = g["r"] * np.sin(theta)
        
        # Gear Pitch Circle
        fig.add_trace(go.Scatter(
            x=x_coords, y=y_coords,
            fill="toself",
            fillcolor=g["color"],
            opacity=0.4,
            line=dict(color=g["color"], width=2),
            name=g["name"],
            text=f"Radius: {g['r']:.2f} cm<br>Pos: {g['x']:.2f} cm",
            hoverinfo="text+name"
        ))
        
        # Shaft Center
        fig.add_trace(go.Scatter(
            x=[g["x"]], y=[0],
            mode='markers',
            marker=dict(color='black', size=8),
            showlegend=False
        ))

    # Add Rail / Holes
    holes = np.arange(0, 26, 2)
    fig.add_trace(go.Scatter(
        x=holes, y=[0]*len(holes),
        mode='markers',
        marker=dict(color='gray', symbol='circle-open', size=10),
        name="Fixed Holes (H1-H13)",
        hoverinfo="skip"
    ))

    # Add Slot H14
    fig.add_shape(type="rect", 
        x0=24.49, y0=-0.5, x1=27.51, y1=0.5, 
        line=dict(color="gray", dash="dash"), 
        fillcolor="lightgray", opacity=0.3
    )
    fig.add_trace(go.Scatter(
        x=[26], y=[0],
        mode='text',
        text=["H14 Slot"],
        textposition="bottom center",
        showlegend=False
    ))

    # Layout
    fig.update_layout(
        title=title,
        xaxis_title="Position along Rail (cm)",
        yaxis_title="Vertical Profile (cm)",
        yaxis=dict(scaleanchor="x", scaleratio=1), # 1:1 Aspect Ratio
        xaxis=dict(range=[-5, 35], dtick=2),
        template="plotly_white",
        height=600,
        width=1000
    )

    # Save HTML
    filepath_html = os.path.join(OUTPUT_DIR, filename)
    fig.write_html(filepath_html, include_plotlyjs='cdn')
    print(f"Generated plot: {filepath_html}")
    
    # Save PNG (Thumbnail)
    filename_png = filename.replace(".html", ".png")
    filepath_png = os.path.join(OUTPUT_DIR, filename_png)
    # Use scale=2 for better quality, but keep it small enough for thumbnail
    fig.write_image(filepath_png, scale=2)
    print(f"Generated image: {filepath_png}")

def visualize_simple_optimized():
    # Simple Train (Verified)
    # H1, H4, H7, H10, H14
    # Radii: 0.2857, 5.7143, 0.2857, 5.7143, 2.2857
    gears = [
        {"name": "G1 (Input)", "x": 0, "r": 0.2857, "color": "firebrick"},
        {"name": "G2 (Idler)", "x": 6, "r": 5.7143, "color": "royalblue"},
        {"name": "G3 (Idler)", "x": 12, "r": 0.2857, "color": "firebrick"},
        {"name": "G4 (Idler)", "x": 18, "r": 5.7143, "color": "royalblue"},
        {"name": "G5 (Output)", "x": 26, "r": 2.2857, "color": "forestgreen"}
    ]
    create_gear_plot(gears, "Solution 1: Simple Optimized ($57.21)", "simple_optimized.html")

def visualize_compound_failed():
    # Compound Train (The "Failed" one from Optimization)
    # Shafts: H1(0), H8(14), H14_shifted(25.59)
    # Radii: 5.03, 8.97, 2.11, 9.47
    gears = [
        {"name": "G1 (Input)", "x": 0, "r": 5.0263, "color": "firebrick"},
        {"name": "G2 (Comp In)", "x": 14, "r": 8.9737, "color": "royalblue"},
        {"name": "G3 (Comp Out)", "x": 14, "r": 2.1141, "color": "lightskyblue"},
        {"name": "G4 (Output)", "x": 25.5873, "r": 9.4732, "color": "forestgreen"}
    ]
    create_gear_plot(gears, "Solution 2: Compound Train (High Cost: ~$91)", "compound_failed.html")

def visualize_chat_hallucination():
    # The "Ideal" Compound Train claimed by Chat (Physically Impossible with these holes)
    # Claimed: H1(0), H8(14), H14(26.6)
    # Claimed Radii: 4.0, 10.0, 3.0, 9.6
    # Why impossible? 
    # Mesh 1: 4+10 = 14 (Matches H1->H8 distance)
    # Mesh 2: 3+9.6 = 12.6. Distance H8(14) -> H14(26.6) = 12.6.
    # Wait, 14 + 12.6 = 26.6. 
    # So the geometry IS possible.
    # Why did it fail cost? 
    # Area: pi*(4^2 + 10^2 + 3^2 + 9.6^2) = pi*(16 + 100 + 9 + 92.16) = pi*217.16 = 682 cm^2
    # Cost Area = 68.2. Cost Gears = 28. Cost Slot = 10*(0.6)^3 = 2.16.
    # Total = 28 + 68.2 + 2.16 = 98.36.
    # Chat claimed $49.10. It lied about the area cost.
    
    gears = [
        {"name": "G1 (Input)", "x": 0, "r": 4.0, "color": "firebrick"},
        {"name": "G2 (Comp In)", "x": 14, "r": 10.0, "color": "royalblue"},
        {"name": "G3 (Comp Out)", "x": 14, "r": 3.0, "color": "lightskyblue"},
        {"name": "G4 (Output)", "x": 26.6, "r": 9.6, "color": "forestgreen"}
    ]
    create_gear_plot(gears, "Chat Hallucination: 'Ideal' Compound (Real Cost: ~$98)", "chat_hallucination.html")

if __name__ == "__main__":
    visualize_simple_optimized()
    visualize_compound_failed()
    visualize_chat_hallucination()
