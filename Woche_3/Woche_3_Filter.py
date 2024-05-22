import enum
import glob
from tkinter import *
import cv2

dDepth = [cv2.CV_8U, cv2.CV_16S, cv2.CV_32F, cv2.CV_64F]


class ImageFilteringDemonstration:
    def __init__(self):
        self.widget_vals = []
        self._filter = None
        self._callbacks = []
        self.image = cv2.imread('koreanSigns.png')

        self.drop = None
        self.master = None
        self.widgets = {}

        self.setup_ui()

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, new_filter):
        self._filter = new_filter
        self._notify_filter_observers()

    def _notify_filter_observers(self):
        for callback in self._callbacks:
            callback()

    def register_callbacks(self, callback):
        self._callbacks.append(callback)

    def change_filter(self, selection):
        self.filter = selection

    def setup_ui(self):
        self.master = Tk()
        self.master.geometry("400x600")

        options = [
            "Gaussian", "bilateral", "median", "Sobel", "Scharr", 'Canny'
        ]

        clicked = StringVar()
        clicked.set("Gaussian")

        self.drop = OptionMenu(self.master, clicked, *options, "Gaussian", command=self.change_filter)
        self.drop.pack()

    def apply_blur(self):
        cv2.destroyAllWindows()
        match str(self.filter):
            case "Gaussian":
                sigmaX = self.widgets['sigmaX'].get()
                sigmaY = self.widgets['sigmaY'].get()
                kSize = self.widgets['kSize'].get()

                blurred_image = cv2.GaussianBlur(self.image, sigmaY=sigmaY, sigmaX=sigmaX, ksize=(kSize, kSize))
                cv2.imshow("gaussian blurred: ", blurred_image)
                cv2.waitKey(1)

            case "bilateral":
                # d SigmaSpace and -Colors
                d = self.widgets['d'].get()
                SigmaSpace = self.widgets['SigmaSpace'].get()
                SigmaColors = self.widgets['SigmaColors'].get()

                blurred_image = cv2.bilateralFilter(self.image, d=d, sigmaColor=SigmaColors, sigmaSpace=SigmaSpace)
                cv2.imshow("bilateral blurred: ", blurred_image)
                cv2.waitKey(1)
            case "median":
                # ksize
                kSize = self.widgets['kSize'].get()

                blurred_image = cv2.medianBlur(src=self.image, ksize=kSize)
                cv2.imshow("median blurred: ", blurred_image)
                cv2.waitKey(1)
            case "Sobel":
                #  ddepth, dx, dy, ksize, scale, delta
                dd = self.widgets['dDepth'].get()
                dd = dDepth[dd]

                dx = self.widgets['dx'].get()
                dy = self.widgets['dy'].get()
                kSize = self.widgets['kSize'].get()

                blurred_image = cv2.Sobel(src=self.image, ddepth=dd, dx=dx, dy=dy, ksize=kSize)
                cv2.imshow("Sobel blurred: ", blurred_image)
                cv2.waitKey(1)
            case "Scharr":
                #  ddepth, dx, dy, scale, delta
                dd = self.widgets['dDepth'].get()
                dd = dDepth[dd]

                dx = self.widgets['dx'].get()
                dy = self.widgets['dy'].get()

                blurred_image = cv2.Scharr(src=self.image, ddepth=dd, dx=dx, dy=dy)
                cv2.imshow("Scharr blurred: ", blurred_image)
                cv2.waitKey(1)
            case 'Canny':
                # https://docs.opencv.org/3.4/da/d5c/tutorial_canny_detector.html
                threshold1 = self.widgets['threshold1'].get()
                src_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                img_blur = cv2.blur(src_gray, (3, 3))
                ratio = 3
                kernel_size = 3
                detected_edges = cv2.Canny(img_blur, threshold1, threshold1 * ratio, kernel_size)

                mask = detected_edges != 0
                dst = self.image * (mask[:,:,None].astype(self.image.dtype))

                cv2.imshow("Canny blurred: ", dst)
                cv2.waitKey(1)

    def demonstrate_blur(self):
        if self.widgets:
            for slider in self.widgets.values():
                slider.destroy()

        match str(self.filter):
            case "Gaussian":
                # ksize sigma x and y
                self.widgets['sigmaX'] = Scale(self.master, from_=0, to=300, resolution=20, tickinterval=10, label="SigmaX", orient=HORIZONTAL, command=lambda x: self.apply_blur())
                self.widgets['sigmaY'] = Scale(self.master, from_=0, to=300, resolution=20, tickinterval=10, label="SigmaX", orient=HORIZONTAL, command=lambda x: self.apply_blur())
                self.widgets['kSize'] = Scale(self.master, from_=1, to=31, resolution=2, label='ksize', orient=VERTICAL, command=lambda x: self.apply_blur())

                self.widgets['sigmaX'].pack()
                self.widgets['sigmaY'].pack()
                self.widgets['kSize'].pack()

            case "bilateral":
                self.widgets['d'] = Scale(self.master, from_=0, to=300, tickinterval=10, label="d", orient=HORIZONTAL, command=lambda x: self.apply_blur())
                self.widgets['SigmaSpace'] = Scale(self.master, from_=0, to=300, tickinterval=30, resolution=20, length=100, label="SigmaSpace", orient=HORIZONTAL, command=lambda x: self.apply_blur())
                self.widgets['SigmaColors'] = Scale(self.master, from_=0, to=300, tickinterval=30, resolution=20, length=100, label="SigmaColors", orient=HORIZONTAL, command=lambda x: self.apply_blur())

                self.widgets['d'].pack()
                self.widgets['SigmaSpace'].pack()
                self.widgets['SigmaColors'].pack()

                # d SigmaSpace and -Colors
            case "median":
                self.widgets['kSize'] = Scale(self.master, from_=1, to=31, tickinterval=2, label='ksize', orient=VERTICAL, command=lambda x: self.apply_blur())

                self.widgets['kSize'].pack()
                # ksize
            case "Sobel":
                #  ddepth, dx, dy, ksize, scale, delta
                self.widgets['dDepth'] = Scale(self.master, from_=0, to=4, resolution=1, label='dDepth', orient=VERTICAL, command=lambda x: self.apply_blur())
                self.widgets['dx'] = Scale(self.master, from_=0, to=1, tickinterval=1, label='dx', orient=VERTICAL, command=lambda x: self.apply_blur())
                self.widgets['dy'] = Scale(self.master, from_=0, to=1, tickinterval=1, label='dy', orient=VERTICAL, command=lambda x: self.apply_blur())
                self.widgets['kSize'] = Scale(self.master, from_=1, to=9, resolution=2, label='ksize', orient=VERTICAL, command=lambda x: self.apply_blur())

                self.widgets['dDepth'].pack()
                self.widgets['dx'].pack()
                self.widgets['dy'].pack()
                self.widgets['kSize'].pack()

            case "Scharr":
                #  ddepth, dx, dy, ksize, scale, delta
                self.widgets['dDepth'] = Scale(self.master, from_=0, to=4, resolution=1, label='dDepth', orient=VERTICAL, command=lambda x: self.apply_blur())
                self.widgets['dx'] = Scale(self.master, from_=0, to=1, tickinterval=1, label='dx', orient=VERTICAL, command=lambda x: self.apply_blur())
                self.widgets['dy'] = Scale(self.master, from_=0, to=1, tickinterval=1, label='dy', orient=VERTICAL, command=lambda x: self.apply_blur())
                self.widgets['kSize'] = Scale(self.master, from_=1, to=9, resolution=2, label='ksize', orient=VERTICAL, command=lambda x: self.apply_blur())

                self.widgets['dDepth'].pack()
                self.widgets['dx'].pack()
                self.widgets['dy'].pack()
                self.widgets['kSize'].pack()
            case 'Canny':
                # threshold1 threshold2, edges, apertureSize, L2Gradient
                self.widgets['threshold1'] = Scale(self.master, from_=0, to=100, resolution=1, label='threshold1', orient=VERTICAL, command=lambda x: self.apply_blur())
                self.widgets['threshold1'].pack()

demonstration = ImageFilteringDemonstration()
demonstration.register_callbacks(demonstration.demonstrate_blur)

mainloop()
