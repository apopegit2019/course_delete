import os
import shutil
import time
import sys


def webmnt():                                     # Gets webdav path from user.
    os.system('clear')
    wmount = ''
    while not os.path.isdir(wmount):
        print('This requires a webdav mount to the client\'s /couses folder \n')
        print('Enter a valid directory or press X to escape \n')
        wmount = raw_input('Path to webdav mount: ')
        if wmount == 'X' or wmount == 'x':
            sys.exit()
        elif os.path.isdir(wmount):
            break
        else:
            print('\n \nDirectory Not Found! Please try again. \n \n')
    return wmount


def feedlocal():                             # Gets feed file path from user.
    os.system('clear')
    feedloc = ''
    while not os.path.isfile(feedloc):
        print('Feed file should be a .txt format file with a list of the foldernames/courses you wish to remove. \n')
        print('Enter a valid file path or press X to escape \n')
        feedloc = raw_input('Provide path to feedfile: ')
        if feedloc == 'X' or feedloc == 'x':
            sys.exit()
        elif os.path.isdir(feedloc):
            break
        else:
            print('\n \n File Not Found! Please try again. \n \n')
    return feedloc


def loglocal():                             # Gets location user wants logs created in. Logs are created with current
    os.system('clear')                      # time to prevent overwriting previous versions.
    logloc = ''
    while not os.path.isdir(logloc):
        print('Two logs will be created, a log for the removals and one for errors. \n')
        logloc = raw_input('Please provide directory path for logging: ')
        print(logloc)
        if logloc == 'X' or logloc == 'x':
            sys.exit()
        elif os.path.isdir(logloc):
            break
        else:
            print('\n \n File Not Found! Please try again. \n \n')
    rmlname = 'rmlog' + time.strftime("%Y%m%d%H%M%S") + '.log'
    erlname = 'errlog' + time.strftime("%Y%m%d%H%M%S") + '.log'
    rmlog = os.path.join(logloc, rmlname)
    errlog = os.path.join(logloc, erlname)
    return rmlog, errlog


def confirm_paths(webdav, feed, rmlog, errlog):                     # Final check to confirm paths. Users can go back
    os.system('clear')                                              # to the creation function for any incorrect path
    print('Please confirm the following paths: \n \n')              # listed. 3 and 4 both amount to logloc()
    print('1. WebDav: %s \n' % webdav)
    print('2. Feed location: %s \n' % feed)
    print('3. Progress Log: %s \n' % rmlog)
    print('4. Error Log: %s \n' % errlog)
    conf = raw_input('Are these correct? (Y/N): ')
    if conf == 'Y' or conf == 'y':
        removal(webdav, feed, rmlog, errlog)
    else:
        cornum = raw_input('Which one is incorrect (1/2/3): ')
        if cornum == '1':
            webdav = webmnt()
            confirm_paths(webdav, feed, rmlog, errlog)
        elif cornum == '2':
            feed = feedlocal()
            confirm_paths(webdav, feed, rmlog, errlog)
        else:
            rmlog, errlog = loglocal()
            confirm_paths(webdav, feed, rmlog, errlog)


def rem_logs(loglocat, message):                                # simple logging takes a location argument and message
    with open(loglocat, 'a+') as n:                             # The location is a full path to the file
        n.write(time.ctime() + ' %s \n' % message)              # writes user readable time and message


def fleng(feed):                                      # feed length for progress comparison. current/fleng in logs.
    with open(feed, 'r') as a:
        length = len(a.readlines())
    return length


def safety_dance(webdav, dir, rmlog, errlog):           # Check to ensure we don't attempt to delete /courses
    rmdir = os.path.join(webdav, dir)                   # This is checked 2 ways. Comparing paths and
    if os.path.isdir(rmdir):                            # then checking for an empty line in the feed file.
        if os.path.normpath(rmdir) == os.path.normpath(webdav) or len(dir.rstrip()) == 0:  # If anyone comes up with
            rem_logs(rmlog, 'Blank feed line detected. See error log %s \n' % errlog)      # another check let me know
            rem_logs(errlog, 'Attempt to delete /courses detected! Skipping Entry! \n')    # I never ever want this to
            return 'no'                                                                    # happen. Ever.
        else:
            return rmdir
    else:
        rem_logs(errlog, 'Directory not found: %s \n' % rmdir)
        rem_logs(rmlog, 'Course %s not found. Please see error log: %s \n' % (dir, errlog))
        return 'no'


def finish(rmlog, errlog):                                   # A way to close out the show. A log summary and exit.
    os.system('clear')
    print('Feed file complete \n')
    print('Please see logs for more information \n')
    print('Removal log: %s \n' % rmlog)
    print('Error log: %s \n' % errlog)
    sys.exit()


def removal(webdav, feed, rmlog, errlog):           # open the feed, check the line for a blank or missing directory,
    feedlen = fleng(feed)                           # enter in a log line for progress, call to safety dance for
    current = 0                                     # not deleting /courses, and then delete and add log entry.
    with open(feed, 'r') as fd:                     # We also track progress through current/fleng()
        for line in fd:
            current += 1
            line = line.rstrip('\n')
            rem_logs(rmlog, 'Processing: %d/%d \n' % (current, feedlen))
            rem_logs(errlog, 'Processing: %d/%d \n' % (current, feedlen))
            rmdir = safety_dance(webdav, line, rmlog, errlog)
            if rmdir == 'no':
                pass
            else:
                for dir, file, path in os.walk(rmdir, topdown=False):
                    try:                                                 # try to remove - get exception or delete.
                        #  shutil.rmtree(dir)
                        rem_logs(rmlog, 'Successfully Deleted: %s \n' % dir)
                    except Exception as err:
                        rem_logs(errlog, 'Exception while processing: %s \n %s \n' % (dir, err))
    finish(rmlog, errlog)


def startup():                     # Clear the screen, get paths for webdav, feed file, logs location, confirm that
    os.system('clear')             # those directories/files are correct/exist with comfirm_paths()
    wddir = webmnt()
    feedloc = feedlocal()
    rmlog, errlog = loglocal()
    confirm_paths(wddir, feedloc, rmlog, errlog)


startup()
