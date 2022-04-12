import numpy as np
import matplotlib.pyplot as plt
header_size = 54
palet_size = 1024
with open("lena_bmp_512x512_new.bmp", "rb") as f:
    rectype = np.dtype(np.uint8)
    bdata = np.fromfile(f, dtype=rectype)
header = bdata[0:header_size-1]
palet = bdata[header_size:palet_size + header_size-1]
bmp_data = bdata[palet_size + header_size:].reshape((512, 512))
plt.imshow(bmp_data, vmin = 0, vmax = 255,cmap='gray')
plt.show()