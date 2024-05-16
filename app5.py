# -*- coding: utf-8 -*-
"""
Created on Thu May 16 15:09:46 2024

@author: marya
"""
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import process

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///notes.db')
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)

def categorize_note(content):
    categories = {
        'appointment': ['appointment', 'meeting', 'schedule'],
        'task': ['TODO', 'task', 'finish', 'complete'],
        'plan': ['plan', 'plans', 'schedule', 'weekend'],
        'shopping': ['grocery', 'shopping', 'buy', 'list'],
        'learning': ['learn', 'study', 'research', 'check']
    }
    for category, keywords in categories.items():
        if any(keyword in content.lower() for keyword in keywords):
            return category
    return 'general'

@app.route('/add_note', methods=['POST'])
def add_note():
    content = request.json['content']
    category = categorize_note(content)
    new_note = Note(content=content, category=category)
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note added successfully'}), 201

@app.route('/get_recent_notes', methods=['GET'])
def get_recent_notes():
    limit = request.args.get('limit', 5, type=int)
    notes = Note.query.order_by(Note.id.desc()).limit(limit).all()
    return jsonify([note.content for note in notes])

@app.route('/search_notes', methods=['POST'])
def search_notes():
    query = request.json['query']
    print(f"Received search query: {query}")
    try:
        all_notes = Note.query.all()
        note_texts = [note.content for note in all_notes]
        search_results = process.extract(query, note_texts, limit=10)
        results = [match[0] for match in search_results if match[1] > 50]

        categorized_notes = Note.query.filter(Note.category.ilike(f'%{query}%')).all()
        categorized_results = [note.content for note in categorized_notes]
        results.extend(categorized_results)

        results = list(set(results))
        return jsonify({'result': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_notes', methods=['POST'])
def clear_notes():
    try:
        num_rows_deleted = db.session.query(Note).delete()
        db.session.commit()
        return jsonify({'message': f'Cleared {num_rows_deleted} notes successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)







