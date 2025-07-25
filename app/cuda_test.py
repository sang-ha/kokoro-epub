import torch
import torchvision

print("CUDA available:", torch.cuda.is_available())
print("GPU name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")
print("Torch version:", torch.version.cuda)
print("Torchvision version:", torchvision.__version__)