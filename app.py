import os
import logging
from flask import Flask, render_template, request, jsonify, send_file
from password_analyzer import PasswordAnalyzer
from wordlist_generator import WordlistGenerator
import tempfile

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

password_analyzer = PasswordAnalyzer()
wordlist_generator = WordlistGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_password', methods=['POST'])
def analyze_password():
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    try:
        analysis = password_analyzer.analyze(password)
        return jsonify(analysis)
    except Exception as e:
        logging.error(f"Password analysis error: {str(e)}")
        return jsonify({'error': 'Analysis failed'}), 500

@app.route('/generate_wordlist', methods=['POST'])
def generate_wordlist():
    try:
        name = request.form.get('name', '').strip()
        birthdate = request.form.get('birthdate', '').strip()
        pet_names = request.form.get('pet_names', '').strip()
        custom_words = request.form.get('custom_words', '').strip()
        include_leetspeak = request.form.get('include_leetspeak') == 'on'
        include_years = request.form.get('include_years') == 'on'
        
        if not any([name, birthdate, pet_names, custom_words]):
            return render_template('index.html', error='Please provide at least one input for wordlist generation')
        
        wordlist = wordlist_generator.generate(
            name=name,
            birthdate=birthdate,
            pet_names=pet_names,
            custom_words=custom_words,
            include_leetspeak=include_leetspeak,
            include_years=include_years
        )
        
        if not wordlist:
            return render_template('index.html', error='No words generated. Please check your inputs.')
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write('\n'.join(wordlist))
        temp_file.close()
        
        return send_file(temp_file.name, as_attachment=True, download_name='custom_wordlist.txt', mimetype='text/plain')
        
    except Exception as e:
        logging.error(f"Wordlist generation error: {str(e)}")
        return render_template('index.html', error='Wordlist generation failed')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)