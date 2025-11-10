from typing import List
import torch
import tensorflow as tf


def check_torch_can_use_cuda() -> None:
    print(f"PyTorch Version: {torch.__version__}")
    availiability: bool = torch.cuda.is_available()
    print(f"Whether CUDA is available: {availiability}")
    if torch.cuda.is_available():
        print(f"PyTorch GPU Device: {torch.cuda.get_device_name(0)}")

def check_tensorflow_can_use_cuda() -> None:
    print(f"TensorFlow Version: {tf.__version__}")
    gpus: List[tf.config.PhysicalDevice] = tf.config.list_physical_devices('GPU') # type: ignore
    if gpus:
        print(f"Tensorflow GPU Device: {torch.cuda.get_device_name(0)}")
    else:
        print(f"Can't find any GPU Devices: CPU Mode")


if __name__ == '__main__':
    check_torch_can_use_cuda()
    check_tensorflow_can_use_cuda()
    pass
