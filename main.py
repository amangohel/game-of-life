import numpy as np
import random


class GameOfLife:

    def __init__(self, m, iterations, preset_value):
        """
        Constructor for the game of life. This takes in the following arguments
        :param m: size of the matrix, if m = 3 then the matrix will be 3x3
        :param iterations: number of iterations the game will play
        :param preset_value: preset value for one of three preset matrix's. Inputs are block, blinker and beacon.
              If this field is empty, a randomly generated matrix of size m*m will be created with random.
        input of live and dead cells.
        """

        # Number of iterations the game makes.
        self.iterations = iterations
        # The number of rows and columns that need to be created.
        self.m = m
        # Generates the universe grid
        # NB - numpy.zeros creates a 2dim array filled with 0's that are easily resizable
        self.old_universe = np.zeros(self.m * self.m, dtype='i').reshape(self.m, self.m)
        self.new_universe = np.zeros(self.m * self.m, dtype='i').reshape(self.m, self.m)

        # Presets for game of life
        # These are some preset conditions that I found on Wikipedia for testing, you can specify random behaviour
        # or one of the following three.
        if preset_value:
            # glider preset for game of life.
            if preset_value == "glider":
                block = [[0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 1, 0, 0, 0],
                         [0, 0, 1, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0]]
                self.old_universe[0:self.m, 0:self.m] = block
            # Blinker seed for game of life.
            elif preset_value == "blinker":

                blinker = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
                self.old_universe[0:self.m, 0:self.m] = blinker
            # Beacon seed for game of life.
            elif preset_value == "beacon":
                beacon = [[0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 1, 1, 0, 0, 0, 0, 0],
                          [0, 1, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 1, 0, 0, 0],
                          [0, 0, 0, 1, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0]]
                self.old_universe[0:self.m, 0:self.m] = beacon
        else:
            # hit the case where a preset is not defined and random behaviour is selected.
            random_configuration = []
            # # Iterates every column and row, filling each one with either
            # one or zero
            for x in range(self.m):
                random_configuration.append([])
                for y in range(self.m):
                    random_configuration[x].append(self.generate_random_number())

            self.old_universe[0:self.m, 0:self.m] = random_configuration

    def play_game_of_life(self):
        """
        Plays the game of life. Here, depending on the configuration of the cells, different rules will be applied.
        The scenarios for the game are as follows:
        Scenario 0: No interactions
        Given a game of life
        When there are no live cells
        Then on the next step there are still no live cells
    Scenario 1: Underpopulation
        Given a game of life
        When a live cell has fewer than two neighbours
        Then this cell dies
    Scenario 2: Overcrowding
        Given a game of life
        When a live cell has more than three neighbours
        Then this cell dies
    Scenario 3: Survival
        Given a game of life
        When a live cell has two or three neighbours
        Then this cell stays alive
    Scenario 4: Creation of Life
        Given a game of life
        When an empty position has exactly three neighbouring cells
        Then a cell is created in this position
    When applied these scenarios result in the following:
    Scenario 5: Grid with no live cells
        Given a game of life with the initial state containing no live cells
        When the game evolves one turn
        Then the next state also contains no live cells

        """

        iterations = 0


        #Loop that iterates over the matrix, comparing neighbours of the selected cell
        #and applies the relevant rule.
        while iterations < self.iterations:
            for i in range(self.m):
                for j in range(self.m):
                    live_neigbours = self.get_live_count(i, j)
                    #Scenarios
                    #Below are the scenarios/rules that apply to the game of life.
                    #Check for a point
                    if self.old_universe[i][j]:
                        # No interaction
                        if live_neigbours == 0:
                            self.new_universe[i][j] = 0
                        # Underpopulation and overcrowding
                        if live_neigbours < 2 or live_neigbours > 3:
                            self.new_universe[i][j] = 0
                        else:
                            self.new_universe[i][j] = self.old_universe[i][j]
                    else:
                        # creation of life when exactly three neighbours
                        if live_neigbours == 3:
                            self.new_universe[i][j] = 1

            # Sets the old configuration to the new one, snapshotting it
            # for the next iteration.
            self.old_universe = self.new_universe.copy()
            print(self.old_universe)
            #Outputs the current configuration to the terminal

            iterations += 1

    def generate_random_number(self):
        """
        Generates a random number between 1 or 0, used in the case when a preset isn't specified.
        :return: a random number between 1 or 0.
        """
        return random.randint(0, 1)

    # returns the amount of live cells within the grid
    def get_live_count(self, i, j):
        """
        Gets the live count of neighbours around the specified cell in the matrix.
        Here I am looking at the neighours of individual cells to see which are dead or alive.
        If a cell is alive, I increment the count to indicate that the cell has a live neighbour.

        :param i: i - 1, i, i + 1 indicates checking across the row, so if we have 1, 0, 1
        then i - 1 = 1, i = 0, i + 1 = 1.
        :param j: j - 1, j, j + 1 indicates checking up and down a column for the selected cell. so if we have:

        1 = j - 1
        0 = j
        1 = j + 1

        adjacent neighbours are also considered.

        :return: the total count of all neighbours in the matrix.
        """
        # Total count of the neighbours
        count = 0
        for n in [i - 1, i, i + 1]:
            for k in [j - 1, j, j + 1]:
                # skip over the current point as I'm checking its neighours, not the point itself.
                if (n == i and k == j):
                    continue
                #Progressively check each index's neighbour in the row
                if (n != self.m and k != self.m):
                    count += self.old_universe[n][k]
                else:
                    count -= self.old_universe[0][0]
        return count


if (__name__ == "__main__"):
    game = GameOfLife(m=8, iterations=100, preset_value="blinker")
    game.play_game_of_life()
