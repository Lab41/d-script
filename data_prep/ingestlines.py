import h5py
import scipy.misc
import numpy

writename = 'lines.hdf5'

# Line HDF5 file creation
from_form = True
form_path = 'data/forms/'
line_path = 'data/lines/'
word_path = 'data/words/'

### IAM DATASET ###

# Do the mapping from form to author and from author to form
if False:
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
if False:
    author_lines_file='author_lines_debug.hdf5'
    lines_file='lines_debug.hdf5'

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
                the_box = the_image[y:y+h, x:x+w]
            else:
                the_box = scipy.misc.imread( line_path+the_line[0].split('-')[0]+'/'+
                                             the_form+'/'+the_line[0]+'.png' )
            author_groups[the_author].create_dataset( the_line[0], data=the_box.astype(numpy.uint8))
            data_group = l_fout.create_dataset( the_line[0], data=the_box.astype(numpy.uint8) )
            data_group.attrs.create( 'author', the_author )

            break
            
    l_fout.close()
    al_fout.close()

# Make an hdf5 file for all the words
#  1. Get read from original image
#  2. Write image section to HDF5 file
if False:
    author_words_file='author_words.hdf5'
    words_file = 'words.hdf5'
    
    words_unproc = open('data/words.txt','r').read().splitlines()
    lines=[]
    aw_fout = h5py.File(author_words_file,'w')
    w_fout = h5py.File(words_file,'w')
    author_groups = {}

    # Create groups for HDF5 to write out
    for the_author in author2form.keys():
        author_groups[the_author] = aw_fout.create_group(the_author) 
    for line in words_unproc:
        if not line[0]=='#':
            the_line = line.split()
            the_form = the_line[0].split('-')
            the_form = '-'.join((the_form[0], the_form[1]))
            the_author = form2author[the_form]
            if from_form:
                (x,y,w,h) = [int(xywh) for xywh in the_line[3:7]]
                the_image = scipy.misc.imread( form_path+the_form+'.png' )
                the_box = the_image[y:y+h,x:x+w]
            else:
                the_box = scipy.misc.imread( word_path+the_line[0].split('-')[0]+'/'+
                                             the_form+'/'+the_line[0]+'.png' )
            author_groups[the_author].create_dataset( the_line[0], data=the_box.astype(numpy.uint8))
            data_group = w_fout.create_dataset( the_line[0], data=the_box.astype(numpy.uint8) )
            data_group.attrs.create( 'author', the_author )

    w_fout.close()
    aw_fout.close()

# ATTENTION ATTENTION ATTENTION: THIS CODE WILL NOT WORK WITH from_form ON.
# As it turns out, there is NO x,y,h,w information in files.txt file, therefore, the "from_form"
# option is irrelevant. There must be some way to identify the bottom half of the document.
# ATTENTION ATTENTION ATTENTION: THIS CODE WILL NOT WORK WITH from_form ON.
if False:
    author_form_file='author_forms.hdf5'
    form_file = 'forms.hdf5'
    
    form_unproc = open('data/forms.txt','r').read().splitlines()
    lines=[]
    af_fout = h5py.File(author_form_file,'w')
    f_fout = h5py.File(form_file,'w')
    author_groups = {}

    # Create groups for HDF5 to write out
    for the_author in author2form.keys():
        author_groups[the_author] = af_fout.create_group(the_author) 
    for line in form_unproc:
        if not line[0]=='#':
            the_line = line.split()
            the_form = the_line[0]
            the_author = form2author[the_form]
            if the_author != the_line[1]:
                print "ERROR: The author dictionary and the original form do not match"
            if from_form:
                (x,y,w,h) = [int(xywh) for xywh in the_line[4:8]]
                the_image = scipy.misc.imread( form_path+the_form+'.png' )
                the_box = the_image[y:y+h,x:x+w]
            else:
                the_box = scipy.misc.imread( word_path+the_line[0].split('-')[0]+'/'+
                                             the_form+'/'+the_line[0]+'.png' )
            author_groups[the_author].create_dataset( the_line[0], data=the_box.astype(numpy.uint8))
            data_group = f_fout.create_dataset( the_line[0], data=the_box.astype(numpy.uint8) )
            data_group.attrs.create( 'author', the_author )

    f_fout.close()
    af_fout.close()

### ICDAR 2013 DATASET ###
import os, sys
from PIL import Image
def readtif(imname):
    im = Image.open(imname)
    return numpy.array( im.getdata(), numpy.uint8 ).reshape(im.size[1], im.size[0])

if True:
    author_words_file='author_icdar.hdf5'
    words_file = 'icdar.hdf5'

    ### ATTENTION. If you want to extract evaluation dataset, change "benchmarking" to that
    icdar13path = 'icdar13/benchmarking/'
    icdar13exdir = os.listdir(icdar13path)

    ai_fout = h5py.File(author_words_file,'w')
    i_fout = h5py.File(words_file,'w')
    author_groups = {}

    # Create groups for HDF5 to write out
    for the_file in icdar13exdir:
        the_author=the_file.split('_')[0]
        if not author_groups.has_key(the_author):
            author_groups[the_author] = ai_fout.create_group(the_author)
        # the_image = scipy.misc.imread( icdar13path+'/'+the_file )
        the_image = readtif( icdar13path+'/'+the_file )
        author_groups[the_author].create_dataset( the_file, data=the_image.astype(numpy.uint8) )
        data_group = i_fout.create_dataset( the_file, data=the_image.astype(numpy.uint8) )
        data_group.attrs.create( 'author', the_author )
        print "Finished image read and write of file "+the_file+" to "+author_words_file+" and "+words_file
        sys.stdout.flush()

    i_fout.close()
    ai_fout.close()
    

