import cv2
import numpy as np
import sys
import random
import piece


def check_line_col(img, n, piece_row, piece_col):

    #cv2.imshow("laplacian", img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    print("HI",piece_row, piece_col)

    for i in range(piece_row, n*piece_row, piece_row):
        num_white = 0
        for j in range(piece_col):
            if img[i, j] > 200:
                num_white += 1
            if img[i+1, j] > 200:
                num_white += 1
            if img[i - 1, j] > 200:
                num_white += 1
        print("white ", num_white, piece_col, num_white/(piece_col*3))
        if num_white/(piece_col*3) > 0.065:
            return False
    return True

def check_line_row(img, n, piece_row,piece_col):

    for i in range(piece_col, n*piece_col, piece_col):
        num_white = 0
        for j in range(piece_row):
            if img[j, i] > 200:
                num_white += 1
            if img[j, i+1] > 200:
                num_white += 1
            if img[j, i-1] > 200:
                num_white += 1
        print("white ", num_white, piece_col, num_white/(piece_col*3))
        if num_white/(piece_col*3) > 0.065:
            return False
    return True

def match_col(pieces, unchecked, row, col, p, q):
    piece_row = int(row/p)
    piece_col = int(col/q)

    completed = pieces[unchecked[0][0]][unchecked[0][1]].img.copy()
    completed = pieces[unchecked[0][0]][unchecked[0][1]].img[:piece_row, :piece_col]
    unchecked.pop(0)
    num_completed = 1

    i = 0
    while i < len(unchecked) and num_completed < p:
        break_flag = False
        print(unchecked)
        i += 1

        for j in unchecked:
            for k in range(4):
                completed = cv2.flip(completed, k%2)

                merged = cv2.vconcat([completed, pieces[j[0]][j[1]].img])
                gray = cv2.cvtColor(merged, cv2.COLOR_BGR2GRAY)
                laplacian = cv2.Laplacian(gray, cv2.CV_8U, ksize=3)

                if check_line_col(laplacian, num_completed+1, piece_row, piece_col) == True:
                    num_completed += 1
                    print("hihi")
                    completed = merged.copy()
                    completed = merged[:num_completed*piece_row, :piece_col]

                    unchecked.pop(unchecked.index(j))
                    break_flag = True
                    i = 0
                    if num_completed == p:
                        cv2.imshow("completed", completed)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return completed
                    break
            if break_flag:
                break


def match_row(cols, unchecked, row, col, p, q):
    piece_row = int(row/p)
    piece_col = int(col/q)

    completed = cols[unchecked[0]].copy()
    completed = cols[unchecked[0]][:piece_row, :piece_col]
    unchecked.pop(0)
    num_completed = 1

    i = 0
    while i < len(unchecked) and num_completed < p:
        break_flag = False
        print(unchecked)
        i += 1

        for j in unchecked:
            for k in range(4):
                completed = cv2.flip(completed, k%2)
                merged = cv2.hconcat([completed, pieces[j[0]]])
                gray = cv2.cvtColor(merged, cv2.COLOR_BGR2GRAY)
                laplacian = cv2.Laplacian(gray, cv2.CV_8U, ksize=3)

                if check_line_row(laplacian, num_completed+1, row, piece_col) == True:
                    num_completed += 1
                    print("hihi")
                    completed = merged.copy()
                    completed = merged[:num_completed*piece_row, :piece_col]

                    unchecked.pop(unchecked.index(j))
                    break_flag = True
                    i = 0
                    if num_completed == p:
                        cv2.imshow("completed", completed)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return completed
                    break
            if break_flag:
                break




if __name__ == '__main__':

    puzzled_img = cv2.imread("puzzled_image.jpg", cv2.IMREAD_COLOR)
    a = puzzled_img
    row, col, channel = puzzled_img.shape

    p = int(sys.argv[1])
    q = int(sys.argv[2])

    # Split img to pieces
    piece_row = int(row/p)
    piece_col = int(col/q)

    #match column images
    pieces = [[piece.Piece(piece_row, piece_col,
                     puzzled_img[i*piece_row:i*piece_row+piece_row, j*piece_col:j*piece_col+piece_col])
               for j in range(q)]
              for i in range(p)]

    unchecked = []

    for i in range(p):
        for j in range(q):
            unchecked.append((i, j))
    print(unchecked)

    #match all images
    completed_col = []
    for i in range(p):
        completed_col.append(match_col(pieces, unchecked, row, col, p, q))
        print(unchecked)
        print(completed_col)

    unchecked = []
    for i in range(q):
        unchecked.append(q)

    #cv2.imshow("completed!", match_row(completed_col, unchecked, row, col, p, q))




    # Merge to puzzled pieces
    '''
    unpuzzled_image = np.zeros((row, col, 3), np.uint8)
    for i in range(p*q):
        offset_row = piece_row*int(i/q)
        offset_col = piece_col*int(i%q)
        unpuzzled_image[offset_row:offset_row+piece_row, offset_col:offset_col+piece_col] = \
            pieces[int(i/q)][i%q].img'''


#    gray = cv2.cvtColor(puzzled_img, cv2.COLOR_BGR2GRAY)
#    laplacian = cv2.Laplacian(gray, cv2.CV_8U, ksize=3)


#   print(laplacian[piece_row, piece_col])



 #   cv2.imshow("laplacian", laplacian)

#    cv2.imwrite("unpuzzled_image.jpg",puzzled_image)
#    cv2.imshow("image", unpuzzled_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
