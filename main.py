from CNetwork import *
from CCanvas import *
from pygame.locals import *
from CTrainingSet import *
from CStatistics import *

def main():

    # central place for text strings

    txt_loading = "Lade Daten..."
    txt_saving = "Speichere Daten..."
    txt_digits = "Ziffern"
    txt_training = "Training"
    txt_testing = "Test"
    txt_caption = "PyAnno - Python artificial neural network for optical character recognition"

    # percentage of training items to testing items

    rate = 80

    # Initalize Database

    db = CStatistics()

    # Init Pygame with window size etc.

    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption(txt_caption)

    # Set main surface where we are drawing and fill it with black for the beginning

    bg = pygame.image.load("gfx/bgnd.png")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    # Init Fonts for write text

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 20)

    text_loading = font.render(txt_loading, False, (255, 255, 255))

    # draws the loading text in the center of the window
    background.blit(text_loading, (400 - (text_loading.get_width() / 2), 300 - (text_loading.get_height() / 2)))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    #Neural Network with a learn rate of 0.4
    ann = CNetwork(0.4)

    #create training set instance that organize the training items
    training_set = CTrainingSet("training")

    #create test set instance that organize the test items
    testing_set = CTrainingSet("testing")

    # drawing canvas
    draw_canvas = CCanvas(0,0,200,200)

    # learning canvas show which digit the network is learning at the moment
    learn_canvas = CCanvas(0,0,200,200)

    # benchmark lists

    error_bench = [0,1,2,3,4,5,6,7,8,9]

    # error for digits
    # digit 0
    error_bench[0] = []
    # digit 0
    error_bench[1] = []
    # digit 0
    error_bench[2] = []
    # digit 0
    error_bench[3] = []
    # digit 0
    error_bench[4] = []
    # digit 0
    error_bench[5] = []
    # digit 0
    error_bench[6] = []
    # digit 0
    error_bench[7] = []
    # digit 0
    error_bench[8] = []
    # digit 0
    error_bench[9] = []

    # few variables :)

    start_draw = False

    epoche = 0

    last_time = 0

    error = 1

    x_offset_drawing_canvas = 0
    y_offset_drawing_canvas = 50

    loop_counter = 0
    fps = 0

    last_time2 = pygame.time.get_ticks()

    dc_original = draw_canvas.render(200, 200, False)
    dc_resized = draw_canvas.render(20, 20, True)

    while 1:

        db.addRow()

        for event in pygame.event.get():
            if event.type == QUIT:
                background.fill((0, 0, 0))
                text_saving = font.render(txt_saving, False, (255, 255, 255))

                background.blit(text_saving,
                                (400 - (text_loading.get_width() / 2), 300 - (text_loading.get_height() / 2)))

                screen.blit(background, (0, 0))
                pygame.display.flip()

                # store neural network to disk
                ann.saveToFile()

                # store trainings set to disk
                training_set.saveToFile()

                # store testing set to disk
                testing_set.saveToFile()

                # save error benchmark

                for index, d in enumerate(error_bench):
                    f = open("data/benchmark/" + str(index) + ".csv", 'w')
                    for c in d:
                        line = str(c[0])+":"+str(c[1])
                        f.write(line+'\n')
                    f.close()

                # save Statistic Database
                db.save()
                return

            item_digit = -1

            # catches the keydown event for the drawn digit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    draw_canvas.Clear()
                if event.key == pygame.K_0:
                    item_digit = 0
                if event.key == pygame.K_1:
                    item_digit = 1
                if event.key == pygame.K_2:
                    item_digit = 2
                if event.key == pygame.K_3:
                    item_digit = 3
                if event.key == pygame.K_4:
                    item_digit = 4
                if event.key == pygame.K_5:
                    item_digit = 5
                if event.key == pygame.K_6:
                    item_digit = 6
                if event.key == pygame.K_7:
                    item_digit = 7
                if event.key == pygame.K_8:
                    item_digit = 8
                if event.key == pygame.K_9:
                    item_digit = 9

                # only saves digit when a key was pressed

                if item_digit != -1:
                    if random.randint(0,100) < 80:
                        training_set.addItem(draw_canvas.render(200,200).copy(), item_digit)
                        draw_canvas.Clear()
                    else:
                        testing_set.addItem(draw_canvas.render(200,200).copy(), item_digit)
                        draw_canvas.Clear()


            # when mousebutton down event occure then start drawing mode for the canvas
            if event.type == MOUSEBUTTONDOWN:
                start_draw = True
                draw_canvas.Draw(pygame.mouse.get_pos()[0] - x_offset_drawing_canvas, pygame.mouse.get_pos()[1] - y_offset_drawing_canvas)

            # when drawing mode is active and mouse is moving send this points to the canvas
            if event.type == MOUSEMOTION:
                if start_draw:
                    draw_canvas.Draw(pygame.mouse.get_pos()[0] - x_offset_drawing_canvas,pygame.mouse.get_pos()[1] - y_offset_drawing_canvas)

            # drawing on canvas ends when mousebuttin is released
            if event.type == MOUSEBUTTONUP:
                draw_canvas.endDraw()
                start_draw = False


        now_time = pygame.time.get_ticks()
        diff_time = now_time - last_time

        if (pygame.time.get_ticks() - last_time2) > 1000:
            fps = loop_counter
            loop_counter = 0
            last_time2 = pygame.time.get_ticks()

        loop_counter += 1


        for i in range(1):

            if training_set.getItemCount() > 0:
                training_item = training_set.getRandomItem()
                training_image_as_array = training_item[0][4]

                learn_canvas.set_surface(training_item[0][2])
                #if epoche < 10:
                ann.learn(training_image_as_array, training_item[1])
                error = ann.getError(training_item[1])
                error_item = [epoche, error]
                error_bench[int(training_item[0][1])].append(error_item)

                epoche += 1

        # Draw everything every 50ms => max. 20 FPS
        if diff_time > 50:
            background.blit(bg,(0,0))

            output_guess = ann.guess(draw_canvas.getPixelArray())
            output_learn = ann.guess(learn_canvas.getPixelArray())

            last_time = pygame.time.get_ticks()

            for index, o in enumerate(output_guess[0]):

                pygame.draw.circle(background, (255 * o, 255 * o, 255 * o), (360, 60+index*20), 10)
                background.blit(font.render(str(index), False, (255, 255, 255)), (380, 50+index*20))

            for index, o in enumerate(output_learn[0]):

                pygame.draw.circle(background, (255 * o, 255 * o, 255 * o), (360, 310+index*20), 10)
                background.blit(font.render(str(index), False, (255, 255, 255)), (380, 300+index*20))

            background.blit(font.render(txt_digits, False, (255, 255, 255)), (0, 540))
            background.blit(font.render(txt_training, False, (255, 255, 255)), (0, 560))
            background.blit(font.render(txt_testing, False, (255, 255, 255)), (0, 580))

            for d in range(10):

                background.blit(font.render(str(d), False, (255, 255, 255)), (100+d*30, 540))
                background.blit(font.render(str(training_set.getItemCount(d)), False, (255, 255, 255)), (100+d*30, 560))
                background.blit(font.render(str(testing_set.getItemCount(d)), False, (255, 255, 255)), (100+d*30, 580))

            font = pygame.font.SysFont('Comic Sans MS', 16)

            text_loop_counter = font.render("Learning Rate: " + str(fps) + "/s", False, (255, 255, 255))
            text = font.render("Fehler: " + str(round(error,4)), False, (255, 255, 255))
            text_training_vectors = font.render("Anzahl Trainingsdaten: " + str(training_set.getItemCount()), False, (255, 255, 255))
            text_epoche = font.render("Epoche: " + str(epoche), False, (255, 255, 255))

            background.blit(text_loop_counter, (400, 560))
            background.blit(text, (400, 500))
            background.blit(text_training_vectors, (400, 520))
            background.blit(text_epoche, (400, 540))

            if start_draw:
                dc_original = draw_canvas.render(200,200, False)
                dc_resized = draw_canvas.render(20, 20, True)

            background.blit(dc_original, (0, 50))
            background.blit(dc_resized, (300, 140))

            background.blit(learn_canvas.render(200,200, False), (0, 300))
            background.blit(learn_canvas.render(20, 20, True), (300, 390))

            screen.blit(background, (0, 0))
            pygame.display.flip()

if __name__ == '__main__': main()