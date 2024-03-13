import pytesseract
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
from Levenshtein import distance

# Load the image
image_path = 'images/scored3.jpeg'
image = Image.open(image_path)

left = image.width // 4
top = image.height // 4
right = 3 * image.width // 4
bottom = 2 * image.height // 4

cropped_image = image.crop((left, top, right, bottom))
cropped_image.show()

# Convert the image to grayscale
gray_image = cropped_image.convert('L')

# Increase the image contrast
enhancer = ImageEnhance.Contrast(gray_image)
enhanced_image = enhancer.enhance(2.0)

# Apply thresholding
threshold = 200
binary_image = enhanced_image.point(lambda p: p > threshold and 255)

# Resize the image
resized_image = binary_image.resize((binary_image.width * 2, binary_image.height * 2), Image.BICUBIC)

#save image
processed_image_path = 'images/processed_scored.png'
resized_image.save(processed_image_path)

# Perform OCR on the preprocessed image
text = pytesseract.image_to_string(resized_image)
print(text)

# # Check if the word "scored" is present in the extracted text
# if 'scored' in text.lower():
#     print("The image contains the word 'scored'.")
# else:
#     print("The image does not contain the word 'scored'.")

# Define a similarity threshold
similarity_threshold = 3

# Check if the word "scored" or a similar word is present in the extracted text
for word in text.lower().split():
    if distance(word, 'scored') <= similarity_threshold:
        print("The image contains a word similar to 'scored'.")
        break
else:
    print("The image does not contain a word similar to 'scored'.")