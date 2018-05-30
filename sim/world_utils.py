def milliseconds_convert(ms):
    s = ms / 1000
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return d, h, m, s


def addPlotingBuilding():
    import matplotlib.pyplot as plt
    from sim.world import World
    state = World().state

    f, subplots = plt.subplots(len(state.building.rooms), 3, sharex='all')
    xData = [0]
    subplotsData = []

    for i in range(len(subplots)):
        subplotsData.append([[0], [0], [0]])

    f.subplots_adjust(hspace=0.5)

    def animate():
        state = World().state

        # Add new timestep
        xData.append(xData[len(xData) - 1] + 1)

        # Add data to rooms
        for i in range(len(state.building.rooms)):
            subplots[i, 0].clear()
            subplotsData[i][0].append(state.building.rooms[i].temperature)
            subplots[i, 0].set_title(state.building.rooms[i].name)
            subplots[i, 0].set_ylabel('temperature')
            subplots[i, 0].plot(xData, subplotsData[i][0], color='red')

            subplots[i, 1].clear()
            subplotsData[i][1].append(sum(map(lambda light: 1 if light.state else 0, state.building.rooms[i].lights.values())))
            subplots[i, 1].set_title(state.building.rooms[i].name)
            subplots[i, 1].set_ylabel('light')
            subplots[i, 1].plot(xData, subplotsData[i][1], color='blue')

            subplots[i, 2].clear()
            subplotsData[i][2].append((state.building.rooms[i].hvac.summedPower + sum(map(lambda light: light.summedPower, state.building.rooms[i].lights.values())))/60)
            subplots[i, 2].set_title(state.building.rooms[i].name)
            subplots[i, 2].set_ylabel('power')
            subplots[i, 2].plot(xData, subplotsData[i][2], color='green')

        subplots[len(state.building.rooms) - 1, 0].set_xlabel('time')
        subplots[len(state.building.rooms) - 1, 1].set_xlabel('time')
        subplots[len(state.building.rooms) - 1, 2].set_xlabel('time')

        plt.draw()
        plt.pause(0.001)

    plt.draw()
    plt.show(block=False)
    return animate
