import plotly.graph_objs as go
import numpy as np
from datetime import timedelta
from classes import Orbit


def design_maket(fig: go, r_apofocus: float):
    # Обновляем макет
    fig.update_layout(
        template="plotly_dark",
        title="На каждом шаге отображаем 12-ую орбиту",
        updatemenus=[
            dict(
                direction="left",
                pad={"r": 10, "t": 80},
                x=0.1,
                xanchor="right",
                y=0,
                yanchor="top",
                showactive=False,
                type="buttons",
                buttons=[
                    dict(label="►", method="animate", args=[None, {"fromcurrent": True}]),
                    dict(label="❚❚", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False},
                                                                      "mode": "immediate",
                                                                      "transition": {"duration": 0}}])
                ]
            )
        ],
    )
    fig.update_layout(scene=dict(aspectmode="data"))
    fig.update_layout(scene_aspectmode='cube')
    fig.update_layout(scene=dict(xaxis=dict(title='X'), yaxis=dict(title='Y'), zaxis=dict(title='Z')))
    fig.update_layout(
        scene=dict(xaxis=dict(range=[-r_apofocus, r_apofocus]), yaxis=dict(range=[-r_apofocus, r_apofocus]),
                   zaxis=dict(range=[-r_apofocus, r_apofocus])))


def static_3d_fig(orbit: Orbit) -> list:
    r_apofocus = 1.05 * orbit.result_a[0] * (1 + orbit.result_e[0])

    # Добавляем сферу, представляющую Землю
    r_earth = 6371 * 1000
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_earth = r_earth * np.outer(np.cos(u), np.sin(v))
    y_earth = r_earth * np.outer(np.sin(u), np.sin(v))
    z_earth = r_earth * np.outer(np.ones(np.size(u)), np.cos(v))
    sphere_color = np.full_like(x_earth, 0.8)  # Задаем цвета сферы (голубой)
    earth_trace_surface = go.Surface(visible=True,
                                     x=x_earth,
                                     y=y_earth,
                                     z=z_earth,
                                     opacity=0.5,
                                     surfacecolor=sphere_color,
                                     colorscale='blues',  # Можно использовать другие цветовые градиенты
                                     name='Земля',
                                     showscale=False)

    # Добавляем нулевой меридиан
    zero_meridian = go.Scatter3d(visible=True,
                                 x=r_earth * np.cos(u),
                                 y=np.zeros(100),
                                 z=r_earth * np.sin(u),
                                 mode='lines',
                                 line=dict(width=2),
                                 name='Нулевой меридиан')

    # Добавляем плоскость экватора
    xx, yy = np.meshgrid(np.linspace(-r_apofocus, r_apofocus, 10), np.linspace(-r_apofocus, r_apofocus, 10))
    zz = np.zeros(xx.shape)
    plane_trace = go.Surface(visible=True,
                             x=xx,
                             y=yy,
                             z=zz,
                             opacity=0.3,
                             name='Плоскость экватора',
                             colorscale='Viridis',
                             showscale=False)

    # Добавляем точку старта
    start_point_trace = go.Scatter3d(visible=True,
                                     x=[orbit.result_x[0]],
                                     y=[orbit.result_y[0]],
                                     z=[orbit.result_z[0]],
                                     mode='markers',
                                     marker=dict(size=2),
                                     name='Точка старта')

    return [earth_trace_surface, start_point_trace, zero_meridian, plane_trace]


def make_list_coords_orbits(orbit: Orbit) -> list:
    # Находим индексы, где значение становится меньше предыдущего
    end_of_circle_indices = np.where(orbit.result_nu < np.roll(orbit.result_nu, 1))[0]
    list_coords_orbits = []
    for i in range(0, len(end_of_circle_indices), 12):
        list_coords_orbits.append({"x": orbit.result_x[end_of_circle_indices[i]: end_of_circle_indices[i + 1]],
                                   "y": orbit.result_y[end_of_circle_indices[i]: end_of_circle_indices[i + 1]],
                                   "z": orbit.result_z[end_of_circle_indices[i]: end_of_circle_indices[i + 1]],
                                   "t_start": orbit.gravity.start_datetime + timedelta(
                                       seconds=orbit.result_t[end_of_circle_indices[i]]),
                                   "t_end": orbit.gravity.start_datetime + timedelta(
                                       seconds=orbit.result_t[end_of_circle_indices[i+1]])})
    return list_coords_orbits


def orbit_plot_plotly(orbit: Orbit, where_save: str):
    # Создаем графики
    static_figs = static_3d_fig(orbit=orbit)
    list_coords_orbits = make_list_coords_orbits(orbit=orbit)

    list_objects_for_frames = []  # список объектов которые будут меняться
    orbit_trace_list = []  # это последний кадр

    for i, coords_orbit in enumerate(list_coords_orbits):
        # костыль, который решает вывод больше 4 фигур в кадре
        trick_point_trace = go.Scatter3d(visible=False,
                                         x=[coords_orbit["x"][0]],
                                         y=[coords_orbit["y"][0]],
                                         z=[coords_orbit["z"][0]])
        static_figs.append(trick_point_trace)

        # Добавляем орбиту на i кадр
        orbit_trace = go.Scatter3d(visible=True,
                                   x=coords_orbit["x"],
                                   y=coords_orbit["y"],
                                   z=coords_orbit["z"],
                                   mode='lines',
                                   line=dict(width=5),
                                   name=f'Орбита {12*i+1}: {coords_orbit["t_start"]} - {coords_orbit["t_end"]}')
        orbit_trace_list.append(orbit_trace)
        list_objects_for_frames.append([orbit_trace, static_figs[0], static_figs[1], static_figs[2], static_figs[3]])

    # последний кадр добавляем
    orbit_trace_list.append(static_figs[0])
    orbit_trace_list.append(static_figs[1])
    list_objects_for_frames.append(orbit_trace_list)

    # Создаем начальный график
    fig = go.Figure(data=static_figs)

    frames = []
    steps = []
    for i in range(len(list_objects_for_frames)):
        # Создаем кадры для анимации
        frames.append(go.Frame(name=str(i),
                               data=list_objects_for_frames[i]))
        # Создаем шаги для анимации
        if i == 0:
            step = dict(label="start", method="animate", args=[[str(i)]])
        elif i == len(list_objects_for_frames) - 1:
            step = dict(label="end", method="animate", args=[[str(i)]])
        else:
            step = dict(label=str(i), method="animate", args=[[str(i)]])
        steps.append(step)

    # Создаем слайдер
    sliders = [dict(currentvalue={"prefix": "Шаг: ", "font": {"size": 20}},
                    len=0.9,
                    x=0.1,
                    pad={"b": 10, "t": 50},
                    steps=steps,
                    )]

    # Обновляем макет
    r_apofocus = 1.05 * orbit.result_a[0] * (1 + orbit.result_e[0])
    design_maket(fig=fig, r_apofocus=r_apofocus)

    # Устанавливаем слайдер
    fig.layout.sliders = sliders
    fig.frames = frames

    # Показываем график
    if where_save == "days_14":
        fig.write_html("result/days_14/3d_plot.html")
    elif where_save == "other":
        fig.write_html("result/other/3d_plot.html")




