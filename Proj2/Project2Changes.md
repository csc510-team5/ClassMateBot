# Project 2 Changes
## Additions
### Assignments/Grading
An essential part of any course is the delivery of assignments and the grading of these. This feature allows instructors to add assignments into the server, and assign grades to them based on grading categories. Both the students and the instructor are able to have an easy interface to view their grades, and do calculations based on them. For example, the instrcutor can view a grading breakdown for a given grading category or asssignment, and the students can do calculations to determine how well they need to do on a given assignment to maintain a desired grade.

Details on these additions can be found here: [Assignments Docs](https://github.com/nfoster1492/ClassMateBot-1/tree/main/docs/Assignments) |  [Grading Docs](https://github.com/nfoster1492/ClassMateBot-1/tree/main/docs/Grades)

### Calendar Integration
Although being able to set deadlines on discord is useful, a good number of students would like to have those deadlines on their calendar. This feature allows deadlines to be automically added to a Google calendar that the students can see as well as functionality to move those calendar events to other formats that the student may prefer. After the instructor has added events to the calendar students will be able to download these events either as a .ics file they can upload to outlook or other calendar software, or they can download the events as a pdf. Lastly, the bot will check the calendar daily for events due that day and ping everyone in general of the items that are due that day.

Details on these additions can be found here: [Calendar Docs](https://github.com/nfoster1492/ClassMateBot-1/tree/main/docs/Calendar)

### Database
#### grades table
This table was required for the grading functionality to hold grades for students.
|guild_id|member_name|assignment_id|grade|
|-------|---------------|---|--|
|.|.|.|.|

#### grade_categories table
This table was required for the instructor to be able to assign different weights to different types of grades (ex: Exams, HW, Projects)
|id|guild_id|category_name|category_weight|
|--|----------|--------|--|
|.|.|.|.|

#### assignments table
This table was required for the instructor to be able to create assignments and assign them a weight based on the category
|id|guild_id|category_id|assignment_name|points|
|--|--------|--|-----------|--|
|.|.|.|.|

## Modifications

### Database
Supporting the functionality added in this project required the modification of the existing `reminders` table. To better reflect how we leveraged this table, the `homework_name` column was renamed `reminder_name`.

## Documentation
This version includes a more detailed [Installation Guide](../docs/installation.md) including the new database and calendar setup instructions.

This version includes a [troubleshooting guide](../docs/troubleshoot.md) to help future developers or users resolve issues.
