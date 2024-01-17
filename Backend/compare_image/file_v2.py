
##############################################################3 graph with score in box 



import cv2
from skimage.metrics import structural_similarity as ssim
import itertools
import matplotlib.pyplot as plt
import numpy as np

def calculate_ssim(image1, image2):
    # Check for same dimensions and resize if necessary
    if image1.shape == image2.shape:
        larger_image = image1  # No resizing needed
        resized_image = image2
    else:
        smaller_image = image2 if image2.shape[0] < image1.shape[0] else image1
        larger_image = image1 if image1.shape[0] >= image2.shape[0] else image2
        resized_image = cv2.resize(smaller_image, (larger_image.shape[1], larger_image.shape[0]))

    # Feature-based matching using ORB
    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(larger_image, None)
    keypoints2, descriptors2 = orb.detectAndCompute(resized_image, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)

    # SSIM calculation
    gray1 = cv2.cvtColor(larger_image, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    ssim_score = ssim(gray1, gray2, multichannel=True)

    total = ssim_score + len(matches)

    return total

    #return ssim_score, len(matches)

# List of image files
image_files = ["win.png", "html1.jpg", "html.png", "html_crop.png"]  # Add more image files as needed

# Create a matrix to store SSIM scores
ssim_matrix = np.zeros((len(image_files), len(image_files)))

# Compare all pairs of images
for i, image_file1 in enumerate(image_files):
    for j, image_file2 in enumerate(image_files):
        if i != j:
            image1 = cv2.imread(image_file1)
            image2 = cv2.imread(image_file2)

            #ssim_score, num_matches = calculate_ssim(image1, image2)
            to = calculate_ssim(image1, image2)

            # Store SSIM score in the matrix
            ssim_matrix[i, j] = to

# Plot the heatmap
plt.imshow(ssim_matrix, cmap='viridis', interpolation='nearest')

# Add labels and annotations
plt.xticks(range(len(image_files)), image_files, rotation=45)
plt.yticks(range(len(image_files)), image_files)

for i in range(len(image_files)):
    for j in range(len(image_files)):
        if i != j:
            plt.text(j, i, f"{ssim_matrix[i, j]:.5f}", ha='center', va='center', color='w')

# Display the colorbar
cbar = plt.colorbar()
cbar.set_label('SSIM Score', rotation=270, labelpad=15)

# Display the plot
plt.show()
