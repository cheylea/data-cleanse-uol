'''
    File name: python_clean.py
    Author: Cheylea Hopkinson
    Python Version: 3.9.12
'''
# Importing and Data Preparation #
# =============================================================================

# Import Packages
import numpy as np
import pandas as pd
import re
from collections import Counter

# Import Data
data = pd.read_csv('source_data\SIS_Faculty-List.csv', encoding='utf-8')

# Data Preparation
# Remove new lines from column names
data.columns = data.columns.str.replace('\n', ' ')
# Update Long Column Name
data.columns = data.columns.str.replace('DOCUMENT OTHER PROFESSIONAL '
                                        'CERTIFICATION CRITIERA '
                                        'Five Years Work '
                                        'Experience Teaching '
                                        'Excellence Professional '
                                        'Certifications',
                                        'Other Experience')
data.columns = data.columns.str.replace('Courses Taught- '
                                        'Term 201510',
                                        'Courses Taught')
data.columns = data.columns.str.replace('All Qualifications '
                                        'from Profile',
                                        'All Qualifications')


# Trim all remaining columns that are strings
data['Name'] = data['Name'].str.strip()
data['Location'] = data['Location'].str.strip()
data['Title'] = data['Title'].str.strip()
data['Reports To'] = data['Reports To'].str.strip()
data['Highest Qualification'] = data['Highest Qualification'].str.strip()
data['Major'] = data['Major'].str.strip()
data['University'] = data['University'].str.strip()
data['All Qualifications'] = data['All Qualifications'].str.strip()
data['Courses Taught'] = data['Courses Taught'].str.strip()
data['MAJOR TEACHING FIELD'] = data['MAJOR TEACHING FIELD'].str.strip()
data['Other Experience'] = data['Other Experience'].str.strip()
data['Criteria'] = data['Criteria'].str.strip()

# Check for duplicates
print(data['ID'].value_counts())

# Check for nulls
id_missing = data['ID'].isnull().sum()
print("\nNumber of missing values:", id_missing)

# Add a unique id column
u_id = data.index
data.insert(0, 'u_id', u_id)


# Data Analysis
# =============================================================================

# Get total number of rows
total = len(data)
print("Total Number of Rows", total)

# Summarise the data
data.describe(include='O')

# Print the counts for each of the values within the columns
print(data['Grade'].value_counts())
print(data['LWD'].value_counts())
print(data['Type'].value_counts())
print(data['Divison'].value_counts())

# Drop irrelevant columns Grade, Type, Division
data = data.drop(columns=['Grade', 'Type', 'Divison'])

# Count Missing
count_missing = data.isnull().sum()
total = len(data)

percent_missing = (count_missing/total) * 100
print(percent_missing)

# Extracting Information from Data
# =============================================================================

# Courses Table
# Split out the courses in new columns
courses_t = data['Courses Taught'].str.split(',|\n', expand=True)

# Ensure the unique id is added to the new dataframe
courses_t.insert(0, 'u_id', u_id)

# Transform the new dataframe so the columns become rows
courses_t = courses_t.melt(id_vars=['u_id'],
                           var_name='column',
                           value_name='Course')

# Remove empty rows
courses_t = courses_t[~courses_t['Course'].isnull()]

# Trim columns and remove redudnant column
courses_t['Course'] = courses_t['Course'].str.strip()
courses_t = courses_t.drop(columns=['column'])

# Export to a new file
courses_t.to_csv('cleaned_data\courses_table.csv')
courses_t.head()

# Convert the column to a list of courses and split by new line and space
courses_list = data['Courses Taught'].to_list()
courses_list_keywords = []
for x in range(0, len(courses_list)-1):
    y = str(courses_list[x])
    courses_list_keywords.append(re.split(r' |\n', y))

# Count the occurance of each of the keywords
courses_list_keywords = [x for y in courses_list_keywords for x in y]
courses_list_keywords_count = Counter(courses_list_keywords)

# Get most common keywords
common = courses_list_keywords_count.most_common(20)
items = [x[0] for x in common]

for x in items:
    if x.isalpha():
        print(x)

# Clean Courses
# Adding a '1' for yes where the keyword exists in the courses taught column
data['t_business'] = np.where(data['Courses Taught'].str.contains('Business') |
                              data['Courses Taught'].str.contains('Busi '),
                              1, 0)

data['t_management'] = np.where(data['Courses Taught'].str.contains('Manag') |
                                data['Courses Taught'].str.contains('Mgmnt') |
                                data['Courses Taught'].str.contains('Mgt'),
                                1, 0)

data['t_account'] = np.where(data['Courses Taught'].str.contains('Accounting'),
                             1, 0)

data['t_finance'] = np.where(data['Courses Taught'].str.contains('Financ'),
                             1, 0)

data['t_market'] = np.where(data['Courses Taught'].str.contains('Marketing'),
                            1, 0)

# Print the counts for each of the values within the columns
print(data['Title'].value_counts())

# Clean Title
data['Title_clean'] = np.where(data['Title'].str.contains('HR') &
                               data['Title'].str.contains('Business'),
                               'Business (HR & Admin)',
                      np.where(data['Title'].str.contains('Admin') &
                               data['Title'].str.contains('Business'),
                               'Business (Admin)',
                      np.where(data['Title'].str.contains('Comp') &
                               data['Title'].str.contains('Business') &
                               data['Title'].str.contains('Math'),
                               'Business, Comp & Math',
                      np.where(data['Title'].str.contains('Comp Lit') &
                               data['Title'].str.contains('Business'),
                               'Business & Comp Lit',
                      np.where(data['Title'].str.contains('Trainee'),
                               'Trainee',
                      np.where(data['Title'].str.contains('Business'),
                               'Business', 'Other'))))))

# Clean Highest Qualification
# Print the counts for each of the values within the columns
print(data['Highest Qualification Level'].value_counts())

# Print the counts for each of the values within the columns
print(data['Highest Qualification'].value_counts())

# Clean Highest Qualification Level
data['HQL_clean'] = np.where(data['Highest Qualification Level'].isna() &
                             data['All Qualifications'].str.contains('Ph.D'),
                             'Doctorate',
                    np.where(data['Highest Qualification Level'].isna() &
                             data['All Qualifications'].str.contains('Master'),
                             'Masters',
                    np.where(data['Highest Qualification Level'].isna() &
                             data['All Qualifications'].str.contains('Bachelor'),
                             'Bachelors',
                    np.where(data['Highest Qualification Level'].str.contains('Master'),
                    'Masters',
                    np.where(data['Highest Qualification Level'].str.contains('Ph.D') |
                             data['Highest Qualification Level'].str.contains('PhD'),
                             'Doctorate',
                    np.where(data['Highest Qualification Level'].str.contains('MBA'),
                    'Masters',
                    np.where(data['Highest Qualification Level'].str.contains('Doctor') &
                            (data['Highest Qualification'].str.contains('Ph.D') |
                             data['Highest Qualification'].str.contains('philosophy')),
                             'Doctorate',
                    np.where(data['Highest Qualification Level'].str.contains('Doctor'),
                    'Doctorate',
                    np.where(data['Highest Qualification'].str.contains('Doctor'),
                    'Doctorate',
                    np.where(data['Highest Qualification Level'].str.contains('Bachelor'),
                    'Bachelors',
                             'Unknown'))))))))))

# Clean Highest Qualification
data['HQ_clean'] = np.where(data['Highest Qualification Level'].isna() &
                             data['All Qualifications'].str.contains('Ph.D'), 'Ph.D',
                    np.where(data['Highest Qualification Level'].isna() &
                             data['All Qualifications'].str.contains('Master'), 'Masters',
                    np.where(data['Highest Qualification Level'].isna() &
                             data['All Qualifications'].str.contains('Bachelor'), 'Bachelors',
                    np.where(data['Highest Qualification'].str.contains('Master of Arts'), 'Master of Arts',
                    np.where(data['Highest Qualification'].str.contains('Master of Science'), 'Master of Science',
                    np.where(data['Highest Qualification'].str.contains('Master of Business Administrat'), 'Master of Business Administration',
                    np.where(data['Highest Qualification'].str.contains('Bachelor of Applied Science'), 'Bachelor of Applied Science',
                    np.where(data['Highest Qualification'].str.contains('Master of Commerce'), 'Master of Commerce',
                    np.where(data['Highest Qualification'].str.contains('Master of Marketing'), 'Master of Marketing',
                    np.where(data['Highest Qualification'].str.contains('Master of Business'), 'Master of Business',
                    np.where(data['Highest Qualification'].str.contains('Master of Management'), 'Master of Management',
                    np.where(data['Highest Qualification'].str.contains('Master of Law'), 'Master of Law',
                    np.where(data['Highest Qualification'].str.contains('Master of Philosophy'), 'Master of Philosophy',
                    np.where(data['Highest Qualification'].str.contains('Master of Education'), 'Master of Education',
                    np.where(data['Highest Qualification'].str.contains('Master of International Business'), 'Master of International Business',
                    np.where(data['Highest Qualification'].str.contains('Bachelor of Science'), 'Bachelor of Science',
                    np.where(data['Highest Qualification'].str.contains('Bachelor of Business Admin'), 'Bachelor of Business Administration',
                    np.where(data['Highest Qualification'].str.contains('Master of Professional Studies'), 'Master of Professional Studies',
                    np.where(data['Highest Qualification Level'].str.contains('MBA'), 'Master of Business Administration',
                    np.where(data['Highest Qualification Level'].str.contains('Master'), 'Masters',
                    np.where(data['Highest Qualification Level'].str.contains('Ph.D') |
                             data['Highest Qualification Level'].str.contains('PhD') |
                             data['Highest Qualification'].str.contains('Ph.D') |
                             data['Highest Qualification'].str.contains('PhD'), 'Ph.D',
                    np.where(data['Highest Qualification Level'].str.contains('MBA'), 'Masters',
                    np.where(data['Highest Qualification Level'].str.contains('Doctor') &
                            (data['Highest Qualification'].str.contains('Ph.D') |
                             data['Highest Qualification'].str.contains('philosophy')), 'Ph.D',
                    np.where(data['Highest Qualification Level'].str.contains('Doctor'), 'Doctorate (Other)',
                    np.where(data['Highest Qualification'].str.contains('Doctor'), 'Doctorate (Other)',
                    np.where(data['Highest Qualification Level'].str.contains('Bachelor'), 'Bachelors',
                             'Unknown'))))))))))))))))))))))))))

# Get counts of values
print(data['HQL_clean'].value_counts())
print(data['HQ_clean'].value_counts())


# Remove Unknown
data['HQL_clean'] = data['HQL_clean'].str.replace('Unknown', 'Masters', regex=False)
data['HQ_clean'] = data['HQ_clean'].str.replace('Unknown', 'Masters', regex=False)

# Qualifications Table
# Split out the courses in new columns
qualifs = data['All Qualifications'].str.split(',', expand=True)

# Ensure the unique id is added to the new dataframe
qualifs.insert(0, 'u_id', u_id)

# Transform the new dataframe so the columns become rows
qualifs_t = qualifs.melt(id_vars=['u_id'], var_name='column', value_name='qualif')

# Remove empty rows
qualifs_t = qualifs_t[~qualifs_t['qualif'].isnull()]

# Split out qualification from subject
qualifs_t[['Qualification', 'Major']] = qualifs_t['qualif'].str.split('(', 1, expand=True)

# Clean up
qualifs_t['Major'] = qualifs_t['Major'].str.replace('))', 'nnn', regex=False)
qualifs_t['Major'] = qualifs_t['Major'].str.replace(')', '', regex=False)
qualifs_t['Major'] = qualifs_t['Major'].str.replace('nnn', ')', regex=False)
qualifs_t['Major'] = qualifs_t['Major'].str.replace('(', '', regex=False)
qualifs_t['Qualification'] = qualifs_t['Qualification'].str.strip()
qualifs_t['Major'] = qualifs_t['Major'].str.strip()
qualifs_t = qualifs_t.drop(columns=['column', 'qualif'])

# Export to a new file
qualifs_t.to_csv('cleaned_data\qualifications_table.csv')
qualifs_t.head()

# Clean Other Experience - Teaching Experience
# Make all lower case
data['Other Experience'] = data['Other Experience'].str.lower()

# Remove double spaces
data['Other Experience'] = data['Other Experience'].str.replace('  ', ' ')

# Split column by common phrasing
teaching_experience = data['Other Experience'].str.split('years of high school|'
                                                         'years high school|'
                                                         'years school|'
                                                         'years of school|'
                                                         'years university|'
                                                         'years of university|'
                                                         'years teaching experience|'
                                                         'years of teaching experience|'
                                                         'years teaching|'
                                                         'years of teaching', expand=True)

# Strip out irrelevant symbols
teaching_experience[0] = teaching_experience[0].str.replace('+', '', regex=True)
teaching_experience[0] = teaching_experience[0].str.replace('\n', '', regex=True)
teaching_experience[0] = teaching_experience[0].str.strip()
teaching_experience[1] = teaching_experience[1].str.replace('\n', '', regex=True)
teaching_experience[1] = teaching_experience[1].str.replace(':', '')
teaching_experience[1] = teaching_experience[1].str.replace('&', '')
teaching_experience[1] = teaching_experience[1].str.strip()

# Extract numbers from columns
teaching_experience['n'] = teaching_experience[0].str.split(' ').str[-1]
teaching_experience['n2'] = teaching_experience[1].str.split(' |y').str[0]

# Combine isolated numerical values
teaching_experience['years'] = np.where(teaching_experience[0].str.isdigit(), teaching_experience[0],
                               np.where(teaching_experience['n'].str.isdigit(), teaching_experience['n'],
                               np.where(teaching_experience['n2'].str.isdigit(), teaching_experience['n2'],
                               None)))

# Convert column to numeric
teaching_experience['years'] = pd.to_numeric(teaching_experience['years'])

# Remove outliers
teaching_experience['years'] = np.where(teaching_experience['years'] > 40, None, teaching_experience['years'])

# Add column to original dataset
data['years_teaching'] = teaching_experience['years']

# Check for nulls
missing = data['years_teaching'].isnull().sum()
print("\nNumber of missing values:", missing)

# Calculate the mean
mean = round(np.mean(pd.to_numeric(data['years_teaching'])))

# Correct the column
data['years_teaching'] = np.where(data['Other Experience'].str.contains('teach') &
                                  data['years_teaching'].isna(), mean,
                         np.where(data['years_teaching'].isna(), 0, data['years_teaching']))

# Ensure column is all the same data type
data['years_teaching'] = pd.to_numeric(data['years_teaching'])

# Clean Other Experience - Professional Experience
# Split column by common phrasing
prof_experience = data['Other Experience'].str.split('years professional experience|'
                                                     'years of professional experience|'
                                                     'years professional|'
                                                     'years of professional|'
                                                     'years work|'
                                                     'years industry|'
                                                     'years of industry', expand=True)

# Strip out irrelevant symbols
prof_experience[0] = prof_experience[0].str.replace('+', '', regex=True)
prof_experience[0] = prof_experience[0].str.replace('\n', '', regex=True)
prof_experience[0] = prof_experience[0].str.strip()
prof_experience[1] = prof_experience[1].str.replace('\n', '', regex=True)
prof_experience[1] = prof_experience[1].str.replace(':', '')
prof_experience[1] = prof_experience[1].str.replace('&', '')
prof_experience[1] = prof_experience[1].str.strip()

# Extract numbers from columns
prof_experience['n'] = prof_experience[0].str.split(' ').str[-1]
prof_experience['n2'] = prof_experience[1].str.split(' |y').str[0]

# Combine isolated numerical values
prof_experience['years'] = np.where(prof_experience[0].str.isdigit(), prof_experience[0],
                               np.where(prof_experience['n'].str.isdigit(), prof_experience['n'],
                               np.where(prof_experience['n2'].str.isdigit(), prof_experience['n2'],
                               None)))

# Convert column to numeric
prof_experience['years'] = pd.to_numeric(prof_experience['years'])

# Remove outliers
prof_experience['years'] = np.where(prof_experience['years'] > 40, None, prof_experience['years'])

# Add column to original dataset
data['years_prof'] = prof_experience['years']

# Check for nulls
missing = data['years_prof'].isnull().sum()
print("\nNumber of missing values:", missing)

# Calculate the mean
mean = round(np.mean(pd.to_numeric(data['years_prof'])))

# Correct the column
data['years_prof'] = np.where(data['Other Experience'].str.contains('prof') &
                                  data['years_prof'].isna(), mean,
                         np.where(data['years_prof'].isna(), 0, data['years_prof']))

# Ensure column is all the same data type
data['years_prof'] = pd.to_numeric(data['years_prof'])

# Add column for active researcher
data['active_researcher'] = np.where(data['Other Experience'].str.contains('active') &
                                     data['Other Experience'].str.contains('research'), 1, 0)


# Converting Cleaned Columns to Machine Readable
# =============================================================================

# Create dictionaries

# Location
location_list = list(set(data['Location'].dropna().to_list()))
location_dict = {k: v for v, k in enumerate(location_list)}
print(location_dict)
# Reports To
reports_list = list(set(data['Reports To'].dropna().to_list()))
reports_dict = {k: v for v, k in enumerate(reports_list)}
print(reports_dict)
# Title
title_list = list(set(data['Title_clean'].dropna().to_list()))
title_dict = {k: v for v, k in enumerate(title_list)}
print(title_dict)
# Highest Qualification Level
hql_list = list(set(data['HQL_clean'].dropna().to_list()))
hql_dict = {k: v for v, k in enumerate(hql_list)}
print(hql_dict)
# Replace Columns
data = data.replace({"Location": location_dict})
data = data.replace({"Reports To": reports_dict})
data = data.replace({"Title_clean": title_dict})
data = data.replace({"HQL_clean": hql_dict})

# Remove remaining redundant columns
data = data.drop(columns=['ID', 'Name', 'Title', 'LWD', 'Highest Qualification Level',
                          'Highest Qualification', 'HQ_clean', 'Major', 'University',
                          'All Qualifications', 'Courses Taught',
                          'MAJOR TEACHING FIELD', 'Other Experience', 'Criteria'])

# Count Missing
count_missing = data.isnull().sum()
total = len(data)

percent_missing = (count_missing/total) * 100
print(percent_missing)

# Remove null rows
data = data.dropna()

# Save to file
data.to_csv('cleaned_data\staff_table.csv')
