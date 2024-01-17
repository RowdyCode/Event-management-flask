from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
db = SQLAlchemy(app)

# Define the Event model
class Event(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)

# Create the database tables
db.create_all()

# Define routes
@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/create_event', methods=['POST'])
def create_event():
    event_name = request.form.get('event_name')
    event_date = request.form.get('event_date')

    # Generate a unique random ID using UUID
    event_id = str(uuid.uuid4())

    new_event = Event(id=event_id, name=event_name, date=event_date)
    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_event/<string:event_id>')
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')

    if search_term:
        # Perform the search logic based on serial number (UUID)
        filtered_results = Event.query.filter(
            or_(
                Event.id.ilike(f"%{search_term}%"),
                Event.name.ilike(f"%{search_term}%"),
                Event.date.ilike(f"%{search_term}%")
            )
        ).all()
    else:
        # If no search term is provided, return all events
        filtered_results = Event.query.all()

    return render_template('index.html', events=filtered_results, search_term=search_term)
@app.route('/manage_event/<string:event_id>')
def manage_event(event_id):
    # Add logic for managing a specific event with ID 'event_id'
    # For now, let's just render a template
    return render_template('manage_event.html', event_id=event_id)

# Rest of the code remains the same

if __name__ == '__main__':
    app.run(debug=True)
