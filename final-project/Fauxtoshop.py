from Netpbm import Netpbm # import the student's Netpbm class

import copy
import tkinter as tk
import tkinter.filedialog as tkfile
import tkinter.messagebox as tkmsg

###########################################################################
# Class:         Fauxtoshop
# Author:        Barry Lawson
# Last modified: 19 Nov 2020
#
# This class implements a graphical interface for a simple image
# processing utility, a la a scaled-down Photoshop.  The class uses
# tkinter to draw a window, to display images within the window, and to
# provide various menu options (Open, Save, Quit, Invert, Rotate, etc.).
# The class presumes use of ASCII PGM/PPM images (i.e., Netbpm images).
#
# This class relies on the student to implement a separate Netpbm class.
# A fully-functioning version of the Netpbm class will contain the following
# methods, internally handling either PGM (grayscale) or PPM (color) images.
#
#    def __init__(self, filename)  # reading an ASCII PGM/PPM image
#    def writeImage(self, filename) # writing an ASCII PGM/PPM
#    def getMagicNumber(self)
#    def getComment(self)
#    def getNumCols(self)
#    def getNumRows(self)
#    def getMaxLevel(self)
#    def getHeader(self)
#    def getPixels(self)
#    def changeBrightness(self, amount)
#    def flip(self, vertical = True)
#    def rotate(self, rotateRight = True)
#    def halve(self)
#    def double(self)
#    def invert(self)
#    def crop(self, ulRow, ulCol, lrRow, lrCol)
#    def posterize(self, numLevels)
#    def toGrayscale(self)
#
class FauxtoShop:

    #####################
    # Constructor for the Fauxtoshop window / object.
    # Note that among the instance variables are two copies (evenutally)
    # of a Netpbm object.
    #
    def __init__(self):
        self.currentImage  = None  # will be a Netpbm object
        self.imageCopy     = None  # will be a Netpbm object

        self.currentOption = None  # img processing algorithm underway as
                                   # (common) slider is being used

        # instance variables used in handling interactive cropping
        self.cropIsActive = False
        self.cropStartPos = None
        self.cropEndPos   = None

        # create the overall tkinter window, with menus
        self.window = tk.Tk()
        self.window.title("FauxtoShop")
        [self.menubar, self.imageMenuItems] = self.createMenu()
        self.window.config(menu = self.menubar)

        # use a tk.Canvas for displaying the image -- which can be either
        # a GIF or a raw (not ASCII) PGM or PPM
        image = tk.PhotoImage(file = "images/.startup.gif")  # Bobcat image
        self.imageLabel = \
            tk.Canvas(master = self.window, width = 450, height = 525)
        self.imageLabel.create_image((0,0), image = image, anchor=tk.NW)
        self.imageLabel.pack(fill = tk.X, padx = 5, pady = 5)

        # bind the callbacks for button events for handling crop
        self.imageLabel.bind("<Button-1>", self.cropClick)
        self.imageLabel.bind("<B1-Motion>", self.cropDrag)
        self.imageLabel.bind("<ButtonRelease-1>", self.cropRelease)

        # a slide and OK/Cancel buttons will appear and disappear as
        # appropriate based on different image processing algorithms
        self.createSliderAndButtons()

        # plop the window in the center of the screen
        self.window.eval('tk::PlaceWindow . center')

        ########## USE THIS ONLY FOR TESTING ################
        # Uncomment three lines of code below if you get tired of having
        # to load an image via menu operation while testing.  Make sure
        # to hardcode the correct path for your situation, and make sure
        # to comment this out before submitting.
        #
        #self.currentImage = Netpbm("images/pgm/lilly.pgm")
        self.currentImage = Netpbm("images/ppms/cat.ppm")
        self.showImage()
        self.enableMenus()
        #
        ##########                           ################

        # and then start listening for mouse-click events
        self.window.mainloop()

    #####################
    # Simple internal method in case student implements getMagicNumber()
    # but no isPGM() (e.g., if student implements PGM only or PPM only).
    #
    def __isPGM(self):
        return self.currentImage.getMagicNumber().upper() == "P2"


    #####################
    # This method handles what should be done on mouse-click within the
    # canvas _after_ the user has selected the "crop" menu option (where
    # self.cropIsActive will become True) --- simply record the (x,y)
    # location of where the crop will begin.
    #
    def cropClick(self, event):
        if not self.cropIsActive: return
        self.window.configure(cursor = "crosshair")
        self.cropStartPos = (event.x, event.y)

    #####################
    # This method handles what should be done on mouse-drag within the
    # canvas _after_ the user has already clicked in the canvas to start
    # a crop.  This will delete the old rubber-banded red cropping box,
    # and draw a new box that extends from the current (x,y) back to
    # (x,y) recorded in cropClick when the crop began.
    #
    def cropDrag(self, event):
        if not self.cropIsActive: return
        self.window.configure(cursor = "crosshair")

        self.imageLabel.delete("box")
        x1 = self.cropStartPos[0]; y1 = self.cropStartPos[1]
        x2 = event.x; y2 = event.y
        self.imageLabel.create_line(x1, y1, x2, y1, fill = "red", tags = "box")
        self.imageLabel.create_line(x1, y1, x1, y2, fill = "red", tags = "box")
        self.imageLabel.create_line(x1, y2, x2, y2, fill = "red", tags = "box")
        self.imageLabel.create_line(x2, y1, x2, y2, fill = "red", tags = "box")

    #####################
    # This method handles what should be done on mouse-release within the
    # canvas _after_ the user has dragged a rubber-banded red cropping box.
    # Simply record the (x,y) position of where the crop will end.
    #
    def cropRelease(self, event):
        if not self.cropIsActive: return
        self.window.configure(cursor = "")
        self.cropEndPos = (event.x, event.y)

    #####################
    # This method will be called whenever the user clicks the OK or Cancel
    # button that appear in the bottom frame of the window based on choice of
    # image-processing algorithm.
    # In general,
    #   - clicking OK should just update and show the current image,
    #     and hide the bottom frame, and renable menus as appropriate.
    #   - clicking cancel should not update the image, should show the previous
    #     version, and hide the bottom frame, and renable menus as appropriate.
    # In the case that OK or Cancel is during a crop, we need to call the
    # student's method to crop the image, which will then be used to update
    # and show the current image.
    #
    def buttonClick(self, clickedOK = True):
        if clickedOK:
            if self.currentOption == self.cropImage and \
                    self.cropStartPos != None and self.cropEndPos != None:
                self.handleCrop()  # method below which calls student's crop
            if self.imageCopy != None:
                # update image to the current working version
                self.currentImage = self.imageCopy

        self.imageCopy = None
        self.hideBottomFrame()
        self.enableMenus()

        # show self.currentImage -- which will be correct should the user have
        # clicked OK or Cancel (see logic above)
        self.showImage()

        # if button clicked (OK or cancel) was during crop, reset those states
        if self.currentOption == self.cropImage:
            self.imageLabel.delete("box")
            self.cropIsActive = False
            self.cropStartPos = None
            self.cropEndPos = None

    #####################
    # This method is used to setup and then call the student's crop method
    # inside Netpbm.
    #
    def handleCrop(self):
        self.imageCopy = copy.deepcopy(self.currentImage)
        # recall that row/col are reversed from GUI x/y
        x1 = self.cropStartPos[0]; y1 = self.cropStartPos[1]
        x2 = self.cropEndPos[0];   y2 = self.cropEndPos[1]

        # handle cases of rectangle drawn in direction other than NW to SE
        upperLeftRow  = min(y1, y2); upperLeftCol  = min(x1, x2)
        lowerRightRow = max(y1, y2); lowerRightCol = max(x1, x2)

        # handle case of rectangle strecthed outside image bounds
        numCols = self.currentImage.getNumCols()
        numRows = self.currentImage.getNumRows()
        upperLeftRow  = min(max(0, upperLeftRow), numRows - 1)
        upperLeftCol  = min(max(0, upperLeftCol), numCols - 1)
        lowerRightRow = min(max(0, lowerRightRow), numRows - 1)
        lowerRightCol = min(max(0, lowerRightCol), numCols - 1)

        # call the student's crop method inside Netpbm
        self.imageCopy.crop(upperLeftRow, upperLeftCol, \
                            lowerRightRow, lowerRightCol)

    #####################
    # This method is called whenever the slider is changed (e.g., for
    # changing brightness or posterize algorithms).  Note that use of
    # self.imageCopy allows us to update the image being displayed while
    # the slider is changed, but still able to revert back to the original
    # self.currentImage should the user ultimately decide to Cancel.
    # This method will cor
    #
    def sliderChange(self, event):
        value = int(self.slider.get())  # the numeric value of the slider
        self.imageCopy = copy.deepcopy(self.currentImage)

        if self.currentOption == self.brightenImage:
            self.imageCopy.changeBrightness(value) # student's changeBrightness
        elif self.currentOption == self.posterizeImage:
            self.imageCopy.posterize(value) # calls student's posterize method
        elif self.currentOption == self.glassImage:
            self.imageCopy.glass(int(value)) # call student's glass method
        elif self.currentOption == self.gaussianBlur:
            self.imageCopy.gaussianBlur(int(value))


        self.showImage(self.imageCopy)  # show the working version (copy)

    #####################
    # This method is called to unhide the bottom frame containing
    # OK and Cancel buttons, and slider when appropriate.
    #
    def showBottomFrame(self, showSlider = True):
        self.slider.pack_forget()
        self.buttonFrame.pack_forget()
        if showSlider:
            self.slider.configure(length = 250)
            self.slider.pack()
        self.buttonFrame.pack(pady = 10)
        self.bottomFrame.pack()
        self.window.eval('tk::PlaceWindow . center')

    #####################
    # This method is called to hide the bottom button/slider frame.
    def hideBottomFrame(self):
        self.bottomFrame.pack_forget()
        self.window.eval('tk::PlaceWindow . center')

    #####################
    # This method is called whenever we need to update the image shown in
    # the canvas.  Note the optional parameter for which, defaulting to
    # the original self.currentImage.  In cases where the user can "play
    # then cancel" (e.g., with brightness, levels), the which parameter
    # can instead be passed as self.imageCopy -- the current working version --
    # while still maintaining the original self.currentImage should the user
    # decide to cancel the process
    #
    def showImage(self, which = None):
        if which == None: which = self.currentImage
        magic = which.getMagicNumber().upper()

        # call an internal private method to write a hidden raw version of the
        # pgm/ppm, since the canvas can handle only raw pgm/pgm (not ASCII)
        fname = "images/.img." + ("pgm" if magic == "P2" else "ppm")
        self.__writeImageRaw(fname, which)

        # construct and then display in the canvas a tk.PhotoImage image
        # object using the hidden raw pgm/ppm
        image = tk.PhotoImage(file = fname)
        self.imageLabel.delete("all")
        self.imageLabel.configure(width = self.currentImage.getNumCols())
        self.imageLabel.configure(height = self.currentImage.getNumRows())
        self.imageLabel.create_image((0,0), image = image, anchor=tk.NW)
        self.imageLabel.image = image
        self.window.eval('tk::PlaceWindow . center')

    #####################
    # This method is called whenever the user selects the Open menu option.
    #
    def openImage(self):
        # default looking in ".", the current directory
        fname = tkfile.askopenfilename(initialdir = ".", title = "Open Image")
        if fname == "": return  # do nothing on cancel

        try:
            # call the student's Netpbm constructor
            self.currentImage = Netpbm(fname)
        except:
            tkmsg.showerror(message = f"Unable to open \"{fname}\"")
        else:
            self.showImage()
            self.enableMenus()

    #####################
    # This method is called whenever the user selects the Save menu option.
    #
    def saveImage(self):
        # default saving into ".", the current directory
        fname = tkfile.asksaveasfilename(initialdir = ".", title = "Save Image")
        if fname == "": return  # do nothing on cancel

        # we could have a function that converts pgm to ppm, but we don't...
        if self.__isPGM() and fname.lower().endswith(".ppm"):
            tkmsg.showerror(message = f"Cannot save PGM as PPM")
            return

        # if ppm and trying to save as pgm, convert to grayscale first
        if (not self.__isPGM()) and fname.lower().endswith(".pgm"):
            try:
                # call the student's toGrayscale method in the Netpbm class
                self.currentImage.toGrayscale()
            except:
                tkmsg.showerror(message = f"Unable to convert to grayscale...")
                return
            else:
                # let the user know that we are converting to PGM before saving
                tkmsg.showerror(message = \
                    f"Converting to grayscale before saving PGM...")
                self.showImage()  # show the updated (gray) PGM

        try:
            # call the student's writeImage method inside Netpbm
            self.currentImage.writeImage(fname)
        except:
            tkmsg.showerror(message = f"Unable to save \"{fname}\"")

    #####################
    # This method is called whenever the user selects the Brightness menu option
    #
    def brightenImage(self):
        try:
            # self.currentOption is used so that we know slider and OK/Cancel
            # will in this case be handling brightness
            self.currentOption = self.brightenImage
            self.slider.configure(from_ = -self.currentImage.getMaxLevel(), \
                                  to    =  self.currentImage.getMaxLevel())
            self.slider.set(0)
            self.disableMenus()
            self.showBottomFrame(True)  # show slider
        except:
            tkmsg.showerror(message = f"Unable to change brightness...")

        # here, the image is not shown, but rather is shown when the user
        # clicks either OK or Cancel (see buttonClick method above);
        # the student's changeBrightness function is called within sliderChange

    #####################
    # This method is called whenever the user selects the Invert menu option
    #
    def invertImage(self):
        try:
            # call the student's invert method inside Netpbm
            self.currentImage.invert()
        except:
            tkmsg.showerror(message = f"Unable to invert current image...")
        else:
            self.showImage()

    #####################
    # This method is called whenever the user selects the rotateLeft or
    # rotateRight menu options.  The parameter indicates choice, and is
    # passed to the student's rotate method inside Netpbm.
    #
    def rotateImage(self, rotateRight = True):
        try:
            # call the student's rotate method inside Netpbm
            self.currentImage.rotate(rotateRight)
        except:
            tkmsg.showerror(message = f"Unable to rotate current image...")
        else:
            self.showImage()

    #####################
    # This method is called whenever the user selects the flipVertical or
    # flipHorizontal menu options.  The parameter indicates choice, and is
    # passed to the student's flip method inside Netpbm.
    def flipImage(self, vertical = True):
        try:
            # call the student's flip method inside Netpbm
            self.currentImage.flip(vertical)
        except:
            tkmsg.showerror(message = f"Unable to flip image...")
        else:
            self.showImage()

    #####################
    # This method is called whenever the user selects the Posterize menu option.
    #
    def posterizeImage(self):
        try:
            # self.currentOption is used so that we know slider and OK/Cancel
            # will in this case be handling posterizing
            self.currentOption = self.posterizeImage
            numLevels = self.currentImage.getMaxLevel() + 1
            self.slider.configure(from_ = 2, to = numLevels)
            self.slider.set(numLevels)
            self.disableMenus()
            self.showBottomFrame(True)  # show slider
        except:
            tkmsg.showerror(message = f"Unable to posterize image...")

        # here, the image is not shown, but rather is shown when the user
        # clicks either OK or Cancel (see buttonClick method above);
        # the student's posterize function is called within sliderChange

    #####################
    # This method is called whenever the user selects the Glass menu option.
    #
    def glassImage(self):
        try:
            # self.currentOption is used so that we know slider and OK/Cancel
            # will in this case be handling "glassing"
            self.currentOption = self.glassImage
            maxRadius = min(self.currentImage.getNumRows(), \
                            self.currentImage.getNumCols())
            maxRadius = 20
            self.slider.configure(from_ = 0, to = maxRadius)
            self.slider.set(0)
            self.disableMenus()
            self.showBottomFrame(True)  # show slider
        except:
            tkmsg.showerror(message = f"Unable to glass image...")

        # here, the image is not shown, but rather is shown when the user
        # clicks either OK or Cancel (see buttonClick method above);
        # the student's glass function is called within sliderChange


    #####################
    # This method is called whenever the user selects the crop menu option.
    # Activate the crop sequence, which requires the user to first click,
    # then drag, then release -- see the cropClick, cropDrag, and cropRelease
    # methods above.
    #
    def cropImage(self):
        self.cropIsActive = True
        self.window.configure(cursor = "crosshair")
        self.currentOption = self.cropImage
        self.disableMenus()
        self.showBottomFrame(False)  # no slider, but OK and Cancel buttons

    #####################
    # This method is called whenever the user selects the Halve menu option.
    #
    def halveImage(self):
        try:
            # call the student's halve method inside Netpbm
            self.currentImage.halve()
        except Exception as e:
            tkmsg.showerror(message = f"Unable to halve image...")
            print(e)
        else:
            self.showImage()

    #####################
    # This method is called whenever the user selects the Double menu option.
    #
    def doubleImage(self):
        try:
            # call the student's halve method inside Netpbm
            self.currentImage.double()
        except:
            tkmsg.showerror(message = f"Unable to double image...")
        else:
            self.showImage()

    #####################
    # This method is called whenever the user selects the Grayscale menu option
    # or whenver the user tries to save a PPM (color) with a PGM (grayscale)
    # filename extension.
    #
    def toGrayscale(self):
        if self.__isPGM():
            tkmsg.showerror(message = f"PGM is already a grayscale image...")
        else:
            try:
                # call the student's toGrayscale method inside Netpbm
                self.currentImage.toGrayscale()
            except:
                tkmsg.showerror(message = f"Unable to convert to grayscale...")
            else:
                self.showImage()

    def gaussianBlur(self):
        try:
            # self.currentOption is used so that we know slider and OK/Cancel
            # will in this case be handling posterizing
            self.currentOption = self.gaussianBlur
            self.slider.configure(from_ = 0, to = 10)
            self.slider.set(0)
            self.disableMenus()
            self.showBottomFrame(True)  # show slider
        except:
            tkmsg.showerror(message = f"Unable to gaussian blur image...")

        # here, the image is not shown, but rather is shown when the user
        # clicks either OK or Cancel (see buttonClick method above);
        # the student's posterize function is called within sliderChange


    #######################
    # This method is called whenever an interactive processing method is chosen
    # (e.g., brightness, posterize, crop) so that the user must select OK or
    # Cancel before having the ability to do anything via menu other than Quit.
    #
    def disableMenus(self):
        openIndex = 0; self.fileMenu.entryconfig(openIndex, state=tk.DISABLED)
        saveIndex = 1; self.fileMenu.entryconfig(saveIndex, state=tk.DISABLED)
        for i in range(self.imageMenuItems):
            self.imageMenu.entryconfig(i, state=tk.DISABLED)

    #######################
    # This method is called whenever an interactive processing method
    # (e.g., brightness, posterize, crop) is finished, so that the user gets
    # full menu functionality back.
    #
    def enableMenus(self):
        openIndex = 0; self.fileMenu.entryconfig(openIndex, state=tk.NORMAL)
        saveIndex = 1; self.fileMenu.entryconfig(saveIndex, state=tk.NORMAL)
        for i in range(self.imageMenuItems):
            self.imageMenu.entryconfig(i, state=tk.NORMAL)

    #####################
    # This method is called in the constructor to build the menus displayed
    # within the Fauxtoshop window.
    #
    def createMenu(self):
        # the overall menubar for the window
        self.menubar  = tk.Menu(self.window)

        # The file menu (consisting of Open, Save, Quit) within the menubar.
        # Note that 'command' sets the callback method for a given menu option.
        # Those callack methods are defined elsewhere in this class.
        self.fileMenu = tk.Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label = "Open", command = self.openImage)
        self.fileMenu.add_command(label = "Save", \
                    command = self.saveImage, state = tk.DISABLED)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Quit", command = self.window.quit)

        # add the file menu as a cascading menu to the menubar
        self.menubar.add_cascade(label = "File", menu = self.fileMenu)

        # The image-processing-options menu.  Note the use of a list for
        # labels and a corresponding list of methods-as-1st-class-objects
        # for the callbacks.  (Python lambdas are needed for those methods
        # requiring an argument.)
        self.imageMenu = tk.Menu(self.menubar, tearoff=0)
        labels = ["Brightness", "Invert", "Rotate Left", "Rotate Right", \
                  "Flip Horizontal", "Flip Vertical", "Posterize", "Glass", \
                  "Crop", "Halve Image", "Double Image", "To Grayscale", \
                  "Gaussian Blur"]
        functions = [self.brightenImage, self.invertImage, \
             lambda: self.rotateImage(False), lambda: self.rotateImage(True), \
             lambda: self.flipImage(False), lambda: self.flipImage(True), \
             self.posterizeImage, self.glassImage, self.cropImage, \
             self.halveImage, self.doubleImage, self.toGrayscale, \
             self.gaussianBlur]

        # Loop through the labels & add to the menu with corresponding callback
        for i in range(len(labels)):
            self.imageMenu.add_command(label = labels[i], \
                    command = functions[i], state = tk.DISABLED)

        # add the image-processing menu as a cascading menu to the menubar
        self.menubar.add_cascade(label = "Image", menu = self.imageMenu)

        return [self.menubar, len(labels)]

    ################################
    # This method is called in the constructor to build the slide-and-buttons
    # frame that will appear/disappear at the bottom of the Fauxtoshop window.
    # Include two helper methods to allow the user to hit left or right arrow
    # inside the window and move/update the slider
    #
    def __leftArrow(self, event):
        if not self.bottomFrame.winfo_viewable(): return
        minValue = self.slider.cget("from")
        self.slider.set( max(minValue, int(self.slider.get()) - 1) )
        self.sliderChange(event)

    def __rightArrow(self, event):
        if not self.bottomFrame.winfo_viewable(): return
        maxValue = self.slider.cget("to")
        self.slider.set( min(maxValue, int(self.slider.get()) + 1) )
        self.sliderChange(event)

    def createSliderAndButtons(self):
        self.bottomFrame = tk.Frame(master = self.window)

        # rather than using 'command' for a callback, instead tie the callback
        # to when the slider is released -- otherwise, updates to drawing will
        # happen too often, slowing window updating waaaaay down.
        self.slider = tk.Scale(master = self.bottomFrame, length = 250, \
            orient = tk.HORIZONTAL) #, command = self.sliderChange)
        self.slider.bind("<ButtonRelease-1>", self.sliderChange)

        self.window.bind("<Left>", self.__leftArrow)
        self.window.bind("<Right>", self.__rightArrow)

        self.slider.pack()  # pack the slider in the bottom frame

        # create a frame for the OK and Cancel buttons, using lambdas for
        # their callbacks (one function requiring a boolean argument)
        self.buttonFrame = tk.Frame(master = self.bottomFrame)
        self.ok = tk.Button(master = self.buttonFrame, text = "OK", \
            command = lambda: self.buttonClick(True))
        self.cancel = tk.Button(master = self.buttonFrame, text = "Cancel", \
            command = lambda: self.buttonClick(False))
        self.ok.pack(side = tk.LEFT, padx = 10)
        self.cancel.pack(side = tk.LEFT, padx = 10)
        self.buttonFrame.pack(pady = 10) # pack the buttons in the bottom frame

    ######################################################################
    # This method is called from withing __writeImageRaw below, to write
    # the header portion of a PGM/PPM to an output file opened in raw
    # (binary) mode.
    #
    def __writeHeaderRaw(self, outfile, header):
        encoding = 'utf8'
        magic = "P5" if header[0].upper() == "P2" else "P6"  # pgm or ppm?
        outfile.write(bytes(magic + '\n', encoding))
        outfile.write(bytes(header[1] + '\n', encoding))
        outfile.write(bytes(str(header[2][0]) + ' ' + str(header[2][1]) \
            + '\n', encoding))
        outfile.write(bytes(str(header[3]) + '\n', encoding))

    ######################################################################
    # This method is called from within __writeImageRaw below, to write
    # the pixel payload portion of a PGM/PPM to an output file opened in raw
    # raw (binary) mode.  Note the use of .to_bytes from the int class to
    # write each pixel value out in binary form.
    #
    def __writePixelsRaw(self, outfile, pixels, isPGM = True):
        # write each grayscale/rgb out in binary form
        if isPGM:
            for i in range(len(pixels)):
                outfile.write(pixels[i].to_bytes(1, 'big'))
        else:
            reds = pixels[0]; greens = pixels[1]; blues = pixels[2]
            for i in range(len(reds)):
                outfile.write(reds[i].to_bytes(1, 'big'))
                outfile.write(greens[i].to_bytes(1, 'big'))
                outfile.write(blues[i].to_bytes(1, 'big'))

    ######################################################################
    # This method is called from within showImage above, which writes out
    # a hidden raw (not ASCII) version of the student's PPM/PGM.  We need
    # a raw version because tk.Canvas can handle raw PPM/PGM (P5/P6) but
    # not ASCII PPM/PGM (P2/P3).
    #
    def __writeImageRaw(self, filename, image):
        outfile = open(filename, "wb")
        magic = image.getMagicNumber().upper()
        self.__writeHeaderRaw(outfile, image.getHeader())
        self.__writePixelsRaw(outfile, image.getPixels(), \
            image.getMagicNumber().upper() == "P2")
        outfile.close()

###########
def main():
    window = FauxtoShop()

main()
