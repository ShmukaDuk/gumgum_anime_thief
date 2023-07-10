import pyautogui
import pytesseract

# Take a screenshot
screenshot = pyautogui.screenshot()

# Save the screenshot as an image file
screenshot.save('screenshot.png')

# Perform OCR on the screenshot image
text = pytesseract.image_to_string('screenshot.png')

# Print the extracted text
print(text)

# Get the location of the text file
text_file_location = pyautogui.locateOnScreen('screenshot.png', confidence=0.8)
print("Text file location:", text_file_location)