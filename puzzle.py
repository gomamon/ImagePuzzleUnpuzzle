import cv2
import numpy as np
import sys
import random
import piece




if __name__ == "__main__":
    img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
    row, col, channel = img.shape

    p = int(sys.argv[2])
    q = int(sys.argv[3])


    # Split img to pieces
    piece_row = int(row/p)
    piece_col = int(col/q)

    pieces = [[piece.Piece(piece_row, piece_col,
                     img[i*piece_row:i*piece_row+piece_row, j*piece_col:j*piece_col+piece_col])
               for j in range(q)]
              for i in range(p)]

    #Flip pieces
    for i in range(p):
        for j in range(q):
            flip_flag = random.randint(0, 4)
            for k in range(flip_flag % 2,int(flip_flag/2),2):
                pieces[i][j].flip(flip_flag % 2)


    #shuffle pieces
    piece_idx = [i for i in range(p*q)]
    random.shuffle(piece_idx)

    # Merge to puzzled pieces
    puzzled_image = np.zeros((row,col, 3), np.uint8)
    for i in range(p*q):
        offset_row = piece_row*int(i/q)
        offset_col = piece_col*int(i%q)
        puzzled_image[offset_row:offset_row+piece_row, offset_col:offset_col+piece_col] = \
            pieces[int(piece_idx[i]/q)][piece_idx[i]%q].img

    cv2.imwrite("puzzled_image.jpg",puzzled_image)
    cv2.imshow("image", puzzled_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


