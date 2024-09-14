from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="yash",
    password="cyber#VIT22",
    database="my_database"
)

cursor = db.cursor()

# Set the upload folder path
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route for joining a team
@app.route('/join-team', methods=['POST'])
def join_team():
    data = request.json
    team_code = data.get('teamCode')

    # Query to verify the team code
    cursor.execute("SELECT * FROM Teams WHERE team_code = %s", (team_code,))
    result = cursor.fetchone()

    if result:
        return jsonify({"success": True, "message": "Successfully joined the team."})
    else:
        return jsonify({"success": False, "message": "Invalid team code."})

# Route for file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileUpload' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    
    file = request.files['fileUpload']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400

    # Save the file to the specified folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    return jsonify({"success": True, "message": "File uploaded successfully!"})

@app.route('/post-announcement', methods=['POST'])
def post_announcement():
    data = request.get_json()
    announcement = data['announcement']
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO announcements (announcement) VALUES (%s)", (announcement,))
        connection.commit()
        return jsonify({"success": True, "message": "Announcement posted successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    finally:
        cursor.close()
        connection.close()

@app.route('/get-announcements', methods=['GET'])
def get_announcements():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT announcement FROM announcements")
        announcements = cursor.fetchall()
        return jsonify([{"text": announcement[0]} for announcement in announcements])
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)