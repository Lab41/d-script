from PIL import Image, ImageOps, ImageMath, ImageEnhance

# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt


class CoffeeStainer:
    @staticmethod
    def nmec_post(x, **kwargs):
        stainer = CoffeeStainer()
        x = stainer.get_rand_stain_w_random_brightness(Image.fromarray(x, 'L'), kwargs["shingle_dim"], kwargs["rng"])
        return x

    def __init__(self):
        self.stain = Image.open("./coffee_stain_1.jpg").convert('RGBA')

    def get_rand_stain_w_random_brightness(self, shingle_img, shin_dim, rng):
        # assumes RGBA stain > shingle in both dim
        # assumes shingle is 'L'
        assert shingle_img is not None
        assert shin_dim is not None
        assert rng is not None
        stain_img = self.stain
        stain_w, stain_h = stain_img.size
        max_rand_x = stain_w - shin_dim[1]
        max_rand_y = stain_h - shin_dim[0]
        startx = rng.randint(max_rand_x)
        starty = rng.randint(max_rand_y)
        rand_cropped_stain = stain_img.crop((startx, starty, startx + shin_dim[1], starty + shin_dim[0]))
        rand_bright = rng.random_sample() + 1.0
        rand_faded_stain = ImageEnhance.Brightness(rand_cropped_stain).enhance(rand_bright).convert('L')
        stain_inv = ImageOps.invert(rand_faded_stain)
        shingle_inv = ImageOps.invert(shingle_img)
        assert stain_inv is not None
        assert shingle_inv is not None
        final_img = np.asarray(ImageOps.invert(ImageMath.eval("convert(a+b, 'L')", a=stain_inv, b=shingle_inv)))
        assert final_img is not None
        return final_img
