import torch
import torchvision
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as PathEffects
import random
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import os


class CustomDataset(Dataset):
    def __init__(self, data_dir, annotation_dir, transform=None):
        self.data_dir = data_dir
        self.annotation_dir = annotation_dir
        self.transform = transform
        self.data_list = self._load_data_list()

    def _load_data_list(self):
        data_list = []
        for img_file in os.listdir(self.data_dir):
            if img_file.endswith('.png'):
                img_path = os.path.join(self.data_dir, img_file)
                annotation_file = os.path.splitext(img_file)[0] + '.txt'
                annotation_path = os.path.join(self.annotation_dir, annotation_file)
                data_list.append((img_path, annotation_path))
        return data_list

    def __len__(self):
        return len(self.data_list)

    def __getitem__(self, idx):
        img_path, annotation_path = self.data_list[idx]

        # Carga la imagen
        image = Image.open(img_path).convert('L')  # 'L' para blanco y negro

        # Carga las anotaciones desde el archivo de texto
        annotations = []
        with open(annotation_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                label = parts[0]
                xmin, ymin, xmax, ymax = map(int, parts[1:])
                annotations.append({
                    'label': label,
                    'bbox': [xmin, ymin, xmax, ymax]
                })

        if self.transform:
            image = self.transform(image)

        return image, annotations

# Define las transformaciones que deseas aplicar a las imágenes
transform = transforms.Compose([transforms.Resize((224, 224)),
                                transforms.ToTensor()])

# Directorios de datos y anotaciones
data_dir = 'data/'
annotation_dir = 'annotations/'

# Crea una instancia de tu DataLoader personalizado
dataset = CustomDataset(data_dir, annotation_dir, transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
           'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
           'U', 'V', 'W', 'X', 'Y', 'Z', ':', '/', '\\']


def get_sample(ix):
    img, annotations = dataset[ix]  # Accede al índice ix del conjunto de datos personalizado
    img_pil = transforms.ToPILImage()(img)
    img_size = img_pil.size

    labels = []
    bbs = []

    for annotation in annotations:
        label = annotation['label']  # Obtén la etiqueta
        bbox = annotation['bbox']  # Obtén las coordenadas de la caja delimitadora

        labels.append(classes.index(label))
        bbs.append(bbox)

    labels = np.array(labels)
    bbs = np.array(bbs)

    return img_pil, (labels, bbs), img_size

def norm(bb, shape):
  # normalize bb
  # shape = (heigh, width)
  # bb = [x_min, y_min, x_max, y_max]
  h, w = shape
  return np.array([bb[0]/w, bb[1]/h, bb[2]/w, bb[3]/h])


def unnorm(bb, shape):
  # unnormalize bb
  # shape = (heigh, width)
  # bb = [x_min, y_min, x_max, y_max]
  h, w = shape
  return np.array([bb[0]*w, bb[1]*h, bb[2]*w, bb[3]*h])


def xyxy2xywh(bb):
  return torch.stack([bb[:,0], bb[:,1], bb[:,2]-bb[:,0], bb[:,3]-bb[:,1]], axis=1)


#def xywh2xyxy(bb):
#  return torch.stack([bb[:,0], bb[:,1], bb[:,0]+bb[:,2], bb[:,1]+bb[:,3]], axis=1)


def generate_anchors(scales, centers, sizes):
    k, anchors, grid_size = [], [], []
    for s in scales:
        cnt = 0
        for (x, y) in centers:
            for (w, h) in sizes:
                for i in range(s):
                    for j in range(s):
                        # cwh
                        #anchors.append(np.array([x+i, y+j, w, h])/s)
                        # xyxy
                        anchors.append(np.array([x+i-w/2, y+j-h/2, x+i+w/2, y+j+h/2])/s)
                        grid_size.append(np.array([1./s,1./s]))
                cnt = cnt + 1
        k.append(cnt)
    return k, torch.tensor(anchors).float(), torch.tensor(grid_size).float()


def plot_anchors(img, anns, anchors, ax=None, overlap=False):
  # anns is a tuple with (bbs, labels)
  # bbs is an array of bounding boxes in format [x_min, y_min, x_max, y_max]
  # labels is an array containing the label
  if not ax:
    fig, ax = plt.subplots(figsize=(10, 6))
  ax.imshow(img)
  labels, bbs = anns

  anchors = xyxy2xywh(anchors)
  _anchors = np.array([unnorm(a, img_size) for a in anchors])
  for a in _anchors:
    x, y, w, h = a
    rect = mpatches.Rectangle((x, y), w, h, fill=False, edgecolor='green', linewidth=2)
    ax.add_patch(rect)

  labels, bbs = anns
  for lab, bb in zip(labels, bbs):
    x, y, xm, ym = bb
    w, h = xm - x, ym - y
    rect = mpatches.Rectangle((x, y), w, h, fill=False, edgecolor='red', linewidth=2)
    text = ax.text(x, y - 10, classes[lab], {'color': 'red'})
    text.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
    ax.add_patch(rect)
  plt.show()


ix = 0
img_np, anns,_ = get_sample(ix)
labels, bbs = anns

scales = [6, 3, 1]
centers = [(0.5, 0.5)]
size_scales = [0.5]
aspect_ratios = [(1., 1.), (1.5, 0.8), (1.8, 0.4)]
sizes = [(s*a[0], s*a[1]) for s in size_scales for a in aspect_ratios]
k, anchors, grid_size = generate_anchors(scales, centers, sizes)

plot_anchors(img_np, anns, anchors)
len(anchors), k

fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(img_np)
plt.show()
