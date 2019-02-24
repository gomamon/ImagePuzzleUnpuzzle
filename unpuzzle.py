import cv2
import numpy as np
import sys
import random
import piece



def get_color(img, row, col, flag):
    # <flag::: 0:top, 1:right, 2:bottom, 3:left, 4:all>

    if flag == 0:
        return [
            list(img[0, 0]),
            list(img[1, 0]),
            list(img[0, int(col / 3)]),
            list(img[1, int(col / 3)]),
            list(img[0, col-1]),
            list(img[1, col-1])
        ]

    if flag == 2:
        return [
            list(img[row - 1, 0]),
            list(img[row - 2, 0]),
            list(img[row - 1, int(col / 3)]),
            list(img[row - 2, int(col / 3)]),
            list(img[row - 1, col-1]),
            list(img[row - 2, col-1])
        ]

    if flag == 4:
        return [
            img[0, 0],
            img[0, int(col / 2)],
            img[0, col - 1],
            img[int(row / 2), col - 1],
            img[row - 1, col - 1],
            img[row - 1, int(col / 2)],
            img[row - 1, 0],
            img[int(row / 2), 0]
    ]

def get_color_diff(dst, src):
    diff = 0
    tot_diff = 0
    for i in range(6):
        for j in range(3):
            diff += abs(int(dst[i][j]) - int(src[i][j]))
        diff /= 3
    diff /= 3
    return diff



def get_horiz_line_score(img, n, piece_row, piece_col):

    print(piece_row*n)
    score = 0
    print(img)
    for i in range(piece_col):
        if img[piece_row*n, i] > 30:
            score += 1
        if img[piece_row*n-1, i] > 30:
            score+=1
        if img[piece_row*n+1, i] > 30:
            score += 1


    return score






def vertical_merge(pieces, remainder, row, col, p, q):
    piece_row = int(row/p)
    piece_col = int(col/q)

    merged = pieces[remainder[0]].img.copy()
    merged = pieces[remainder[0]].img[:piece_row, :piece_col]

    remainder.pop(0)
    num_merged = 1
    merge_info = []
    line_score = -1
    bottom_flag = 0


    while num_merged < p:
        #Get minimum diff and information
        min_line_score = -1

        for src_idx in remainder:
            for flip_flag_dst in range(4):
                merged = cv2.flip(merged, flip_flag_dst % 2)
                gray_dst = cv2.cvtColor(merged, cv2.COLOR_BGR2GRAY)
                for flip_flag_src in range(4):
                    pieces[src_idx].flip(flip_flag_src % 2)

                    gray_src = cv2.cvtColor(pieces[src_idx].img, cv2.COLOR_BGR2GRAY)
                    tmp_merged = cv2.vconcat([gray_dst, gray_src])
                    laplacian = cv2.Laplacian(tmp_merged, cv2.CV_8U, ksize=3)
                    line_score = get_horiz_line_score(laplacian, num_merged, piece_row, piece_col)

                    if min_line_score == -1 or min_line_score > line_score:
                        merge_info = [flip_flag_dst, flip_flag_src, src_idx]
                        min_line_score = line_score

        if num_merged < p:
            for flip_flag_dst in range(merge_info[0]+1):
                merged = cv2.flip(merged, flip_flag_dst % 2)
            for flip_flag_src in range(merge_info[1]+1):
                pieces[merge_info[2]].flip(flip_flag_src%2)
            merged = cv2.vconcat([merged, pieces[merge_info[2]].img])

            remainder.pop(remainder.index(merge_info[2]))
            num_merged += 1

    return merged




if __name__ == '__main__':

    puzzled_img = cv2.imread("puzzled_image.jpg", cv2.IMREAD_COLOR)
    a = puzzled_img
    row, col, channel = puzzled_img.shape

    p = int(sys.argv[1])
    q = int(sys.argv[2])

    # Split img to pieces
    piece_row = int(row/p)
    piece_col = int(col/q)
    pieces = []

    #match column images
    for i in range(p):
        for j in range(q):
            pieces.append(piece.Piece(piece_row, piece_col,
                     puzzled_img[i*piece_row:i*piece_row+piece_row, j*piece_col:j*piece_col+piece_col]))

    remainder = [i for i in range(p*q)]

    for i in range(q):
        cv2.imshow("laplacian", vertical_merge(pieces, remainder, row, col, p, q))
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    #cv2.imshow("completed!", match_row(completed_col, unchecked, row, col, p, q))


    cv2.waitKey(0)
    cv2.destroyAllWindows()
