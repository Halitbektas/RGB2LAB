import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def convert_image_rgb_to_lab(image_path, output_dir):
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        print("image not found")
        return

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    L, a, b = cv2.split(img_lab)

    sobelx = cv2.Sobel(L, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(L, cv2.CV_64F, 0, 1, ksize=3)

    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    # Panel A: RGB Clinical Image
    axs[0, 0].imshow(img_rgb)
    axs[0, 0].set_title('A: RGB clinical image', fontsize=10, loc='left')
    axs[0, 0].axis('off')

    im_a = axs[0, 1].imshow(a, cmap='coolwarm')
    axs[0, 1].set_title('B: CIELAB a* red-green channel', fontsize=10, loc='left')
    axs[0, 1].axis('off')
    fig.colorbar(im_a, ax=axs[0, 1], fraction=0.046, pad=0.04)

    im_l = axs[1, 0].imshow(L, cmap='gray')
    axs[1, 0].set_title('C: L* luminance channel', fontsize=10, loc='left')
    axs[1, 0].axis('off')
    fig.colorbar(im_l, ax=axs[1, 0], fraction=0.046, pad=0.04)

    im_g = axs[1, 1].imshow(gradient_magnitude, cmap='magma')
    axs[1, 1].set_title('D: Gradient magnitude / boundary cue', fontsize=10, loc='left')
    axs[1, 1].axis('off')
    fig.colorbar(im_g, ax=axs[1, 1], fraction=0.046, pad=0.04)

    plt.tight_layout()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.basename(image_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    save_path = os.path.join(output_dir, f"{file_name_without_ext}_analyzed.png")

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Görsel başarıyla kaydedildi: {save_path}")

    plt.close(fig)


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    input_image = os.path.join(BASE_DIR, "photos", "aug_749_acne-cystic-118.jpg")
    output_folder = os.path.join(BASE_DIR, "outputs")

    convert_image_rgb_to_lab(input_image, output_folder)