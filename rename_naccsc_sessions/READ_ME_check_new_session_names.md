check_new_session_names.py runs weekly via cron job set up by Emily on bscsub cluster. Program checks that new flywheel session names have the correct format and fixes them, if enough information is present. Log is emailed to Emily, who manually fixes any sessions with unknown information.

### Fuctions
- main()
  - check_correct(sessionlabellist, subject, date)
  - rename_session(session, subject, date)
- email_log(filepath)
- parse_log(filepath)

### Debugging levels
- Debug level: correct session label
- Info level: renamed session label
- Warning level: incorrectly formatted subject label & insufficient information for full renaming

### Parsing each run's log file
get list of renamed sessions with: `cat log_check_new_session_names_{current_time}.txt | grep INFO | cut -d ":" -f 3,4`
get list of items needing attention with: `cat log_check_new_session_names_{current_time}.txt | grep WARNING`

### Log of all session names changed by check_new_session_names.py
all_fw_session_renames.txt: old name:new name:date changed