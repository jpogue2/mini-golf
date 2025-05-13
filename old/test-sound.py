import pygame

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Load your .wav file
pygame.mixer.music.load("049.wav")

# Create a simple window
screen = pygame.display.set_mode((300, 100))
pygame.display.set_caption("Press Spacebar to Play Sound")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for key press
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.mixer.music.play()

pygame.quit()
