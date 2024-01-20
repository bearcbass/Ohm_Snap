import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

# from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
# from segment_anything.utils.onnx import SamOnnxModel
from PIL import Image


def show_mask(mask, ax):
    color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def save_mask(mask):
    color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    image = Image.fromarray(mask_image)
    image.save("src/assets/data/img.jpeg")
    # np.save("src/assets/data/img.jpeg", image_embedding)


def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(
        plt.Rectangle((x0, y0), w, h, edgecolor="green", facecolor=(0, 0, 0, 0), lw=2)
    )


def show_img(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.axis("on")
    plt.show()
