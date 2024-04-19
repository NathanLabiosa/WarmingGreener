import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import cv2


global min_val
global max_val


def calculate_average(image, x1, y1, x2, y2):
   cropped_image = image[y1:y2, x1:x2]
   average_color = np.mean(cropped_image, axis=(0, 1))
   return average_color




#file_path = input("Enter the path of the image: ")
image = np.array(Image.open("/Users/nathanlabiosa/Downloads/FLIR0139.jpg"))
global click_num
click_num = 0


fig, ax = plt.subplots()
ax.imshow(image)
rect = patches.Rectangle((0,0), 0, 0, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)


coords = []
global min_temp
min_temp = []
global max_temp
max_temp = []






def on_click(event):
   global click_num
   if click_num == 0:
       if event.inaxes != ax:
           return
       global min_temp
       min_temp.append([int(event.xdata), int(event.ydata)])
       click_num += 1
   elif click_num == 1:
       if event.inaxes != ax:
           return
       global max_temp
       max_temp.append([int(event.xdata), int(event.ydata)])
       click_num += 1
   else:
       if event.inaxes != ax:
           return
       coords.append((int(event.xdata), int(event.ydata)))
       if len(coords) == 2:
           rect.set_width(abs(coords[1][0] - coords[0][0]))
           rect.set_height(abs(coords[1][1] - coords[0][1]))
           rect.set_xy((min(coords[0][0], coords[1][0]), min(coords[0][1], coords[1][1])))
           plt.draw()
           if len(coords) == 2:
               global min_val
               global max_val
               x1, y1 = coords[0]
               x2, y2 = coords[1]
               average_color = calculate_average(image, min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
               min_val = input("Enter the minimum value: ")
               max_val = input("Enter the maximum value: ")
               #print("Average pixel value within the box: ", average_color)
              


               #Set up pixel value to temperature conversion
               min_temp = float(min_val)
               max_temp = float(max_val)
               temp_range = max_temp - min_temp
               pixel_range = 255
               box = image[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
               box_to_temp = box/pixel_range * temp_range + min_temp
               temp_val = np.mean(box_to_temp)




               #Get average temperature value of the box
               print("Average temperature value within the box: ", np.mean(temp_val))
               coords.clear()


fig.canvas.mpl_connect('button_press_event', on_click)




plt.show()





