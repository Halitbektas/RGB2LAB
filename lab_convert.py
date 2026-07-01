import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def convert_image_rgb_to_lab(image_path, output_dir):
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        print(f"Görüntü bulunamadı: {image_path}")
        return

    # Orijinal RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # LAB Dönüşümü ve Kanalları Ayırma
    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    L, a, b = cv2.split(img_lab)

    # Gradyan Büyüklüğü (Doku / Kenar Tespiti)
    sobelx = cv2.Sobel(L, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(L, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobelx ** 2 + sobely ** 2)

    # Çıktı klasörü yoksa oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dosya ismini uzantısız olarak al (Örn: "aug_749_acne-cystic-118")
    base_name = os.path.basename(image_path)
    file_name = os.path.splitext(base_name)[0]

    # 1. L Kanalını Kaydet (Gri Tonlama)
    path_L = os.path.join(output_dir, f"{file_name}_L_channel.png")
    plt.imsave(path_L, L, cmap='gray')

    # 2. a Kanalını Kaydet (Kızarıklık - Coolwarm Isı Haritası)
    path_a = os.path.join(output_dir, f"{file_name}_a_channel.png")
    plt.imsave(path_a, a, cmap='coolwarm')

    # 3. b Kanalını Kaydet (Sarı/Mavi - Coolwarm Isı Haritası)
    path_b = os.path.join(output_dir, f"{file_name}_b_channel.png")
    plt.imsave(path_b, b, cmap='coolwarm')

    # 4. Gradyan Büyüklüğünü Kaydet (Doku - Magma Isı Haritası)
    path_grad = os.path.join(output_dir, f"{file_name}_gradient.png")
    plt.imsave(path_grad, gradient_magnitude, cmap='magma')

    # Opsiyonel: Orijinal RGB'yi de referans olarak kaydetmek isterseniz
    path_rgb = os.path.join(output_dir, f"{file_name}_original.png")
    plt.imsave(path_rgb, img_rgb)

    print(f"[{file_name}] için tüm kanallar ayrı ayrı kaydedildi.")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    input_image = os.path.join(BASE_DIR, "photos", "aug_749_acne-cystic-118.jpg")
    output_folder = os.path.join(BASE_DIR, "outputs")

    convert_image_rgb_to_lab(input_image, output_folder)