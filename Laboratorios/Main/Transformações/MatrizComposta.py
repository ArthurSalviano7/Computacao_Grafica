import numpy as np

from Transformações import ReflexaoQualquer
from Transformações import Rotacao
from Transformações import Translacao
from Transformações import Escala
from Transformações import Cisalhamento
from Transformações import Reflexao

def apply_composite_matrix(cube_points_list, compose_list, tx, ty, tz, log_callback):
    # Construir a lista temporária de composição levando em conta translação para origem se necessario
    full_compose_list = []

    log_callback(f"\nLista de Transformações:")

    # Se fora da origem, colocar translacao inicial na lista
    if tx or ty or tz:
        log_callback(f"> Translação para origem (Tx={tx}, Ty={ty}, Tz={tz})") #log_callback para enviar as mensagens para o usuário
        full_compose_list.append(["Translacao", tx, ty, tz])
    
    # Adicionar transformacoes do usuario
    full_compose_list.extend(compose_list)
    
    for transformacao in full_compose_list:
        log_callback(f">{transformacao}")

    # Se o cubo não estava na origem, adicionar translação de volta no final
    if tx or ty or tz:
        full_compose_list.append(["Translacao", -tx, -ty, -tz])
        log_callback(f"> Transladar de volta (Tx={-tx}, Ty={-ty}, Tz={-tz})")

    # Chama a função para criar matriz M composta e depois aplicar ponto a ponto
    compose_Matrix = build_composite_matrix(full_compose_list)

    # Realiza a transformação um ponto por vez e retorna a lista de pontos transformada
    for i in range(len(cube_points_list)):
        cube_points_list[i] = transf_point3D(cube_points_list[i], compose_Matrix) 

    return [cube_points_list, compose_Matrix]

def transf_point3D(point, compose_Matrix):
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [point[2]], [point[3]]]) # (x, y, z, 1)

    # Aplicando a transformação no vetor coluna (x, y, z, 1)
    vetor_point_transf = np.dot(compose_Matrix, point_vector)
    
    return [vetor_point_transf[0][0], vetor_point_transf[1][0], vetor_point_transf[2][0], vetor_point_transf[3][0]] 

def build_composite_matrix(compose_list):
    """ Exemplo da lista:
        compose_list:[["Escala", 2.0, 1.0, 1.0],
                     ["Translacao", 1.0, 20, 1],
                     ["Rx", 35.0],
                     ["RefXY"],
                     ["Cisalhamento", 1.0, 2.0, 'CisXY']]
    """
    composite_matrix_M = np.identity(4, dtype=float) # Cria a matriz identidade M

    for transform_info in compose_list:
        transf_type = transform_info[0]
        params = transform_info[1:] # pega os parametros

        # Cria matriz de transformacao atual (Muda dependendo da transformacao)
        current_matrix_T = np.identity(4, dtype=float) 

        if transf_type == "Escala":
            sx, sy, sz = params
            current_matrix_T = Escala.get_scale_Matrix3D(sx, sy, sz)
        elif transf_type == "Translacao":
            tx, ty, tz = params
            current_matrix_T = Translacao.get_translate_Matrix3D(tx, ty, tz)
        elif transf_type in ["Rx", "Ry", "Rz"]:
            angle = params[0] # Ângulo é o primeiro parâmetro
            if transf_type == "Rx":
                current_matrix_T = Rotacao.get_RotateX_Matrix3D(angle)
            elif transf_type == "Ry":
                current_matrix_T = Rotacao.get_RotateY_Matrix3D(angle)
            elif transf_type == "Rz":
                current_matrix_T = Rotacao.get_RotateZ_Matrix3D(angle)
        elif transf_type == "RefXY":
            current_matrix_T = Reflexao.get_RefXY_Matrix3D()
        elif transf_type == "RefYZ":
            current_matrix_T = Reflexao.get_RefYZ_Matrix3D()
        elif transf_type == "RefXZ":
            current_matrix_T = Reflexao.get_RefXZ_Matrix3D()
        elif transf_type == "RefOrig":
            current_matrix_T = Reflexao.get_RefOrig_Matrix3D()
        elif transf_type == "Cisalhamento":
            # Cisalhamento tem 3 parâmetros: 
            a, b, cis_subtype = params
            if cis_subtype == 'CisXY': # Cisalhamento XY por Z
                current_matrix_T = Cisalhamento.get_CisXY_Matrix3D(a, b)
            elif cis_subtype == 'CisYZ': # Cisalhamento YZ por X
                current_matrix_T = Cisalhamento.get_CisYZ_Matrix3D(a, b)
            elif cis_subtype == 'CisXZ': # Cisalhamento XZ por Y
                current_matrix_T = Cisalhamento.get_CisXZ_Matrix3D(a, b)
        else:
            print(f"AVISO: Tipo de transformação desconhecido '{transf_type}'. Ignorando esta transformação.")
            continue # Pula se transformação for inválida
        
        # "@" multiplica matrizes: M' = T x M
        composite_matrix_M = current_matrix_T @ composite_matrix_M 

        # Multiplica a matriz de transformação atual pela matriz composta acumulada.
        # ordem de multiplicação é da direita para esquerda: 
        #   M_final = M_ultima_da_lista @ ... @ M_primeira_da_lista.
        # Na primeira iteração:
        # composite_matrix = T1 @ Identidade = T1
        #
        # Na segunda iteração:
        # composite_matrix = T2 @ T1
        #
        # Na terceira iteração (processando T3):
        # composite_matrix = T3 @ (T2 @ T1) = T3 @ T2 @ T1
        
    return composite_matrix_M


def apply_composite_matrix2D(square_points_list, compose_list, tx, ty, log_callback):
    # Construir a lista temporária de composição levando em conta translação para origem se necessario
    full_compose_list = []

    log_callback(f"\nLista de Transformações:")

    # Se fora da origem, colocar translacao inicial na lista
    if tx or ty:
        log_callback(f"> Translação para origem (Tx={tx}, Ty={ty})") #log_callback para enviar as mensagens para o usuário
        full_compose_list.append(["Translacao", tx, ty])
    
    # Adicionar transformacoes do usuario
    full_compose_list.extend(compose_list)
    
    for transformacao in full_compose_list:
        log_callback(f">{transformacao}")

    # Se o cubo não estava na origem, adicionar translação de volta no final
    if tx or ty:
        full_compose_list.append(["Translacao", -tx, -ty])
        log_callback(f"> Transladar de volta (Tx={-tx}, Ty={-ty})")

    # Chama a função para criar matriz M composta e depois aplicar ponto a ponto
    compose_Matrix = build_composite_matrix2D(full_compose_list)

    # Realiza a transformação um ponto por vez e retorna a lista de pontos transformada
    for i in range(len(square_points_list)):
        square_points_list[i] = transf_point2D(square_points_list[i], compose_Matrix) 

    return [square_points_list, compose_Matrix]

def transf_point2D(point, compose_Matrix):
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [1]]) # (x, y, 1)
    print("POINT VECTOR: ", point_vector)
    # Aplicando a transformação no vetor coluna (x, y, 1)
    vetor_point_transf = np.dot(compose_Matrix, point_vector)
    
    return [vetor_point_transf[0][0], vetor_point_transf[1][0]] 

def build_composite_matrix2D(compose_list):
    """ Exemplo da lista:
        compose_list:[["Escala", 2.0, 1.0],
                     ["Translacao", 1.0, 20],
                     ["Rotacao", 35.0],
                     ["RefX"],
                     ["Cisalhamento", 1.0, 2.0]
    """
    composite_matrix_M = np.identity(3, dtype=float) # Cria a matriz identidade M

    for transform_info in compose_list:
        transf_type = transform_info[0]
        params = transform_info[1:] # pega os parametros

        # Cria matriz de transformacao atual (Muda dependendo da transformacao)
        current_matrix_T = np.identity(3, dtype=float) 

        if transf_type == "Escala":
            sx, sy = params
            current_matrix_T = Escala.get_scale_Matrix2D(sx, sy)
        elif transf_type == "Translacao":
            tx, ty = params
            current_matrix_T = Translacao.get_translate_Matrix2D(tx, ty)
        elif transf_type == "Rotacao":
            angle = params[0] # Ângulo é o primeiro parâmetro
            current_matrix_T = Rotacao.get_Rotate_Matrix2D(angle)
        elif transf_type == "RefX":
            current_matrix_T = Reflexao.get_RefX_Matrix2D()
        elif transf_type == "RefY":
            current_matrix_T = Reflexao.get_RefY_Matrix2D()
        elif transf_type == "Ref45":
            current_matrix_T = Reflexao.get_Ref45_Matrix2D()
        elif transf_type == "RefOrig":
            current_matrix_T = Reflexao.get_RefOrig_Matrix2D()
        elif transf_type == "RefAny":
            m, b = params
            current_matrix_T = ReflexaoQualquer.get_Ref_Any_Matrix2D(m, b)
        elif transf_type == "Cisalhamento":
            # Cisalhamento tem 3 parâmetros: 
            a, b = params
            current_matrix_T = Cisalhamento.get_Cis_Matrix2D(a, b)
        else:
            print(f"AVISO: Tipo de transformação desconhecido '{transf_type}'. Ignorando esta transformação.")
            continue # Pula se transformação for inválida
        
        # "@" multiplica matrizes: M' = T x M
        composite_matrix_M = current_matrix_T @ composite_matrix_M 

        # Multiplica a matriz de transformação atual pela matriz composta acumulada.
        # ordem de multiplicação é da direita para esquerda: 
        #   M_final = M_ultima_da_lista @ ... @ M_primeira_da_lista.
        # Na primeira iteração:
        # composite_matrix = T1 @ Identidade = T1
        #
        # Na segunda iteração:
        # composite_matrix = T2 @ T1
        #
        # Na terceira iteração (processando T3):
        # composite_matrix = T3 @ (T2 @ T1) = T3 @ T2 @ T1
        
    return composite_matrix_M




