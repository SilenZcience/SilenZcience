import os
import numpy as np
from PIL import Image

# [0] == RGBA_light, [1] == RGBA_dark
color_dead = [[255, 254, 254, 255], [20, 19, 33, 255]]
color_alive = [[65, 183, 130, 255], [216, 58, 125, 255]]
color_dying = [[40, 57, 74, 255], [247, 215, 71, 255]]

canvas_size = (420, 1200)  # height, width
cell_grid = (84, 240)

cell_size = [canvas_size[0]/cell_grid[0],
             canvas_size[1]/cell_grid[1]]
for i, size in enumerate(cell_size):
    if not size.is_integer():
        cell_size[i] += 1
    cell_size[i] = int(cell_size[i])+1

workingDir = os.path.abspath(os.path.join(__file__,  '..', '..'))
target_images = [os.path.join(workingDir, 'GameOfLifeBright.png'),
                 os.path.join(workingDir, 'GameOfLifeDark.png')]


def updateGame(cells):
    """Calculate the next cycle of cells, aswell
    as the cycle after that, to flag the cells,
    which are about to die."""
    nextArray = np.zeros(cell_grid, dtype=np.int8)

    for row, col in np.ndindex(cells.shape):
        num_alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]

        if (cells[row, col] in [1, 2] and 2 <= num_alive <= 3) or (cells[row, col] == 0 and num_alive == 3):
            nextArray[row, col] = 1

    cells = nextArray.copy()
    for row, col in np.ndindex(nextArray.shape):
        num_alive = np.sum(
            nextArray[row-1:row+2, col-1:col+2]) - nextArray[row, col]

        if nextArray[row, col] == 1 and num_alive < 2 or num_alive > 3:
            cells[row, col] = 2

    return cells


def generateImage(cells, dark):
    newArray = np.zeros([canvas_size[0], canvas_size[1], 4], dtype=np.int8)

    for row, col in np.ndindex(cells.shape):
        if cells[row, col] == 0:
            newArray[row * cell_size[0]:(row+1) * cell_size[0], col *
                     cell_size[1]:(col+1) * cell_size[1]] = color_dead[dark]
        elif cells[row, col] == 1:
            newArray[row * cell_size[0]:(row+1) * cell_size[0], col *
                     cell_size[1]:(col+1) * cell_size[1]] = color_alive[dark]
        elif cells[row, col] == 2:
            newArray[row * cell_size[0]:(row+1) * cell_size[0], col *
                     cell_size[1]:(col+1) * cell_size[1]] = color_dying[dark]

    return Image.fromarray(newArray.astype('uint8'))


def initRunningGame(imageFile, dark):
    image = Image.open(imageFile)
    currentColorArray = np.array(image)
    currentColorArray = currentColorArray[::cell_size[0], ::cell_size[1]]
    currentArray = np.zeros(
        [currentColorArray.shape[0], currentColorArray.shape[1]], dtype=np.int8)

    for row, col in np.ndindex(currentArray.shape):
        if np.array_equal(currentColorArray[row, col], color_dead[dark]):
            currentArray[row:(row+1), col:(col+1)] = 0
        elif np.array_equal(currentColorArray[row, col], color_alive[dark]):
            currentArray[row:(row+1), col:(col+1)] = 1
        elif np.array_equal(currentColorArray[row, col], color_dying[dark]):
            currentArray[row:(row+1), col:(col+1)] = 1

    return (currentArray, image)


def initNewGame():
    return np.random.randint(0, 2, cell_grid, dtype=np.int8)


def startNewGame(target_image, dark):
    cells = initNewGame()
    image = generateImage(cells, dark)
    image.save(target_image)


def main():
    for i, target_image in enumerate(target_images):
        if os.path.exists(target_image):
            cells, currentImage = initRunningGame(target_image, i)
            cells = updateGame(cells)
            image = generateImage(cells, i)
            if np.array_equal(currentImage, image):
                startNewGame(target_image, i)
            else:
                image.save(target_image)
        else:
            startNewGame(target_image, i)


if __name__ == '__main__':
    main()
