# Image Puzzler and Image Unpuzzler
This program is able to puzzle images with random piece flips and rearrange (unpuzzle) them.

## Requirement
* cv2 4.0.0
* Python 3.6.4
* numpy 1.16.1


## Getting started

### puzzling
```bash
[usage]: python3 puzzle.py file_name pieces_in_vertical pieces_in_horizontal
python3 puzzle.py sample.png 4 3
```
Execute puzzling program with above usage. Result image is generated as __puzzled_image.jpg__
In the case of the example, sample.jpeg will be puzzled into 4 pieces vertically and 3 pieces horizontally.

### unpuzzling
```bash
[usage]: python3 unpuzzle.py pieces_in_vertical pieces_in_horizontal
python3 unpuzzle.py 4 3
```
Execute unpuzzling program with above usage. It will attempt to rearrange puzzled_image.jpg created from the puzzling program. Result image is generated as unpuzzled_image.jpg
In the case of the example, __puzzled_image.jpg__ will be unpuzzled given 4 pieces vertically and 3 pieces horizontally.

###### You can adjust the threshold value in lines 139 and 140 in "unpuzzle.py" to increase the accuracy of the image.


## Running test
### puzzling
```bash
python3 puzzle.py sample.png 4 4
```

![puzzled_image](./puzzled_image.jpg)
puzzled_image.jpg

### unpuzzling
```bash
python3 unpuzzle.py 4 4
```
![unpuzzled_image](./unpuzzled_image.jpg)
unpuzzled_image.jpg



