import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=0.2)
xpix, ypix = 1000, 1000
xxpix, yypix = 100, 100

pic = [[noise([i/xxpix, j/yypix]) for j in range(xpix)] for i in range(ypix)]
for row_index, row in enumerate(pic):
    for col_index, col in enumerate(row):

        if col < 0: 
            if col >= -0.0950:
                pic[row_index][col_index] = (222,194,123) # Sand
            elif col >= -0.1981:
                pic[row_index][col_index] = (91,137,26) # Light Green
            elif col >= -0.2401:
                pic[row_index][col_index] = (61,120,32) # Dark Green
            elif col >= -0.303:
                pic[row_index][col_index] = (33,33,35) # Dark Brown
            elif col >= -0.357:
                pic[row_index][col_index] = (67,54,46) # Light Brown
            else:#elif col >= -0.019:
                pic[row_index][col_index] = (255,255,255) # Snow

        if col > 0:
            if col <= 0.0920:
                pic[row_index][col_index] = (23,65,117) # Light Blue
            elif col <= 0.1980:
                pic[row_index][col_index] = (19,52,97) # Blue
            else:#elif col < 0.0012:
                pic[row_index][col_index] = (16,44,85) # Dark Blue

        if col == 0:
            pic[row_index][col_index] = (19,52,97)

# plt.imshow(pic, cmap='gray', vmin=-1, vmax=1)
plt.imshow(pic)
plt.show()