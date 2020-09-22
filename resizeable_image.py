"""
Rotman Daniel Leiva Henriquez
Professor Daniels
CSC440 - Algorithms
Assignment 5 - Dynamic Programmins - Seam Carving
April 10, 2020
"""

import imagematrix
import operator

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=True):
        self.pixel_energies = {}
        for i in range(self.width):
            for j in range(self.height):
                self.pixel_energies[i,j] = self.energy(i,j)
        # print(self.pixel_energies)
        if dp:
            return self.best_seam_dp(self.pixel_energies)
        else:
            return self.best_seam_naive(self.pixel_energies)

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())

    # i = x = columns = width, j = y = rows = height
    def best_seam_dp(self, pixel_energies):
        """
        dynamic programming implementation of finding the seam with the lowest energy in an image
        seams and their corresponding energies will be stored in a dictionary
        the seam with the lowest energy will be removed
        """
        # stored results of seam calculations
        self.temp_best_seams = {}
        self.memo = {}

        # first row is the original best seam
        for i in range(self.width):
            self.memo[i,0] = self.pixel_energies[i,0]
            self.temp_best_seams[i,0] = [(i,0)]

        last_row_min = []
        # for every row after the first one
        for j in range(1, self.height):
            
            # for every pixel in current row j
            for i in range(self.width):
                minimum_list = []
                minimum_list_path = {}

                left = (i-1, j-1)
                middle = (i, j-1)
                right = (i+1, j-1)
                # if i is in the first column, no left
                if(i == 0):
                    options_above = [middle, right]
                # if i is in the last column, no right
                elif(i == self.width-1):
                    options_above = [left, middle]
                # if i is in between
                else:
                    options_above = [left, middle, right]

                for option in options_above:
                    minimum_list.append(self.memo[option])
                    minimum_list_path[self.memo[option]] = option
                
                minimum_energy = min(minimum_list)
                
                # remember the pixel energy of minimum energy seam at depth j so far
                self.memo[i,j] = minimum_energy + self.pixel_energies[i,j]

                for m in minimum_list:
                    if(m == minimum_energy):
                        # remember path so far for future reference
                        self.temp_best_seams[i,j] = self.temp_best_seams[minimum_list_path[m]] + [(i,j)]

                # getting the last details from the last row to build best seam
                if(j==self.height-1):
                    if(i==0):
                        last_row_min.append(self.memo[i,j])
                        last_row_min.append((i,j))
                        last_row_min.append(min(minimum_list))
                        last_row_min.append(minimum_list_path[self.memo[option]])
                    else:
                        if(last_row_min[0]>self.memo[i,j]):
                            last_row_min[0] = self.memo[i,j]                        # row min energy 
                            last_row_min[1] = (i,j)                                 # row min location
                            last_row_min[2] = min(minimum_list)                     # min above
                            last_row_min[3] = minimum_list_path[self.memo[option]]  # min above location
        # best seam
        return self.temp_best_seams[last_row_min[3]] + [last_row_min[1]]
  


    def best_seam_naive(self, pixel_energies):
        """
        naive implementation of finding the seam with the lowest energy in an image
        seams and their corresponding energies will be stored in a dictionary
        the seam with the lowest energy will be removed
        """
        seam = []
        # for every pixel in top row find all the possible seam locations
        for i in range(self.width-1):
            # get best seam at i 0 and store it in best_seams along with its energy
            seam = self.rec_best_seam(i,0)
        print(seam)
        return seam


    # i = x = column, j = y = row
    def rec_best_seam(self, i, j):
        """ 
        Recursively finds the seam with the lowest seam energy and returns
        a list of tuples with the locations of pixels at i j
        i = x = columns = width, j = y = rows = height
        """
        # if j at the last row of pixels in image
        if(j == self.height-1):
            return [(i,j)]
        else:
            # if i is at the first column of pixels
            if(i == 0):
                # no left
                middle = self.rec_best_seam(i, j+1)
                right = self.rec_best_seam(i+1, j+1)
                seams = [middle, right]
                seam_energies = [self.seam_energy(middle), \
                                self.seam_energy(right)]

            # if i is in the last column
            elif(i == self.width-1):
                left = self.rec_best_seam(i-1, j+1)
                middle = self.rec_best_seam(i, j+1)
                # no right
                seams = [left, middle]
                seam_energies = [self.seam_energy(left), \
                                self.seam_energy(middle)]

            # if i is in between
            else:
                left = self.rec_best_seam(i-1, j+1)
                middle = self.rec_best_seam(i, j+1)
                right = self.rec_best_seam(i+1, j+1)
                seams = [left, middle, right]
                seam_energies = [self.seam_energy(left), \
                                self.seam_energy(middle), \
                                self.seam_energy(right)]

            best_seam_index = seam_energies.index(min(seam_energies))
            best_seam_here = seams[best_seam_index]

            return [(i,j)] + best_seam_here


    def seam_energy(self, seam):
        """
        takes seam composed of tuples of i and j locations
        returns the sum of all pixel energies in the seam
        """
        seam_energy_sum = 0
        for s in seam:
            seam_energy_sum += self.pixel_energies[s]
        return seam_energy_sum