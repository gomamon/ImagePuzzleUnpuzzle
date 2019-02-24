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
            list(img[0, int(col / 2)]),
            list(img[0, col-1])
        ]

    if flag == 2:
        return [
            list(img[row - 1, 0]),
            list(img[row - 1, int(col / 2)]),
            list(img[row - 1, col-1])
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
    for i in range(3):
        for j in range(3):
            diff += abs(int(dst[i][j]) - int(src[i][j]))
        diff /= 3
    diff /= 3
    return diff

def vertical_merge(pieces, remainder, row, col, p, q):
    piece_row = int(row/p)
    piece_col = int(col/q)

    merged = pieces[remainder[0]].img.copy()
    merged = pieces[remainder[0]].img[:piece_row, :piece_col]

    remainder.pop(0)
    num_merged = 1
    merge_info = []
    min_diff = 98765
    bottom_flag = 0


    while num_merged < p:
        #Get minimum diff and information
        min_diff = 98765

        for src_idx in remainder:
            for flip_flag_dst in range(4):
                merged = cv2.flip(merged, flip_flag_dst % 2)
                for flip_flag_src in range(2):
                    pieces[src_idx].flip(0)
                    diff = get_color_diff(get_color(merged, piece_row*num_merged, piece_col, 2)
                                          , get_color(pieces[src_idx].img, piece_row, piece_col, 0))
                    if min_diff > diff:
                        merge_info = [flip_flag_dst, flip_flag_src, src_idx]
                        min_diff = diff

        if min_diff < 98765 and num_merged < p:
            for flip_flag_dst in range(merge_info[0]+1):
                merged = cv2.flip(merged, flip_flag_dst % 2)
            for flip_flag_src in range(merge_info[1]+1):
                pieces[merge_info[2]].flip(0)
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
        cv2.imshow("laplacian", vertical_merge(pieces,remainder,row,col,p,q))
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    #cv2.imshow("completed!", match_row(completed_col, unchecked, row, col, p, q))


    cv2.waitKey(0)
    cv2.destroyAllWindows()
