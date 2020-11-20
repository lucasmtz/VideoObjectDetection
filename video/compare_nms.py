import os
import re
from glob import glob

import cv2
import numpy as np


def get_frame_number(img_path):
    return int(re.search(r"\d+", img_path.split("/")[-1]).group())


def vstack_imgs(imgs_path):
    list_imgs = []
    for img_path in imgs_path:
        im = cv2.imread(img_path)
        im = cv2.copyMakeBorder(
            im, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=(255, 255, 255)
        )
        cv2.putText(
            im,
            f"Frame{str(get_frame_number(img_path))}",
            (5, im.shape[0] - 5),
            cv2.FONT_HERSHEY_COMPLEX,
            0.4,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
        list_imgs.append(im)
    return np.vstack(list_imgs)


def show_comparison(yolo_dir, nms_dir, n_stacks=5, n_comparisons=1, imshow=False):
    yolo_dir = sorted(glob(f"{yolo_dir}/*"), key=get_frame_number)
    nms_dir = sorted(glob(f"{nms_dir}/*"), key=get_frame_number)

    for comparison, stack in enumerate(
        range(0, len(yolo_dir) + n_stacks - len(yolo_dir) % n_stacks, n_stacks)
    ):
        if imshow:
            cv2.imshow(
                "YoloV2 vs YoloV2+SeqNMS",
                np.hstack(
                    (
                        vstack_imgs(yolo_dir[stack : stack + n_stacks]),
                        vstack_imgs(nms_dir[stack : stack + n_stacks]),
                    )
                ),
            )
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            os.makedirs("SeqNMS_results", exist_ok=True)
            cv2.imwrite(
                f"SeqNMS_results/YoloV2 vs YoloV2+SeqNMS_{comparison}.png",
                np.hstack(
                    (
                        vstack_imgs(yolo_dir[stack : stack + n_stacks]),
                        vstack_imgs(nms_dir[stack : stack + n_stacks]),
                    )
                ),
            )
        if comparison >= n_comparisons - 1:
            break


if __name__ == "__main__":
    show_comparison(
        "tests", "output", n_stacks=5, n_comparisons=1000, imshow=False
    )
