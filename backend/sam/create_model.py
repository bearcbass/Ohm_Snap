import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
from segment_anything.utils.onnx import SamOnnxModel
from PIL import Image
import onnxruntime
from onnxruntime.quantization import QuantType
from onnxruntime.quantization.quantize import quantize_dynamic
import sys
import util

CHECKPOINT = "./sam/sam_vit_h_4b8939.pth"
MODEL_TYPE = "vit_h"


def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels == 1]
    neg_points = coords[labels == 0]
    ax.scatter(
        pos_points[:, 0],
        pos_points[:, 1],
        color="green",
        marker="*",
        s=marker_size,
        edgecolor="white",
        linewidth=1.25,
    )
    ax.scatter(
        neg_points[:, 0],
        neg_points[:, 1],
        color="red",
        marker="*",
        s=marker_size,
        edgecolor="white",
        linewidth=1.25,
    )


# output path must have file ext. np
def embed_image(input_path: str, output_path: str):
    sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT)
    image = cv2.imread(input_path)
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(image)
    predictor = SamPredictor(sam)
    predictor.set_image(image)
    image_embedding = predictor.get_image_embedding().cpu().numpy()
    np.save(output_path, image_embedding)


def save_mask_img(mask, ax, output):
    print(mask.shape)
    mask_image = mask_img(mask, ax, output)
    im = Image.fromarray(mask_image)
    im.save(output + ".jpeg")
    ax.imshow(mask_image)


def mask_img(mask):
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1)  # * color.reshape(1, 1, -1)
    mask_image = np.squeeze(mask_image, axis=2)
    return mask_image


def show_mask(mask, ax, output):
    # color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    print(mask.shape)
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1)  # * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def point_image(input_path, output_path, x, y):
    sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT)
    image = cv2.imread(input_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mask_generator = SamAutomaticMaskGenerator(sam)
    # masks = mask_generator.generate(image)
    # save_mask(masks)
    # masks = mask_generator.generate(image)
    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    show_points(input_point, input_label, plt.gca())
    plt.axis("on")
    plt.show()

    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    for i, (mask, score) in enumerate(zip(masks, scores)):
        plt.figure(figsize=(10, 10))
        # plt.imshow(image)
        show_mask(mask, plt.gca(), output_path)
        show_points(input_point, input_label, plt.gca())
        plt.title(f"Mask {i+1}, Score: {score:.3f}", fontsize=18)
        plt.axis("off")
        plt.show()
        # image_embedding = predictor.get_image_embedding().cpu().numpy()
        # np.save(output_path, image_embedding)


def mask_query(img_path, point) -> []:
    """
    img_path - path to the image
    point - cartesian coord query for the mask
    returns - array of np-arrays representative of images (JPEG)
    """
    sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT)
    image = cv2.imread(input_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mask_generator = SamAutomaticMaskGenerator(sam)
    predictor = SamPredictor(sam)
    predictor.set_image(image)
    input_point = np.array([[point.x, point.y]])
    input_label = np.array([1])
    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    mask_images = []
    for i, (mask, score) in enumerate(zip(masks, scores)):
        # save_mask_img(mask, plt.gca(), output_path + "i")
        mask_images.append(mask_img(mask))
    return mask_images


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    embed_image(input_path, output_path)  # for embedding images

    # uncomment if you want to get only a point image
    # x = sys.argv[3]
    # y = sys.argv[4]
    # point_image(input_path, output_path, x, y)
