import main

def desenhar_reta_pm(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = (2 * dy) - dx #Valor inicial de d

    incE = 2 * dy #incremento de E
    incNE = 2 * (dy - dx)

    x = x1
    y = y1

    points = []
    points.append((round(x), round(y)))

    main.draw_pixel(round(x), round(y))

    while (x < x2):
        if d <= 0:
            #Escolhe E, incrementa 1 em x
            d += incE
            x += 1
        else:
            #Escolhe NE, incrementa 1 em x e y
            d += incNE
            x += 1
            y += 1
        
        points.append((round(x), round(y)))
        main.draw_pixel(round(x), round(y))
    
    return points