import cv2
import numpy as np

# Armazenamento dos pontos
v_points = []
w_points = []

# Controle de estado
current_image = 0  # 0 = imagem inicial (v), 1 = imagem final (w)
awaiting_click = True

def click_event(event, x, y, flags, params):
    global current_image, v_points, w_points, awaiting_click

    if event == cv2.EVENT_LBUTTONDOWN and awaiting_click:
        if current_image == 0:
            v_points.append((x, y))
            print(f"[{len(v_points)}] Ponto v (imagem inicial): {x}, {y}")
            cv2.circle(params['img'], (x, y), 3, (0, 255, 0), -1)
        else:
            w_points.append((x, y))
            print(f"[{len(w_points)}] Ponto w (imagem final): {x}, {y}")
            cv2.circle(params['img'], (x, y), 3, (0, 0, 255), -1)

        cv2.imshow(params['win_name'], params['img'])
        current_image = (current_image + 1) % 2  # alterna
        awaiting_click = False  # desativa clique até ENTER

def marcar_pontos_sincronizado(img0_path, img1_path):
    global current_image, awaiting_click

    img0 = cv2.imread(img0_path)
    img1 = cv2.imread(img1_path)
    img0_clone = img0.copy()
    img1_clone = img1.copy()

    cv2.namedWindow("Imagem Inicial (v)")
    cv2.namedWindow("Imagem Final (w)")

    cv2.setMouseCallback("Imagem Inicial (v)", click_event, {'img': img0_clone, 'win_name': "Imagem Inicial (v)"})
    cv2.setMouseCallback("Imagem Final (w)", click_event, {'img': img1_clone, 'win_name': "Imagem Final (w)"})

    print("Clique alternadamente: primeiro na imagem inicial, depois na final.")
    print("Pressione ENTER após cada clique. ESC para sair e salvar.")

    while True:
        cv2.imshow("Imagem Inicial (v)", img0_clone)
        cv2.imshow("Imagem Final (w)", img1_clone)

        key = cv2.waitKey(0)

        if key == 27:  # ESC
            break
        elif key == 13:  # ENTER
            awaiting_click = True  # permite novo clique

    cv2.destroyAllWindows()

    # Salvar os pontos
    v_np = np.array(v_points, dtype=np.float32)
    w_np = np.array(w_points, dtype=np.float32)
    np.save("v_pontos.npy", v_np)
    np.save("w_pontos.npy", w_np)
    print(f"\n{len(v_np)} pares de pontos salvos como 'v_pontos.npy' e 'w_pontos.npy'.")

if __name__ == "__main__":
    marcar_pontos_sincronizado("./imagens/jessica-alba1.pgm", "./imagens/jessica-alba2.pgm")