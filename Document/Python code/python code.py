from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage
doctors = {}  # {"Dr. Smith": ["2025-07-01 10:00", "2025-07-01 11:00"]}
appointments = []  # {"doctor": ..., "patient": ..., "datetime": ...}

@app.route('/')
def home():
    return render_template('index.html', doctors=doctors)

@app.route('/add_slot', methods=['POST'])
def add_slot():
    doctor = request.form['doctor']
    date = request.form['date']
    time = request.form['time']
    datetime = f"{date} {time}"
    if doctor not in doctors:
        doctors[doctor] = []
    doctors[doctor].append(datetime)
    return redirect(url_for('home'))

@app.route('/book/<doctor>', methods=['GET', 'POST'])
def book(doctor):
    if request.method == 'POST':
        slot = request.form['slot']
        patient = request.form['patient']
        if slot in doctors[doctor]:
            doctors[doctor].remove(slot)
            appointments.append({
                'doctor': doctor,
                'patient': patient,
                'datetime': slot
            })
        return redirect(url_for('view_appointments'))
    return render_template('book.html', doctor=doctor, slots=doctors.get(doctor, []))

@app.route('/appointments')
def view_appointments():
    return render_template('appointments.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)
    