import cv2
import os
from PIL import Image, ImageOps, ImageDraw

def create_player_icon(image_path, output_path, size=(500, 500)):
    # 1. Load the image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Detect Face
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        print(f"No face detected in {image_path}. Skipping.")
        return

    # Get the first face detected (x, y, width, height)
    (x, y, w, h) = faces[0]

    # 3. Add Padding (to show hair and shoulders)
    padding = int(w * 0.6) 
    center_x, center_y = x + w // 2, y + h // 2
    
    # Calculate crop boundaries (Square)
    side = max(w, h) + padding
    left = max(0, center_x - side // 2)
    top = max(0, center_y - side // 2)
    right = min(img.shape[1], left + side)
    bottom = min(img.shape[0], top + side)

    # 4. Crop and Convert to PIL
    crop = img[top:bottom, left:right]
    crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(crop_rgb)
    pil_img = pil_img.resize(size, Image.LANCZOS)

    # 5. Apply Circular Mask
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    
    output = ImageOps.fit(pil_img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    # 6. Save as PNG (to keep transparency)
    output.save(output_path, "PNG")
    print(f"Saved icon to: {output_path}")

# Example usage for a folder
input_folder = "public/img"
output_folder = "img_icons"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):

    if filename.endswith((".jpg", ".png", ".jpeg")) and  filename.startswith("MHB"):
        create_player_icon(
            os.path.join(input_folder, filename),
            os.path.join(output_folder, f"icon_{filename.split('.')[0]}.png")
        )