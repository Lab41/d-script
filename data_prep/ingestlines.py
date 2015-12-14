import h5py
import scipy.misc
import numpy

writename = 'lines.hdf5'
form_path = 'data/forms/'

# Line HDF5 file creation
from_form = True
line_path = 'data/lines/'

forms_unproc = open('data/forms.txt','r').read().splitlines()
forms=[]
for line in forms_unproc:
    if line[0]!='#':
        forms.append(line)

# Create two dictionaries:
#  1. authors -> forms
#  2. forms -> authors
author2form = {}
form2author = {}
for form in forms:
    the_author = form.split()[1]
    the_form = form.split()[0]
    if author2form.has_key( the_author ):
        author2form[the_author].append( the_form )
    else:
        author2form[the_author] = [ the_form ]
    form2author[the_form] =   the_author

# Make an hdf5 file for all the lines
#  1. Get read from the original image
#  2. Write image section to HDF5 file

author_lines_file='author_lines.hdf5'
lines_file='lines.hdf5'

lines_unproc = open('data/lines.txt','r').read().splitlines()
lines=[]
al_fout = h5py.File(author_lines_file,'w')
l_fout = h5py.File(lines_file,'w')
author_groups = {}

# Create groups for HDF5 to write out
for the_author in author2form.keys():
    author_groups[the_author] = al_fout.create_group(the_author) 
for line in lines_unproc:
    if not line[0]=='#':
        the_line = line.split()
        the_form = the_line[0].split('-')
        the_form = '-'.join((the_form[0], the_form[1]))
        the_author = form2author[the_form]
        if from_form:
            (x,y,w,h) = [int(xywh) for xywh in the_line[4:8]]
            the_image = scipy.misc.imread( form_path+the_form+'.png' )
            the_box = the_image[x:x+w,y:y+h]
        else:
            the_box = scipy.misc.imread( line_path+the_line[0].split('-')[0]+'/'+
                                         the_form+'/'+the_line[0]+'.png' )
        author_groups[the_author].create_dataset( the_line[0], data=the_box.astype(numpy.uint8))
        data_group = l_fout.create_dataset( the_line[0], data=the_box.astype(numpy.uint8) )
        data_group.attrs.create( 'author', the_author )

l_fout.close()
al_fout.close()
