import os
from pathlib import Path
from random import randrange

train_dir = Path('./train')
image_dir = train_dir / 'images'
label_dir = train_dir / 'labels'



count = 0
val_size = 10
test_size = 10
try:
    os.mkdir('test')
    os.mkdir('val')
    os.mkdir('test/images')
    os.mkdir('test/labels')
    os.mkdir('val/labels')
    os.mkdir('val/images')
except:
    print("Test and Validation folders are already created")


while count < 10:
    file_list = os.listdir(image_dir)
    list_size = len(file_list)
    test_index = randrange(0, list_size)
    selected_test_image = Path(file_list[test_index]) 
    selected_test_label = Path(f"{os.path.splitext(selected_test_image)[0]}.txt")
    os.rename(image_dir / selected_test_image, Path('test/images') / selected_test_image)
    os.rename(label_dir / selected_test_label, Path('test/labels') / selected_test_label)
    

    file_list = os.listdir(image_dir)
    list_size = len(file_list)
    val_index = randrange(0, list_size)
    selected_val_image = Path(file_list[val_index]) 
    selected_val_label = Path(f"{os.path.splitext(selected_val_image)[0]}.txt")
    os.rename(image_dir / selected_val_image, Path('val/images') / selected_val_image)
    os.rename(label_dir / selected_val_label, Path('val/labels') / selected_val_label)
    
    count+=1
