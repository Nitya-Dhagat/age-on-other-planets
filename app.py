# from flask import Flask, render_template, request
#
# app = Flask(__name__)
#
# # Orbital periods in Earth years
# planet_years = {
#     "Mercury": 0.24,
#     "Venus": 0.62,
#     "Earth": 1.00,
#     "Mars": 1.88,
#     "Jupiter": 11.86,
#     "Saturn": 29.46,
#     "Uranus": 84.01,
#     "Neptune": 164.79
# }
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/result', methods=['POST'])
# def result():
#     try:
#         earth_age = float(request.form['age'])
#     except ValueError:
#         return render_template('index.html', error="Please enter a valid number.")
#
#     planetary_ages = {
#         planet: round(earth_age / year_length, 2)
#         for planet, year_length in planet_years.items()
#     }
#
#     return render_template('result.html', earth_age=earth_age, planetary_ages=planetary_ages)
#
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, make_response
import pdfkit

app = Flask(__name__)

planet_years = {
    "Mercury": 0.24,
    "Venus": 0.62,
    "Earth": 1.00,
    "Mars": 1.88,
    "Jupiter": 11.86,
    "Saturn": 29.46,
    "Uranus": 84.01,
    "Neptune": 164.79
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    try:
        earth_age = float(request.form['age'])
    except ValueError:
        return render_template('index.html', error="Please enter a valid number.")

    planetary_ages = {
        planet: round(earth_age / year_length, 2)
        for planet, year_length in planet_years.items()
    }

    return render_template('result.html', earth_age=earth_age, planetary_ages=planetary_ages)

@app.route('/age-report', methods=['POST'])
def passport():
    earth_age = float(request.form['earth_age'])
    planetary_ages = {
        planet: round(earth_age / year_length, 2)
        for planet, year_length in planet_years.items()
    }

    rendered_html = render_template('passport_template.html',
                                    earth_age=earth_age,
                                    planetary_ages=planetary_ages)

    # Generate PDF using pdfkit
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered_html, False, configuration=config)

    # Return as downloadable response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=space_age_report.pdf'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
