#! /usr/bin/env python3

import pygame
import numpy as np
from time import time

def draw_mandelbrot(surface, width, height, max_iter, cx, cy, zoom):
    re_vals = np.linspace(cx - width / (2 * zoom), cx + width / (2 * zoom), width)
    px = pygame.surfarray.pixels3d(surface)

    for y in range(height):
        im_val = cy + (y - height/2) / zoom
        c = re_vals + 1j * im_val
        z = np.zeros_like(c)
        div_iter = np.full(c.shape, max_iter, dtype=np.int32)
        mask = np.ones(c.shape, dtype=bool)
  
        for i in range(max_iter):
            z[mask] = z[mask] * z[mask] + c[mask]
            escaped = (z.real*z.real + z.imag*z.imag) > 4
            div_now = escaped & mask
            div_iter[div_now] = i
            mask &= ~escaped
            if not mask.any():
                break

        r = (div_iter % 8) * 32
        g = (div_iter % 16) * 16
        b = (div_iter % 32) * 8
        
        inside = div_iter >= max_iter
        r[inside] = g[inside] = b[inside] = 0
        
        px[:, y, 0] = r
        px[:, y, 1] = g
        px[:, y, 2] = b
        
        if y % 16 == 0:
            pygame.display.update(pygame.Rect(0, y, width, min(16, height - y)))

    pygame.display.update()
    del px


def main():
    width, height = 800, 600
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mandelbrot Interactive")
    cx, cy = -0.5, 0.0
    zoom = 200.0
    base_iter = 100

    dragging = False
    drag_start = (0, 0)
    center_start = (cx, cy)
    redraw = True
    clock = pygame.time.Clock()

    running = True
    last_time = time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    drag_start = event.pos
                    center_start = (cx, cy)
                elif event.button in (4, 5):
                    mx, my = event.pos
                    wx = cx + (mx - width/2)/zoom
                    wy = cy + (my - height/2)/zoom
                    factor = 1.2 if event.button == 4 else 1/1.2
                    zoom *= factor
                    cx = wx - (mx - width/2)/zoom
                    cy = wy - (my - height/2)/zoom
                    redraw = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - drag_start[0]
                dy = event.pos[1] - drag_start[1]
                cx = center_start[0] - dx/zoom
                cy = center_start[1] - dy/zoom
                redraw = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    cx, cy = -0.5, 0.0
                    zoom = 200.0
                    redraw = True
        if redraw and time() - last_time > 0.05:
            last_time = time()
            max_iter = int(base_iter + np.log(zoom) * 20)
            draw_mandelbrot(screen, width, height, max_iter, cx, cy, zoom)
            redraw = False

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
