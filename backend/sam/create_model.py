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
import os
from vision.mask_to_original import mask_to_original

CHECKPOINT = "./sam/sam_vit_h_4b8939.pth"
MODEL_TYPE = "vit_h"


def load_model():
    return sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT)


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
    mask_image = mask_img(mask)
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


def mask_query(
    img_path,
    point,
    model=None,
) -> []:
    """
    img_path - path to the image
    point - cartesian coord query for the mask
    returns - array of np-arrays representative of images (JPEG)
    """
    if not model:
        sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT)
    else:
        sam = model
    assert os.path.isfile(img_path) == True
    image = cv2.imread(img_path)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mask_generator = SamAutomaticMaskGenerator(sam)
    predictor = SamPredictor(sam)
    predictor.set_image(image)
    input_point = np.array([[point[0], point[1]]])
    input_label = np.array([1])
    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    mask_images = []
    for i, (mask, score) in enumerate(zip(masks, scores)):
        normalized_bw_image = (mask * 255).astype(np.uint8)
        rgb_image = np.stack([normalized_bw_image] * 3, axis=-1)
        mask = mask_to_original(image, rgb_image)
        # save_mask_img(mask, plt.gca(), "i")
        # mask_image = mask_img(mask)
        # mask = mask_to_original(image, mask_image)

        # im = Image.fromarray((mask_img(mask)))
        im = Image.fromarray(mask)
        mask_images.append(im)
    return mask_images


def show_anns(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x["area"]), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones(
        (
            sorted_anns[0]["segmentation"].shape[0],
            sorted_anns[0]["segmentation"].shape[1],
            4,
        )
    )
    img[:, :, 3] = 0
    for ann in sorted_anns:
        m = ann["segmentation"]
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    ax.imshow(img)


def matrix_reduce(image):
    rows, cols = np.where(matrix == 1)
    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)
    return matrix[min_row : max_row + 1, min_col : max_col + 1]


def all_masks(img):
    sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT)
    image = cv2.imread(input_path)
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(image)
    return masks


def add_black_padding(image, padding_size):
    # Pad the image with black pixels
    padded_image = np.pad(
        image,
        ((padding_size, padding_size), (padding_size, padding_size), (0, 0)),
        mode="constant",
    )

    return padded_image


def crop_non_black_region(image):
    # Find indices of non-black pixels
    non_black_indices = np.any(image != [0, 0, 0], axis=-1)

    # Check if there are any non-black pixels in the image
    if not np.any(non_black_indices):
        return np.array([])

    # Calculate the bounding box
    rows, cols = np.where(non_black_indices)
    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)

    # Extract the portion of the image within the bounding box
    cropped_image = image[min_row : max_row + 1, min_col : max_col + 1]

    return add_black_padding(cropped_image, 100)


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    mask_query(input_path, (100, 100))
    # image = cv2.imread(input_path)
    # plt.figure(figsize=(10, 10))
    # embed_image(input_path, output_path)
    # # show_points(input_point, input_label, plt.gca())
    # plt.axis("on")
    # image = crop_non_black_region(image)
    # plt.imshow(image)
    # plt.axis("off")
    # masks = all_masks(image)
    # show_anns(masks)
    # plt.axis("off")
    # plt.show()

    # embed_image(input_path, output_path)  # for embedding images

    # uncomment if you want to get only a point image
    # x = sys.argv[3]
    # y = sys.argv[4]
    # point_image(input_path, output_path, x, y)
