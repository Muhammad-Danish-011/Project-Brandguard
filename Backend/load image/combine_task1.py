from tkinter import Tk, filedialog
from PIL import Image
import requests
from io import BytesIO

def get_image_size(file_path):
    try:
        image = Image.open(file_path)
        width, height = image.size
        return width, height
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def select_image():
    root = Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image files", ("*.png", "*.jpg", "*.jpeg", "*.gif"))]
    )

    return file_path


def main():
    image_path = select_image()


    try:
        if image_path:
            if image_path.startswith('http://') or image_path.startswith('https://'):
                response = requests.get(image_path)
                image_size = get_image_size(BytesIO(response.content))
            else:
                image_size = get_image_size(image_path)
            if image_size:
                print(f"Selected image width size: {image_size[0]} pixels")
                print(f"Selected image height size: {image_size[1]} pixels" )
            else:
                print("Failed to get image size.")
        else:
            print("No image or url selected.")

    except IOError:
        print("Unable to open the image or it may not be an image.")
        return None
    

if __name__ == "__main__":
    main()
