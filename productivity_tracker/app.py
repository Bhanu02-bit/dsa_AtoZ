from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Database setup
def init_db():
    conn = sqlite3.connect('productivity.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            scheduled_time DATETIME,
            completed BOOLEAN DEFAULT FALSE,
            completion_time DATETIME,
            category TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_of_week TEXT,
            start_time TEXT,
            end_time TEXT,
            task_name TEXT,
            priority INTEGER DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('productivity.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks ORDER BY scheduled_time')
    tasks = cursor.fetchall()
    
    # Convert to list of dicts
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task[0],
            'title': task[1],
            'description': task[2],
            'scheduled_time': task[3],
            'completed': bool(task[4]),
            'completion_time': task[5],
            'category': task[6]
        })
    
    conn.close()
    return jsonify(task_list)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    
    conn = sqlite3.connect('productivity.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tasks (title, description, scheduled_time, category)
        VALUES (?, ?, ?, ?)
    ''', (data['title'], data.get('description', ''), 
                   data.get('scheduled_time'), data.get('category', 'General'))
    
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    
    conn = sqlite3.connect('productivity.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE tasks SET completed = ?, completion_time = ?
        WHERE id = ?
    ''', (data['completed'], datetime.now(), task_id))
    
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/analytics/daily')
def daily_analytics():
    conn = sqlite3.connect('productivity.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total_tasks,
            SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed_tasks
        FROM tasks 
        WHERE DATE(scheduled_time) = DATE(?) 
    ''', (datetime.now().date(),))
    
    result = cursor.fetchone()
    conn.close()
    
    return jsonify({
        'total_tasks': result[0],
        'completed_tasks': result[1] if result[1] else 0
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)