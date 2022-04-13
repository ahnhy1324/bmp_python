########################################################################################################################
#                                                   2017253019 안희영                                                   #
########################################################################################################################
import numpy as np
import matplotlib.pyplot as plt
header_size = 54
cmp_size = 1024
image_height = 512
image_width = 512
end_in_min = 42
end_in_max = 210
file_name = "lena_bmp_512x512_new.bmp"


def image_read(file):
    with open(file, "rb") as f:
        rectype = np.dtype(np.uint8)
        image_data = np.fromfile(f, dtype=rectype)
    header = image_data[0:header_size]
    cmp = image_data[header_size:cmp_size + header_size]
    data = image_data[len(image_data):cmp_size + header_size - 1:-1].reshape((image_height, image_width))
    data = np.flip(data, axis=1)
    return header, cmp, data


def histogram_equal(origin_data):
    sum_of = np.zeros(256)
    lut_out = np.zeros(256)
    for index in range(len(np.unique(bmp_data, return_counts=True)[0])):
        sum_of[np.unique(origin_data, return_counts=True)[0][index]] = \
            np.unique(origin_data, return_counts=True)[1][index]
    for index in range(len(sum_of) - 1):
        sum_of[index + 1] = sum_of[index] + sum_of[index + 1]
    for index in range(len(lut_out)):
        lut_out[index] = int(round(sum_of[index] / (512 * 512) * 255))
    return lut_out


def stretch(origin_data):
    bmp_high = np.max(origin_data)
    bmp_low = np.min(origin_data)
    lut_out = np.zeros(256)
    for i in range(bmp_high - bmp_low + 1):
        lut_out[i + bmp_low] = int(round(i * 255 / (bmp_high - bmp_low)))
    return lut_out


def end_in():
    lut_out = np.zeros(256)
    for i in range(len(lut_out)):
        if i < end_in_min:
            lut_out[i] = 0
        elif i > end_in_max:
            lut_out[i] = 255
        else:
            lut_out[i] = int(round((i - end_in_min) * 255 / (end_in_max - end_in_min)))
    return lut_out


def lut_to_data(lut, origin_data):
    out_data = np.zeros((image_height, image_width), dtype='u1')
    for index in range(image_height):
        for E in range(image_width):
            out_data[E][index] = lut[origin_data[E][index]]
    return out_data


def image_write(name, header, cmp, image):
    with open(name, "wb") as f:
        f.write(bytes(header))
        f.write(bytes(cmp))
        f.write(bytes( np.flipud(image)))


bmp_header, bmp_cmp, bmp_data = image_read(file_name)
img_equ = lut_to_data(histogram_equal(bmp_data), bmp_data)
img_stretching = lut_to_data(stretch(bmp_data), bmp_data)
img_end_in = lut_to_data(end_in(), bmp_data)
image_write("lena_equ.bmp", bmp_header, bmp_cmp, img_equ)
image_write("lena_stretching.bmp", bmp_header, bmp_cmp, img_stretching)
image_write("lena_end_in.bmp", bmp_header, bmp_cmp, img_end_in)
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
ax4.imshow(img_end_in, vmin=0, vmax=255, cmap='gray')
ax4.text(200, -15, 'Ends-in ')
ax4.axis('off')
ax5 = fig.add_subplot(245)
ax5.hist(np.ravel(bmp_data, order='C'), color='k', range=(0, 255), bins=256)
ax6 = fig.add_subplot(246)
ax6.hist(np.ravel(img_equ, order='C'), color='k', range=(0, 255), bins=256)
ax7 = fig.add_subplot(247)
ax7.hist(np.ravel(img_stretching, order='C'), color='k', range=(0, 255), bins=256)
ax8 = fig.add_subplot(248)
ax8.hist(np.ravel(img_end_in, order='C'), color='k', range=(0, 255), bins=256)
plt.show()
