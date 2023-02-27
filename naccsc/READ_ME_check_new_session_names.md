Debugging levels: 
Debug level: correct session label
Info level: renamed session label
Warning level: incorrectly formatted subject label & insufficient information for full renaming

Fuctions:
main()
    check_correct(sessionlabellist, subject, date)
    rename_session(session, subject, date)
email_log(filepath)
parse_log(filepath)



parsing log_check_new_session_names_{current_time}.txt
get list of renamed sessions with:
cat log_check_new_session_names_2023-02-13T16_27_33.txt | grep INFO | cut -d ":" -f 3,4
get list of items needing attention with:
cat log_check_new_session_names_2023-02-13T16_27_33.txt | grep WARNING