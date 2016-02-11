import numpy as np
import running_stats


def decide_cutoff(run_med, run_med_max, median, half_max, drop_size=0, run_size=0):
    run_count = 0
    passed_max_flag = False
    inc_run_flag = False
    keep_counting_flag = False
    for i in range(0,len(run_med)):
        if run_med[i] == run_med_max:
            passed_max_flag = True
        else:
            #good for non-empty backgrounds; 75 is heuristic for medians with whitespace backgrounds
            if median > 75:
                if passed_max_flag and run_med[i] < (median - drop_size) :
                    keep_counting_flag = True
                if run_med[i] >= half_max:
                    keep_counting_flag = False
                    run_count = 0

                if keep_counting_flag and passed_max_flag:
                    run_count += 1
            #good for clean clear backgrounds
            else:
                if passed_max_flag and run_med[i] < 50 :
                    keep_counting_flag = True
                if run_med[i] >= half_max / 2.0:
                    keep_counting_flag = False
                    run_count = 0

                if keep_counting_flag and passed_max_flag:
                    run_count += 1

        if run_count >= run_size:
            break
    return i

def crop_using_heatmap(orig_im, heat2d):
    heat1d = heat2d.sum(axis=1)
    max_raw = max(heat1d)
    
    #running median window size
    window_size = 50
    run_med = running_stats.RunningMedian(heat1d, window_size)
    run_med_max = np.zeros(len(run_med)) + max(run_med)
    median_arr = np.zeros(len(run_med)) + np.median(heat1d)
    
    #max_raw / 2.0 == experimentally-determined (e.d.) peak representing the re-encounter of text, probably in the signature line
    #50 == with rule-lined paper, dropping below the median by some e.d. amount (50) probably means that we're in non-text space
    #400 after this many rows of being in e.d. non-text space, cut off the rest
    i = decide_cutoff(run_med, max(run_med), np.median(heat1d), max_raw / 2.0, 50, 400)
    return orig_im[0:i,:], i

def create_heatmap(im):
    im = 1.0 - im/255.0
    heat2d = np.zeros(im.shape)
    def conv_1d(image_heat_tup):
        for i in xrange(len(image_heat_tup[0])):
            image_heat_tup[1][i,:] = np.convolve(image_heat_tup[0][i], np.ones(56), mode='same')
        return (image_heat_tup[0].T, image_heat_tup[1].T)

    im, heat2d = conv_1d(conv_1d((im, heat2d)))
    return heat2d

def create_cropped_np_arr_from_orig(np_arr_input_im):
    heat2d = create_heatmap(np_arr_input_im)
    cropped, i = crop_using_heatmap(np_arr_input_im, heat2d)
    return cropped
    