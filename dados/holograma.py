#Gerar modelo 3d

import laspy
import numpy as np
import plotly.graph_objects as go

def modelo3d():
    las = laspy.read("C:/Users/Davy/Desktop/Projetos programação/exposicao de cursos/las_3d_recortado.las")

    x = np.array(las.x)
    y = np.array(las.y)
    z = np.array(las.z)

    indices = np.random.choice(len(x), 50000, replace=False)

    x = x[indices]
    y = y[indices]
    z = z[indices]
    
    #criação do holograma e configuração de cores

    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        marker=dict(
            size=1,
            color=z,
            colorscale="jet"
        )
    )])

    fig.show()