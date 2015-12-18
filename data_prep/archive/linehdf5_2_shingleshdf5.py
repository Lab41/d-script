import h5py
import random
import numpy as np

random.seed(1024) # So that data create is repeatable


def create_shingles(original_line, shingle_dim=(120,120), num_shingles=20):
    '''
    Take in a line and return a 3d array that of dimensionality (num_shingles,shingle_dim[0], shingle_dim[1])
    '''
    (height, width) = original_line.shape

    max_x = width - shingle_dim[1]
    output_data = np.zeros((num_shingles, shingle_dim[0], shingle_dim[1]), dtype=np.uint8)

    for i in range(num_shingles):
        x_start = random.randint(0, max_x)
        #print max_x, x_start,x_start+shingle_dim[1]
        output_data[i] = original_line[0:shingle_dim[0], x_start:x_start+shingle_dim[1]]
    return output_data


def process_file(input_file, output_file):
    '''
    Read in hdf5 file and output data create n shingles per line
    '''
    fIn = h5py.File(input_file, 'r')
    fOut = h5py.File(output_file, 'w')

    for author in fIn.keys():
        author_grp = fOut.create_group(author)
        for form in fIn[author].keys():
            print author, form
            form_grp = author_grp.create_group(form)
            for line in fIn[author][form].keys():
                if fIn[author][form][line].shape[1] > 123: # Suppress short lines?
                    output_dataset = create_shingles(fIn[author][form][line])
                    form_grp.create_dataset(line, data=output_dataset)
    fOut.close()

def main():
    process_file('raw_lines.hdf5', 'output_shingles_sparse.hdf5')

if __name__ == "__main__":
    main()