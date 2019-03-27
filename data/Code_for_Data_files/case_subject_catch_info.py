from collections import Counter
import re
import json

All_Cases = {} #Dict. used to store all cases info, here file_name is used as a key

with open("subject_keywords.txt", encoding="utf8") as cases:
    for case in cases:
        if not(case[0] == '1' or case[0] == '2'):
            continue

        file_name, case_title, sub_catch = case.split('-->')

        if (sub_catch == '\n'):
            subjects = []
            catchwords = []
        else:
            subjects, catchwords = sub_catch.split('$$$')
            if (len(subjects) > 1):
                subjects = subjects[1:].split('; ')
                subjects = [x.lower() for x in subjects]
            else:
                subjects = []

            if (catchwords == '\n'):
                catchwords = []
            else:
                catchwords = catchwords[1:len(catchwords)-1].split(', ')
                catchwords = [x.lower() for x in catchwords]
                # if file_name == '1987_C_65':
                #     print(catchwords)
        corrected_catchwords = []
        prev = curr = ''
        for catch in catchwords:
            curr = catch
            match = re.match(r'.*([1-2][0-9]{3})', curr[:4])
            if match is not None:
                new = prev + ', ' + curr
                prev = ''
                corrected_catchwords.append(new)
            else:
                if not(prev == ''):
                    corrected_catchwords.append(prev)
                prev = curr
        if not(prev == ''):
            corrected_catchwords.append(prev)

        All_Cases[file_name] = {}
        All_Cases[file_name]['case_title'] = case_title
        All_Cases[file_name]['subjects'] = subjects
        All_Cases[file_name]['catchwords'] =corrected_catchwords

#print(All_Cases['2017_S_104'])
#print(All_Cases['1987_C_65'])

Case_to_subjects = {}
subject_to_case = {}
Case_to_catchwords = {}
catchword_to_case = {}
year_to_case = {}

for case in All_Cases:
    Case_to_subjects[case] = All_Cases[case]['subjects']
    Case_to_catchwords[case] = All_Cases[case]['catchwords']

    for subject in All_Cases[case]['subjects']:
        if not(subject in subject_to_case):
            subject_to_case[subject] = []
        subject_to_case[subject].append(case)

    for catchword in All_Cases[case]['catchwords']:
        if not(catchword in catchword_to_case):
            catchword_to_case[catchword] = []
        catchword_to_case[catchword].append(case)

    #for year_to_case
    year = case[0:4]
    if not(year in year_to_case):
        year_to_case[year] = []
    year_to_case[year].append(case)

#print(json.dumps(year_to_case, indent = 2))
#print(json.dumps(subject_to_case, indent = 2))
#print(json.dumps(catchword_to_case, indent = 2))
#print(json.dumps(Case_to_subjects, indent = 2))
#print(json.dumps(Case_to_catchwords, indent = 2))
