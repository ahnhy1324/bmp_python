########################################################################################################################
#                                                   2017253019 안희영                                                   #
########################################################################################################################
import numpy as np
import matplotlib.pyplot as plt
header_size = 54
palet_size = 1024
image_height = 512
image_width = 512
endin_low = 42
endin_high = 210
file_name = "lena_bmp_512x512_new.bmp"
########################################################################################################################




########################################################################################################################

########################################################################################################################
with open(file_name, "rb") as f:
    rectype = np.dtype(np.uint8)
    bdata = np.fromfile(f, dtype=rectype)
bmp_header = bdata[0:header_size - 1]
bmp_palet = bdata[header_size:palet_size + header_size - 1]
bmp_data = bdata[len(bdata):palet_size + header_size - 1:-1].reshape((image_height, image_width))
bmp_data = np.flip(bmp_data, axis=1)

LUT = np.zeros(256)
Sum = np.zeros(256)
bmp_high = np.max(bmp_data)
bmp_low = np.min(bmp_data)

img_equ = np.copy(bmp_data)
img_stretching = np.copy(bmp_data)
img_endin = np.copy(bmp_data)
########################################################################################################################
for i in range(len(np.unique(bmp_data, return_counts=True)[0])):
    Sum[np.unique(bmp_data, return_counts=True)[0][i]] = np.unique(bmp_data, return_counts=True)[1][i]
for i in range(len(Sum)-1):
    Sum[i+1] = Sum[i]+Sum[i+1]
for i in range(len(LUT)):
    LUT[i] = int(round(Sum[i] / (512 * 512) * 255))
for i in range(image_height):
    for e in range(image_width):
        img_equ[e][i] = LUT[bmp_data[e][i]]
########################################################################################################################
for i in range(bmp_high-bmp_low+1):
    LUT[i+bmp_low] = int(round(i * 255 / (bmp_high - bmp_low)))
for i in range(image_height):
    for e in range(image_width):
        img_stretching[e][i] = LUT[bmp_data[e][i]]
########################################################################################################################
for i in range(len(LUT)):
    if i< endin_low:
        LUT[i] = 0
    elif i> endin_high:
        LUT[i] = 255
    else:
        LUT[i] = int(round((i - endin_low) * 255 / (endin_high - endin_low)))
for i in range(image_height):
    for e in range(image_width):
        img_endin[e][i] = LUT[bmp_data[e][i]]
########################################################################################################################


########################################################################################################################
fig = plt.figure()
fig.suptitle("Lena")

ax1 = fig.add_subplot(241)
ax1.imshow(bmp_data, vmin=0, vmax=255, cmap='gray')
ax1.text(200, -15, 'normal')
ax1.axis('off')
ax2 = fig.add_subplot(242)
ax2.imshow(img_equ, vmin=0, vmax=255, cmap='gray')
ax2.text(150, -15, 'Histogram Equalization ')
ax2.axis('off')
ax3 = fig.add_subplot(243)
ax3.imshow(img_stretching, vmin=0, vmax=255, cmap='gray')
ax3.text(150, -15, 'Contrast Stretching ')
ax3.axis('off')
ax4 = fig.add_subplot(244)
ax4.imshow(img_endin, vmin=0, vmax=255, cmap='gray')
ax4.text(200, -15, 'Ends-in ')
ax4.axis('off')

ax5 = fig.add_subplot(245)
ax5.hist(np.ravel(bmp_data, order='C'), color='k', range=(0, 255), bins=256)
ax6 = fig.add_subplot(246)
ax6.hist(np.ravel(img_equ, order='C'), color='k', range=(0, 255), bins=256)
ax7 = fig.add_subplot(247)
ax7.hist(np.ravel(img_stretching, order='C'), color='k', range=(0, 255), bins=256)
ax8 = fig.add_subplot(248)
ax8.hist(np.ravel(img_endin, order='C'), color='k', range=(0, 255), bins=256)

plt.show()
