from PIL import Image
import requests
from io import BytesIO
from tkinter import Tk, filedialog

def calculate_image_dimensions(image_source):
    try:
        if image_source.startswith('http://') or image_source.startswith('https://'):
            response = requests.get(image_source)
            response.raise_for_status()  
            img = Image.open(BytesIO(response.content))
        else:
            img = Image.open(image_source)

        width, height = img.size
        return width, height
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from URL: {e}")
        return None
    except IOError as e:
        print(f"Error opening the image: {e}")
        return None

def display_result(image_dimensions):
    if image_dimensions:
        print(f"Image width: {image_dimensions[0]} pixels")
        print(f"Image height: {image_dimensions[1]} pixels")
    else:
        print("No image dimensions calculated.")

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

def main():
    image_source = select_image_source()
    if image_source:
        image_dimensions = calculate_image_dimensions(image_source)
        display_result(image_dimensions)

if __name__ == "__main__":
    main()
