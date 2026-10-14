#Estimativa de altura de árvores utilizando LiDAR e Machine Learning.

import laspy
import numpy as np

las = laspy.read("C:/Users/Davy/Desktop/Projetos programação/exposicao de cursos/las_3d_recortado.las")

def leitura_de_dados(las):
    print(np.unique(las.classification))
    print("Número de pontos:", len(las.points))

#coleta de dados max e min de XYZ
    x = np.array(las.x)
    max_x = (np.max(x))
    min_x = (np.min(x))

    y = np.array(las.y)
    max_y = (np.max(y))
    min_y = (np.min(y))

    z = np.array(las.z)
    max_z = (np.max(z))
    min_z = (np.min(z))

    return x, y, z

#DTM modelo de terreno

def pontos_prox_0(las):
    x, y, z = leitura_de_dados(las)

    pontos = z < 1

    x_solo = x[pontos]
    y_solo = y[pontos]
    z_solo = z[pontos]

    return x_solo, y_solo, z_solo

def celulas_1x1(las):
#parte responsável por separar essa nuvem de pontos em 1x1m
    x_solo, y_solo, z_solo = pontos_prox_0(las)

    x_celula = np.floor(x_solo)
    y_celula = np.floor(y_solo)

    celulas = np.column_stack((x_celula, y_celula))

    celulas_unicas = np.unique(celulas, axis=0)

#Menor células de 1x1m:

#Classificação do Terreno e normalização:
    #0 m     --> terreno
    #0–1 m   --> vegetação baixa
    #1–5 m   --> vegetação
    #5–15 m  --> copa
    #15+ m   --> partes superiores das árvores

    z_min = []

    x, y, z = leitura_de_dados(las)

    x_celula_todos = np.floor(x)
    y_celula_todos = np.floor(y)

    for valores in celulas_unicas:
        pontos_valor = (x_celula == valores[0]) & (y_celula == valores[1])

        menor_z = np.min(z_solo[pontos_valor])

        z_min.append(menor_z)

        pontos = (x_celula_todos == valores[0]) & (y_celula_todos == valores[1])

        z_celula = z[pontos]

        z_relativo = z_celula - menor_z

        vegetacao_relativa = z_relativo > 1

        menor_z = np.min(z_solo[pontos_valor])

        z_min.append(menor_z)

        x_vegetacao_relativa = x[pontos][vegetacao_relativa]
        y_vegetacao_relativa = y[pontos][vegetacao_relativa]
        z_vegetacao_relativa = z_relativo[vegetacao_relativa]

    z_min = np.array(z_min)

    for valores in celulas_unicas:

        pontos_solo = (x_celula == valores[0]) & (y_celula == valores[1])

        menor_z = np.min(z_solo[pontos_solo])

        pontos = (x_celula_todos == valores[0]) & (y_celula_todos == valores[1])

        z_celula = z[pontos]

        z_relativo = z_celula - menor_z

        vegetacao = z_relativo > 1

        z_vegetacao = z_relativo[vegetacao]

        if len(z_vegetacao) > 0:

            altura = np.max(z_vegetacao)

    # Selecionar a árvore e gera a altura da árvore:

    x_centro = 577688
    y_centro = 9120457
    raio = 2

    distancia = np.sqrt(
        (x - x_centro) ** 2 +
        (y - y_centro) ** 2
    )

    pontos_arvore = distancia <= raio

    z_arvore = z[pontos_arvore]

    if len(z_arvore) > 0:

        altura = np.max(z_arvore)

        return round(altura, 2)