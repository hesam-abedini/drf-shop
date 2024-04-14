from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent


def delete_image(image):
    last_image=BASE_DIR/'uploads'/str(image)
    try:
        os.remove(last_image)
    except:
        print('image was not found')