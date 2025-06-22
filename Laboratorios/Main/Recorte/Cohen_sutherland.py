
def aplicar_recorte_cohen(p1, p2, xmin, xmax, ymin, ymax, logCallback):
    x1, y1 = p1
    x2, y2 = p2
    
    # Codificando p1:
    bit1 = 1 if y1 > ymax else 0  # Bit 1: Acima (0001)
    bit2 = 1 if y1 < ymin else 0  # Bit 2: Abaixo (0010)
    bit3 = 1 if x1 > xmax else 0  # Bit 3: Direita (0100)
    bit4 = 1 if x1 < xmin else 0  # Bit 4: Esquerda (1000)

    code1_list = [bit1, bit2, bit3, bit4] 
    
    # Codificando p2:
    p2_bit1 = 1 if y2 > ymax else 0
    p2_bit2 = 1 if y2 < ymin else 0
    p2_bit3 = 1 if x2 > xmax else 0
    p2_bit4 = 1 if x2 < xmin else 0
    
    code2_list = [p2_bit1, p2_bit2, p2_bit3, p2_bit4]

    # 1. Aceita se os pontos estão dentro da janela (todos os bits 0)
    if all(b == 0 for b in code1_list) and all(b == 0 for b in code2_list):
        return (x1, y1), (x2, y2)

    # 2. Rejeita se os pontos estão no mesmo lado de uma borda externa
    if any(code1_list[i] == 1 and code2_list[i] == 1 for i in range(4)):
        logCallback("Linha trivialmente rejeitada. Fora da janela.")
        return None

    # 3. Recorte Necessário: A linha cruza a janela.
    
    # Define qual ponto está fora e será recortado nesta iteração
    p1_is_out = any(b == 1 for b in code1_list) 
    
    # Coordenadas do novo ponto de intersecção
    new_x, new_y = 0.0, 0.0

    # Para evitar divisão por zero
    dx = x2 - x1
    dy = y2 - y1

    # --- Lógica de Recorte: Prioriza uma borda por vez ---
    # Decidir qual ponto (p1 ou p2) está fora e usar seus bits para o recorte

    # Se P1 está fora:
    if p1_is_out:
        # Recorte ACIMA (bit 1 de P1)
        if code1_list[0] == 1:
            logCallback(f"Recorte acima ymax={ymax}")
            if dy != 0: 
                t = (ymax - y1) / dy
            
            new_x = x1 + t * dx
            new_y = ymax
            x1, y1 = new_x, new_y # Atualiza P1
        
        # Recorte ABAIXO (bit 2 de P1)
        elif code1_list[1] == 1:
            logCallback(f"Recorte abaixo ymin={ymin})")
            if dy != 0: 
                t = (ymin - y1) / dy
            
            new_x = x1 + t * dx
            new_y = ymin
            x1, y1 = new_x, new_y # Atualiza P1

        # Recorte DIREITA (bit 3 de P1)
        elif code1_list[2] == 1:
            logCallback(f"Recorte a direita xmax={xmax})")
            if dx != 0: 
                t = (xmax - x1) / dx
            
            new_x = xmax
            new_y = y1 + t * dy
            x1, y1 = new_x, new_y # Atualiza P1

        # Recorte ESQUERDA (bit 4 de P1)
        elif code1_list[3] == 1:
            logCallback(f"Recorte a esquerda xmin={xmin})")
            if dx != 0: 
                t = (xmin - x1) / dx
            
            new_x = xmin
            new_y = y1 + t * dy
            x1, y1 = new_x, new_y # Atualiza P1
                
    # Se P2 está fora (e P1 não estava fora, ou P1 já foi recortado e agora está dentro):
    else: # p2_is_out é True
        # Recorte ACIMA (bit 1 de P2)
        if code2_list[0] == 1:
            logCallback(f"Recorte acima ymax={ymax}")
            if dy != 0: 
                t = (ymax - y1) / dy
            
            new_x = x1 + t * dx
            new_y = ymax
            x2, y2 = new_x, new_y # Atualiza P2
        
        # Recorte ABAIXO (bit 2 de P2)
        elif code2_list[1] == 1:
            logCallback(f"Recorte abaixo ymin={ymin})")
            if dy != 0: 
                t = (ymin - y1) / dy
            
            new_x = x1 + t * dx
            new_y = ymin
            x2, y2 = new_x, new_y # Atualiza P2

        # Recorte DIREITA (bit 3 de P2)
        elif code2_list[2] == 1:
            logCallback(f"Recorte a direita xmax={xmax})")
            if dx != 0: 
                t = (xmax - x1) / dx
            
            new_x = xmax
            new_y = y1 + t * dy
            x2, y2 = new_x, new_y # Atualiza P2

        # Recorte ESQUERDA (bit 4 de P2)
        elif code2_list[3] == 1:
            logCallback(f"Recorte a esquerda xmin={xmin})")
            if dx != 0: 
                t = (xmin - x1) / dx
            
            new_x = xmin
            new_y = y1 + t * dy
            x2, y2 = new_x, new_y # Atualiza P2
                
    
    # --- Chamada Recursiva: continua chamando recorte até ser aceito (sem pontos fora) ---
    # Retorna o resultado da próxima chamada recursiva.
    return aplicar_recorte_cohen((x1, y1), (x2, y2), xmin, xmax, ymin, ymax, logCallback)