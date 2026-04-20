from flask import Flask, render_template, request
import joblib

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Load model yang sudah dilatih
# Pastikan file .joblib ada di folder yang sama
try:
    model = joblib.load('model_sms_pintar.joblib')
except:
    print("Error: File model tidak ditemukan!")

@app.route('/', methods=['GET', 'POST'])
def home():
    prediksi = ""
    text_input = ""
    
    if request.method == 'POST':
        # Ambil teks dari form HTML
        text_input = request.form['sms_text']
        
        if text_input:
            # Lakukan prediksi
            hasil = model.predict([text_input])[0]
            
            # Ubah teks hasil biar lebih rapi
            if hasil == 'penipuan':
                prediksi = "🚨 HATI-HATI! Ini SMS PENIPUAN."
            elif hasil == 'promo':
                prediksi = "🏷️ Ini hanya SMS PROMO."
            else:
                prediksi = "✅ Aman. Ini SMS NORMAL."
    
    return render_template('index.html', prediksi=prediksi, text_input=text_input)

if __name__ == '__main__':
    app.run(debug=True)