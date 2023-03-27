# Creating a program to scrape .txt files of Reddit pages for usernames of commenters
# Importing os module to be able to iterate through files in the `txt-files` directory
import copy
import os

path = "/Users/syrrgordon/Desktop/development/CSCI/Spring-Break-Lab/txt-files/"
# Creating an empty list to store usernames
usernames = []
# Creating empty list to store usernames without duplicates
unique_users = []
# Creating list of words that can't be in username
restricted_words = [
    'AutoModerator', '[deleted]', 'Comment deleted by user', 'Comment removed by moderator', ' ', 'https://www.']
# Creating a list to hold the final version of usernames
clean_usernames = []
# Creating a dictionary to hold the post dates as keys and the number of posters as values
dates_and_names = {}
# Creating a dictionary to hold the post dates as keys and the comments as values
dates_and_comments = {}


# Using `os.lsitdir()` method to create a list of file names
dir_list = os.listdir(path)

# Creating directory list with path in front
dir_list_with_path = []

# Appending the full path of files to the new list above
for file in dir_list:
    new_name = path + file
    dir_list_with_path.append(new_name)

# Opening all the files
for file in dir_list_with_path:
    # Creating a list to hold usernames from each file
    files_usernames = []
    opened_file = open(file, 'r')
    # Turning each line of the file to an element of a list
    lines = opened_file.readlines()
    # Iterating through the list to find usernames
    for line in lines:
        i = lines.index(line)
        # Every username in the file is proceeded by the user's level
        # Finding level and going to the next line allows us to find the username
        # Adding usernames to new list
        if 'level' in line:
            next_line = lines[i+1]
            # Iterating through list of restricted words to ensure it's actually a username
            counter = 0
            for word in restricted_words:
                if word not in next_line:
                    counter += 1
            if counter == len(restricted_words) and len(next_line) > 2:
                usernames.append(next_line)
                # Adding the usernames to the list of usernames from this specifc file
                files_usernames.append(next_line)
    # Adding the name of the file to the `dates_and_names` dictionary
    dates_and_names[file] = copy.deepcopy(files_usernames)
    # Clearing the list to prepare for next file
    files_usernames.clear()
    # Closing file to free up memory space
    opened_file.close()

# List copmrehension to remove duplicates from the username list
[unique_users.append(x) for x in usernames if x not in unique_users]

# Removing the newline characters from the usernames
for user in unique_users:
    clean_usernames.append(user.strip('\n'))
clean_usernames.sort()
# clean_usernames = clean_usernames.sort()

# Saving the number of unique/original commenters and printing it out
number_of_commenters = len(clean_usernames)
num_unique_commenters = "Number of unique commenters: " + str(number_of_commenters)

# For each user who published a post, print out the user names of those who published 2 or more posts
# Creating a dictionary that hold the username as the key and the number of comments made as the value
users_comments_frequency = {}
for name in unique_users:
    users_comments_frequency[name] = usernames.count(name)

# Creating an empty list to hold the usernames that have 2 or more comments
users_with_multiple_posts = []
temp = []

# Scraping dictionary to save the names (keys) of users with 2 or more posts
for i in users_comments_frequency:
    if users_comments_frequency[i] >= 2:
        users_with_multiple_posts.append(i)
for i in users_with_multiple_posts:
    temp.append(i)

# 78-83 strip the list of users who post multiple comments of newline characters
# Clearing the list of users with multiple posts
users_with_multiple_posts = []

for i in temp:
    users_with_multiple_posts.append(i.strip('\n'))

num_repeat_commenters = "The following users published two or more comments: " + str(users_with_multiple_posts)

# Print out the posts that mention the following symptoms: (i) cough, (ii) cold, (iii) fever
# The following lines congregate the actual comments
# Creating a list of words that we want to flag comments for
flag_words = ['cough', 'cold', 'fever']
# Creating a list of comments that have the flag word
comments = []
# Opening all the files (again)
for file in dir_list_with_path:
    # Creating a list to hold comments specific to each file
    files_comments = []
    opened_file = open(file, 'r')
    # Turning each line of the file to an element of a list
    lines = opened_file.readlines()
    # Iterating through the list to find flagged comments
    for line in lines:
        # i = lines.index(line)
        # Adding flagged comments to new list
        for flag in flag_words:
            if flag in line and ' ' in line:
                comments.append(line)
                # Adding the comment to the list of comments from this specific file
                files_comments.append(line)
                break
    # Adding the name of the file to the `dates_and_comments` dictionary
    dates_and_comments[file] = copy.deepcopy(files_comments)
    # Clearing the list to prepare for next file
    files_comments.clear()
    # Closing file to free up memory space
    opened_file.close()
    
# Creating a list to hold unique comments
unique_comments = []
# List copmrehension to remove duplicates from the username list
[unique_comments.append(x) for x in comments if x not in unique_comments]


# REMEMBER TO UNCOMMENT LINES 130-132
# print("Comments that mention fevers, colds, or coughs: ")
# for comment in comments:
#     print(comment)


# Over the course of the week, was there an increase in the number of users who published posts?

# Creating a list to hold the usernames that will form the values of the dict above
unique_users_for_dict = []

# Creating a final nested list to hold the unique usernames for each day
final_unique_users = []

# Removing duplicates from values in `dates_and_names` dictionary
# Iterating through each list (each value is a list) in the dictionary
for val in dates_and_names.values():
    # List copmrehension to remove duplicates from the value
    [unique_users_for_dict.append(x) for x in val if x not in unique_users_for_dict]
    # Appends list of unique users to final list
    final_unique_users.append(copy.deepcopy(unique_users_for_dict))
    # Clears initial list of unique users to prepare for next value
    unique_users_for_dict.clear()

# Creating a list of all the keys from `dates_and_names` to store the dates
dates = []
for key in dates_and_names:
    dates.append(key[-8:])

# Merging the dates and the final list of usernames to create a dictionary
# The dictionary will have dates as the keys and the numeber of unique commenters that day as the values
dates_and_names_clean = {dates[i]: final_unique_users[i] for i in range(len(dates))}

# Sorting the dictionary keys by date order
myKeys = list(dates_and_names_clean.keys())
myKeys.sort()
sorted_dict = {i: dates_and_names_clean[i] for i in myKeys}

# Creating a list to store the number of unique posters for each day
frequency = []
for val in sorted_dict.values():
    frequency.append(len(val))

# Checking to see if there was an increase in the number of users who published posts over the course of the week
# Comparing the first value in the frequency list to the last value

def user_frequency():
    if frequency[0] >  frequency[-1]:
        freq = 'There was an increase in the number of users who published comments over the course of a week.'
    elif frequency[0] < frequency[-1]:
        freq = 'There was a decrease in the number of users who published comments over the course of a week.'
    else:
        freq = "print('There was no change in the number of users who published comments over the course of a week."

    return freq


# Was there an increase in the number of posts that mentioned the following symptoms: (i) cough, (ii) cold, (iii) fever?
# Creating a list to hold the comments that mention the symptoms
unique_comments_for_dict = []

# Creating a final nested list to hold the flagged comments for each day
final_unique_comments = []

# Removing duplicates from values in `dates_and_comments` dictionary
# Iterating through each list (each value is a list) in the dictionary
for val in dates_and_comments.values():
    # List copmrehension to remove duplicates from the value
    [unique_comments_for_dict.append(x) for x in val if x not in unique_comments_for_dict]
    # Appends list of unqiue comments to final list
    final_unique_comments.append(copy.deepcopy(unique_comments_for_dict))
    # Clears initial list of unique comments to prepare for next value
    unique_comments_for_dict.clear()

# Creating a list of all the keys from `dates_and_comments` to store the dates
dates = []
for key in dates_and_comments:
    dates.append(key[-8:])

# Merging the dates and the final list of comments to create a dictionary
# The dictionary will have dates as the keys and the number of unique comments that day as the values
dates_and_comments_clean = {dates[i]: final_unique_comments[i] for i in range(len(dates))}

# Sorting the dictionary keys by date order
myKeys_2 = list(dates_and_comments_clean.keys())
myKeys_2.sort()
sorted_dict_2 = {i: dates_and_comments_clean[i] for i in myKeys_2}

# Creating a list to store the number of unique comments that mention symptoms for each day
comment_frequency = []
for val in sorted_dict_2.values():
    comment_frequency.append(len(val))

# Checking to see if there was an increase in the number of comments who mentioned the symptoms
# Comparing the first value in the frequency list to the last value
def comment_freq():
    if comment_frequency[0] >  comment_frequency[-1]:
        freq = 'There was an increase in the number of posts that mentioned the following symptoms: cough, cold, or fever over the course of a week.'
    elif comment_frequency[0] < comment_frequency[-1]:
        freq = 'There was a decrease in the number of posts that mentioned the following symptoms: cough, cold, or fever over the course of a week.'
    else:
        freq = "There was no change in the number of posts that mentioned the following symptoms: cough, cold, or fever over the course of a week."
    return freq
# Writing all the requested information to a new .txt file to make reading it easier
f = open("info.txt", "a")
f.write(num_unique_commenters+'\n')
f.write(num_repeat_commenters+'\n')
f.write(user_frequency()+'\n')
f.write(comment_freq()+'\n')
f.close()

f = open("info.txt", 'r')
print(f.read())
