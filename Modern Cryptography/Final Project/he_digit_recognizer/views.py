from django.shortcuts import render
import torch
import tenseal as ts
from django.views.decorators.csrf import ensure_csrf_cookie
import os
from torchvision import transforms
from PIL import Image
import base64
import io
import json
from time import time
from django.conf import settings
from django.core.files.base import *
from django.core.files.storage import *

json_path = os.path.join(settings.STATICFILES_DIRS[0],"digits_index.json")

digits = json.load(open(json_path))

class ConvNet(torch.nn.Module):
    def __init__(self, hidden=64, output=10):
        super(ConvNet, self).__init__()        
        self.conv1 = torch.nn.Conv2d(1, 4, kernel_size=7, padding=0, stride=3)
        self.fc1 = torch.nn.Linear(256, hidden)
        self.fc2 = torch.nn.Linear(hidden, output)

    def forward(self, x):
        x = self.conv1(x)
        # the model uses the square activation function
        x = x * x
        # flattening while keeping the batch axis
        x = x.view(-1, 256)
        x = self.fc1(x)
        x = x * x
        x = self.fc2(x)
        return x

## Encryption Parameters

# controls precision of the fractional part
bits_scale = 26

# Create TenSEAL context
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[31, bits_scale, bits_scale, bits_scale, bits_scale, bits_scale, bits_scale, 31]
)

# set the scale
context.global_scale = pow(2, bits_scale)

# galois keys are required to do ciphertext rotations
context.generate_galois_keys()

class EncConvNet:
    def __init__(self, torch_nn):
        self.conv1_weight = torch_nn.conv1.weight.data.view(
            torch_nn.conv1.out_channels, torch_nn.conv1.kernel_size[0],
            torch_nn.conv1.kernel_size[1]
        ).tolist()
        self.conv1_bias = torch_nn.conv1.bias.data.tolist()
        
        self.fc1_weight = torch_nn.fc1.weight.T.data.tolist()
        self.fc1_bias = torch_nn.fc1.bias.data.tolist()
        
        self.fc2_weight = torch_nn.fc2.weight.T.data.tolist()
        self.fc2_bias = torch_nn.fc2.bias.data.tolist()
        
        
    def forward(self, enc_x, windows_nb):
        # conv layer
        enc_channels = []
        for kernel, bias in zip(self.conv1_weight, self.conv1_bias):
            y = enc_x.conv2d_im2col(kernel, windows_nb) + bias
            enc_channels.append(y)
        # pack all channels into a single flattened vector
        enc_x = ts.CKKSVector.pack_vectors(enc_channels)
        # square activation
        enc_x.square_()
        # fc1 layer
        enc_x = enc_x.mm(self.fc1_weight) + self.fc1_bias
        # square activation
        enc_x.square_()
        # fc2 layer
        enc_x = enc_x.mm(self.fc2_weight) + self.fc2_bias
        return enc_x
    
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)
model = ConvNet()
model.load_state_dict(torch.load("model.h5"))
model.eval()
kernel_shape = model.conv1.kernel_size
stride = model.conv1.stride[0]
enc_model = EncConvNet(model)


def transform_image(image_bytes):
    """
    Transform image into required format: 28x28.
    Return the corresponding tensor.
    """
    my_transforms = transforms.Compose([
                                        transforms.ToTensor(),
                                        transforms.Resize((28,28))
                                       ])
    image = Image.open(io.BytesIO(image_bytes)).convert('L')
    return my_transforms(image).unsqueeze(0)
def encrypted_model(tensor):
    x_enc, windows_nb = ts.im2col_encoding(
            context, tensor.view(28, 28).tolist(), kernel_shape[0],
            kernel_shape[1], stride
        )
    # print(tensor)
    enc_outputs = enc_model.forward(x_enc, windows_nb)
    outputs = enc_outputs.decrypt()
    outputs = torch.tensor(outputs).view(1,-1)
    return outputs
def plain_model(tensor):
     return model.forward(tensor)

def get_prediction(image_bytes, option):
    tensor = transform_image(image_bytes)
    outputs = encrypted_model(tensor) if option=='he' else plain_model(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    human_label = digits[predicted_idx]
    return human_label



   
def index(request):
    predicted_label = None
    time_info = None
    if request.method=="POST":
            image_data = request.POST.get("canvasData")
            model_option = request.POST.get("model")
            image_bytes = base64.b64decode(image_data)
            try:
                start = time()
                predicted_label = get_prediction(image_bytes,model_option)
                end = time()
                time_info = end-start
                time_info = round(time_info,5)
            except RuntimeError as ex:
                print(ex) 
    context = {
        "predicted_label": predicted_label,
        "time_info": time_info
    }
    return render(request, "index.html",context)