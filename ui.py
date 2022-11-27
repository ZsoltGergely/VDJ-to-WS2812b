import pygame
import pygame_gui


window_width = 200
window_height = 800

pygame.init()

pygame.display.set_caption('Light Controller')
window_surface = pygame.display.set_mode((window_width, window_height))

background = pygame.Surface((window_width, window_height))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((window_width, window_height))

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 50)),
                                            text='Say Hello',
                                            manager=manager)

clp_scroll = pygame_gui.elements.UIVerticalScrollBar(relative_rect=pygame.Rect((10, 100), (30, 160)),
                                        visible_percentage=0.2,
                                        manager=manager)

clp_scroll_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 70), (30, 30)),
                            text='CLP',
                            manager=manager)

spd_scroll = pygame_gui.elements.UIVerticalScrollBar(relative_rect=pygame.Rect((50, 100), (30, 160)),
                                        visible_percentage=0.2,
                                        manager=manager)

spd_scroll_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 70), (30, 30)),
                            text='SPD',
                            manager=manager)

frq_scroll = pygame_gui.elements.UIVerticalScrollBar(relative_rect=pygame.Rect((90, 100), (30, 160)),
                                        visible_percentage=0.2,
                                        manager=manager)

frq_scroll_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((90, 70), (30, 30)),
                            text='FRQ',
                            manager=manager)


mode_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=['Beat', 'BeatGrid'],
                                   starting_option='Beat',
                                   relative_rect=pygame.Rect((10, 300), (125, 50)),
                                   manager=manager)
mode_dropdown_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20, 270), (30, 30)),
                            text='MODE',
                            manager=manager)
                            

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print('FLASH!')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()