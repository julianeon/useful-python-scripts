import pygame
import sys

# Initialize Pygame
pygame.init()

# Function to draw the rectangle with left-aligned text lines and customizable colors
def draw_rectangle_with_text(text_lines, text_color, gradient_start_color, gradient_end_color, rectangle_color):
    # Set up the off-screen surface
    width, height = 1600, 900
    screen = pygame.Surface((width, height))

    # Create a font for the text
    font = pygame.font.Font(None, 100)

    # Calculate the maximum text width and total text height
    max_text_width = 0
    total_text_height = 0

    for line in text_lines:
        text_surface = font.render(line, True, text_color)
        max_text_width = max(max_text_width, text_surface.get_width())
        total_text_height += text_surface.get_height()

    # Padding around the text
    text_padding = 20

    # Calculate the size of the rectangle based on the text size and padding
    text_rect = pygame.Rect(0, 0, max_text_width + 2 * text_padding, total_text_height + 2 * text_padding)
    text_rect.center = (width // 2, height // 2)

    # Create a gradient background
    for y in range(height):
        # Calculate the color based on the gradient
        r = int(gradient_start_color[0] + (y / height) * (gradient_end_color[0] - gradient_start_color[0]))
        g = int(gradient_start_color[1] + (y / height) * (gradient_end_color[1] - gradient_start_color[1]))
        b = int(gradient_start_color[2] + (y / height) * (gradient_end_color[2] - gradient_start_color[2]))
        color = (r, g, b)

        pygame.draw.line(screen, color, (0, y), (width, y))

    # Draw the rectangle with the specified color
    pygame.draw.rect(screen, rectangle_color, text_rect)

    # Draw each line of text with padding inside the rectangle (left-aligned)
    text_y = text_rect.centery - total_text_height // 2

    for line in text_lines:
        text_surface = font.render(line, True, text_color)
        text_x = text_rect.left + text_padding  # Left-align the text
        screen.blit(text_surface, (text_x, text_y))
        text_y += text_surface.get_height()

    # Save the content of the off-screen surface as a PNG image
    pygame.image.save(screen, "output.png")

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Example usage with custom colors and multiple lines of text
    gradient_start_color = (0, 0, 255)  # Starting color (Blue)
    gradient_end_color = (255, 255, 0)  # Ending color (Yellow)
    rectangle_color = (0, 0, 0)  # Black
    text_color = (255, 255, 255)  # White
    text_lines = ["Hello there", "Welcome to California", "Enjoy your stay", "And the weather!"]

    draw_rectangle_with_text(text_lines, text_color, gradient_start_color, gradient_end_color, rectangle_color)
