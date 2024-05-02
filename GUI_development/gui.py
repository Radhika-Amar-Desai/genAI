import pygame
import random
import time
import os
from game import AI_player, initialize_game, Banker, play_round

def play_game(num_players, num_rounds = 13):

  ai_player = AI_player()
  players = initialize_game(ai_player, num_players)
  banker = Banker()
  
  # Define screen size
  screen_width = 800
  screen_height = 600

  # Initialize pygame
  pygame.init()

  # Create the screen
  screen = pygame.display.set_mode((screen_width, screen_height))

  # Set window title
  pygame.display.set_caption("Four Player Bidding")

  # Define some colors
  background_color = (200, 200, 200)
  text_color = (0, 0, 0)
  yellow = (255, 255, 0)  # Color for the yellow box
  red = ( 255, 0, 0 )

  # Create a font for text
  font = pygame.font.Font(None, 32)

  # Define player areas as rectangles
  rectangle_width = 250
  rectangle_height = 100
  yellow_box_width = 100  # Width of the yellow box

  # Calculate positions for top and bottom rectangles
  top_left_x = 50  # Center horizontally
  top_left_y = 50  # Distance from top
  bottom_left_x = top_left_x
  bottom_left_y = screen_height - rectangle_height - 50  # Distance from bottom

  # Create rectangles for player areas and yellow boxes
  player_areas = []
  yellow_boxes = []
  gap = 20  # Gap between player areas

  # Load an image (replace "image.png" with your actual image path)
  image = pygame.image.load("image.png")  # Make sure the image path is correct
  image_width = 50  # Get the image width
  image_height = 70  # Get the image height
  image = pygame.transform.scale(image, (image_width, image_height))
  #print ( image_width, image_height )

  #List for card value and card's image 
  diamonds_card_val_image = {
    "Diamonds_" + str(index) : \
    pygame.image.load(os.path.join("cards", str(index) + "_of_diamonds.png")) \
    for index in range ( 2, 11 )
  }

  diamonds_card_val_image.update({
    "Diamonds_" + card: \
    pygame.image.load(os.path.join("cards", card + "_of_diamonds.png" )) \
    for card in ["ace","jack","king","queen"]
  })

  spades_card_val_image = {
    "Spades_" + str(index) : \
    pygame.image.load(os.path.join("cards", str(index) + "_of_spades.png")) \
    for index in range ( 2, 11 )
  }

  spades_card_val_image.update({
    "Spades_" + card: \
    pygame.image.load(os.path.join("cards", card + "_of_spades.png" )) \
    for card in ["ace","jack","king","queen"]
  })

  clubs_card_val_image = {
    "Clubs_" + str(index) : \
    pygame.image.load(os.path.join("cards", str(index) + "_of_clubs.png")) \
    for index in range ( 2, 11 )
  }

  clubs_card_val_image.update({
    "Clubs_" + card: \
    pygame.image.load(os.path.join("cards", card + "_of_clubs.png" )) \
    for card in ["ace","jack","king","queen"]
  })

  hearts_card_val_image = {
    "Hearts_" + str(index) : \
    pygame.image.load(os.path.join("cards", str(index) + "_of_hearts.png")) \
    for index in range ( 2, 11 )
  }

  hearts_card_val_image.update({
    "Hearts_" + card: \
    pygame.image.load(os.path.join("cards", card + "_of_hearts.png" )) \
    for card in ["ace","jack","king","queen"]
  })

  other_cards = {**diamonds_card_val_image, **hearts_card_val_image, 
                **clubs_card_val_image, **spades_card_val_image}

  for i in range(4):
    # Player area rectangle
    player_rect = pygame.Rect(top_left_x if i % 2 == 0 else top_left_x + rectangle_width + gap, 
                              top_left_y if i < 2 else bottom_left_y, 
                              rectangle_width, rectangle_height)
    player_areas.append(player_rect)

    # Yellow box rectangle
    yellow_box_rect = pygame.Rect(player_rect.right - yellow_box_width, player_rect.top, yellow_box_width, player_rect.height)
    yellow_boxes.append(yellow_box_rect)

  running = True
  for index in range(num_rounds):
    players_and_cards, winner, round_points  = play_round(players, banker, ai_player )
    print ( players_and_cards, "\n", winner )
    player_names = ["Banker"] + list(players_and_cards.keys())
    # Check for events (like closing the window)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    # Fill the screen with background color
    screen.fill(background_color)

    # Render images inside player areas (adjust position as needed)
    for i, area in enumerate(player_areas):
      # Center the image horizontally and vertically within the area
      image_x = area.centerx - image_width
      image_y = area.centery - image_height // 2
      screen.blit(image, (image_x, image_y))

    banker_box = yellow_boxes[0]
    image_x = banker_box.centerx - image_width // 2
    image_y = banker_box.centery - image_height // 2
    #print ( len(list(diamonds_card_val_image.values())) )
    yellow_box_image = list(diamonds_card_val_image.values())[random.randint(0,12)]
    yellow_box_image = pygame.transform.scale(yellow_box_image, 
                                              (image_width, image_height))
    screen.blit( yellow_box_image, ( image_x, image_y ) )

    # Draw yellow boxes with other players
    for i, box in enumerate(yellow_boxes[1:]):
      yellow_box_image = other_cards[players_and_cards[player_names[i]]]
      yellow_box_image = pygame.transform.scale(yellow_box_image, 
                                              (image_width, image_height))
      image_x = box.centerx - image_width // 2
      image_y = box.centery - image_height // 2
      screen.blit(yellow_box_image, (image_x, image_y))

    # Render and display player names
    for i, area in enumerate(player_areas):
      name_text = player_names[i]
      name_surface = font.render(name_text, True, text_color)
      # Center the name text horizontally below the area
      name_x = area.centerx - name_surface.get_width() // 2
      name_y = area.bottom + 10
      screen.blit(name_surface, (name_x, name_y))
    # Winner logic (replace with your actual logic to determine the winner)

    # Calculate winner text surface
    winner_text = "Winners : " + " ".join(winner) + " Points won : " + round_points
    winner_text_surface = font.render(winner_text, True, text_color)

    # Calculate winner text position
    screen_center_x = screen_width // 2
    screen_center_y = screen_height // 2
    winner_text_width = winner_text_surface.get_width()
    winner_text_height = winner_text_surface.get_height()
    winner_text_x = screen_center_x - winner_text_width // 2
    winner_text_y = (top_left_y + bottom_left_y) // 2 - winner_text_height // 2

    # Render winner text
    screen.blit(winner_text_surface, (winner_text_x, winner_text_y))

    # Update the display
    pygame.display.flip()
    time.sleep(2)  # Uncomment to add delay

  # Quit pygame
  pygame.quit()

play_game ( 2, 3 )