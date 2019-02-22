import cv2

class Piece:
    def __init__(self, row, col, imgorigin):
        self.row = row
        self.col = col
        self.img = imgorigin.copy()
        self.img = imgorigin[:self.row, :self.col]

    def show(self, name):
        cv2.imshow(name, self.img)
        cv2.waitKey(0)

    def flip(self, flip_flag):
        if flip_flag != 2:
            self.img = cv2.flip(self.img,flip_flag)
