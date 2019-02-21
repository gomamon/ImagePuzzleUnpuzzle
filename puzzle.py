
import cv2
import numpy as np
import sys
import random

class Piece:

    def __init__(self, row, col, imgorigin):
        self.row = row
        self.col = col
        self.img = imgorigin.copy()
        self.img = imgorigin[:self.row, :self.col]



    def show(self):
        cv2.imshow("piece",self.img)



if __name__ == "__main__":

    img = cv2.imread('sample.jpeg', cv2.IMREAD_COLOR)
    row, col, channel = img.shape

    p = int(sys.argv[1])
    q = int(sys.argv[2])


    # Split img to pieces
    piece_row = int(row/p)
    piece_col = int(col/q)

    pieces = [[Piece(piece_row, piece_col,
                     img[i*piece_row:i*piece_row+piece_row, j*piece_col:j*piece_row+piece_col])
               for j in range(q)]
              for i in range(q)]

    #flip pieces


    #shuffle pieces


    cv2.imshow("image", pieces[0][0].img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


