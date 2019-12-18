import numpy as np
import math
from transformations import interpolation


class resample:
    def resize(self, image, fx=None, fy=None, interpolation=None):
        """calls the appropriate funciton to resample an image based on the interpolation method
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        interpolation: method used for interpolation ('either bilinear or nearest_neighbor)
        returns a resized image based on the interpolation method
        """
        if interpolation == 'bilinear':
            return self.bilinear_interpolation(image, float(fx), float(fy))

        elif interpolation == 'nearest_neighbor':
            return self.nearest_neighbor(image, float(fx), float(fy))

        elif interpolation == 'bicubic':
            return self.bicubic_interpolation(image, float(fx), float(fy))

        elif interpolation == 'lanczos':
            return self.lanczos_interpolation(image, float(fx), float(fy))

    def nearest_neighbor(self, image, fx, fy):
        """resizes an image using nearest neighbor approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the nearest neighbor interpolation method
        """

        # Processing the size of the original and new image to be formed
        originalImageRows, originalImageColumns = image.shape
        newImageRows = round(originalImageRows*fx)
        newImageColumns = round(originalImageColumns*fy)

        # new Image with just zeros
        newImage = np.zeros((newImageRows, newImageColumns), np.uint8)
        # Scaling the newImage pixel's according to match the oldImage pixel values
        for newImageIndexRow in range(newImageRows):
            for newImageIndexColumn in range(newImageColumns):
                oldX = newImageIndexRow/fx
                oldY = newImageIndexColumn/fy
                oldX = math.floor(oldX)
                oldY = math.floor(oldY)
                newImage[newImageIndexRow, newImageIndexColumn] = image[oldX, oldY]

        return newImage

    def bilinear_interpolation(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the bilinear interpolation method
        Note: Do not write the code to perfrom interpolation between points in this file.
        There is a file named interpolation.py, and two function definitions are provided
        linear_interpolation: Write your code to perform linear interpolation between two in this function
        bilinear_interpolation: Write your code to perfrom bilinear interpolation using four points in this functions.
                                As bilinear interpolation essentially does linear interpolation three times,you could
                                simply call the linear_interpolation function three times, with the correct parameters.
        """

        # creating the interpolation object to call methods from the class interpolation
        interpolation_obj = interpolation()

        # Processing the size of the original and new image to be formed
        originalImageRows, originalImageColumns = image.shape
        newImageRows = int(originalImageRows*fx)
        newImageColumns = int(originalImageColumns*fy)
        newImage = np.zeros((newImageRows, newImageColumns), np.uint8)

        for newImageIndexRow in range(newImageRows):
            for newImageIndexColumn in range(newImageColumns):

                oldX = math.floor(newImageIndexRow/fx)
                oldY = math.floor(newImageIndexColumn/fy)

                # Index X and Y both are out of bounds in the original Image
                #   [i]|[ ]
                #   -------
                #   [ ]|[ ]
                if (oldX + 1 > originalImageRows - 1) and (oldY + 1 > originalImageColumns - 1):
                    pt1 = (oldX, oldY, image[oldX, oldY])
                    pt2 = (oldX, oldY+1, image[oldX, oldY])
                    pt3 = (oldX+1, oldY, image[oldX, oldY])
                    pt4 = (oldX+1, oldY+1, image[oldX, oldY])
                # Index X is out of bounds in the original Image
                #   [i][i]
                #   ------
                #   [ ][ ]
                elif oldX + 1 > originalImageRows - 1:
                    pt1 = (oldX, oldY, image[oldX, oldY])
                    pt2 = (oldX, oldY+1, image[oldX, oldY+1])
                    pt3 = (oldX+1, oldY, image[oldX, oldY])
                    pt4 = (oldX+1, oldY+1, image[oldX, oldY+1])
                # Index Y is out of bounds in the original Image
                #   [i]|[ ]
                #   [i]|[ ]
                elif oldY + 1 > originalImageColumns - 1:
                    pt1 = (oldX, oldY, image[oldX, oldY])
                    pt2 = (oldX, oldY+1, image[oldX, oldY])
                    pt3 = (oldX+1, oldY, image[oldX+1, oldY])
                    pt4 = (oldX+1, oldY+1, image[oldX+1, oldY])
                # Within the bounds
                #   [i][i]
                #   [i][i]
                else:
                    pt1 = (oldX, oldY, image[oldX, oldY])
                    pt2 = (oldX, oldY+1, image[oldX, oldY+1])
                    pt3 = (oldX+1, oldY, image[oldX+1, oldY])
                    pt4 = (oldX+1, oldY+1, image[oldX+1, oldY+1])

                unknown = (newImageIndexRow / fx, newImageIndexColumn / fy)

                newImage[newImageIndexRow, newImageIndexColumn] = interpolation_obj.bilinear_interpolation(
                    pt1, pt2, pt3, pt4, unknown)

        return newImage

    def lanczos_interpolation(self, image, fx, fy):
        n = 2
        x = image.shape[0]
        y = image.shape[1]

        def sinc(ang):
            if ang == 0:
                return 1
            else:
                return math.sin(math.pi*ang)/(math.pi*ang)

        def l(x, n):
            if abs(x) <= n:
                return sinc(x)*sinc(x/n)
            else:
                return 0

        new_x = fx * x
        new_y = fy * y
        r_ratio = new_x / x
        c_ratio = new_y / y
        new_x = int(new_x)
        new_y = int(new_y)
        new_image = np.zeros([new_x, new_y])
        nearest_row = np.array(range(x))
        nearest_col = np.array(range(y))

        nearest_row = nearest_row * r_ratio
        nearest_col = nearest_col * c_ratio

        nearest_row = np.ceil(nearest_row)
        nearest_col = np.ceil(nearest_col)
        for i in range(new_x):
            for j in range(new_y):
                w = 0
                sum = 0
                xi = np.abs(nearest_row - i).argmin()
                yi = np.abs(nearest_col - j).argmin()
                for i1 in range(-n+1, n):
                    for j1 in range(-n+1, n):
                        w = w + l(i1, n)*l(j1, n)

                for i1 in range(-n+1, n):
                    for j1 in range(-n+1, n):
                        sum = sum + image[xi, yi]*l(i1, n)*l(j1, n)

                if w != 0:
                    new_image[i, j] = sum/w
                else:
                    new_image[i, j] = 0

        return new_image
