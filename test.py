# Display one image
import numpy as np
import os
import torch
import matplotlib.pyplot as plt
import torchvision.transforms as T

DATA_PATH = 'data'
DATA_SET_PATH = os.path.join(DATA_PATH, 'datset')

if __name__ == '__main__':
    i = 0

    img_path = os.path.join(DATA_SET_PATH, 'image')
    lab_path = os.path.join(DATA_SET_PATH, 'label')

    img_file = os.path.join(img_path, f'{i}.npy')
    lab_file = os.path.join(lab_path, f'{i}.npy')

    img = torch.from_numpy(np.moveaxis(np.load(img_file), -1, 0))
    lab = torch.from_numpy(np.load(lab_file))

    img = torch.squeeze(img)
    lab = torch.squeeze(lab)

    transform = T.ToPILImage()
    lab = lab.detach().numpy()+1
    img = transform(img)

    f, axs = plt.subplots(1,2)
    axs[0].imshow(img)
    axs[1].imshow(lab)
    plt.show()


