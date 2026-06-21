from flask import Flask, render_template, request
import joblib
import os
from flask_mysqldb import MySQL

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sms_ai'

mysql = MySQL(app)

# Load model dengan path absolut
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model_sms_pintar.joblib')

try:
    model = joblib.load(model_path)
    print("✓ Model berhasil dimuat!")
except Exception as e:
    print("ERROR memuat model:", e)
    model = None


@app.route('/', methods=['GET', 'POST'])
def home():
    prediksi = ""
    text_input = ""

    if request.method == 'POST':
        text_input = request.form.get('sms_text', '').strip()

        if text_input:
            # Cek apakah model berhasil dimuat
            if model is None:
                prediksi = "Error: Model tidak berhasil dimuat."
            else:
                # Lakukan prediksi
                hasil = model.predict([text_input])[0]

                # Format hasil prediksi
                if hasil == 'penipuan':
                    prediksi = "HATI-HATI! Ini SMS PENIPUAN."
                elif hasil == 'promo':
                    prediksi = "Ini hanya SMS PROMO."
                else:
                    prediksi = "Aman. Ini SMS NORMAL."

                # Simpan ke database
                try:
                    cur = mysql.connection.cursor()
                    cur.execute(
                        "INSERT INTO hasil_prediksi (isi_sms, hasil) VALUES (%s, %s)",
                        (text_input, hasil)
                    )
                    mysql.connection.commit()
                    cur.close()
                except Exception as e:
                    print("ERROR menyimpan ke database:", e)

    return render_template('index.html', prediksi=prediksi, text_input=text_input)


if __name__ == '__main__':
    app.run(debug=True)
