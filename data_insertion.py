import csv
import logging

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

# Initialize database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://dbuser:admin1234@EmoSound"
db = SQLAlchemy(app)

# Define SQLAlchemy model for the 'songs' table
class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    emotion = db.Column(db.String(255), nullable=False)

# Route to insert data from CSV into the 'songs' table
@app.route('/insert_data_from_csv', methods=['POST'])
def insert_data_from_csv():
    try:
        logging.info('Attempting to insert data from CSV.')
        # Read data from CSV file
        file_path = r'C:\Users\Nimesh Nilanga\Documents\Hiruni\happy.csv'
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Create a Song object and insert into the database
                song = Song(
                    name=row['Name'],
                    album=row['Album'],
                    artist=row['Artist'],
                    emotion=row['Emotion']
                )
                db.session.add(song)
            db.session.commit()
        logging.info('Data inserted successfully from CSV.')
        return jsonify({'message': 'Data inserted successfully'}), 200
    except Exception as e:
        logging.error(f'Failed to insert data from CSV: {str(e)}')
        return jsonify({'error': 'Failed to insert data'}), 500
