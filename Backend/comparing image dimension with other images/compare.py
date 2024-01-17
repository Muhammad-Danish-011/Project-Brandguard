import os
from PIL import Image
import requests
from io import BytesIO
from tkinter import Tk, filedialog

# Function to calculate image dimensions
def calculate_image_dimensions(image_source):
    try:
        if image_source.startswith('http://') or image_source.startswith('https://'):
            response = requests.get(image_source)
            img = Image.open(BytesIO(response.content))
        else:
            img = Image.open(image_source)

        width, height = img.size
        return width, height
    
    except IOError:
        print("Unable to open the image or it may not be an image.")
        return None

# Function to display image dimensions
def display_result(image_dimensions):
    if image_dimensions:
        print(f"Image width: {image_dimensions[0]} pixels")
        print(f"Image height: {image_dimensions[1]} pixels")
    else:
        print("No image dimensions calculated.")

# Function to select image source (file or URL)
def select_image_source():
    root = Tk()
    root.withdraw()

    print("Select an option:")
    print("1. Select an image file")
    print("2. Input image URL")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        file_path = filedialog.askopenfilename(
            title="Select an image file",
            filetypes=[("Image files", ("*.png", "*.jpg", "*.jpeg", "*.gif"))]
        )
        return file_path
    elif choice == '2':
        image_url = input("Enter the URL of the image: ")
        return image_url
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return None

# Function to compare image dimensions
def compare_image_dimensions(image_dimensions, reference_dimensions):
    if image_dimensions and reference_dimensions:
        return image_dimensions == reference_dimensions
    return False

# Function to compare images
def compare_images():
    reference_source = select_image_source()
    if reference_source:
        reference_dimensions = calculate_image_dimensions(reference_source)
        display_result(reference_dimensions)

        compare_choice = input("Do you want to compare with multiple images? (Y/N): ")
        if compare_choice.lower() == 'y':
            while True:
                image_source = select_image_source()
                if image_source:
                    image_dimensions = calculate_image_dimensions(image_source)
                    if image_dimensions:
                        match = compare_image_dimensions(image_dimensions, reference_dimensions)
                        if match:
                            print(f"Reference image matches with Image: {os.path.basename(image_source)}")
                        else:
                            print(f"Reference image does not match with Image: {os.path.basename(image_source)}")
                    else:
                        print("Failed to get dimensions of the image.")
                add_more = input("Do you want to add more images to compare? (Y/N): ")
                if add_more.lower() != 'y':
                    break
        else:
            print("Comparison with multiple images skipped.")

# Main function
def main():
    compare_images()

if __name__ == "__main__":
    main()
