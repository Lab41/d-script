import h5py
import random
import numpy as np
import pickle
import scipy.misc
import os
from scipy.sparse import csr_matrix

def get_sample(input_file, output_file, num_authors=40, num_forms_per_author=15):
    '''
    Create a small set of training data from the larger hdf5 file. Limit output to authors with a sufficient number
    of forms

    Output:
      A pickle file containing a dictionary of the format {author:[csr_matrix() ..] }
    '''
    fIn = h5py.File(input_file, 'r')
    authors = []
    for author in fIn.keys():
        if len(fIn[author]) > num_forms_per_author:
            authors.append(author)

    if len(authors) < num_authors:
        raise ValueError("There are only %d authors with more than %d forms"%(len(authors), num_forms_per_author))

    author_info = {}
    for author in authors[:num_authors]: # Limit us to num_authors
        shingles  = []
        forms = list(fIn[author])
        for form in forms[:num_forms_per_author]: # Limit us to num_form_per_author
            print author, form
            for line_name in fIn[author][form].keys():
                for shingle in range(fIn[author][form][line_name].shape[0]):
                    x = fIn[author][form][line_name][shingle, :,:]
                    x = 1.0 - x/255.0
                    x[x< 1e-3] = 0
                    #shingles.append(fIn[author][form][line_name][shingle, :,:])
                    shingles.append(csr_matrix(x))

        author_info[author] = shingles

    fOut = open(output_file, 'w')
    pickle.dump(author_info, fOut, protocol=pickle.HIGHEST_PROTOCOL)
    fOut.close()

def get_sample_png(input_file, output_folder, num_authors=5, num_forms_per_author=2):
    '''
    Create a small set of training data from the larger hdf5 file. Limit output to authors with a sufficient number
    of forms

    Output:
      A directory with the structure output_folder/author/(png files)
    '''
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    fIn = h5py.File(input_file, 'r')
    authors = []
    for author in fIn.keys():
        if len(fIn[author]) > num_forms_per_author:
            authors.append(author)

    if len(authors) < num_authors:
        raise ValueError("There are only %d authors with more than %d forms"%(len(authors), num_forms_per_author))

    for author in authors[:num_authors]: # Limit us to num_authors
        author_folder = os.path.join(output_folder, author)
        os.mkdir(author_folder)
        forms = list(fIn[author])
        for form in forms[:num_forms_per_author]: # Limit us to num_form_per_author
            print author, form
            for line_name in fIn[author][form].keys():
                for shingle in range(fIn[author][form][line_name].shape[0]):
                    file_name = '%s_%s.png'%(line_name.split('.')[0], str(shingle))
                    scipy.misc.imsave(os.path.join(author_folder, file_name), fIn[author][form][line_name][shingle, :,:])

def main():
    #get_sample_png('output_shingles.hdf5', 'output_shingles_sample')
    get_sample('output_shingles.hdf5', 'output_shingles_sparse.pkl')

if __name__ == "__main__":
    main()