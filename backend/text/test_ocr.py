from ocr_lib import *


# Testing
path = "../imgs/fav_juices.jpg"

# Get the bounding boxes and text
(bbs, texts, txt_to_bb) = detect_text_path(path)
print(bbs)

image = cv2.imread(path)
text_to_write = "10"
bounding_box = bbs[5]

# Get a blank white image with the text written inside the bounding box
transparent_image_with_text = write_text_in_bounding_box(image, bounding_box, text_to_write)

# Show image
# Press any key to exit the window
cv2.imshow('painted image', transparent_image_with_text)
k = cv2.waitKey(0)
