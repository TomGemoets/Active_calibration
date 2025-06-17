import numpy as np
import subprocess

class GridTarget():
    def __init__(self,name):
        self.name = name
        #self.dot_grid_spacing = dot_grid_spacing

    # Define the grid of the calibration target
    def define_dotted_grid_target(self, name, dot_grid_size,dot_grid_spacing):
        """Create grid target from the grid size and the grid spacing

        Keyword arguments:
        dot_grid_size -- tuple of the number of dots (length, width)
        dot_grid_spacing -- spacing between each dot in mm

        Returns an array of all the positions in mm of the grids.
        """
        grid_target_points = np.zeros((self.dot_grid_size[0] * self.dot_grid_size[1], 3), np.float32)
        grid_target_points[:, :2] = np.mgrid[0: self.dot_grid_size[0], 0: self.dot_grid_size[1]].T.reshape(-1,
                                                                                                           2) * self.dot_grid_spacing
        return grid_target_points

class ActiveDottedGrid(GridTarget):
    def __init__(self, name,dot_grid_size, dot_grid_spacing, list_image):
        self.name = name
        self.dot_grid_size = dot_grid_size
        self.dot_grid_spacing = dot_grid_spacing
        self.list_image = list_image

    # Define the grid of the calibration target
    def define_dotted_grid_target(self):
        """Create grid target from the grid size and the grid spacing

        Keyword arguments:
        dot_grid_size -- tuple of the number of dots (length, width)
        dot_grid_spacing -- spacing between each dot in mm

        Returns an array of all the positions in mm of the grids.
        """
        grid_target_points = np.zeros((self.dot_grid_size[0] * self.dot_grid_size[1], 3), np.float32)
        grid_target_points[:, :2] = np.mgrid[0: self.dot_grid_size[0], 0: self.dot_grid_size[1]].T.reshape(-1,
                                                                                                           2) * self.dot_grid_spacing
        return grid_target_points

class ChessboardGrid(GridTarget):
    def __init__(self, name, columns, lines):
        self.name = name
        self.columns = columns
        self.lines = lines


    # Define the grid of the calibration target
    def define_chessboard_target(self):
        """Create grid target from the grid size and the grid spacing

        Keyword arguments:
        dot_grid_size -- tuple of the number of dots (length, width)
        dot_grid_spacing -- spacing between each dot in mm

        Returns an array of all the positions in mm of the grids.
        """

        # Génération du chessboard
        #col_chessboard, ligne_chessboard = dimensions_chessboard()
        cmd = [
            "python",
            "Module/calibration_grid_generation/gen_pattern.py",
            "-o", "chessboard.svg",
            "-r", str(self.lines),
            "-c", str(self.columns),
            "--type", "checkerboard",
            "-s", str(20)
        ]
        subprocess.run(cmd)



