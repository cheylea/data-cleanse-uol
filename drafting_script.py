import numpy as np
import pandas as pd
import re
from collections import Counter

# Set seed
np.random.seed(13)

# Import Data
data = pd.read_csv('source_data\SIS_Faculty-List.csv', encoding='utf-8')


# Data Preparation
# Remove new lines from column names
data.columns = data.columns.str.replace('\n', ' ')
# Update Long Column Name
data.columns = data.columns.str.replace('DOCUMENT OTHER PROFESSIONAL CERTIFICATION CRITIERA Five Years Work Experience Teaching Excellence Professional Certifications', 'Other Experience')
# Drop irrelevant columns --Grade, Type, Division
data = data.drop(columns=['Grade','Type','Divison'])

# Trim all remaining columns that are strings
data['Name'] = data['Name'].str.strip()
data['Location'] = data['Location'].str.strip()
data['Title'] = data['Title'].str.strip()
data['Reports To'] = data['Reports To'].str.strip()
data['Highest Qualification'] = data['Highest Qualification'].str.strip()
data['Major'] = data['Major'].str.strip()
data['University'] = data['University'].str.strip()
data['All Qualifications from Profile'] = data['All Qualifications from Profile'].str.strip()
data['Courses Taught- Term 201510'] = data['Courses Taught- Term 201510'].str.strip()
data['MAJOR TEACHING FIELD'] = data['MAJOR TEACHING FIELD'].str.strip()
data['Other Experience'] = data['Other Experience'].str.strip()
data['Criteria'] = data['Criteria'].str.strip()




# Examine Each Column

# ID
# Missing some values, so add new unique id column
# Add a unique id column
u_id = data.index
data.insert(0, 'u_id', u_id)

# Clean up Highest Qualification Level / Highest Qualification
data['HQL_clean'] = np.where(data['Highest Qualification Level'].isna() & 
                             data['All Qualifications from Profile'].str.contains('Ph.D'),'Doctorate',
                    np.where(data['Highest Qualification Level'].isna() & 
                             data['All Qualifications from Profile'].str.contains('Master'),'Masters',
                    np.where(data['Highest Qualification Level'].isna() & 
                             data['All Qualifications from Profile'].str.contains('Bachelor'),'Bachelors', 
                    np.where(data['Highest Qualification Level'].str.contains('Master'), 'Masters',
                    np.where(data['Highest Qualification Level'].str.contains('Ph.D') |
                             data['Highest Qualification Level'].str.contains('PhD'), 'Doctorate',
                    np.where(data['Highest Qualification Level'].str.contains('MBA'), 'Masters',
                    np.where(data['Highest Qualification Level'].str.contains('Doctor') &
                            (data['Highest Qualification'].str.contains('Ph.D') |
                             data['Highest Qualification'].str.contains('philosophy')), 'Doctorate',
                    np.where(data['Highest Qualification Level'].str.contains('Doctor'), 'Doctorate',
                    np.where(data['Highest Qualification'].str.contains('Doctor'), 'Doctorate',
                    np.where(data['Highest Qualification Level'].str.contains('Bachelor'), 'Bachelors',
                             'Unknown'))))))))))

data['HQT_clean'] = np.where(data['Highest Qualification Level'].isna() & 
                             data['All Qualifications from Profile'].str.contains('Ph.D'),'Ph.D',
                    np.where(data['Highest Qualification Level'].isna() & 
                             data['All Qualifications from Profile'].str.contains('Master'),'Masters',
                    np.where(data['Highest Qualification Level'].isna() & 
                             data['All Qualifications from Profile'].str.contains('Bachelor'),'Bachelors',
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


qualifs = data['All Qualifications from Profile'].str.split(',', expand=True)
qualifs['highest'] = np.where(data['All Qualifications from Profile'].str.contains('Ph.D') |
                             (data['All Qualifications from Profile'].str.contains('Phil') &
                              data['All Qualifications from Profile'].str.contains('Doc')),'Ph.D',
                     np.where(data['All Qualifications from Profile'].str.contains('Doctor'),'Doctorate',
                     np.where(data['All Qualifications from Profile'].str.contains('Master'),'Masters',
                     np.where(data['All Qualifications from Profile'].str.contains('Bachelor'),'Bachelors','Other')))) # needs work this one
qualifs.insert(0, 'u_id', u_id)


# Qualifications & Majors
qualifs = data['All Qualifications from Profile'].str.split(',', expand=True)
qualifs.insert(0, 'u_id', u_id)

# Transform to List of Qualifications
qualifs_t = qualifs.melt(id_vars=['u_id'], var_name='column', value_name='qualif')
qualifs_t = qualifs_t[~qualifs_t['qualif'].isnull()]

qualifs_t[['Qualification','Major']] = qualifs_t['qualif'].str.split('(', 1, expand=True)

# Clean up parentheses
qualifs_t['Major'] = qualifs_t['Major'].str.replace('))', 'nnn', regex=False)
qualifs_t['Major'] = qualifs_t['Major'].str.replace(')', '', regex=False)
qualifs_t['Major'] = qualifs_t['Major'].str.replace('nnn', ')', regex=False)
qualifs_t['Major'] = qualifs_t['Major'].str.replace('(', '', regex=False)
qualifs_t['Qualification'] = qualifs_t['Qualification'].str.strip()
qualifs_t['Major'] = qualifs_t['Major'].str.strip()

qualifs_t = qualifs_t.drop(columns=['column', 'qualif'])
qualifs_t.to_csv('cleaned_data\qualifications_table.csv')

# Clean up Title
data['Title_clean'] = np.where(data['Title'].str.contains('HR') &
                               data['Title'].str.contains('Business'), 'Business (HR & Admin)',
                      np.where(data['Title'].str.contains('Admin') &
                               data['Title'].str.contains('Business'), 'Business (Admin)',
                      np.where(data['Title'].str.contains('Comp') &
                               data['Title'].str.contains('Business') &
                               data['Title'].str.contains('Math'), 'Business, Comp & Math',
                      np.where(data['Title'].str.contains('Comp Lit') &
                               data['Title'].str.contains('Business'), 'Business & Comp Lit',
                      np.where(data['Title'].str.contains('Trainee'), 'Trainee',
                      np.where(data['Title'].str.contains('Business'), 'Business', 'Other'))))))
data = data.drop(columns=['Title'])


# Extract Teaching Experience from Courses Taught

# List keywords for analysis
courses_list = data['Courses Taught- Term 201510'].to_list()
courses_list_keywords = []
for x in range(0,len(courses_list)-1):
    y = str(courses_list[x])
    courses_list_keywords.append(re.split(r' |\n',y))

courses_list_keywords = [x for y in courses_list_keywords for x in y]
courses_list_keywords_count = Counter(courses_list_keywords)

# Transform to List of Courses Taught
courses_t  = data['Courses Taught- Term 201510'].str.split(',|\n', expand=True)
courses_t.insert(0, 'u_id', u_id)
courses_t = courses_t.melt(id_vars=['u_id'], var_name='column', value_name='Course')
courses_t = courses_t[~courses_t['Course'].isnull()]
courses_t['Course'] = courses_t['Course'].str.strip()

courses_t = courses_t.drop(columns=['column'])
courses_t.to_csv('cleaned_data\courses_table.csv')

#qualifs_t[['Qualification','Major']] = qualifs_t['qualif'].str.split('(', 1, expand=True)

#print(courses_list_keywords_count) # This gives the most popular subjects

# Generate suggested columns for most common subjects

data['taught_business'] = np.where(data['Courses Taught- Term 201510'].str.contains('Business') |
                                   data['Courses Taught- Term 201510'].str.contains('Busi '), 1, 0)
data['taught_management'] = np.where(data['Courses Taught- Term 201510'].str.contains('Manag') |
                                     data['Courses Taught- Term 201510'].str.contains('Mgmnt') |
                                     data['Courses Taught- Term 201510'].str.contains('Mgt'), 1, 0)
data['taught_accounting'] = np.where(data['Courses Taught- Term 201510'].str.contains('Accounting'), 1, 0)
data['taught_finance'] = np.where(data['Courses Taught- Term 201510'].str.contains('Financ'), 1, 0)
data['taught_marketing'] = np.where(data['Courses Taught- Term 201510'].str.contains('Marketing'), 1, 0)
data['taught_hrm'] = np.where(data['Courses Taught- Term 201510'].str.contains('HRM') |
                              data['Courses Taught- Term 201510'].str.contains('Human Resources'), 1, 0)

data = data.drop(columns=['Courses Taught- Term 201510'])


# Extract Years of Experience from Other Experience


#print(data)
# Analyse Missing
# Count Missing
count_missing = data.isnull().sum()
total = len(data)

percent_missing = (count_missing/total) * 100
#print(percent_missing)

data.to_csv('cleaned_data\staff_table.csv')