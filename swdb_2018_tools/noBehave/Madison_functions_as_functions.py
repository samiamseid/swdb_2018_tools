def eng_window(trials, catch=False, preview = False, change_1 = 0.75, change_2 = 0.15):
    eng_st = []
    eng_end = []

    for i in range(len(trials.trial)):
        if catch == False:
            if trials.trial_type[i] == 'go':
                last_initial_image =(trials.change_time[i] - change_1)
                eng_st.append(last_initial_image)
                resp_window_start = (trials.change_time[i] + change_2)
                eng_end.append(resp_window_start) 
            else:
                continue
        if catch== True:
            last_initial_image =(trials.change_time[i] - change_1)
            eng_st.append(last_initial_image)
            resp_window_start = (trials.change_time[i] + change_2)
            eng_end.append(resp_window_start) 
    
    if preview == True:
        
        print("preview: ", eng_st[:3], eng_end[:3], "length is: ", len(eng_st))
        
    return(eng_st, eng_end)

    def singletrial_eng_binary(trials, catch=False, preview = False):
    eng_binary= []
    for i in range(len(trials.trial)): #problem if remove ctch trials, differnt length?
        if ((trials.trial_type[i] == 'go') and (trials.response_type[i] == 'HIT')):
            success = 1
        elif((trials.trial_type[i] == 'go') and (trials.response_type[i] == 'MISS')):
            success = 0
        elif catch==False:
            continue
        elif catch == True:
            if ((trials.trial_type[i] == 'catch') and (trials.response_type[i] == 'CR')):
                success = 1
            elif((trials.trial_type[i] == 'catch') and (trials.response_type[i] == 'FA')):
                success = 0
            
        eng_binary.append(success)
        
    if preview == True:
        print("preview: ", eng_binary[:20], "length is: ", len(eng_binary)) 
        
    return(eng_binary)

 #wide engagement binary for 2 successes in 3 consecutive trials 
#1 out in each direction
#includes success rate df function

def wide_engage_binary(trials, trials_before_and_after=1, num_successes=2, preview = False):
    
    trials['success']= 'x'

    #create column in dataframe: success
    for i in range(len(trials.trial)):
        if ((trials.trial_type[i] == 'go') and (trials.response_type[i] == 'HIT')):
            #create success column
            success = True
        elif ((trials.trial_type[i] == 'catch') and (trials.response_type[i] == 'CR')):
            success= True
        else:
            success = False

        trials.success[i]= success #should be bool
    
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
    return wide_engage_binary   