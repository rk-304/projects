*Flat hirarchy is intentional, easier to debug and collaborate*  
Files in logical order:

Steps:

1. Extract folder:
    - run scraping scripts
2. Transform folder:
    - run clean_fbref, clean_transfermarkt, match_fbref_to_transfermarkt
    - Tableau: run fbref_transfermarkt_merge.tflx (fbref_player_statistics_fuzzy + transfermarkt_player_marketvalue_cleaned = fbref_transfermarkt_merged)  
    - run clean_tableau_output to produce final_merged
3. Answer questions
    - etl_questions_answers (uses final_merged to answer the project questions)

---
todo:
Mby cleaning in python (done)
Implementation in tableau (done)
Documentation (requirements?), answer questions from ETL plan (done)
load to sql (?)


Comments from bruno:
// Tableau with high level documentation
Delete euro values intentionally and try to put them in seprate file: 'error records'

