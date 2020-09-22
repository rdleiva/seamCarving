'''
Image resizer script
Usage: python seamresize.py <resize|enlarge> <picture> <number_of_pixels> [save_partials]

Notice: This script requires the "Python Image Library" extension.
	You can download it here : http://www.pythonware.com/products/pil/

@author: Pierre de La Morinerie
Based on the "Seam Carving for Content-Aware Image Resizing" paper
	by Shai Avidan and Ariel Shamir
	
Copyright (c) 2009 Pierre de La Morinerie

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
'''

from PIL import Image, ImageFilter
import sys
import os

'''Returns an energy function for processing the image'''
def energy(image):
    return e1(image);

'''Returns a simple gradient map of the image'''
def e1(image):
    kh = ImageFilter.Kernel((3,3), (-1, 0, 1, -1, 0, 1, -1, 0 ,1), 1, 128)
    kv = ImageFilter.Kernel((3,3), (1, 1, 1, 0, 0, 0, -1, -1 , -1), 1, 128)
    
    hFilter = image.filter(kh).point(lambda i : abs(i-128))
    vFilter = image.filter(kv).point(lambda i : abs(i-128))
    
    return Image.blend(hFilter, vFilter, 0.5)

'''Given an energy map, returns all the vertical seams'''
def computeSeams(energyMap):
    (width, height) = energyMap.size
    emap = energyMap.convert('L').load();
    
    costs = [];
    seams = [];
    
    # For each pixel column, compute a seam
    for col in range(0, width):
        currentCol = col
        cost = 0
        seam = [0]
        
        for row in range(1, height):
            # Look which underneath pixel (left, middle or right) has the least energy
            adj = (emap[currentCol-1, row] if (currentCol - 1 >= 0)    else 1000,
                   emap[currentCol  , row],
                   emap[currentCol+1, row] if (currentCol + 1 < width) else 1000)
            
            # Add the energy of the pixel to the total energy of the seam
            eMin = min(adj)
            cost += eMin
            
            # Did we move one pixel down on the left, middle or right ?
            offset = adj.index(eMin) - 1
            currentCol += offset
            
            # We now have a new value for this seam
            seam.append(offset)
        
        # Update the global costs and seams arrays with the computed cost and seam
        costs.append(cost)
        seams.append(seam)
     
    return (costs, seams)

'''Given a filename, resize it by removing n pixels vertically'''
def resize(filename, pixels, partialSave=0):
    
    im = Image.open(filename)
    
    removedSeams = []
    
    for i in range(0, pixels):
        # Load the image
        (width, height) = im.size
        imap = im.load()
        
        # Find the energy map, and the least energy seam
        energyMap = energy(im)
        (costs, seams) = computeSeams(energyMap)
        
        bestSeamIndex = costs.index(min(costs))
        bestSeam = seams[costs.index(min(costs))]
        
        # Resize the image
        newim = Image.new("RGB", (width - 1, height))
        newim.paste(im, (0, 0))
        
        newimmap = newim.load()
        (nwidth, nheight) = newim.size
        
        # ...and remove the least energy seam
        currentCol = bestSeamIndex
        for row in range(0, nheight):
            currentCol += bestSeam[row]
            for col in range(currentCol, nwidth):
                newimmap[col, row] = imap[col + 1, row]
                
        im = newim
        
        # Save partial result if requested
        if partialSave > 0 and (i % partialSave) == 0:
            im.save("resizePartials/pic" + str(i) + ".png")  
        
        # Save removed seam
        removedSeams.append((bestSeamIndex, bestSeam)) 
    
    return (im, removedSeams)

def enlarge(filename, pixels, partialSave):
    
    im = Image.open(filename) 
        
    # Extract seams 
    (dummy, seams) = resize(filename, pixels, 0)
    
    # Normalize indexes : if we removed a seam on the left of another one,
    # the start index of the seam will have an offset of one. Let's correct this.
    for n in range(0, len(seams) - 1):
        (removedCol, dummy) = seams[n]
        seams[n+1:] = [(col+1, seam) if col >= removedCol else (col, seam)
					   for (col, seam) in seams[n+1:]]
    
    # Add seams where we would normally have removed them
    for i in range(0, pixels):
        
        (seamCol, bestSeam) = seams[i];
        
        (width, height) = im.size
        (width, height) = (width + 1, height)
        
        newim = Image.new("RGB", (width, height))
        newim.paste(im, (0, 0))
        
        imap = im.load()
        newimmap = newim.load()
        
        currentCol = seamCol
        for row in range(0, height):
            currentCol += bestSeam[row]
            for col in range(currentCol + 1, width):
                newimmap[col, row] = imap[col - 1, row]
                
        im = newim
        
        # Update seams offset
        seams = [(pos, seam) if pos <= seamCol else (pos + 1, seam)
				 for (pos, seam) in seams]
        
        # Save partial result if requested
        if partialSave > 0 and (i % partialSave) == 0:
            im.save("enlargePartials/pic" + str(i) + ".png")   
        
    return (im, seams)

if __name__ == '__main__':
    
    if len(sys.argv) < 4:
        sys.exit("Error: invalid arguments.\nSyntax: python " + sys.argv[0] + " <resize|enlarge> <picture> <number_of_pixels> [save_partials]")
    
    action = sys.argv[1]
    filename = sys.argv[2]
    pixels = int(sys.argv[3])
    
    partialSave = 0 if len(sys.argv) < 5 else int(sys.argv[4])    
    
    if action == "resize":
        operation = resize
        
    elif action == "enlarge":
        operation = enlarge
    else:
        sys.exit("Error: first argument must be a valid action type ('resize' or 'enlarge')")
    
    # If needed, create partial folder
    if partialSave > 0 and not os.path.exists(action + 'Partials'):
    	os.makedirs(action + 'Partials')

    # Process picture 
    (image, dummy) = operation(filename, pixels, partialSave)
    image.save(action + "_" + str(pixels) + ".png")
    image.show()