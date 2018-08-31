from __future__ import print_function
def eng_window(trials,
               catch=False,
               preview = False,
               change_1 = 0.75,
               change_2 = 0.15,
               pre_change = False,
               all_pre_change = False, 
               meta = False, 
               wide_model=False, 
               model = False):
    eng_st = []
    eng_end = []
    change_image_list = []
    if pre_change == True:
        pre_eng_st = []
        pre_eng_end = []
        
    for i in range(len(trials.trial)):
        if ((wide_model == True)|(model == True)):
            last_initial_image =(trials.change_time[i] - change_1)
            eng_st.append(last_initial_image)
            resp_window_start = (trials.change_time[i] + change_2)
            eng_end.append(resp_window_start)
        
        elif catch == False:
            if trials.trial_type[i] == 'go':
                last_initial_image =(trials.change_time[i] - change_1)
                eng_st.append(last_initial_image)
                resp_window_start = (trials.change_time[i] + change_2)
                eng_end.append(resp_window_start) 
                if pre_change ==True:
                        pre_last_initial_image =(last_initial_image - 0.75)
                        pre_eng_st.append(pre_last_initial_image)
                        pre_resp_window_start = (resp_window_start - 0.75)
                        pre_eng_end.append(pre_resp_window_start)

                        if all_pre_change == True:
                            trial_length =  trials.trial_length[i]
                            repeats = int(trial_length / 0.75)
                            way_back = 1
                            while repeats > 3:
                                pre_last_initial_image =(last_initial_image - (0.75+way_back))
                                pre_eng_st.append(pre_last_initial_image)
                                pre_resp_window_start = (resp_window_start - (0.75+way_back))
                                pre_eng_end.append(pre_resp_window_start)
                                repeats -=1
                                way_back += 1
            elif ((trials.trial_type[i] == 'catch') and (trials.response_type[i] == 'CR')):
                success= True   
                if meta == True:
                    change_image = trials.change_image_name[i]
                    change_image_list.append(change_image)
        if catch== True:
            last_initial_image =(trials.change_time[i] - change_1)
            eng_st.append(last_initial_image)
            resp_window_start = (trials.change_time[i] + change_2)
            eng_end.append(resp_window_start) 
    
    if preview == True:
        
        print("preview: ", eng_st[:3], eng_end[:3], "length is: ", len(eng_st))
    if pre_change == True:
        return(eng_st, eng_end, pre_eng_st, pre_eng_end)
    if meta == True:
        return(eng_st, eng_end, change_image_list)
    else:
        return(eng_st, eng_end)

def wide_engage_binary(trials,
                       trials_before_and_after=1,
                       num_successes=2,
                       preview = False,
                       catch = False):
    
    success_list = []

    #create column in dataframe: success
    for i in range(len(trials.trial)):
        if ((trials.trial_type[i] == 'go') and (trials.response_type[i] == 'HIT')):
            #create success column
            success = True
            
        elif catch == True:
            if ((trials.trial_type[i] == 'catch') and (trials.response_type[i] == 'CR')):
                success= True
        else:
            success = False

        success_list.append(success)
    trials['success'] = success_list
    
    width= trials_before_and_after
    wide_engage_binary = []

    for i in range(len(trials.trial)):
        #want to look at window from one trial before to one trial after. unless first of last trial, then there isnt a before or after trial respectively
        if i <= width:
            pre = 0
            post = (i+width)
        elif i + width >= len(trials.trial):
            pre= (i-width)
            post= len(trials.trial)
        else:
            pre= (i-width)
            post= (i+width)
        trialwindow = (trials[pre:(post+1)])#-1 because non-inclusive
        successonly_list = trialwindow.success[trialwindow.success == True]
        if len(successonly_list) >= num_successes:
            performing_task = 1
        else:
            performing_task = 0
        wide_engage_binary.append(performing_task)  
    #adds wide eng binary as a column in dataset
    trials["wide_engage_binary"]= wide_engage_binary

    #prints 4 columns to check your work
    if preview == True:
        
        print(trials[['trial_type','response_type','success', 'wide_engage_binary']])
    return(wide_engage_binary)