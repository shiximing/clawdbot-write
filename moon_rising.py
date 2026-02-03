from PIL import Image, ImageDraw
import math

def create_moon_rising_gif():
    # Image dimensions
    width, height = 400, 300
    
    # Colors
    dark_blue = (0, 0, 50)  # Dark night sea background
    light_blue = (0, 0, 100)
    moon_color = (255, 255, 230)  # Soft yellow-white
    
    # Create frames
    frames = []
    
    for i in range(30):  # 30 frames for smooth animation
        # Create a new image with a dark background
        img = Image.new('RGB', (width, height), dark_blue)
        draw = ImageDraw.Draw(img)
        
        # Create gradient sky
        for y in range(height):
            # Interpolate between dark and light blue
            r = int(dark_blue[0] + (light_blue[0] - dark_blue[0]) * (y / height))
            g = int(dark_blue[1] + (light_blue[1] - dark_blue[1]) * (y / height))
            b = int(dark_blue[2] + (light_blue[2] - dark_blue[2]) * (y / height))
            for x in range(width):
                img.putpixel((x, y), (r, g, b))
        
        # Draw sea
        draw.rectangle([0, height*2//3, width, height], fill=(0, 0, 80))
        
        # Moon position - starts below horizon, rises smoothly
        moon_y = height * 2//3 + i * 10  # Rises from below horizon
        moon_size = 50
        
        # Draw moon with soft glow
        for glow in range(5):
            glow_alpha = 30 - glow * 5  # Decreasing opacity for glow effect
            glow_size = moon_size + glow * 10
            moon_glow = Image.new('RGBA', (glow_size*2, glow_size*2), (0,0,0,0))
            moon_glow_draw = ImageDraw.Draw(moon_glow)
            moon_glow_draw.ellipse([0, 0, glow_size*2, glow_size*2], 
                                    fill=(255, 255, 230, glow_alpha))
            moon_glow = moon_glow.resize((glow_size, glow_size))
            img.paste(moon_glow, 
                      (width//2 - glow_size//2, moon_y - glow_size//2), 
                      moon_glow)
        
        # Draw moon
        draw.ellipse([width//2 - moon_size//2, moon_y - moon_size//2, 
                      width//2 + moon_size//2, moon_y + moon_size//2], 
                     fill=moon_color)
        
        frames.append(img)
    
    # Save the animation
    frames[0].save('moon_rising.gif', 
                   save_all=True, 
                   append_images=frames[1:], 
                   optimize=False, 
                   duration=50,  # 50 ms between frames
                   loop=0)  # Infinite loop

# Run the animation creation
create_moon_rising_gif()
print("Moon rising GIF has been created as 'moon_rising.gif'")
