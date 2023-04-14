import numpy as np
import pandas as pd
from skyfield.api import Topos, Loader
from datetime import datetime
import plotly.graph_objects as go
from ipywidgets import interact, widgets
import random

# Initialize Skyfield library
load = Loader('~/skyfield-data')
ts = load.timescale()
planets = {
    'Sun': load('de421.bsp')['sun'],
    'Mercury': load('de421.bsp')['mercury barycenter'],
    'Venus': load('de421.bsp')['venus barycenter'],
    'Earth': load('de421.bsp')['earth barycenter'],
    'Mars': load('de421.bsp')['mars barycenter'],
    'Jupiter': load('de421.bsp')['jupiter barycenter'],
    'Saturn': load('de421.bsp')['saturn barycenter'],
    'Uranus': load('de421.bsp')['uranus barycenter'],
    'Neptune': load('de421.bsp')['neptune barycenter'],
    'Pluto': load('de421.bsp')['pluto barycenter']
}

# Compute positions
def compute_positions(date):
    t = ts.utc(date.year, date.month, date.day)
    positions = {}
    for name, planet in planets.items():
        position = planet.at(t).position.km
        positions[name] = position
    return positions

# Generate random stars
def generate_stars(num_stars=200, max_distance=5000000):
    stars = []
    for _ in range(num_stars):
        x = random.uniform(-max_distance, max_distance)
        y = random.uniform(-max_distance, max_distance)
        z = random.uniform(-max_distance, max_distance)
        stars.append((x, y, z))
    return stars

# Create 3D solar system plot
def create_solar_system_plot(positions, stars):
    fig = go.Figure()

    # Add planets
    for name, position in positions.items():
        fig.add_trace(go.Scatter3d(x=[position[0]], y=[position[1]], z=[position[2]],
                                   mode='markers', name=name, marker=dict(size=8)))

    # Add stars
    star_x, star_y, star_z = zip(*stars)
    fig.add_trace(go.Scatter3d(x=star_x, y=star_y, z=star_z, mode='markers',
                               name='Stars', marker=dict(size=2, color='white', opacity=0.5), showlegend=False))

    # Add orbit lines
    for name, planet in planets.items():
        if name == 'Sun':
            continue
        orbit = planet.orbit(np.arange(0, 366))
        fig.add_trace(go.Scatter3d(x=orbit.x.km, y=orbit.y.km, z=orbit.z.km,
                                   mode='lines', name=f"{name} Orbit", line=dict(width=1, color='grey', dash='dash'), showlegend=False))

    fig.update_layout(scene=dict(xaxis_title='X (km)', yaxis_title='Y (km)', zaxis_title='Z (km)', bgcolor='black'),
                      margin=dict(r=10, l=10, b=10, t=10))

    return fig

# Update plot
def update(date):
    positions = compute_positions(date)
    stars = generate_stars()
    fig = create_solar_system_plot(positions, stars)
    fig.show()

# Slider widget
start_date = datetime(2000, 1, 1)
end_date = datetime(2023, 4, 14)
date_picker = widgets.DatePicker(min=start_date, max=end_date, value=start_date, description='Date:')
interact(update, date=date_picker)
