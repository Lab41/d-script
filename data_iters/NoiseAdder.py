from PIL import Image, ImageOps, ImageMath, ImageEnhance

import numpy as np
import matplotlib.pyplot as plt
import glob

class NoiseAdder:

    @staticmethod
    def nmec_post(x, **kwargs):
        stainer = NoiseAdder()
        x = stainer.add_noise(Image.fromarray(x, 'L'), kwargs["shingle_dim"], kwargs["rng"])
        return x
    
    def __init__(self, noisedir, grayscale=True):
        self.noisedir = noisedir
        imagenames = glob.glob(noisedir+'/*.*')
        if grayscale:
            self.images = [ Image.open(imname).convert('L') for imname in imagenames ]
        else:
            self.images = [ Image.open(imname).convert('RGBA') for imname in imagenames ]
        # self.stain = Image.open("/work/johnm/d-script/data_iters/coffee_stain_1.jpg").convert('RGBA')
    
    def add_noise(self, shingle_img, shingle_dim, rng):
        
        #assumes RGBA stain > shingle in both dim
        #assumes shingle is 'L'
        
        # Convert the image
        shingle_img2 = Image.fromarray(np.uint8( shingle_img), 'L')
        
        # Choose a random image and a random section inside of the image
        stain_img = self.images[ rng.randint( len(self.images )) ]
        stain_w, stain_h = stain_img.size
        max_rand_x = stain_w - shingle_dim[1]
        max_rand_y = stain_h - shingle_dim[0]
        startx = rng.randint(max_rand_x)
        starty = rng.randint(max_rand_y)
        rand_cropped_stain = stain_img.crop((startx, starty, startx+shingle_dim[1], starty+shingle_dim[0]))
        rand_bright = rng.random_sample()+1.0
        
        # Invert both images and add them together
        rand_faded_stain = ImageEnhance.Brightness(rand_cropped_stain).enhance(rand_bright).convert('L')
        stain_inv = ImageOps.invert(rand_faded_stain)
        shingle_inv = ImageOps.invert(shingle_img2)
        return ImageOps.invert(ImageMath.eval("convert(min(a+b, 255), 'L')", a=stain_inv, b=shingle_inv))
    
    def add_noise_np(self, shingle_img, shingle_dim, rng):
        
        #assumes RGBA stain > shingle in both dim
        #assumes shingle is 'L'
        assert shingle_img is not None
        assert shingle_dim is not None
        assert rng is not None
        
        # Choose a random image and a random section inside of the image
        stain_img = self.images[ rng.randint( len(self.images) ) ]
        stain_w, stain_h = stain_img.size
        max_rand_x = stain_w - shingle_dim[1]
        max_rand_y = stain_h - shingle_dim[0]
        startx = rng.randint(max_rand_x)
        starty = rng.randint(max_rand_y)
        
        # Crop the image
        rand_cropped_stain = stain_img.crop((startx, starty, startx+shingle_dim[1], starty+shingle_dim[0]))
        
        # Invert both images and add them together
        shingle_inv = (255 - shingle_img) # .astype(np.uint16)
        stain_inv = (255 - np.asarray( rand_cropped_stain )) #.astype(np.uint16)
        final_img = shingle_inv+stain_inv
        np.place(final_img, final_img > 255, 255)
        
        assert final_img is not None

        # Invert image back to 255
        final_img = 255 - final_img
        
        return final_img

    def add_noise_batch(self, shingle_imgs, shingle_dim, rng):
        
        #assumes RGBA stain > shingle in both dim
        #assumes shingle is 'L'
        assert shingle_imgs is not None
        assert shingle_dim is not None
        assert rng is not None
        
        randseq = rng.randint( len(self.images), size=len(shingle_imgs) )
        return_images = np.zeros( shingle_imgs.shape )
        
        # Choose a random image and a random section inside of the image
        for i, randnoise in enumerate(randseq):
            stain_img = self.images[ randnoise ]
            stain_w, stain_h = stain_img.size
            max_rand_x = stain_w - shingle_dim[1]
            max_rand_y = stain_h - shingle_dim[0]
            startx = rng.randint(max_rand_x)
            starty = rng.randint(max_rand_y)
        
            # Crop the image
            rand_cropped_stain = stain_img.crop((startx, starty, startx+shingle_dim[1], starty+shingle_dim[0]))
        
            # Invert both images and add them together
            shingle_inv = (255 - shingle_imgs[i]) # .astype(np.uint16)
            stain_inv = (255 - np.asarray( rand_cropped_stain )) #.astype(np.uint16)
            final_img = shingle_inv+stain_inv
            np.place(final_img, final_img > 255, 255)
        
            assert final_img is not None

            # Invert image back to 255
            return_images[i] = 255 - final_img
        
        return return_images


