#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is a very ad-hoc script to delete any number of tweets.

What you do is put all the tweets in the file which is declared at the top of main
	fileToDelete = 'tweets_to_delete.txt'
	
This uses: https://github.com/bear/python-twitter 
 To use it put all the tweets you want to delete in a file with one line per twitter id. 
 In the script the name I'm using is: 'tweets_to_delete.txt' 
 
 You also have to put your consumer and access token keys and secrets in the file.  

It's a python3 script and you will have to have python-twitter installed. 
https://github.com/bear/python-twitter  has installation instructions. 

I'm not sure of twitter's rate limiting on deletion so I was conservative with it. 
It deletes 1250 tweets at a time then sleeps for an hour.  It deletes roughly 25k+ tweets a day. 

This script also stores the tweets that you delete here at: deletion_results.txt.
I don't think it includes children of deleted tweets so don't rely on it for a primary backup of deleted tweets.

If you are feeling adventurous go ahead and bump that up and let me know about where you run into rate limiting issues.

"""
import twitter
import traceback
import sys
import time



class DeleteStatusFromFile():

    MAX_CALLS_PER_HOUR = 1250
    SECONDS_IN_AN_HOUR = 3600

    LOGFILE = 'data_from_deletion.txt'
    LOGDELETERESULTS = 'deletion_results.txt'

    def __init__(self):
        self.api_call_count = 0
        self.total_statuses = 0
        self.total_favorites =0 
        self.status_deleted = 0
        self.favorites_deleted =0
        
    api = twitter.Api(consumer_key='yoursuperSecretConsumerKey',
                    consumer_secret='yoursuperSecretConsumerSecret',
                    access_token_key='yoursuperSecretAccessToken',
                    access_token_secret='yoursuperSecretAccessSecret')

    def increment_or_sleep(self):
        '''
        Increments the call count or sleeps if the max call count per hour
        has been reached
        '''
        self.api_call_count = self.api_call_count + 1
        if self.api_call_count > self.MAX_CALLS_PER_HOUR:
            sleepytime = time.strftime("%Y%m%d-%H%M%S")
            with open(DeleteStatusFromFile.LOGFILE, 'a') as f:
                            f.writelines("going to sleep at: ")
                            f.write(str(sleepytime) )
                            f.write('\n')
            time.sleep(self.SECONDS_IN_AN_HOUR)
            wakeytime = time.strftime("%Y%m%d-%H%M%S")
            with open(DeleteStatusFromFile.LOGFILE, 'a') as f:
                            f.writelines("waking up at: ")
                            f.write(str(wakeytime) )
                            f.write('\n')
            self.api_call_count = 0   
        return    

    def delete_status(self, statusid, api):
        succeeded = True
        try:
            result = api.DestroyStatus(statusid,trim_user=True)
            print(result)
            with open(DeleteStatusFromFile.LOGDELETERESULTS, 'a') as f:
                            f.writelines("delete result: ")
                            f.write(str(result) )
                            f.write('\n')   
        except Exception as err:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tbe = traceback.TracebackException(
                exc_type, exc_value, exc_tb,
            )
            succeeded = False
            print('\nunable to delete:', statusid)
            print(''.join(tbe.format_exception_only()))
            with open(DeleteStatusFromFile.LOGFILE, 'a') as f:
                            f.writelines("unable to delete: ")
                            f.write(str(statusid) )
                            f.write('\n')    
            with open(DeleteStatusFromFile.LOGDELETERESULTS, 'a') as f:
                            f.writelines("unable to delete: ")
                            f.write(str(statusid) )
                            f.write('\n') 

        return succeeded

    def delete_from_file(self, filename):
        try:
            with open(filename, 'r') as fp:
                cnt = 0
                for line in fp:
                    print("line {} contents {}".format(cnt, line))
                    self.total_statuses = self.total_statuses +1
                    if DeleteStatusFromFile.delete_status(self,line.strip(),DeleteStatusFromFile.api):
                        self.status_deleted = self.status_deleted +1
                    cnt += 1
                    self.increment_or_sleep()

        except Exception as err:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tbe = traceback.TracebackException(
                exc_type, exc_value, exc_tb,
            )
            print(''.join(tbe.format()))
        print("Statuses Deleted" , self.status_deleted)
        print("Out of Total Statuses", self.total_statuses)
        with open(DeleteStatusFromFile.LOGFILE, 'a') as f:
                            f.writelines("Statuses Deleted ")
                            f.write(str(self.status_deleted) )
                            f.write('\n')    
                            f.writelines("Out of total Statuses")
                            f.write(str(self.total_statuses) )
                            f.write('\n')    
        return




#Here is the start of program's execution.
if __name__ == "__main__":
    fileToDelete = 'tweets_to_delete.txt'
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print (timestr)
    purgatory = DeleteStatusFromFile() 
    purgatory.LOGFILE = 'data_from_deletion.txt'
    with open(purgatory.LOGFILE, 'a') as f:
        f.write('\n')    
        f.writelines("start time: ")
        f.write(str(timestr) )
        f.write('\n')


    purgatory.delete_from_file(fileToDelete)
    
    timestopped = time.strftime("%Y%m%d-%H%M%S")
    print("time started",timestr)
    print("time stopped", timestopped)
    with open(purgatory.LOGFILE, 'a') as f:
        f.write('\n')    
        f.writelines("time stopped: ")
        f.write(str(timestopped) )
        f.write('\n')
   
