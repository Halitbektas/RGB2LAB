# CIELAB Conversion & Gradient Extractor

## 📌 Algoritmanın Amacı
Bu bileşen (component), verilen RGB/BGR formatındaki bir görüntüyü CIELAB renk uzayına dönüştürür. Ardından $L^*, a^*, b^*$ kanallarını birbirinden ayırır. Ayrıca, aydınlanma/parlaklık ($L^*$) kanalı üzerinden Sobel operatörü (ksize=3) kullanarak X ve Y yönlerindeki türevleri alır ve **gradyan büyüklüğünü (gradient magnitude)** hesaplar. Elde edilen bu 4 farklı veri (L, a, b ve gradyan), görselleştirme amacıyla matplotlib renk haritaları (colormaps) kullanılarak PNG formatında diske kaydedilir.

## ⚙️ Kurulum Adımları
Bu script'i çalıştırmak için sanal bir ortam (virtual environment) oluşturmanız ve gerekli bağımlılıkları yüklemeniz önerilir:
```bash
pip install -r requirements.txt
```

## Nasıl Çalıştırılır
1. Command Line (Script olarak):
Dosya içindeki __main__ bloğunda belirtilen input ve output yollarını kendi ortamınıza göre düzenledikten sonra terminalden çalıştırabilirsiniz:
```bash
python lab_convert.py
```
2. Python Function (Modül olarak import ederek):
Başka bir pipeline içinden doğrudan fonksiyonu çağırabilirsiniz:

```python
from lab_convert import convert_image_rgb_to_lab

convert_image_rgb_to_lab(
    image_path="path/to/your/image.jpg", 
    output_dir="path/to/save/outputs"
)
```

## Beklenen input formatı
Kabul Edilen Format: .jpg, .png gibi OpenCV'nin okuyabildiği standart görüntü dosyası yolları.

Renk Uzayı: BGR (OpenCV cv2.imread varsayılan formatı. Script içinde RGB ve LAB dönüşümleri otomatik yapılmaktadır.)

Veri Tipi (dtype): uint8 (0-255 arası değerler)

Shape: (H,W,3)

Boyut Limitleri: Özel bir boyut limiti yoktur, orijinal görüntünün boyutlarını korur.

## Output formatı

Kaydedilen Dosyalar: Orijinal dosya adının sonuna ekler yapılarak 4 adet .png dosyası oluşturulur.

[filename]_L_channel.png (Siyah-Beyaz / Gray colormap)
[filename]_a_channel.png (Kırmızı-Mavi / Coolwarm colormap)
[filename]_b_channel.png (Sarı-Mavi / Coolwarm colormap)
[filename]_gradient.png (Gradyan yoğunluğu / Magma colormap)

## Bağımlılıklar ve Python Sürümü
Python Sürümü: Python 3.8+ önerilir.

Bağımlılıklar: opencv-python, numpy, matplotlib (Detaylar requirements.txt içindedir).

## Known Limitations / Skip edilmesi gereken durumlar
Bozuk Dosya Yolu: Görüntü okunamadığında (img_bgr is None), kod hata fırlatmak yerine konsola "Görüntü bulunamadı" yazdırır ve o dosyayı atlar (skip eder).

Pipeline Entegrasyonu İçin Kritik Not: Bu script şu anda matrisleri (array) RAM üzerinde döndürmek (return) yerine plt.imsave kullanarak doğrudan diske kaydetmektedir. plt.imsave bir renk haritası (colormap) uyguladığı için diske kaydedilen çıktılar tek kanallı (1D) matrisler değil, RGBA (4 kanallı) görselleştirilmiş imajlardır.
Eğer pipeline'ın bir sonraki adımı bu çıktıları görsel olarak değil, ham matematiksel maske (raw matrix) olarak kullanacaksa, fonksiyonun diske kaydetmek yerine return L, a, b, gradient_magnitude şeklinde güncellenmesi gerekebilir.

# Version v1.0.0 - Stable

### 💡 Ekstra Tavsiye
`README.md`'nin **Known Limitations** kısmında özellikle belirttiğim `plt.imsave` detayı, entegrasyonu yapacak kişi için çok kritiktir. Pipeline'ı birleştiren kişi bu matrisleri bir makine öğrenmesi modeline besleyecekse renk haritası basılmış PNG'ler işini bozabilir. 