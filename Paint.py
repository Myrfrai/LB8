import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

active_color = 'white'
active_size = 0
painting = []
drawing_shape = None 
start_pos = None
eraser_mode = False

def draw_menu():
    pygame.draw.rect(screen, 'gray', [0, 0, 800, 100])
    pygame.draw.rect(screen, 'black', [0, 100, 800, 2])

    
    rectangle_tool = pygame.draw.rect(screen, 'black', [320, 20, 50, 50])
    pygame.draw.rect(screen, 'white', [330, 30, 30, 30], 2)

    circle_tool = pygame.draw.rect(screen, 'black', [380, 20, 50, 50])
    pygame.draw.circle(screen, 'white', (405, 45), 15, 2)
    
    
    xl_brush = pygame.draw.rect(screen, 'black', [20, 20, 50, 50])
    pygame.draw.circle(screen, 'white', (45, 45), 20)

    l_brush = pygame.draw.rect(screen, 'black', [80, 20, 50, 50])
    pygame.draw.circle(screen, 'white', (105, 45), 15)

    m_brush = pygame.draw.rect(screen, 'black', [140, 20, 50, 50])
    pygame.draw.circle(screen, 'white', (165, 45), 10)

    s_brush = pygame.draw.rect(screen, 'black', [200, 20, 50, 50])
    pygame.draw.circle(screen, 'white', (225, 45), 5)
    brush_list = [xl_brush, l_brush, m_brush, s_brush]


    red = pygame.draw.rect(screen, 'red', [760, 20, 25, 25])
    green = pygame.draw.rect(screen, 'green', [735, 20, 25, 25])
    blue = pygame.draw.rect(screen, 'blue', [760, 45, 25, 25])
    yellow = pygame.draw.rect(screen, 'yellow', [735, 45, 25, 25])
    purple = pygame.draw.rect(screen, 'purple', [710, 20, 25, 25])
    orange = pygame.draw.rect(screen, 'orange', [710, 45, 25, 25])
    white = pygame.draw.rect(screen, 'white', [685, 20, 25, 25])
    black = pygame.draw.rect(screen, 'black', [685, 45, 25, 25])
    
    eraser = pygame.draw.rect(screen, 'black', [440, 20, 50, 50])
    font = pygame.font.SysFont('Arial', 20)
    eraser_text = font.render('Er', True, 'white')
    screen.blit(eraser_text, (455, 30))
    
    color_list = [red, green, blue, yellow, purple, orange, white, black]
    rgb_list = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'white', 'black']

    return rectangle_tool, circle_tool, brush_list, color_list, rgb_list, eraser

def draw_painting(paints):
    for paint in paints:
        if paint[0] == 'rectangle':
            color, start, end, width = paint[1], paint[2], paint[3], paint[4]
            rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]), 
                             abs(end[0] - start[0]), abs(end[1] - start[1]))
            pygame.draw.rect(screen, color, rect, width)
        elif paint[0] == 'circle':
            color, center, radius, width = paint[1], paint[2], paint[3], paint[4]
            pygame.draw.circle(screen, color, center, radius, width)
        else:
            pygame.draw.circle(screen, paint[0], paint[1], paint[2])

done = True
fps = pygame.time.Clock()
while done:
    screen.fill("white")
    rectangle_tool, circle_tool, brushes, colors, rgbs, eraser = draw_menu()

    mouse = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    
    if left_click and mouse[1] > 100:
        if drawing_shape == 'rectangle':
            if start_pos is None:
                start_pos = mouse
        elif drawing_shape == 'circle':
            if start_pos is None:
                start_pos = mouse
        elif eraser_mode:
            painting.append(('white', mouse, active_size))
        else:
            painting.append((active_color, mouse, active_size))
    
    if not left_click and start_pos is not None:
        if drawing_shape == 'rectangle':
            painting.append(('rectangle', active_color, start_pos, mouse, active_size//5 + 1))
            start_pos = None
        elif drawing_shape == 'circle':
            radius = int(((mouse[0] - start_pos[0])**2 + (mouse[1] - start_pos[1])**2)**0.5)
            painting.append(('circle', active_color, start_pos, radius, active_size//5 + 1))
            start_pos = None
    
    draw_painting(painting)
    
    if left_click and start_pos is not None and mouse[1] > 100:
        if drawing_shape == 'rectangle':
            rect = pygame.Rect(min(start_pos[0], mouse[0]), min(start_pos[1], mouse[1]), 
                             abs(mouse[0] - start_pos[0]), abs(mouse[1] - start_pos[1]))
            pygame.draw.rect(screen, active_color, rect, active_size//5 + 1)
        elif drawing_shape == 'circle':
            radius = int(((mouse[0] - start_pos[0])**2 + (mouse[1] - start_pos[1])**2)**0.5)
            pygame.draw.circle(screen, active_color, start_pos, radius, active_size//5 + 1)
    
    if mouse[1] > 100 and not drawing_shape and not eraser_mode:
        pygame.draw.circle(screen, active_color, mouse, active_size)
    elif mouse[1] > 100 and eraser_mode:
        pygame.draw.circle(screen, 'white', mouse, active_size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rectangle_tool.collidepoint(event.pos):
                drawing_shape = 'rectangle'
                eraser_mode = False
            elif circle_tool.collidepoint(event.pos):
                drawing_shape = 'circle'
                eraser_mode = False
            elif eraser.collidepoint(event.pos):
                eraser_mode = True
                drawing_shape = None
            else:
                for i in range(len(brushes)):
                    if brushes[i].collidepoint(event.pos):
                        active_size = 20 - (i * 5)
                        drawing_shape = None
                        eraser_mode = False

                for i in range(len(colors)):
                    if colors[i].collidepoint(event.pos):
                        active_color = rgbs[i]
                        eraser_mode = False

    fps.tick(60)
    pygame.display.flip()

pygame.quit()