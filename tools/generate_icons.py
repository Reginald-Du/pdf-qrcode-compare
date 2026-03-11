import os
from PIL import Image, ImageDraw

def create_icon(size, color):
    img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a rounded rectangle background
    padding = size // 10
    draw.rounded_rectangle(
        [(padding, padding), (size - padding, size - padding)],
        radius=size // 5,
        fill=color
    )
    
    # Draw a QR-like pattern (simplified)
    qr_color = (255, 255, 255, 255)
    center = size // 2
    box_size = size // 6
    
    # Center box
    draw.rectangle(
        [(center - box_size, center - box_size), (center + box_size, center + box_size)],
        fill=qr_color
    )
    
    # Corner boxes
    offset = size // 4
    draw.rectangle([(center - offset - box_size//2, center - offset - box_size//2), 
                   (center - offset + box_size//2, center - offset + box_size//2)], fill=qr_color)
    draw.rectangle([(center + offset - box_size//2, center - offset - box_size//2), 
                   (center + offset + box_size//2, center - offset + box_size//2)], fill=qr_color)
    draw.rectangle([(center - offset - box_size//2, center + offset - box_size//2), 
                   (center - offset + box_size//2, center + offset + box_size//2)], fill=qr_color)

    return img

def main():
    if not os.path.exists('resources'):
        os.makedirs('resources')

    # Create base image
    base_img = create_icon(1024, (33, 150, 243)) # Blueish
    
    # Save as PNG
    base_img.save('resources/icon.png')
    
    # Save as ICO (Windows)
    # ICO needs multiple sizes
    base_img.save('resources/icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    
    # Save as ICNS (macOS)
    # Pillow supports writing ICNS directly
    base_img.save('resources/icon.icns', format='ICNS')
    
    print("Icons generated in resources/")

if __name__ == '__main__':
    main()
