import unittest
import sys
from resizeable_image import ResizeableImage

class TestImage(unittest.TestCase):
    def test_small(self):
        self.image_test('16x16.png', 23147)

    # def test_large(self):
    #     self.image_test('sunset_full.png', 26010)

    def image_test(self, filename, expected_cost):
        image = ResizeableImage(filename)
        seam = image.best_seam()
        # print(seam)

        # Make sure the seam is of the appropriate length.
        self.assertEqual(image.height, len(seam), 'Seam wrong size.')

        # Make sure the pixels in the seam are properly connected.
        seam.sort(key=lambda x: x[1]) # Sort by height.
        for i in range(1, len(seam)):
            self.assertTrue(abs(seam[i][0]-seam[i-1][0]) <= 1, 'Not a proper seam.')
            self.assertEqual(i, seam[i][1], 'Not a proper seam.')

        # Make sure the energy of the seam matches what we expect.
        total = sum([image.energy(coord[0], coord[1]) for coord in seam])
        self.assertEqual(total, expected_cost)
            
if __name__ == '__main__':
    unittest.main(argv = sys.argv + ['--verbose'])


    # inverse i and j
    # def rec_best_seam(self, i, j):
    #     """ 
    #     Recursively finds the seam with the lowest seam energy and returns
    #     a tuple with the locations of pixels at i j
    #     i = rows or height, j = columns or width
    #     """
    #     # if at the last row of pixels in image
    #     if(i == self.height-1):
    #         return [(i,j)]
    #     else:
    #         # if j is in the first column of pixels
    #         if(j == 0):
    #             # no left
    #             middle = self.rec_best_seam(i+1, j)
    #             right = self.rec_best_seam(i+1, j+1)

    #             seams = [middle, right]

    #             seam_energies = [self.seam_energy(middle), self.seam_energy(right)]

    #         # if j is in the last column
    #         elif(j == self.width-1):
    #             left = self.rec_best_seam(i+1, j-1)
    #             middle = self.rec_best_seam(i+1, j)
    #             # no right

    #             seams = [left, middle]

    #             seam_energies = [self.seam_energy(left), self.seam_energy(middle)]

    #         # if i is in between
    #         else:
    #             left = self.rec_best_seam(i+1, j-1)
    #             middle = self.rec_best_seam(i+1, j)
    #             right = self.rec_best_seam(i+1, j+1)

    #             seams = [left, middle, right]

    #             seam_energies = [self.seam_energy(left), self.seam_energy(middle), self.seam_energy(right)]

    #     best_seam_index = seam_energies.index(min(seam_energies))

    #     best_seam = seams[best_seam_index]

    #     return [(i,j)] + best_seam



    # def rec_best_seam(self, i, j):
    #         """ 
    #         Recursively finds the seam with the lowest seam energy and returns
    #         a tuple with the locations of pixels at i j
    #         """
    #         # if at the last row of pixels in image
    #         print(i,j)
    #         if(j == 5):
    #             return (i,j)
    #             # print((i,j))
    #         else:
    #             # if i is in the first column of pixels
    #             if(i == 0):
    #                 return (i,j) + (self.rec_best_seam(i, j+1)) + (self.rec_best_seam(i+1, j+1))
    #             # if i is in the last column
    #             elif(i == self.width-1):
    #                 return (i,j) + (self.rec_best_seam(i-1, j+1)) + (self.rec_best_seam(i, j+1))
    #             # if i is in between
    #             else:
    #                 return (i,j) + (self.rec_best_seam(i-1, j+1)) + (self.rec_best_seam(i, j+1)) + (self.rec_best_seam(i+1, j+1))



    # def rec_best_seam(self, i, j):
    #     """ 
    #     Recursively finds the seam with the lowest seam energy and returns
    #     a tuple with the locations of pixels at i j
    #     """
    #     # if at the last row of pixels in image
    #     if(j == self.height-1):
    #         return (i,j)
    #     else:
    #         # if i is in the first column of pixels
    #         if(i == 0):
    #             temp = {(i,j+1):self.pixel_energies[i, j+1], \
    #                     (i+1, j+1):self.pixel_energies[i+1, j+1]}

    #             return (i,j) + self.rec_best_seam(min(self.pixel_energies[i, j+1], \
    #                 self.pixel_energies[i+1, j+1], key = lambda k: self.pixel_energies[k]))
    #         # if i is in the last column
    #         elif(i == self.width-1):
    #             return (i,j) + self.rec_best_seam(min(self.pixel_energies[i-1, j+1], \
    #                 self.pixel_energies[i, j+1], key = lambda k: self.pixel_energies[k]))
    #         # if i is in between
    #         else:
    #             return (i,j) + self.rec_best_seam(min(self.pixel_energies[i-1, j+1], \
    #                 self.pixel_energies[i, j+1], self.pixel_energies[i+1, j+1], key = lambda k: self.pixel_energies[k]))



    # def rec_best_seam(self, i, j):
    #     """ 
    #     Recursively finds the seam with the lowest seam energy and returns
    #     a tuple with the locations of pixels at i j
    #     """
    #     # if at the last row of pixels in image
    #     if(j == self.height-1):
    #         return [(i,j)]
    #     else:
    #         # if i is in the first column of pixels
    #         if(i == 0):

    #             return [(i,j)] + min(self.energies[self.rec_best_seam(i, j+1)], \
    #                 self.energies[self.rec_best_seam(i+1, j+1)], key = lambda k: self.energies[k])
    #         # if i is in the last column
    #         elif(i == self.width-1):
    #             return [(i,j)] + min(self.energies[self.rec_best_seam(i-1, j+1)], \
    #                 self.energies[self.rec_best_seam(i, j+1)], key = lambda k: self.energies[k])
    #         # if i is in between
    #         else:
    #             # left = rec_best_seam(row+1, col-1)
    #             # center = rec_call(row+1, col)
    #             # right = rec_call(row+1, col+1)

    #             # seams = [left,]

    #             return [(i,j)] + min(self.energies[self.rec_best_seam(i-1, j+1)], \
    #                 self.energies[self.rec_best_seam(i, j+1)], \
    #                 self.energies[self.rec_best_seam(i+1, j+1)], key = lambda k: self.energies[k])

    




    # def rec_best_seam(self, i, j, pixel_energies, seams):
    #     """ 
    #     Recursively finds the seam with the lowest seam energy and returns
    #     a collection of tuples representing the pixel locations of pixels
    #     """
    #     # summing up energies within each pixel in seam
    #     seams[i,j][1] += pixel_energies[i,j]
    #     # appending i j pixel coordinates of seam to seams collection
    #     seams[i,j][0] + (i,j)
    #     # if at the last row of pixels
    #     if(j == self.height):
    #         return self.energy(i, j)
    #     else:
    #         # if i is in the first column
    #         if(i == 0):             
    #             seams[i,j][1] += pixel_energies[i,j] + min(rec_best_seam(i+1, j), rec_best_seam(i+1, j+1))
        
    #         # if i is in the last column
    #         elif(i == self.width):  
    #             pixel_energies(i,j) + min(rec_best_seam(i+1, j-1), 
    #                                         rec_best_seam(i+1, j))
    #         # if i is in between 
    #         else:                   
    #             pixel_energies(i,j) + min(rec_best_seam(i+1, j-1),
    #                                         rec_best_seam(i+1, j),
    #                                         rec_best_seam(i+1, j+1))