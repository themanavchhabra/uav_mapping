import os
import shutil
from  natsort import natsorted

# Providing the folder path
origin = 'data/images/'
target = 'data/images_mapping/'

files = natsorted(os.listdir(origin))

# print(files)

for i,file_name in enumerate(files):
    if(i%50 == 0):
        # print(i)
        print(file_name)
        shutil.copy(origin+file_name, target+file_name)
print("Files are copied successfully")
