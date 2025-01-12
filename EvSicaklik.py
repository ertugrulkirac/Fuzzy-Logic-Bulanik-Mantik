import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Giriş ve çıkış değişkenlerini tanımlıyoruz. "Antecedent:Giriş", "Consequent:Çıkış"
sicaklik = ctrl.Antecedent(np.arange(0, 31, 1), 'sicaklik')  # Sıcaklık: 0-30 derece
kombiseviye = ctrl.Consequent(np.arange(0, 101, 1), 'kombiseviye')  # Kombi seviyesi: 0-100, Max Sıcaklık:60-80 derece

# Üyelik fonksiyonlarını tanımlıyoruz
sicaklik['soguk'] = fuzz.trimf(sicaklik.universe, [0, 5, 10])
sicaklik['ilik'] = fuzz.trimf(sicaklik.universe, [5, 10, 20])
sicaklik['sicak'] = fuzz.trimf(sicaklik.universe, [10, 20, 30])

kombiseviye['dusuk'] = fuzz.trimf(kombiseviye.universe, [0, 30, 50])
kombiseviye['orta'] = fuzz.trimf(kombiseviye.universe, [30, 50, 70])
kombiseviye['yuksek'] = fuzz.trimf(kombiseviye.universe, [50, 70, 100])

# Kurallar oluşturuyoruz
kural1 = ctrl.Rule(sicaklik['soguk'], kombiseviye['yuksek'])
kural2 = ctrl.Rule(sicaklik['ilik'], kombiseviye['orta'])
kural3 = ctrl.Rule(sicaklik['sicak'], kombiseviye['dusuk'])

# Kontrol sistemini oluşturuyoruz
kombikontrol = ctrl.ControlSystem([kural1, kural2, kural3])
kombisimulasyon = ctrl.ControlSystemSimulation(kombikontrol)

# Örnek sıcaklık değeri verip, sonucu hesaplıyoruz
sicaklik_degeri = 18  # Örnek sıcaklık değeri, giriş üyelik fonksiyonumuza göre "ılık"
kombisimulasyon.input['sicaklik'] = sicaklik_degeri

# Hesaplama yapıyoruz
kombisimulasyon.compute()

# Sonuçları yazdırıyoruz
print(f"Sıcaklık: {sicaklik_degeri} derece")
print(f"Kombi seviyesi: {kombisimulasyon.output['kombiseviye']:.2f}")

# Sonuçları görselleştiriyoruz
kombiseviye.view(sim=kombisimulasyon)
