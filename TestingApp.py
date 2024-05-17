# -*- coding: utf-8 -*-
"""
Created on Thu May 16 15:32:20 2024

@author: marya
"""

import requests
import json

# Base URL for the API
BASE_URL = 'http://127.0.0.1:5000'

# Function to clear all notes
def clear_notes():
    url = f'{BASE_URL}/clear_notes'
    response = requests.post(url)
    return response.json()

# Function to add a note
def add_note(content):
    url = f'{BASE_URL}/add_note'
    payload = {'content': content}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

# Function to get recent notes
def get_recent_notes(limit=5):
    url = f'{BASE_URL}/get_recent_notes?limit={limit}'
    response = requests.get(url)
    return response.json()

# Function to search notes
def search_notes(query):
    url = f'{BASE_URL}/search_notes'
    payload = {'query': query}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

# Testing the API
if __name__ == '__main__':
    # Clear all notes
    clear_notes_response = clear_notes()
    print('Clear Notes Response:', clear_notes_response)

    # Add a few varied notes
    notes = [
        'Dentist appointment on Monday at 10:00',
        "Recipe for Sunday's pasta dinner: 8 cups of pasta (we used Farfalle) 12 cups of cold water 1 tablespoon of olive oil 1 tablespoon of sea salt or kosher salt 2 medium onions, diced 2 large garlic cloves, minced 1 tablespoon of Italian seasoning ...",
        'TODO: Check articles about LLMs with Memory',
        '#portuguese sorrir - to smile',
        'Meeting with Bob on Tuesday at 14:00',
        'Grocery shopping list: milk, bread, eggs',
        'Finish reading the book by Friday',
        'Call Alice about the project update',
        'Yoga class on Saturday morning'
    ]
    for note in notes:
        add_note_response = add_note(note)
        print('Add Note Response:', add_note_response)

    # Get recent notes
    recent_notes_response = get_recent_notes(limit=5)
    print('Recent Notes Response:', recent_notes_response)

    # Search notes
    queries = [
        'appointment',
        'LLM',
        'Portuguese words',
        'weekend plans',
        'grocery'
    ]
    for query in queries:
        search_notes_response = search_notes(query)
        print(f"Search Notes Response for '{query}':", search_notes_response)


