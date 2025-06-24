import pygame
import numpy as np

def mandelbrot_set(width, height, max_iter, cx, cy, zoom):
    re = np.linspace(cx - width / (2 * zoom), cx + width / (2 * zoom), width)
    im = np.linspace(cy - height / (2 * zoom), cy + height / (2 * zoom), height)
    re, im = np.meshgrid(re, im)
    c = re + 1j * im

    z = np.zeros_like(c)
    div_iter = np.full(c.shape, max_iter, dtype=int)
    mask = np.full(c.shape, True, dtype=bool)

    for i in range(max_iter):
        z[mask] = z[mask] * z[mask] + c[mask]
        escaped = z.real*z.real + z.imag*z.imag > 4
        div_now = escaped & mask
        div_iter[div_now] = i
        mask &= ~escaped
        if not mask.any():
            break
        
    return div_iter

def draw(surface, width, height, max_iter, cx, cy, zoom):
    div_iter = mandelbrot_set(width, height, max_iter, cx, cy, zoom)
    colors = np.zeros((height, width, 3), dtype=np.uint8)

    mask = div_iter < max_iter
    colors[..., 0] = (div_iter % 8) * 32
    colors[..., 1] = (div_iter % 16) * 16
    colors[..., 2] = (div_iter % 32) * 8
    colors[~mask] = (0, 0, 0)

    pygame.surfarray.blit_array(surface, np.transpose(colors, (1, 0, 2)))

def main():
    width, height = 800, 600
    pygame.display.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mandelbrot Set Visualization")

    surface = pygame.Surface((width, height))

    cx, cy = -0.5, 0.0
    zoom = 200
    base_iter = 100

    clock = pygame.time.Clock()
    dragging = False
    drag_start_pos = (0, 0)
    drag_start_center = (cx, cy)

    redraw = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    drag_start_pos = event.pos
                    drag_start_center = (cx, cy)
                elif event.button == 4:
                    mouse_x, mouse_y = event.pos
                    mx = cx + (mouse_x - width / 2) / zoom
                    my = cy + (mouse_y - height / 2) / zoom
                    zoom *= 1.2
                    cx = mx - (mouse_x - width / 2) / zoom
                    cy = my - (mouse_y - height / 2) / zoom
                    redraw = True
                elif event.button == 5:
                    mouse_x, mouse_y = event.pos
                    mx = cx + (mouse_x - width / 2) / zoom
                    my = cy + (mouse_y - height / 2) / zoom
                    zoom /= 1.2
                    cx = mx - (mouse_x - width / 2) / zoom
                    cy = my - (mouse_y - height / 2) / zoom
                    redraw = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - drag_start_pos[0]
                dy = event.pos[1] - drag_start_pos[1]
                cx = drag_start_center[0] - dx / zoom
                cy = drag_start_center[1] - dy / zoom
                redraw = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if redraw:
            max_iter = int(base_iter + np.log(zoom) * 20)
            draw(surface, width, height, max_iter, cx, cy, zoom)
            screen.blit(surface, (0, 0))
            pygame.display.flip()
            redraw = False

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
