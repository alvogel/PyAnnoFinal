import os
import numpy as np
import random
import pygame
from CTrainingItem import *

class CTrainingSet:

    def __init__(self, folder_name):

        # Foldername where files are stored
        self.folder = folder_name

        # counter for quantity of each digit
        self.count = [0,0,0,0,0,0,0,0,0,0]

        # result/target vectors for the output layer
        self.training_vectors = np.array([  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], ])



        # the set contains the training items
        self.set = []

        # load all training images with metadata
        file_list = os.listdir(str(self.folder)+"/")
        for file in file_list:

            #load training images but skip WINDOWS thumbs.db

            if file != "Thumbs.db":
                file_name = file                                            # full file name given from the operating system
                file_extract = file_name.split(".")                         # Split filename and file ending
                file_first = file_extract[0].split("_")                     # split between the metainformation in the filename
                file_id = file_first[0]                                     # extract file id
                file_digit = file_first[1]                                  # extract file digit

                image = pygame.image.load(self.folder+"/"+file_name)              # load image from file name

                self.addItem(image, file_digit, file_id) # add training item to the set with metadata

        return

    # ------------------------------------------------------------------------------------------------------------------

    # returns the highest id from the list of items
    def getLastId(self):
        if self.getItemCount() > 0:
            self.set = sorted(self.set, key=lambda x: x[0], reverse=False)
            return self.set[-1][0]
        else:
            return 1

    # ------------------------------------------------------------------------------------------------------------------

    # returns random training item
    def getRandomItem(self):

        # return random item from set
        item = random.choice(self.set)

        return [item,self.training_vectors[int(item[1])]]

    # ------------------------------------------------------------------------------------------------------------------

    # return the item count of training data

    def getItemCount(self, digit = -1):

        # reset counter to zero
        counter = 0

        # if no digit is given return number of all digits of this set
        if digit == -1:
            return len(self.set)
        # if digit is given count number of this single digit and return this number
        else:
            return self.count[digit]


    # ------------------------------------------------------------------------------------------------------------------

    # decide if new added item becomes training or test item

    def shouldBeTrainingItem(self):

        if random.randint(0,100) < self.training_rate:
            return True
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------

    # Adds a CTrainingItem Object to the TrainingSet with highest ID from List plus 1

    def addItem(self, surface, digit, id=int(0)):

        item = CTrainingItem(surface, digit)
        thumb = item.getImage(20,20,True)
        self.count[int(digit)] += 1

        vector = []

        array = pygame.surfarray.array3d(thumb)

        for x in range(thumb.get_width()):
            for y in range(thumb.get_height()):
                vector.append(array[x][y][0])

        shaped = np.array([vector])

        if id == 0:
            id = int(self.getLastId()) + int(1)

        item = [int(id), digit, surface, thumb, shaped]
        self.set.append(item)

        self.set = sorted(self.set, key=lambda x: x[0], reverse=False)

    # ------------------------------------------------------------------------------------------------------------------

    # Saves all training images to files in folder training, filename is encoded as UNIQUE_ID + DIGIT + TRAINING-TYPE"
    def saveToFile(self):

        for item in self.set:
            file_id = item[0]
            file_digit = item[1]
            file_surface = item[2]
            file_name = str(file_id)+"_"+str(file_digit)+".png"
            pygame.image.save(file_surface, self.folder+"/"+file_name)


    # ------------------------------------------------------------------------------------------------------------------