import cv2
import numpy as np
import sys
import random
import piece



def get_line_score(img, n, piece_row, piece_col, flag):

    print(piece_row*n)
    score = 0
    print(img)

    if flag == 0:
        for i in range(piece_col):
            if img[piece_row*n, i] > 30:
                score += 1
            if img[piece_row*n-1, i] > 30:
                score+=1
            if img[piece_row*n+1, i] > 30:
                score += 1
    else:
        for i in range(piece_row):
            if img[i, piece_col*n] > 30:
                score += 1
            if img[i, piece_col*n-1] > 30:
                score+=1
            if img[i, piece_col*n+1] > 30:
                score += 1

    return score




def vertical_merge(pieces, remainder, row, col, p, q):
    piece_row = int(row/p)
    piece_col = int(col/q)

    merged = pieces[remainder[0]].copy()
    merged = pieces[remainder[0]][:piece_row, :piece_col]

    remainder.pop(0)
    num_merged = 1
    merge_info = []


    while num_merged < p:
        #Get minimum diff and information
        min_line_score = -1

        for src_idx in remainder:
            for flip_flag_dst in range(4):
                merged = cv2.flip(merged, flip_flag_dst % 2)
                gray_dst = cv2.cvtColor(merged, cv2.COLOR_BGR2GRAY)
                for flip_flag_src in range(4):
                    pieces[src_idx] = cv2.flip(pieces[src_idx], flip_flag_src % 2)

                    gray_src = cv2.cvtColor(pieces[src_idx], cv2.COLOR_BGR2GRAY)
                    tmp_merged = cv2.vconcat([gray_dst, gray_src])
                    laplacian = cv2.Laplacian(tmp_merged, cv2.CV_8U, ksize=3)
                    line_score = get_line_score(laplacian, num_merged, piece_row, piece_col,0)

                    if min_line_score == -1 or min_line_score > line_score:
                        merge_info = [flip_flag_dst, flip_flag_src, src_idx]
                        min_line_score = line_score

        if num_merged < p:
            for flip_flag_dst in range(merge_info[0]+1):
                merged = cv2.flip(merged, flip_flag_dst % 2)
            for flip_flag_src in range(merge_info[1]+1):
                pieces[merge_info[2]] = cv2.flip(pieces[merge_info[2]], flip_flag_src%2)
            merged = cv2.vconcat([merged, pieces[merge_info[2]]])

            remainder.pop(remainder.index(merge_info[2]))
            num_merged += 1

    return merged


def horizontal_merge(pieces, remainder, row, col, p, q):
    piece_row = row
    piece_col = int(col / q)

    merged = pieces[remainder[0]].copy()
    merged = pieces[remainder[0]][:piece_row, :piece_col]

    remainder.pop(0)
    num_merged = 1
    merge_info = []


    while num_merged < q:
        # Get minimum diff and save information
        min_line_score = -1

        for src_idx in remainder:
            for flip_flag_dst in range(4):
                merged = cv2.flip(merged, flip_flag_dst % 2)
                gray_dst = cv2.cvtColor(merged, cv2.COLOR_BGR2GRAY)
                for flip_flag_src in range(4):
                    pieces[src_idx] = cv2.flip( pieces[src_idx], flip_flag_src % 2)

                    gray_src = cv2.cvtColor(pieces[src_idx], cv2.COLOR_BGR2GRAY)
                    tmp_merged = cv2.hconcat([gray_dst, gray_src])
                    laplacian = cv2.Laplacian(tmp_merged, cv2.CV_8U, ksize=3)
                    line_score = get_line_score(laplacian, num_merged, piece_row, piece_col, 1)

                    if min_line_score == -1 or min_line_score > line_score:
                        merge_info = [flip_flag_dst, flip_flag_src, src_idx]
                        min_line_score = line_score

        if num_merged < q:
            for flip_flag_dst in range(merge_info[0] + 1):
                merged = cv2.flip(merged, flip_flag_dst % 2)
            for flip_flag_src in range(merge_info[1] + 1):
                pieces[merge_info[2]] = cv2.flip(pieces[merge_info[2]], flip_flag_src % 2)
            merged = cv2.hconcat([merged, pieces[merge_info[2]]])

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

    for i in range(p):
        for j in range(q):
            pieces.append(puzzled_img[i*piece_row:i*piece_row+piece_row, j*piece_col:j*piece_col+piece_col])

    # match vertical images
    remainder = [i for i in range(p*q)]
    vertical_pieces = []

    for i in range(q):
        vertical_pieces.append(vertical_merge(pieces, remainder, row, col, p, q))


    # match horizontal images
    remainder = [i for i in range(q)]
    unpuzzled_img = horizontal_merge(vertical_pieces, remainder, row, col, p, q)


    #save and show result image
    cv2.imwrite("unpuzzled_image.jpg", unpuzzled_img)
    cv2.imshow("unpuzzled_img", unpuzzled_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
