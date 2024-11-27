#!/usr/bin/env python
# coding: utf-8

# Soli Deo gloria



# From Anaconda Prompt (anaconda3), type:
# conda activate "C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\jh_env"; cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\py; cls; python unscored_quals_visualization_dash_app.py

import dash
from dash import html, dcc, Input, Output, State
import requests
import threading
import queue

# Initialize the Dash app
app = dash.Dash(__name__, assets_folder='../saves')

# Thread-safe queue to store pre-fetched qualification strings
qualification_queue = queue.Queue(maxsize=10)

# Function to fetch the qualification string from the API
def fetch_qualification_string():
    """
    Fetch a qualification string from the API and return it.
    Handles request exceptions gracefully.
    """
    message = "No more qualifications strings left"
    try:
        response = requests.get(f'http://localhost:5000/get_qualification')
        if response.status_code == 200:
            return response.json().get('qualification_str', '')
    except requests.exceptions.RequestException as e:
        message += f': {str(e).strip()}'
        print(message)
    return message

def prefetch_qualification_strings():
    """
    Continuously prefetch qualification strings and store them in a queue.
    This function runs in a separate thread.
    """
    while True:
        if not qualification_queue.full():
            qualification_str = fetch_qualification_string()
            qualification_queue.put(qualification_str)

# Start prefetching in a separate thread
threading.Thread(target=prefetch_qualification_strings, daemon=True).start()

# Define the layout of the app
text_height = '40vh'  # Keep text height consistent with images
wrap_width = '40ch'  # Soft-wrap at 40 characters
font_size = '40px'  # Font size for readability
line_height = '1.5'  # Line height for readability
overflow_y = 'auto'  # Allow scrolling if text is too long
app.layout = html.Div(
    style={
        'alignItems': 'center',
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100vh',  # Full viewport height to center content vertically
        'justifyContent': 'center',
        'padding': '0 20px',  # Padding to ensure content isn't too close to edges
    },
    children=[
        html.Div(
            style={
                'alignItems': 'center',
                'display': 'flex',
                'justifyContent': 'center',
                'width': '90%',  # Relax the width constraint
                'maxWidth': '1200px',  # Max width for large screens
                'margin': 'auto',
            },
            children=[
                
                # Green check image on the left
                html.Img(
                    id='green-check',
                    src='assets/png/green_check.png',
                    style={
                        'flex': '0 0 auto',
                        'height': text_height,
                        'margin-right': '10px',
                        'cursor': 'pointer'  # Indicates that the image is clickable
                    }
                ),

                # Qualification text in the center
                html.Div(
                    id='qualification-text',
                    children=fetch_qualification_string(),
                    style={
                        'flex': '1',
                        'font-size': font_size,
                        'lineHeight': line_height,
                        'textAlign': 'justify',  # Default text alignment
                        'whiteSpace': 'pre-wrap',
                        'width': wrap_width,
                        'overflowY': overflow_y,
                        'height': text_height,
                    }
                ),

                # Red x image on the right
                html.Img(
                    id='red-x',
                    src='assets/png/red_x.png',
                    style={
                        'flex': '0 0 auto',
                        'height': text_height,
                        'margin-left': '10px',
                        'cursor': 'pointer'  # Indicates that the image is clickable
                    }
                )
            ]
        )
    ]
)

# Callback to update the qualification text and alignment when an image is clicked
@app.callback(
    [Output('qualification-text', 'children'),
     Output('qualification-text', 'style')],
    [Input('green-check', 'n_clicks'),
     Input('red-x', 'n_clicks')],
    [State('qualification-text', 'children')]
)
def update_qualification_text(green_clicks, red_clicks, current_text):
    
    # Check if qualification strings are available in the queue
    if not qualification_queue.empty():
        new_qualification_str = qualification_queue.get()
    
    # Fallback to current text if no new text is available
    else:
        new_qualification_str = current_text

    # Determine text alignment based on the new qualification string length
    text_align = 'justify' if len(new_qualification_str) > 40 else 'center'
    text_style = {
        'flex': '1',
        'font-size': font_size,
        'lineHeight': line_height,
        'textAlign': text_align,
        'whiteSpace': 'pre-wrap',
        'width': wrap_width,
        'overflowY': overflow_y,
        'height': text_height,
    }

    return new_qualification_str, text_style

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)