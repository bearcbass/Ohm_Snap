# Not needed for hackathon

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
