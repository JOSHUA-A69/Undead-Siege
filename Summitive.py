# I - Import and Initialize
import pygame, pygame.locals, sprite_module, random, os
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
            
def game_over_screen(screen, restart_callback, is_classic_mode=False):
    '''Displays the Game Over screen with retry, back-to-menu, and main menu options.'''
    font = pygame.font.Font("American Captain.ttf", 100)  # Use American Captain font
    option_font = pygame.font.Font("American Captain.ttf", 50)  # Use American Captain font
    game_over_text = font.render("Game Over", True, (255, 0, 0))

    # Button text changes based on mode
    retry_text = "Retry" if not is_classic_mode else "Back to Menu"
    retry_rendered_text = option_font.render(retry_text, True, (255, 255, 255))
    retry_rect = retry_rendered_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    main_menu_text = "Main Menu"
    main_menu_rendered_text = option_font.render(main_menu_text, True, (255, 255, 255))
    main_menu_rect = main_menu_rendered_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    # Load game over background image and sound
    game_over_bg = pygame.transform.scale(pygame.image.load('./img/GameOverBG.png'), (1920, 1080))
    pygame.mixer.music.load("./sound/gameover.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Load hover and click sounds
    hover_sound = pygame.mixer.Sound("./sound/Button hover.ogg")
    click_sound = pygame.mixer.Sound("./sound/Button click.mp3")
    hovered = None  # Track hover state

    while True:
        screen.blit(game_over_bg, (0, 0))  # Display game over background
        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, screen.get_height() // 2 - 150))

        # Draw buttons and handle hover effects
        for rect, text in [(retry_rect, retry_rendered_text), (main_menu_rect, main_menu_rendered_text)]:
            if rect.collidepoint(pygame.mouse.get_pos()):
                if hovered != rect:
                    hover_sound.play()
                    hovered = rect
                pygame.draw.rect(screen, (255, 69, 69), rect.inflate(30, 15), border_radius=15)  # Highlight button with red tint
            else:
                if hovered == rect:
                    hovered = None
                pygame.draw.rect(screen, (139, 0, 0), rect.inflate(30, 15), border_radius=15)  # Default button style with red tint
            screen.blit(text, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    click_sound.play()  # Play click sound
                    pygame.mixer.music.stop()  # Stop game over music
                    pygame.mixer.music.unload()  # Unload game over music
                    restart_callback()  # Call the restart function (back to menu or retry)
                    return  # Exit the game over screen
                elif main_menu_rect.collidepoint(event.pos):
                    click_sound.play()  # Play click sound
                    pygame.mixer.music.stop()  # Stop game over music
                    pygame.mixer.music.unload()  # Unload game over music
                    main_menu(screen)  # Go back to the main menu
                    return

        pygame.display.flip()

def loading_screen(screen):
    '''Displays a loading screen.'''
    font = pygame.font.Font("American Captain.ttf", 100)  # Use American Captain font
    loading_text = font.render("Loading...", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(loading_text, (screen.get_width() // 2 - loading_text.get_width() // 2, screen.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Simulate loading time

def main_menu(screen):
    '''Displays the main menu with game mode options.'''
    font = pygame.font.Font("American Captain.ttf", 100)
    option_font = pygame.font.Font("American Captain.ttf", 50)
    studio_font = pygame.font.Font("American Captain.ttf", 30)  # Smaller font for "JNL Studio"

    # Render texts
    studio_text = studio_font.render("JNL Studio", True, (255, 255, 255))  # White color for "JNL Studio"
    title_text = font.render("Undead Siege", True, (255, 255, 255))
    classic_text = option_font.render("Classic Mode", True, (255, 255, 255))
    time_rush_text = option_font.render("Time Rush Mode", True, (255, 255, 255))
    endless_text = option_font.render("Endless Horde Mode", True, (255, 255, 255))
    boss_text = option_font.render("Boss Mode", True, (255, 255, 255))
    exit_text = option_font.render("Exit", True, (255, 255, 255))

    # Define button positions
    classic_rect = classic_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
    time_rush_rect = time_rush_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    endless_rect = endless_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
    boss_rect = boss_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 200))
    exit_rect = exit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 300))

    # Load menu background and music
    menu_bg = pygame.transform.scale(pygame.image.load('./img/MenuBG.png'), (1920, 1080))
    pygame.mixer.music.load("./sound/Menu soundtrack.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Load hover and click sounds
    hover_sound = pygame.mixer.Sound("./sound/Button hover.ogg")
    click_sound = pygame.mixer.Sound("./sound/Button click.mp3")
    hovered = None

    while True:
        screen.blit(menu_bg, (0, 0))

        # Display "JNL Studio" above the title
        screen.blit(studio_text, (screen.get_width() // 2 - studio_text.get_width() // 2, screen.get_height() // 2 - 400))

        # Display the title
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, screen.get_height() // 2 - 300))

        # Draw buttons and handle hover effects
        for rect, text in [(classic_rect, classic_text), (time_rush_rect, time_rush_text), 
                           (endless_rect, endless_text), (boss_rect, boss_text), (exit_rect, exit_text)]:
            if rect.collidepoint(pygame.mouse.get_pos()):
                if hovered != rect:
                    hover_sound.play()
                    hovered = rect
                pygame.draw.rect(screen, (255, 69, 69), rect.inflate(30, 15), border_radius=15)  # Highlight button with red tint
            else:
                pygame.draw.rect(screen, (139, 0, 0), rect.inflate(30, 15), border_radius=15)  # Default button style with red tint
            screen.blit(text, rect)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if classic_rect.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    loading_screen(screen)
                    return  # Start Classic Mode
                elif time_rush_rect.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    loading_screen(screen)
                    time_rush_mode(screen)
                elif endless_rect.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    loading_screen(screen)
                    endless_horde_mode(screen)
                elif boss_rect.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    loading_screen(screen)
                    boss_mode(screen)
                elif exit_rect.collidepoint(event.pos):
                    click_sound.play()
                    pygame.quit()
                    exit()

        pygame.display.flip()

def pause_menu(screen):
    '''Displays the pause menu with options to resume or go back to the main menu.'''
    font = pygame.font.Font("American Captain.ttf", 100)  # Use American Captain font
    option_font = pygame.font.Font("American Captain.ttf", 50)  # Use American Captain font
    pause_text = font.render("Paused", True, (255, 255, 255))
    resume_text = option_font.render("Resume", True, (255, 255, 255))
    menu_text = option_font.render("Main Menu", True, (255, 255, 255))
    resume_rect = resume_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    menu_rect = menu_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    # Load hover and click sounds
    hover_sound = pygame.mixer.Sound("./sound//Button hover.ogg")
    click_sound = pygame.mixer.Sound("./sound//Button click.mp3")
    hovered_resume = False  # Track hover state for Resume button
    hovered_menu = False  # Track hover state for Main Menu button

    while True:
        screen.fill((0, 0, 0))
        screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, screen.get_height() // 2 - 150))

        # Check for hover effect on Resume button
        if resume_rect.collidepoint(pygame.mouse.get_pos()):
            if not hovered_resume:
                hover_sound.play()  # Play hover sound only once
                hovered_resume = True
            pygame.draw.rect(screen, (255, 69, 69), resume_rect.inflate(30, 15), border_radius=15)  # Highlight button with red tint
        else:
            hovered_resume = False
            pygame.draw.rect(screen, (139, 0, 0), resume_rect.inflate(30, 15), border_radius=15)  # Default button style with red tint

        screen.blit(resume_text, resume_rect)

        # Check for hover effect on Main Menu button
        if menu_rect.collidepoint(pygame.mouse.get_pos()):
            if not hovered_menu:
                hover_sound.play()  # Play hover sound only once
                hovered_menu = True
            pygame.draw.rect(screen, (255, 69, 69), menu_rect.inflate(30, 15), border_radius=15)  # Highlight button with red tint
        else:
            hovered_menu = False
            pygame.draw.rect(screen, (139, 0, 0), menu_rect.inflate(30, 15), border_radius=15)  # Default button style with red tint

        screen.blit(menu_text, menu_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    click_sound.play()  # Play click sound
                    return  # Resume the game
                elif menu_rect.collidepoint(event.pos):
                    click_sound.play()  # Play click sound
                    main_menu(screen)  # Go back to the main menu
                    return

        pygame.display.flip()

def time_rush_mode(screen, time_limit=300):
    '''Time Rush Mode: Survive until the timer runs out.'''
    # Load powerup images
    powerup_images = []
    for file in os.listdir('powerups/'):
        powerup_images.append(pygame.image.load('./powerups/' + file))

    # Initialize game elements
    background = pygame.transform.scale(pygame.image.load('./img/bg.jpg'), (1920, 1080))
    background = background.convert()
    
    # Music setup
    pygame.mixer.music.load("./sound/InGame soundtrack.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Load gun sound
    fire = pygame.mixer.Sound("./sound/bullet1.ogg")
    fire.set_volume(0.5)  # Ensure the volume is set to an audible level

    # Initialize player
    player = sprite_module.Player(screen)
    player.rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    # Timer and score setup
    timer_text = sprite_module.Text(30, (255, 255, 255), (screen.get_width() // 2, 50), str(time_limit), "Time Left: %s", 255)
    score_text = sprite_module.Text(30, (255, 255, 255), (screen.get_width() // 2, 90), "0", "Score: %s", 255)
    score = 0

    # Health and armor setup
    player_status = [[350, 350], [200, 200], 3]
    health = sprite_module.StatusBar((10, 10), (255, 0, 0), (0, 0, 0), (250, 30), 350, 350, 0, None)
    armour = sprite_module.StatusBar((10, 50), (238, 233, 233), (139, 137, 137), (250, 30), 200, 200, 0, None)
    health_text = sprite_module.Text(25, (255, 255, 255), (135, 25), '350,350', '%s/%s', 255)
    armour_text = sprite_module.Text(25, (0, 0, 0), (135, 65), '200,200', '%s/%s', 255)

    # Zombie setup
    z_img = [pygame.image.load('./enemy/' + file) for file in os.listdir('enemy/')]
    z_info = [[3, 5, 10, 100, 2], [3, 5, 20, 100, 4], [3, 5, 20, 100, 6], [3, 5, 20, 100, 8], [3, 5, 20, 100, 10], [3, 5, 20, 100, 12], [15, 20, 100, 100, 40]]
    zombieGroup = pygame.sprite.Group()

    # Bullet setup
    bullet_images = [pygame.image.load('./bullets/' + file) for file in os.listdir('bullets/')]
    bullet_img = pygame.sprite.Group()
    bullet_hitbox = pygame.sprite.Group()
    powerupGroup = pygame.sprite.Group()

    # Gold text setup
    gold_text = sprite_module.Text(30, (255, 215, 0), (screen.get_width() // 2, 130), "0", "Gold: %s", 255)

    # Sprite groups
    allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, powerupGroup,
                                            health, armour, health_text, armour_text, timer_text, score_text, gold_text)

    # Game loop setup
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    keepGoing = True
    spawn_timer = 0

    while keepGoing:
        clock.tick(40)
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000
        remaining_time = time_limit - elapsed_time
        timer_text.set_variable(0, str(remaining_time))
        
        # Check win condition (time's up)
        if remaining_time <= 0:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            show_times_up_screen(screen, score)
            return

        # Spawn zombies periodically
        spawn_timer += 1
        if spawn_timer >= 40:
            spawn_timer = 0
            # Adjusted zombie stats: [speed, damage, health, attack_speed, score_value]
            zombie_stats = [3, 5, 150, 50, 10]  # Increased health from 100 to 150
            zombie = sprite_module.Zombie(screen, *zombie_stats, z_img[0], 0, player.rect.center)
            zombieGroup.add(zombie)
            allSprites.add(zombie)

        # Handle input
        keystate = pygame.key.get_pressed()
        if keystate[pygame.locals.K_w]: player.go_up(screen)
        if keystate[pygame.locals.K_s]: player.go_down(screen)
        if keystate[pygame.locals.K_a]: player.go_left(screen)
        if keystate[pygame.locals.K_d]: player.go_right(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_menu(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bullet1 = sprite_module.Bullet(bullet_images[0], player.get_angle(), player.rect.center, pygame.mouse.get_pos(), 12, 10, False)
                bullet2 = sprite_module.Bullet(None, None, player.rect.center, pygame.mouse.get_pos(), 12, 10, False)
                bullet_img.add(bullet1)
                bullet_hitbox.add(bullet2)
                allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, powerupGroup,
                                                          health, armour, health_text, armour_text, timer_text, score_text, gold_text)
                fire.play()  # Play the gun sound

        # Update player rotation
        player.rotate(pygame.mouse.get_pos())

        # Handle collisions
        if pygame.sprite.spritecollide(player, zombieGroup, False):
            if player_status[1][0] > 0:
                player_status[1][0] -= 5
                if player_status[1][0] < 0:
                    player_status[0][0] += player_status[1][0]
                    player_status[1][0] = 0
            else:
                player_status[0][0] -= 5
                if player_status[0][0] <= 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    game_over_screen(screen, lambda: time_rush_mode(screen, time_limit))
                    return

        # Handle zombie damage from bullets
        hits = pygame.sprite.groupcollide(bullet_hitbox, zombieGroup, True, False)
        for bullet_hit in hits:
            for zombie in hits[bullet_hit]:
                if not zombie.damage_hp(bullet_hit.get_damage()):  # Reduce zombie health
                    zombie.kill()  # Remove zombie if health is zero
                    score += zombie.get_value()  # Increment score
                    score_text.set_variable(0, str(score))  # Update score display
                    player.add_gold(2)  # Add 2 gold per zombie kill
                    gold_text.set_variable(0, str(player.get_gold()))  # Update gold display

                    # After zombie death, chance to spawn powerup
                    if random.random() < 0.15:  # Reduced from 0.2 to make powerups slightly rarer
                        powerup_type = random.randint(0, 5)  # 0=speed, 1=double damage, 2=health, 3=armor, 4=ammo, 5=invincibility
                        powerup = sprite_module.Powerup(
                            zombie.rect.center,  # Spawn at dead zombie's position
                            powerup_type,
                            powerup_images[powerup_type]
                        )
                        powerupGroup.add(powerup)
                        allSprites = pygame.sprite.OrderedUpdates(
                            bullet_img, bullet_hitbox, player, zombieGroup, 
                            powerupGroup, health, armour, health_text, 
                            armour_text, timer_text, score_text, gold_text
                        )

        # Update displays
        health.set_status(player_status[0][0])
        health_text.set_variable(0, str(player_status[0][0]))
        armour.set_status(player_status[1][0])
        armour_text.set_variable(0, str(player_status[1][0]))

        # Update zombies
        for zombie in zombieGroup:
            zombie.rotate(player.rect.center)
            zombie.set_step_amount(player.rect.center)

        # Draw everything
        screen.blit(background, (0, 0))
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

def endless_horde_mode(screen):
    '''Endless Horde Mode: Survive as long as possible with continuously increasing difficulty.'''
    # Load powerup images
    powerup_images = []
    for file in os.listdir('powerups/'):
        powerup_images.append(pygame.image.load('./powerups/' + file))

    # Initialize game elements
    background = pygame.transform.scale(pygame.image.load('./img/bg.jpg'), (1920, 1080))
    background = background.convert()
    
    # Music setup
    pygame.mixer.music.load("./sound/InGame soundtrack.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Load gun sound
    fire = pygame.mixer.Sound("./sound/bullet1.ogg")
    fire.set_volume(0.5)  # Ensure the volume is set to an audible level

    # Initialize player and status
    player = sprite_module.Player(screen)
    player.rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    player_status = [[350, 350], [200, 200], 3]

    # Status bars and text
    health = sprite_module.StatusBar((10, 10), (255, 0, 0), (0, 0, 0), (250, 30), 350, 350, 0, None)
    armour = sprite_module.StatusBar((10, 50), (238, 233, 233), (139, 137, 137), (250, 30), 200, 200, 0, None)
    health_text = sprite_module.Text(25, (255, 255, 255), (135, 25), '350,350', '%s/%s', 255)
    armour_text = sprite_module.Text(25, (0, 0, 0), (135, 65), '200,200', '%s/%s', 255)
    score_text = sprite_module.Text(30, (255, 255, 255), (screen.get_width() // 2, 50), "0", "Score: %s", 255)
    gold_text = sprite_module.Text(30, (255, 215, 0), (screen.get_width() // 2, 90), "0", "Gold: %s", 255)

    # Load images
    bullet_images = [pygame.image.load('./bullets/' + file) for file in os.listdir('bullets/')]
    z_img = [pygame.image.load('./enemy/' + file) for file in os.listdir('enemy/')]

    # Sprite groups
    zombieGroup = pygame.sprite.Group()
    bullet_img = pygame.sprite.Group()
    bullet_hitbox = pygame.sprite.Group()
    powerupGroup = pygame.sprite.Group()

    # Initialize sprite groups
    allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                            powerupGroup, health, armour, health_text, 
                                            armour_text, score_text, gold_text)

    # Game variables
    clock = pygame.time.Clock()
    spawn_timer = 0
    score = 0
    difficulty_multiplier = 1.0
    keepGoing = True

    while keepGoing:
        clock.tick(40)
        spawn_timer += 1

        # Spawn zombies with increasing difficulty based on score
        if spawn_timer >= max(5, 30 - score//500):  # Spawn rate increases with score
            spawn_timer = 0
            zombie_type = random.randint(0, min(len(z_img)-1, score//1000))  # More zombie types as score increases
            zombie_stats = [
                3 + score//1000,  # Speed increases with score
                5 + score//500,   # Damage increases with score
                50 + score//100,  # Health increases with score
                50,              # Attack speed
                10 + score//200  # Score value increases with difficulty
            ]
            zombie = sprite_module.Zombie(screen, *zombie_stats, z_img[zombie_type], 0, player.rect.center)
            zombieGroup.add(zombie)
            allSprites.add(zombie)

        # Handle input
        keystate = pygame.key.get_pressed()
        if keystate[pygame.locals.K_w]: player.go_up(screen)
        if keystate[pygame.locals.K_s]: player.go_down(screen)
        if keystate[pygame.locals.K_a]: player.go_left(screen)
        if keystate[pygame.locals.K_d]: player.go_right(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_menu(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bullet1 = sprite_module.Bullet(bullet_images[0], player.get_angle(), player.rect.center, pygame.mouse.get_pos(), 12, 10, False)
                bullet2 = sprite_module.Bullet(None, None, player.rect.center, pygame.mouse.get_pos(), 12, 10, False)
                bullet_img.add(bullet1)
                bullet_hitbox.add(bullet2)
                allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                                          powerupGroup, health, armour, health_text, 
                                                          armour_text, score_text, gold_text)
                fire.play()  # Play the gun sound

        # Update player rotation
        player.rotate(pygame.mouse.get_pos())

        # Handle collisions
        if pygame.sprite.spritecollide(player, zombieGroup, False):
            if player_status[1][0] > 0:
                player_status[1][0] -= 5
                if player_status[1][0] < 0:
                    player_status[0][0] += player_status[1][0]
                    player_status[1][0] = 0
            else:
                player_status[0][0] -= 5
                if player_status[0][0] <= 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    game_over_screen(screen, lambda: endless_horde_mode(screen))
                    return

        # Handle zombie damage from bullets
        hits = pygame.sprite.groupcollide(bullet_hitbox, zombieGroup, True, False)
        for bullet_hit in hits:
            for zombie in hits[bullet_hit]:
                if not zombie.damage_hp(bullet_hit.get_damage()):  # Reduce zombie health
                    zombie.kill()  # Remove zombie if health is zero
                    score += zombie.get_value()  # Increment score
                    score_text.set_variable(0, str(score))  # Update score display
                    player.add_gold(2)  # Add 2 gold per zombie kill
                    gold_text.set_variable(0, str(player.get_gold()))  # Update gold display

                    # After zombie death, chance to spawn powerup
                    if random.random() < 0.15:  # Reduced from 0.2 to make powerups slightly rarer
                        powerup_type = random.randint(0, 5)  # 0=speed, 1=double damage, 2=health, 3=armor, 4=ammo, 5=invincibility
                        powerup = sprite_module.Powerup(
                            zombie.rect.center,  # Spawn at dead zombie's position
                            powerup_type,
                            powerup_images[powerup_type]
                        )
                        powerupGroup.add(powerup)
                        allSprites = pygame.sprite.OrderedUpdates(
                            bullet_img, bullet_hitbox, player, zombieGroup, 
                            powerupGroup, health, armour, health_text, 
                            armour_text, score_text, gold_text
                        )

        # Update displays
        health.set_status(player_status[0][0])
        health_text.set_variable(0, str(player_status[0][0]))
        armour.set_status(player_status[1][0])
        armour_text.set_variable(0, str(player_status[1][0]))

        # Update zombies
        for zombie in zombieGroup:
            zombie.rotate(player.rect.center)
            zombie.set_step_amount(player.rect.center)

        # Draw everything
        screen.blit(background, (0, 0))
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

def show_times_up_screen(screen, score):
    '''Displays the Times Up celebration screen when player survives time rush mode.'''
    font = pygame.font.Font("American Captain.ttf", 100)
    score_font = pygame.font.Font("American Captain.ttf", 50)
    
    # Create text renders
    times_up_text = font.render("Time's Up - You Survived!", True, (0, 255, 0))
    final_score_text = score_font.render(f"Final Score: {score}", True, (255, 255, 255))
    continue_text = score_font.render("Click anywhere to continue", True, (255, 255, 255))
    
    # Get text positions
    times_up_rect = times_up_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
    score_rect = final_score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    continue_rect = continue_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
    
    # Create fade overlay
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    
    waiting = True
    while waiting:
        screen.blit(overlay, (0, 0))
        screen.blit(times_up_text, times_up_rect)
        screen.blit(final_score_text, score_rect)
        screen.blit(continue_text, continue_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        
        pygame.display.flip()

def show_victory_screen(screen):
    '''Displays the Victory screen after defeating the boss.'''
    font = pygame.font.Font("American Captain.ttf", 100)
    victory_text = font.render("Victory!", True, (0, 255, 0))
    continue_text = font.render("Click anywhere to return to the main menu", True, (255, 255, 255))

    victory_rect = victory_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    continue_rect = continue_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        screen.blit(victory_text, victory_rect)
        screen.blit(continue_text, continue_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        pygame.display.flip()

def boss_mode(screen):
    '''Boss Mode: Similar to Classic Mode, but the last zombie in each wave is a boss.'''
    # Load powerup images
    powerup_images = []
    for file in os.listdir('powerups/'):
        powerup_images.append(pygame.image.load('./powerups/' + file))

    # Load background and music
    background = pygame.transform.scale(pygame.image.load('./img/bg.jpg'), (1920, 1080))
    background = background.convert()

    # Load bullet images - Add this section
    bullet_images = []
    for file in os.listdir('bullets/'):
        bullet_images.append(pygame.image.load('./bullets/' + file))

    # Initialize player first
    player = sprite_module.Player(screen)
    player.rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    # Health and armor setup
    player_status = [[350, 350], [200, 200], 3]
    health = sprite_module.StatusBar((10, 10), (255, 0, 0), (0, 0, 0), (250, 30), 350, 350, 0, None)
    armour = sprite_module.StatusBar((10, 50), (238, 233, 233), (139, 137, 137), (250, 30), 200, 200, 0, None)
    health_text = sprite_module.Text(25, (255, 255, 255), (135, 25), '350,350', '%s/%s', 255)
    armour_text = sprite_module.Text(25, (0, 0, 0), (135, 65), '200,200', '%s/%s', 255)

    # Score and gold setup
    score = 0
    score_text = sprite_module.Text(30, (255, 255, 255), (screen.get_width() // 2, 50), "0", "Score: %s", 255)
    gold_text = sprite_module.Text(30, (255, 215, 0), (screen.get_width() // 2, 90), "0", "Gold: %s", 255)

    # Initialize sprite groups
    zombieGroup = pygame.sprite.Group()
    bullet_img = pygame.sprite.Group()
    bullet_hitbox = pygame.sprite.Group()
    powerupGroup = pygame.sprite.Group()

    # Now create allSprites after all components are initialized
    allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                            powerupGroup, health, armour, health_text, 
                                            armour_text, score_text, gold_text)

    # Music setup
    pygame.mixer.music.load("./sound/InGame soundtrack.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Bullet sound
    bullet_sound = pygame.mixer.Sound("./sound/bullet1.ogg")
    bullet_sound.set_volume(0.5)

    # Zombie setup
    z_img = [pygame.image.load('./enemy/' + file) for file in os.listdir('enemy/')]
    boss_image = pygame.image.load('./enemy/citizenzombieboss.png')

    # Game loop setup
    clock = pygame.time.Clock()
    wave = 1
    keepGoing = True

    while keepGoing:
        # Spawn zombies for the wave
        num_zombies = 10 + wave * 2  # Increase number of zombies with each wave
        for i in range(num_zombies):
            if i == num_zombies - 1:  # Last zombie is the boss
                boss = sprite_module.Zombie(screen, speed=2, damage=20, hp=500, attack_speed=50, value=1000, image=boss_image, zombie_type=99, player_pos=player.rect.center)
                zombieGroup.add(boss)
            else:  # Regular zombies
                zombie = sprite_module.Zombie(screen, speed=2 + wave // 2, damage=10 + wave, hp=50 + wave * 10,
                                              attack_speed=50, value=10, image=z_img[0], zombie_type=0, player_pos=player.rect.center)
                zombieGroup.add(zombie)

        # Update sprite groups
        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, health, armour, health_text, armour_text, score_text, gold_text)

        # Wave loop
        while len(zombieGroup) > 0:
            clock.tick(40)

            # Handle input
            keystate = pygame.key.get_pressed()
            if keystate[pygame.locals.K_w]: player.go_up(screen)
            if keystate[pygame.locals.K_s]: player.go_down(screen)
            if keystate[pygame.locals.K_a]: player.go_left(screen)
            if keystate[pygame.locals.K_d]: player.go_right(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause_menu(screen)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    bullet1 = sprite_module.Bullet(bullet_images[0], player.get_angle(), player.rect.center, pygame.mouse.get_pos(), 12, 10, False)
                    bullet2 = sprite_module.Bullet(None, None, player.rect.center, pygame.mouse.get_pos(), 12, 10, False)
                    bullet_img.add(bullet1)
                    bullet_hitbox.add(bullet2)
                    allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, health, armour, health_text, armour_text, score_text, gold_text)
                    bullet_sound.play()  # Play bullet sound

            # Update player rotation
            player.rotate(pygame.mouse.get_pos())

            # Handle collisions
            if pygame.sprite.spritecollide(player, zombieGroup, False):
                if player_status[1][0] > 0:
                    player_status[1][0] -= 5
                    if player_status[1][0] < 0:
                        player_status[0][0] += player_status[1][0]  # Subtract remaining damage from health
                        player_status[1][0] = 0
                else:
                    player_status[0][0] -= 5

                # Update displays
                armour.set_status(player_status[1][0])
                armour_text.set_variable(0, str(player_status[1][0]))

                if player_status[0][0] <= 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    game_over_screen(screen, lambda: boss_mode(screen))
                    return

            # Handle zombie damage from bullets
            hits = pygame.sprite.groupcollide(bullet_hitbox, zombieGroup, True, False)
            for bullet_hit in hits:
                for zombie in hits[bullet_hit]:
                    if not zombie.damage_hp(bullet_hit.get_damage()):  # Reduce zombie health
                        zombie.kill()  # Remove zombie if health is zero
                        score += zombie.get_value()  # Increment score
                        score_text.set_variable(0, str(score))  # Update score display
                        player.add_gold(2)  # Add 2 gold per zombie kill
                        gold_text.set_variable(0, str(player.get_gold()))  # Update gold display

                        # After zombie death, chance to spawn powerup
                        if random.random() < 0.15:  # Reduced from 0.2 to make powerups slightly rarer
                            powerup_type = random.randint(0, 5)  # 0=speed, 1=double damage, 2=health, 3=armor, 4=ammo, 5=invincibility
                            powerup = sprite_module.Powerup(
                                zombie.rect.center,  # Spawn at dead zombie's position
                                powerup_type,
                                powerup_images[powerup_type]
                            )
                            powerupGroup.add(powerup)
                            allSprites = pygame.sprite.OrderedUpdates(
                                bullet_img, bullet_hitbox, player, zombieGroup, 
                                powerupGroup, health, armour, health_text, 
                                armour_text, score_text, gold_text
                            )

            # Update displays
            health.set_status(player_status[0][0])
            health_text.set_variable(0, str(player_status[0][0]))
            armour.set_status(player_status[1][0])
            armour_text.set_variable(0, str(player_status[1][0]))

            # Update zombies
            for zombie in zombieGroup:
                zombie.rotate(player.rect.center)
                zombie.set_step_amount(player.rect.center)

            # Draw everything
            screen.blit(background, (0, 0))
            allSprites.update()
            allSprites.draw(screen)
            pygame.display.flip()

        # Increment wave counter
        wave += 1

def damage_hp(self, damage):
    self.hp -= damage
    if self.hp <= 0:
        return False  # Indicates the zombie is dead
    return True  # Indicates the zombie is still alive

def main():
    '''This function defines the 'mainline logic' for our game.'''
    while True:
        main_menu(screen)

        pygame.display.set_caption("")
     
        background = pygame.transform.scale(pygame.image.load('./img/bg.jpg'), (1920, 1080))
        background = background.convert()
        screen.blit(background, (0, 0))
    
        pygame.mixer.music.load("./sound/InGame soundtrack.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        fire = pygame.mixer.Sound("./sound/bullet1.ogg")
        fire.set_volume(0.5)
        no = pygame.mixer.Sound("./sound/no.ogg")
        no.set_volume(0.8)
    
        player = sprite_module.Player(screen)
        player.rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    
        # Classic mode - 10 enemies per wave, evenly distributed
        wave = [6, 1, 1, 1, 1, 0, 0]  # Total 10 enemies per wave (6 basic + 4 special)
    
        z_img = []
        for file in os.listdir('enemy/'):
            z_img.append(pygame.image.load('./enemy/' + file))
            
        z_info = [[3, 5, 10, 100, 2], [3, 5, 20, 100, 4], [3, 5, 20, 100, 6], [3, 5, 20, 100, 8], [3, 5, 20, 100, 10], [3, 5, 20, 100, 12], [15, 20, 100, 100, 40]]
    
        # Initialize first wave zombies
        zombies = []
        zombie_types = [0] * 6 + [1, 2, 3, 4]  # 6 basic zombies + 4 special (total 10)
        random.shuffle(zombie_types)  # Randomize spawn order

        for zombie_type in zombie_types:
            zombies.append(sprite_module.Zombie(screen, 
                                                z_info[zombie_type][0], 
                                                z_info[zombie_type][1], 
                                                z_info[zombie_type][2], 
                                                z_info[zombie_type][3], 
                                                z_info[zombie_type][4], 
                                                z_img[zombie_type], 
                                                zombie_type, 
                                                player.rect.center))
            wave[zombie_type] -= 1
    
        ammo = [[20, 30], [40, 20], [15, 10], [100, 10], [30, 30]]
        ammo_capacity = [20, 40, 15, 100, 30]
        temp_string = ''
    
        for index in range(len(ammo)):
            temp_string += str(ammo[index][0]) + ',' + str(ammo[index][1]) + ','
    
        ammo_text = sprite_module.Text(20, (255, 255, 255), (800, 80), temp_string.strip(','), '%s/%s          %s/%s          %s/%s          %s/%s          %s/%s', 255)  
    
        player_status = [[350, 350], [200, 200], 3]   
    
        health = sprite_module.StatusBar((10, 10), (255, 0, 0), (0, 0, 0), (250, 30), 200, 350, 0, None)
        armour = sprite_module.StatusBar((10, 50), (238, 233, 233), (139, 137, 137), (250, 30), 100, 200, 0, None)
    
        health_text = sprite_module.Text(25, (255, 255, 255), (135, 25), '350,350', '%s/%s', 255)
        armour_text = sprite_module.Text(25, (0, 0, 0), (135, 65), '200,200', '%s/%s', 255)
        wave_text = sprite_module.Text(30, (255, 255, 255), (450, 40), '0,1,' + str(sum(wave)), 'Score:%s Wave:%s Zombies Left:%s', 255)
        gold_text = sprite_module.Text(30, (255, 215, 0), (450, 80), '0', 'Gold: %s', 255)  # Gold color (255,215,0)

        # Add this line to define score_text
        score_text = sprite_module.Text(30, (255, 255, 255), (screen.get_width() // 2, 50), "0", "Score: %s", 255)
    
        powerupGroup = pygame.sprite.Group()
        zombieGroup = pygame.sprite.Group()
        for zombie in zombies:
            zombieGroup.add(zombie)

        bullet_img = pygame.sprite.Group()
        bullet_hitbox = pygame.sprite.Group()
        reloading = pygame.sprite.Group()
    
        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, powerupGroup, reloading, health, armour, health_text, armour_text, wave_text, gold_text, ammo_text, score_text)
     
        clock = pygame.time.Clock()
        keepGoing = True

        speed_timer = 0
        damage_timer = 0
        invincible_timer = 0
    
        powerup_status = False     
        speed_status = False       
        double_status = False
        invincible_status = False
    
        boss_spawn = False
    
        powerup_images = []
        for file in os.listdir('powerups/'):
            powerup_images.append(pygame.image.load('./powerups/' + file))
            
        bullet_images = []
        for file in os.listdir('bullets/'):
            bullet_images.append(pygame.image.load('./bullets/' + file))
    
        powerup_chance = 0
    
        wave_num = 1
    
        wave_value = [10, 1, 1, 1, 1, 1, 0]
    
        active_zombies = 10
    
        score = 0
    
        weapon = [True, True, True, True, True]
    
        current_weapon = 0
    
        reload_time = [1.5, 2, 1, 0.5, 1.5]
        reload_status = False
    
        machine_gun_fire = False
        machine_gun_delay = 0
    
        while keepGoing:
            clock.tick(40)
        
            keystate = pygame.key.get_pressed()
            if keystate[pygame.locals.K_w]:
                player.go_up(screen) 
                if reload_status:
                    reload.set_position((player.rect.center[0] - 40, player.rect.center[1] - 60))
                
            if keystate[pygame.locals.K_a]:
                player.go_left(screen)
                if reload_status:
                    reload.set_position((player.rect.center[0] - 40, player.rect.center[1] - 60))          
        
            if keystate[pygame.locals.K_s]:
                player.go_down(screen)
                if reload_status:
                    reload.set_position((player.rect.center[0] - 40, player.rect.center[1] - 60))  
                
            if keystate[pygame.locals.K_d]:
                player.go_right(screen)         
                if reload_status:
                    reload.set_position((player.rect.center[0] - 40, player.rect.center[1] - 60))

            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    keepGoing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu(screen)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if current_weapon == 0 and ammo[0][0]:
                        ammo[0][0] -= 1
                        # Create visual bullet and hitbox with same speed and damage
                        bullet_visual = sprite_module.Bullet(bullet_images[0], player.get_angle(), 
                                                        player.rect.center, pygame.mouse.get_pos(), 12, 2, double_status)
                        bullet_hit = sprite_module.Bullet(None, None, player.rect.center, 
                                                     pygame.mouse.get_pos(), 12, 2, double_status)
                        bullet_img.add(bullet_visual)
                        bullet_hitbox.add(bullet_hit)
                        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup,
                                                              powerupGroup, reloading, health, armour,
                                                              health_text, armour_text, wave_text, gold_text, ammo_text)
                        fire.play()
                
                    elif current_weapon == 1 and ammo[1][0]:
                        ammo[1][0] -= 1
                        # Create visual bullet and hitbox with same speed and damage
                        bullet_visual = sprite_module.Bullet(bullet_images[1], player.get_angle(), 
                                                        player.rect.center, pygame.mouse.get_pos(), 16, 5, double_status)
                        bullet_hit = sprite_module.Bullet(None, None, player.rect.center, 
                                                     pygame.mouse.get_pos(), 16, 5, double_status)
                        bullet_img.add(bullet_visual)
                        bullet_hitbox.add(bullet_hit)
                        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                                              powerupGroup, reloading, health, armour, 
                                                              health_text, armour_text, wave_text, gold_text, ammo_text)
                        fire.play()
                
                    elif current_weapon == 2 and ammo[2][0]:
                        ammo[2][0] -= 1
                        # Create visual bullet and hitbox with same speed and damage
                        bullet_visual = sprite_module.Bullet(bullet_images[2], player.get_angle(), 
                                                        player.rect.center, pygame.mouse.get_pos(), 8, 0, double_status)
                        bullet_hit = sprite_module.Bullet(None, None, player.rect.center, 
                                                     pygame.mouse.get_pos(), 8, 0, double_status)
                        bullet_img.add(bullet_visual)
                        bullet_hitbox.add(bullet_hit)
                        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                                              powerupGroup, reloading, health, armour, 
                                                              health_text, armour_text, wave_text, gold_text, ammo_text)
                
                    elif current_weapon == 3 and ammo[3][0]:
                        machine_gun_fire = True
                    
                    elif current_weapon == 4 and ammo[4][0]:
                        ammo[4][0] -= 1
                        # Create railgun visual and hitbox
                        bullet_visual = sprite_module.RailGun(screen, player.rect.center, pygame.mouse.get_pos())
                        bullet_hit = sprite_module.Bullet(None, None, player.rect.center, 
                                                     pygame.mouse.get_pos(), 20, 20, double_status)
                        bullet_img.add(bullet_visual)
                        bullet_hitbox.add(bullet_hit)
                        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                                             powerupGroup, reloading, health, armour, 
                                                             health_text, armour_text, wave_text, gold_text, ammo_text)
                    
                    else:
                        if reload_status != True and ammo[current_weapon][1]:
                            reload = sprite_module.StatusBar((player.rect.center[0] - 40, player.rect.center[1] - 60), (0, 255, 0), (0, 0, 0), (70, 7), 0, 100, 1, reload_time[current_weapon])
                            reloading.add(reload)
                            allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, powerupGroup, reloading, health, armour, health_text, armour_text, wave_text, gold_text, ammo_text, score_text)
                        reload_status = True
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    if current_weapon == 3:
                        machine_gun_fire = False
            
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and weapon[0]:
                        current_weapon = 0
                        player.change_image(0)
                        machine_gun_fire = False
                        reload_status = False

                    elif event.key == pygame.K_2 and weapon[1]:
                        current_weapon = 1
                        player.change_image(1)
                        machine_gun_fire = False
                        reload_status = False

                    elif event.key == pygame.K_3 and weapon[2]:
                        current_weapon = 2
                        player.change_image(2)
                        machine_gun_fire = False
                        reload_status = False

                    elif event.key == pygame.K_4 and weapon[3]:
                        current_weapon = 3
                        reload_status = False

                    elif event.key == pygame.K_5 and weapon[4]:
                        current_weapon = 4
                        player.change_image(4)
                        machine_gun_fire = False
                        reload_status = False

                    elif event.key == pygame.K_r:  # Reload key
                        if not reload_status and ammo[current_weapon][1] > 0:  # If not already reloading and has ammo clips
                            reload = sprite_module.StatusBar(
                                (player.rect.center[0] - 40, player.rect.center[1] - 60),
                                (0, 255, 0), (0, 0, 0), (70, 7), 0, 100, 1, 
                                reload_time[current_weapon]
                            )
                            reloading.add(reload)
                            allSprites = pygame.sprite.OrderedUpdates(
                                bullet_img, bullet_hitbox, player, zombieGroup,
                                powerupGroup, reloading, health, armour,
                                health_text, armour_text, wave_text, gold_text, ammo_text
                            )
                            reload_status = True

                    elif event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5:
                        no.play()
                    
            x = pygame.sprite.spritecollide(player, zombieGroup, False)
            if x:
                for zombie in x:
                    zombie.move(False)
                
                    if not(invincible_status):
                        if zombie.get_attack():
                            if player_status[1][0] > 0:
                                player_status[1][0] -= 5
                                if player_status[1][0] < 0:
                                    player_status[0][0] += player_status[1][0]  # Subtract remaining damage from health
                                    player_status[1][0] = 0
                            else:
                                player_status[0][0] -= 5

                                if player_status[0][0] <= 0:
                                    pygame.mixer.music.stop()
                                    pygame.mixer.music.unload()
                                    game_over_screen(screen, lambda: boss_mode(screen))
                                    return

            else:
                for zombie in zombieGroup:
                    zombie.move(True)
                    zombie.reset_attack()
                    
            c = pygame.sprite.groupcollide(bullet_hitbox, zombieGroup, True, False)
            v = pygame.sprite.groupcollide(bullet_img, zombieGroup, True, False)
            if c:
                for bullet in c.keys():
                    if bullet.get_damage() == 0:
                        c[bullet][0].slow()
                    
                    else:
                        if not c[bullet][0].damage_hp(10):  # If zombie dies
                            c[bullet][0].kill()  # Remove zombie from the game
                            score += c[bullet][0].get_value()  # Increase score
                            score_text.set_variable(0, str(score))  # Update score display
                            player.add_gold(2)  # Add 2 gold per zombie kill
                            gold_text.set_variable(0, str(player.get_gold()))  # Update gold display

                            # After zombie death, chance to spawn powerup
                            if random.random() < 0.15:  # Reduced from 0.2 to make powerups slightly rarer
                                powerup_type = random.randint(0, 5)  # 0=speed, 1=double damage, 2=health, 3=armor, 4=ammo, 5=invincibility
                                powerup = sprite_module.Powerup(
                                    c[bullet][0].rect.center,  # Spawn at dead zombie's position
                                    powerup_type,
                                    powerup_images[powerup_type]
                                )
                                powerupGroup.add(powerup)
                                allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                                                          powerupGroup, reloading, health, armour, 
                                                                          health_text, armour_text, wave_text, gold_text, 
                                                                          ammo_text, score_text)
                
            y = pygame.sprite.spritecollide(player, powerupGroup, False)
            if y:
                for buff in y:
                    powerup_type = buff.get_type()
                    if powerup_type == 0:
                        speed_timer = 0
                        speed_status = True
                        player.increase_speed()
                    
                    elif powerup_type == 1:
                        double_status = True
                        damage_timer = 0
                    
                    elif powerup_type == 2:
                        player_status[0][0] = player_status[0][0] + 100
                        if player_status[0][0] > player_status[0][1]:
                            player_status[0][0] = player_status[0][1]
                        
                    elif powerup_type == 3:
                        player_status[1][0] = player_status[1][0] + 100
                        if player_status[1][0] > player_status[1][1]:
                            player_status[1][0] = player_status[1][1]
                        
                    elif powerup_type == 4:
                        ammo_type = random.randint(0, len(ammo) - 1)
                        ammo[ammo_type][0] = ammo_capacity[ammo_type]
                        ammo[ammo_type][1] = ammo[ammo_type][1] + 2
                    
                    elif powerup_type == 5:
                        invincible_status = True
                        invincible_timer = 0
                
                    buff.kill()
                
            player.rotate(pygame.mouse.get_pos())
        
            if machine_gun_fire:
                machine_gun_delay += 1
                if machine_gun_delay % 3 == 0:
                    if ammo[3][0] > 0:  # Only fire if we have ammo
                        ammo[3][0] -= 1
                        # Create machine gun bullet and hitbox with same speed and damage
                        bullet_visual = sprite_module.Bullet(bullet_images[0], player.get_angle(), 
                                                        player.rect.center, pygame.mouse.get_pos(), 14, 6, double_status)
                        bullet_hit = sprite_module.Bullet(None, None, player.rect.center, 
                                                     pygame.mouse.get_pos(), 14, 6, double_status)
                        bullet_img.add(bullet_visual)
                        bullet_hitbox.add(bullet_hit)
                        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                                             powerupGroup, reloading, health, armour, 
                                                             health_text, armour_text, wave_text, gold_text, ammo_text)
                        fire.play()
                
            if ammo[3][0] == 0:
                machine_gun_fire = False
        
            if reload_status:
                if reload.get_reload():
                    ammo[current_weapon][0] = ammo_capacity[current_weapon]
                    ammo[current_weapon][1] = ammo[current_weapon][1] - 1
                    reload_status = False
        
        
            if speed_status: 
                speed_timer += 1
            if double_status:         
                damage_timer += 1
            if invincible_status:         
                invincible_timer += 1
        
            if speed_timer == 800:  # Was 450
                player.reset_speed()
            if damage_timer == 800:  # Was 450
                double_status = False
            if invincible_timer == 800:  # Was 450
                invincible_status = False
    
            # Update score, wave number, and remaining zombies display
            wave_text.set_variable(0, str(score))
            wave_text.set_variable(1, str(wave_num))
            wave_text.set_variable(2, str(len(zombieGroup)))
        
            health.set_status(player_status[0][0])
            armour.set_status(player_status[1][0])
        
            health_text.set_variable(0, str(player_status[0][0]))
            armour_text.set_variable(0, str(player_status[1][0]))
        
        
            index = 0
            for i in range(5):
                for n in range(2):
                    ammo_text.set_variable(index, str(ammo[i][n]))
                    index += 1
        
            for zombie in zombieGroup:
                zombie.rotate(player.rect.center)
                zombie.set_step_amount(player.rect.center)
        
            if len(zombieGroup) == 0:
                wave_num += 1
                # Spawn new zombies for the next wave
                enemy_count = 10 + (wave_num - 1) * 5
                zombie_types = [0] * (enemy_count // 2) + [1, 2, 3, 4] * (enemy_count // 8)
                random.shuffle(zombie_types)

                for zombie_type in zombie_types:
                    zombie = sprite_module.Zombie(screen, 
                                                  z_info[zombie_type][0], 
                                                  z_info[zombie_type][1], 
                                                  z_info[zombie_type][2], 
                                                  z_info[zombie_type][3], 
                                                  z_info[zombie_type][4], 
                                                  z_img[zombie_type], 
                                                  zombie_type, 
                                                  player.rect.center)
                    zombieGroup.add(zombie)

                allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, powerupGroup, reloading, health, armour, health_text, armour_text, wave_text, gold_text, ammo_text, score_text)
        
            if player_status[0][0] <= 0:
                print("Game Over triggered!")
                pygame.mixer.music.stop()
                game_over_screen(screen, lambda: boss_mode(screen))
                return

            score_text.set_variable(0, str(score))  # Update score display

            screen.blit(background, (0, 0))
            allSprites.update()
            allSprites.draw(screen)
         
            pygame.display.flip()
     
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
     
    pygame.quit()    
     
         
main()