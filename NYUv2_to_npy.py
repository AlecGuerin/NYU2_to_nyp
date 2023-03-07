import numpy as np
import mat73
import shutil
import urllib.request
import pyopencl as cl
import os
import time
import argparse


DATA_PATH = 'data'
DATA_SET_PATH = os.path.join(DATA_PATH, 'datset')


def make_map():
    """Create a map to reduce input"""
    SIZE = 895

    bed_1 = np.array([156, 247, 351, 483, 484, 575, 803]) + 1
    book_2 = np.array([0, 84]) + 1
    ceiling_3 = np.array([3]) + 1
    chair_4 = np.array([4, 42, 149, 203, 358, 459, 486, 488, 493])+1
    floor_5 = np.array([10, 868])+1
    furniture_6 = np.array([2, 6, 7, 41, 44, 50, 64, 86, 87, 88, 93, 123, 152, 157, 160, 168, 173, 214, 215, 224, 223, 224, 240,
                    293, 298, 391, 400, 419, 427, 429,
                    443, 447, 455, 523, 525, 552, 573, 662, 667, 771, 191, 799, 854])+1
    objects_7 = np.array([1, 8, 9, 11, 12, 13, 14, 15, 16, 17, 21, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39,
                    40, 43, 44, 45, 47, 46, 49, 51, 52, 53, 54,55, 57, 59, 60, 61, 62, 65, 66, 67, 68, 69, 70, 71, 72,
                    73, 74, 75, 76, 77, 78, 79, 80, 81, 83, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103,
                    104, 105, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 124, 125,
                    126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145,
                    146, 147, 148, 150, 151, 153, 154, 155, 158, 159, 161, 162, 163, 164, 165, 166, 167, 169, 170, 172,
                    174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 186, 187, 188, 189, 190, 191, 192, 193, 194,
                    195, 196, 197, 198, 198, 200, 201, 202, 204, 205, 206, 207, 208, 209, 210, 211, 212, 113, 216, 217,
                    218, 219, 220, 221, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 241,
                    242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261,
                    262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281,
                    282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 294, 295, 296, 297, 299, 300, 301, 302, 303,
                    304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 322, 323, 324,
                    325, 326, 327, 328, 329, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 344, 345, 346,
                    347, 348, 349, 350, 352, 353, 354, 355, 356, 357, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368,
                    369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388,
                    389, 390, 392, 394, 395, 396, 397, 398, 399, 401, 402, 403, 404, 405, 406, 407, 409, 410, 411, 412,
                    413, 414, 415, 416, 417, 420, 421, 422, 423, 424, 425, 426, 430, 431, 432, 432, 433, 434, 435, 436,
                    437, 438, 439, 440, 441, 442, 444, 445, 446, 448, 449, 450, 451, 452, 453, 454, 456, 457, 458, 460,
                    461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 489, 490,
                    491, 492, 485, 489, 490, 491, 492, 494, 495, 496, 497, 498, 499, 501, 502, 503, 504, 505, 506, 508,
                    510, 511, 512, 513, 515, 516, 517, 518, 519, 520, 521, 522, 524, 536, 537, 528, 530, 531, 532, 533,
                    534, 535, 536, 537, 538, 539, 540, 541, 542, 544, 545, 546, 547, 548, 549, 550, 551, 553, 554, 555,
                    556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 573, 574, 576, 577,
                    578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597,
                    598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618,
                    619, 620, 621, 621, 622, 623, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638,
                    639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 659, 660, 661,
                    663, 664, 665, 666, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683,
                    684, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 702, 703, 704, 705, 706,
                    707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726,
                    728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747,
                    748, 749, 750, 560, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 772, 774, 775, 778, 779, 780,
                    781, 782, 783, 784, 785, 786, 787, 788, 790, 792, 793, 794, 795, 796, 797, 798, 800, 801, 802, 804,
                    805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824,
                    825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844,
                    845, 846, 847, 848, 849, 850, 851, 852, 853, 855, 856, 857, 858, 859, 861, 862, 863, 864, 865, 866,
                    868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887,
                    888, 889, 890, 891, 892, 893])+1
    painting_8 = np.array([22, 63, 106, 185, 393, 418, 507, 453, 789])+1
    sofa_9 = np.array([82, 487, 776])+1
    table_10 = np.array([18, 35, 355, 428, 509, 514, 525, 624])+1
    tv_11 = np.array([48, 56, 171])+1
    wall_12 = np.array([20])+1
    window_13 = np.array([58])+1

    res = np.zeros(SIZE)

    for i in range(0, SIZE):
        if np.isin(i, window_13):
            res[i] =13
        elif np.isin(i, wall_12):
            res[i] =12
        elif np.isin(i, ceiling_3):
            res[i] =3
        elif np.isin(i, book_2):
            res[i] =2
        elif np.isin(i, floor_5):
            res[i] =5
        elif np.isin(i, tv_11):
            res[i] =11
        elif np.isin(i, sofa_9):
            res[i] =9
        elif np.isin(i, bed_1):
            res[i] =1
        elif np.isin(i, chair_4):
            res[i] =4
        elif np.isin(i, painting_8):
            res[i] =8
        elif np.isin(i, table_10):
            res[i] =8
        elif np.isin(i, furniture_6):
            res[i] =6
        elif np.isin(i, objects_7):
            res[i] = 7

    return(res.astype(np.intc))


def label_reduction(data, map):    
    w,h = data.shape
    res = np.zeros((w, h))
    for x in range(0, w):
        for y in range(0, h):
            res[x][y] = map[data[x][y]]
    return res


def gpu_label_reduction(data, map):

    # TODO: Adapt to your system
    os.environ['PYOPENCL_COMPILER_OUTPUT'] = 'NVIDIA CUDA'
    os.environ['PYOPENCL_CTX'] = 'NVIDIA CUDA'

    res_shape=data.shape
    data = data.flatten().astype(np.short)
    res = np.zeros(len(data)).astype(np.int8)

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    map = map.astype(np.short)
    mf = cl.mem_flags
    data_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)
    map_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=map)
    res_buf = cl.Buffer(ctx, mf.WRITE_ONLY, res.nbytes)

    prg = cl.Program(ctx, """
        __kernel void reduce_labels(__global const short *labels, __global const short *map, __global char * res){
            int id = get_global_id(0);
            res[id] = (char)map[labels[id]];
        }
        """).build()

    kernel = prg.reduce_labels
    kernel(queue, data.shape, None, data_buf, map_buf, res_buf)

    cl.enqueue_copy(queue, res, res_buf)

    res = res.reshape(res_shape)
    return res


def img_to_npy(file_name):
    img_path = 'image'
    res_path = os.path.join(DATA_SET_PATH, img_path)
    os.makedirs(res_path, exist_ok=True)

    data = mat73.loadmat(file_name, only_include='images')
    data = data['images']
    cnt = data.shape[3]
    
    for i in range(0, cnt):
        file = f'{i}.npy'
        with open(os.path.join(res_path, file), 'wb') as f:
            np.save(f, data[:, :, :, i]/255.0)
    del data
    return cnt


def label_to_npy(file_name, gpu_acc=False):
    img_path = 'label'
    res_path = os.path.join(DATA_SET_PATH, img_path)
    os.makedirs(res_path, exist_ok=True)

    data = mat73.loadmat(file_name, only_include='labels')
    data = data['labels']
    cnt = data.shape[2]

    map = make_map()

    if gpu_acc:
        data = gpu_label_reduction(data, map)

    for i in range(0, cnt):
        if not gpu_acc:
            data[:, :, i] = label_reduction(data[:, :, i], map)
        file = f'{i}.npy'
        with open(os.path.join(res_path, file), 'wb') as f:
            np.save(f, data[:, :, i].astype(np.int8))
    del data
    return cnt


def depth_to_npy(file_name):
    img_path = 'depth'
    res_path = os.path.join(DATA_SET_PATH, img_path)
    os.makedirs(res_path, exist_ok=True)

    data = mat73.loadmat(file_name, only_include='depths')
    data = data['depths']
    cnt = data.shape[2]

    for i in range(0, cnt):
        file = f'{i}.npy'
        with open(os.path.join(res_path, file), 'wb') as f:
            np.save(f, data[:, :, i])
    del data
    return cnt


def make_datasets(cnt, test_per=0.25):
    # Get the paths to train and test datasets
    train_path = os.path.join(DATA_PATH, 'train')
    test_path = os.path.join(DATA_PATH, 'val')
    # Get the paths to train dataset items
    image_train_path = os.path.join(train_path, 'image')
    label_train_path = os.path.join(train_path, 'label')
    depth_train_path = os.path.join(train_path, 'depth')
    # Get the paths to test dataset items
    image_test_path = os.path.join(test_path, 'image')
    label_test_path = os.path.join(test_path, 'label')
    depth_test_path = os.path.join(test_path, 'depth')
    # Get the paths to default dataset items
    image_dataset_path = os.path.join(DATA_SET_PATH, 'image')
    label_dataset_path = os.path.join(DATA_SET_PATH, 'label')
    depth_dataset_path = os.path.join(DATA_SET_PATH, 'depth')

    # Remove the previous datasets
    clean_datasets([train_path, test_path])

    # Make directories
    os.makedirs(train_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)

    os.makedirs(image_train_path, exist_ok=True)
    os.makedirs(label_train_path, exist_ok=True)
    os.makedirs(depth_train_path, exist_ok=True)

    os.makedirs(image_test_path, exist_ok=True)
    os.makedirs(label_test_path, exist_ok=True)
    os.makedirs(depth_test_path, exist_ok=True)

    test_i = 0
    train_i = 0

    for i in range(0, cnt):
        # put img to train data if random value is bigger than  test percentage
        if np.random.rand(1)[0] > test_per:
            # Copy image
            sr = os.path.join(image_dataset_path, f'{i}.npy')
            dt = os.path.join(image_train_path, f'{train_i}.npy')
            shutil.copyfile(sr, dt)
            # Copy label
            sr = os.path.join(label_dataset_path, f'{i}.npy')
            dt = os.path.join(label_train_path, f'{train_i}.npy')
            shutil.copyfile(sr, dt)
            # Copy depth
            sr = os.path.join(depth_dataset_path, f'{i}.npy')
            dt = os.path.join(depth_train_path, f'{train_i}.npy')
            shutil.copyfile(sr, dt)
            train_i += 1
        else:
            # Copy image
            sr = os.path.join(image_dataset_path, f'{i}.npy')
            dt = os.path.join(image_test_path, f'{test_i}.npy')
            shutil.copyfile(sr, dt)
            # Copy label
            sr = os.path.join(label_dataset_path, f'{i}.npy')
            dt = os.path.join(label_test_path, f'{test_i}.npy')
            shutil.copyfile(sr, dt)
            # Copy depth
            sr = os.path.join(depth_dataset_path, f'{i}.npy')
            dt = os.path.join(depth_test_path, f'{test_i}.npy')
            shutil.copyfile(sr, dt)
            test_i += 1


def clean_datasets(dirs):
    for i in range(len(dirs)):
        shutil.rmtree(dirs[i], True)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='Path to nyu_depth_v2_labeled.mat')
    parser.add_argument('--balance', type=float, help='Balance between train and test datasets. Default value 0.25')
    parser.add_argument('--gpu', action='store_true', help='Use GPU for label reduction')
    parser.add_argument('--regenerate', action='store_false', help='Force to regenerate the dataset.')
    args = parser.parse_args()

    if args.file == None:
        data_file = 'nyu_depth_v2_labeled.mat'
    else:
        data_file = args.file

    if args.balance == None:
        test_per = 0.25
    else:
        test_per = args.balance

    img_dir = os.path.join(DATA_SET_PATH, 'image')
    file_cnt = 0


    # Get the file if it doesn't exist
    if not os.path.isfile(data_file):
        t = time.time()
        print('Downloading the dataset (Can be long)...')
        urllib.request.urlretrieve('http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v2/nyu_depth_v2_labeled.mat',
                                   data_file)
        print(f'Dataset downloaded in {time.time()-t:.3f}s')

    # Check if dataset hqs already been converted. Convert it if needed
    if os.path.exists(img_dir) and args.regenerate:
        # Not beautifull...
        file_cnt = len([entry for entry in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, entry))])
    else:
        print('Convert data...')
        t = time.time()
        print('Convert images...')
        img_to_npy(data_file)
        print('Convert labels...')
        label_to_npy(data_file, args.gpu)
        print('Convert depths...')
        file_cnt = depth_to_npy(data_file)
        print(f'Dataset generated in {time.time() - t:.3f}s')

    make_datasets(file_cnt, test_per)
