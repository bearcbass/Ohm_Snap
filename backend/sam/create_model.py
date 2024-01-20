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
    # save_mask(masks)

    predictor = SamPredictor(sam)
    predictor.set_image(image)
    image_embedding = predictor.get_image_embedding().cpu().numpy()
    np.save(output_path, image_embedding)


def point_image(input_path, output_path):
    sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT)
    image = cv2.imread(input_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mask_generator = SamAutomaticMaskGenerator(sam)
    # masks = mask_generator.generate(image)
    # save_mask(masks)

    predictor = SamPredictor(sam)
    predictor.set_image(image)
    input_point = np.array([[500, 500]])
    input_label = np.array([1])
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
    # image_embedding = predictor.get_image_embedding().cpu().numpy()
    # np.save(output_path, image_embedding)


# onnx_model_path = None

# import warnings

# onnx_model_path = "sam_onnx_example.onnx"

# onnx_model = SamOnnxModel(sam, return_single_mask=True)

# dynamic_axes = {
#     "point_coords": {1: "num_points"},
#     "point_labels": {1: "num_points"},
# }
onnx_model_quantized_path = "sam_onnx_quantized_example.onnx"
# quantize_dynamic(
#     model_input=onnx_model_path,
#     model_output=onnx_model_quantized_path,
#     # optimize_model=True,
#     per_channel=False,
#     reduce_range=False,
#     weight_type=QuantType.QUInt8,
# )
# onnx_model_path = onnx_model_quantized_path

# ort_session = onnxruntime.InferenceSession(onnx_model_path)
# embed_dim = sam.prompt_encoder.embed_dim
# embed_size = sam.prompt_encoder.image_embedding_size
# mask_input_size = [4 * x for x in embed_size]
# dummy_inputs = {
#     "image_embeddings": torch.randn(1, embed_dim, *embed_size, dtype=torch.float),
#     "point_coords": torch.randint(low=0, high=1024, size=(1, 5, 2), dtype=torch.float),
#     "point_labels": torch.randint(low=0, high=4, size=(1, 5), dtype=torch.float),
#     "mask_input": torch.randn(1, 1, *mask_input_size, dtype=torch.float),
#     "has_mask_input": torch.tensor([1], dtype=torch.float),
#     "orig_im_size": torch.tensor([1500, 2250], dtype=torch.float),
# }
# output_names = ["masks", "iou_predictions", "low_res_masks"]

# with warnings.catch_warnings():
#     warnings.filterwarnings("ignore", category=torch.jit.TracerWarning)
#     warnings.filterwarnings("ignore", category=UserWarning)
#     with open(onnx_model_path, "wb") as f:
#         torch.onnx.export(
#             onnx_model,
#             tuple(dummy_inputs.values()),
#             f,
#             export_params=True,
#             verbose=False,
#             opset_version=17,
#             do_constant_folding=True,
#             input_names=list(dummy_inputs.keys()),
#             output_names=output_names,
#             dynamic_axes=dynamic_axes,
#         )


# onnx_model_quantized_path = "sam_onnx_quantized_example.onnx"
# quantize_dynamic(
#     model_input=onnx_model_path,
#     model_output=onnx_model_quantized_path,
#     # optimize_model=True,
#     per_channel=False,
#     reduce_range=False,
#     weight_type=QuantType.QUInt8,
# )
# onnx_model_path = onnx_model_quantized_path

# ort_session = onnxruntime.InferenceSession(onnx_model_path)

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    embed_image(input_path, output_path)
    # point_image(input_path, output_path)
