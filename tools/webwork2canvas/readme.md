
# webwork2canvas

A tool for automating the assignment creation process in Canvas for content in Webwork

silviana amethyst


---

## Why to use my tool

* Due dates.  The date picker in Webwork is far superior to the date picker in Canvas.  My tool will automatically set due dates for the assignments in Canvas to match the ones in Webwork.
* This tool, though complicated to get through for the first time, will likely save you several hundred loads of pages on Canvas (1-4 seconds a piece) and several thousand mouse clicks.
* This tool forces you to be methodical and deliberate about several choices.
* Easier setting of names for assignments using a modern text editor, for fun patterning using "selection selection".



---

# Step-by-step instructions


These instructions guide you through my process for automating the webwork2canvas step.  


## 1. Select which content you want to use

ℹ️ You have to do this step yourself, regardless of whether you use my Python tool.  This step controls what content new users in your section are assigned.

### 1.A. Background and context

There are four kinds of content in the Webwork problems:

* Training sets -- untimed.  answers submitted per-problem, not per-set.  infinite attempts.  direct instruction on how to solve the problems on the pages.  some videos, some embedded Desmos graphs, hints, etc.
* Speedruns sets -- timed problems.  submit answers for all problems at same time, and can do that an infinite number of times.  highest per-set score kept.
* Challenge sets -- untimed problems.  submit answers for all problems at same time, and can do that an infinite number of times.  highest per-set score kept.
* Team quizzes -- all students get the same content.

"Visible" content in Webwork is ready for students.  "Invisible" content in Webwork should/must not be assigned to students.

### 1.B. Making the selection

1. togo the Hmwk Sets Editor
2. Select the "Edit" tab
3. Check to select all sets ☑️ .  The upper left does it for you, do not click hundreds of times.
4. Click "Edit"
5. Use the "Visible" column.  Uncheck to declare your intent to not assign that to students.  Check to make sure that new users created in the system are assigned that content.


## 2. Adjust your due dates in  Webwork

ℹ️ You have to do this step yourself, regardless of whether you use my Python tool.  

1. goto Hmwk Sets Editor
2. select "Edit" from the tabs of actions, and probably check all assignments
3. click "Edit"
4. adjust the due dates. copy paste is your friend, but *SEE MY NOTES* below before over-writing my deliberately-set times-of-day.
5. click "Save Edit"


Notes:

* the due dates are also the sort order for content in the "Hmwk Sets Editor" page, so I suggest you do not change any due dates between 
    * "------------------------------- BEGIN CONTENT STUDENTS INTERACT WITH" 
    * "----------------------- END CURRENT ACTIVE CONTENT"
* Times also matter for the sort order.  I use open times to help encode the section numbes in the book, and I keep them in the early morning.
* My initial close and answer dates are 9:59pm on the Sunday before Finals week.  



---

## 3. Canvas structure decisions

ℹ️ You have to do at least the first two steps of this even if you don't use my tool.


Think about your modules and gradebook categories.  Decide on a naming scheme for the modules, and names for the categories.  Might I suggest using emoji as part of the category names?


### 3.A. Mentally decide on a module naming scheme

I have out-of-the-box supported two naming schemes for Modules: 

* Weekly.  The names of the modules *start with* "Week 1", "Week 2", etc.


### 3.B. Mentally decide on grade category naming

I have supported one scheme out of the box.

* By type: 
    * "🏋️ Training"
    * "🏔️ Challenge"
    * "⏩ Speedrun"
    * "🎽 Team quiz"


### 3.C. Edit the .json file that specifies these

I have provided two .json files with my naming choices, and the module naming schemes.   You'll use ONE of them:

* `name_map_week_and_chapter.json` -- Every item will be put into a "Week X" module and a "Chapter Webwork" module.
* `name_map_week_.json`  -- Every item will be put into a "Week X" module.
* `name_map_chapter.json` -- Every item will be put into "Chapter Webwork" module.  

🎯 Copy the ONE desired .json file to `$FOLDER`.  

You may choose which modules the assignments go in (in Canvas) by editing the .json fields:
* `"modules"` -- a list like `["module 1", "Module Two"]` A list of strings.  If these modules don't exist, they will be created.  They are case sensitive.  There's also a wildcard in effect.  Here are the rules:
    * If there is exactly one module that starts with this (up to case), the content will go into that existing module
    * If there are no modules matching using `startswith`, a module will be created
    * If there are more than one module matching using `startswith`, it will go in the first such module.  The order should be as-ordered in Canvas.
* `"assignment_group_name"` -- The string name of the assignment group in Canvas.  will be made if they don't exist
* `"name"` -- the string name of the content as exposed in Canvas.  

ℹ️ There is no need to remove lines for assignments or content you're not using.  My code never loops over this file, just looks up into it.  The key is the name of the assignment in Webwork, with underscores mapped to spaces.  

⚠️ If you happen to rename a webwork assignment in webwork (don't do that -- it has other consequences, and it's kinda hard to do -- deliberately), then this `name_map_*.json` must also change.  Don't attempt to change the names of the webwork assignments.

💡 Use a modern text editor for big wins.  I have no idea what software is installed on your computer, or if you even can, but VS Code is awesome.  Sublime is great too, and you can use it for free.  silviana is happy to help teach you how to use a modern text editor.



## 4. Choose configuration options for my tool 🐍

I provide a configuration tool, in the form of a `config.json` file.  It's a json file.  Modify it, but do not invalidate it.

* Do you want your Webwork assignments embedded into the Canvas pages?  It saves a load of a page, but costs a bunch of page real estate.  Students may escape out of the embedded environment, but you have to teach them how to do it.  By default, my tool will NOT embed the assignments, but attempt to load in a new page.
    * In `config.json,` change `"embed_webwork_in_canvas_page":false` to  `"embed_webwork_in_canvas_page":true`


* Want to select between multiple name maps?  Switch `"name_map"` in `config.json`.

There are more, but I'll have you set the last important one after you do some other setup.  Let's move to a readiness check.

----------------

---


## Pause! ⚠️ Check for readiness

🛑 Did you complete steps 1-3?  
* Did you decide on a schedule?  My tool will set the due dates in Canvas for you, and manually setting due dates in Canvas is painful.  
* Did you decide on a module naming scheme, gradebook categories, and save them in the json file?  My tool will automatically create modules for you, add content to modules, and put assignments into their correct categories.
* Did you adjust config settings?  

🧐 You may also proceed as an experiment if you make a Sandbox course, and use that course for the steps.  In fact that's probably a good idea, the act of creating the assignments in your course ... there's no easy "undo" of the action, except to completely reset the Canvas course.  Only actually take my steps with your real course when you're really ready, especially if you've already put effort into your framework!


---

-------------------------------------


## 12. Save two webwork webpages to disk


🎯 Make a Folder on your computer, and name it something memorable, like "webwork2canvas_20230824" or whatever.   I'll call this `$FOLDER` from now on.

⚠️ Do not put spaces in the names of things on computers.  It's more difficult to code around.  I am not sure if my tool works correctly with a space in the path / name.


### 12.A. Save the "Hmwk Sets Editor page" from Webwork

* "Hmwk Sets Editor" from the left
* In your browser, save page source as `dates.html` to `$FOLDER`.






### 12.B. Save a student view of the list of assigned content

#### 12.B.i. Make a fake student in Webwork

* "Classlist editor" tool on the left
* Select the "Add" tab, leave at 1 user to add, click "Add"
    * Make up a name.  I chose "content, student facing" as the last, first.  
    * Don't bother to use the clicking menu for "Select sets below to assign them to the newly-created users.".  There's a much easier way.
* Click "Add Students"
* Classlist Editor, and verify the new fake student exists

#### 12.B.ii. Assign that fake student all content you wish to send to Canvas

This step is nearly trivial if the set of visible homework sets in the "Hmwk Sets Editor" is exactly the set you'll assign to your students.  Go back and do step 1 if you didn't already.  

* "Set assigner" tool from the left
* Select the fake student from the left panel.

Do a sort on the right panel.  

* In the "Sort" dropdown menu, Choose "Field: Visible".
* click "Change Display Settings".  The visible ones are now at the bottom.
* Scroll to the bottom, select the bottom assignment.  
* Scroll up and find the first visible one.  You have to remember which one this is, though it's probably "limits introducing limits - speedrun", and the last "invisible" one is hopefully 'unused problems'.  (😵‍💫 It's not clear to me what the secondary sorting trait is)
* Shift-click that first visible assignment.
* Click "Assign selected sets ot selected users".


The fake user should now have all of your visible content assigned to them.  

🎯 Verify this step is done by:

* "Student progress" from the left bar
* Click on the fake student's name
* Look at the list.  Is it correct?


#### 12.B.iii. Save the "Homework Sets" page from Webwork while 'acting as' the fake student

Are you still on the "Student Progress for fakename" page?  If not, 

* "Student progress" from the left bar
* Click on the fake student's name

Ok, now you're definitely on "Student Progress for fakename".  Click "Act as: fakename", just below the big words "Student Progress".

* Click "Homework Sets" from the left bar.  This should take you to a view of what the student will see when they click that button.  You'll also be drawn to the right bar, where there's a Course Info box.  You want to click the "Edit" button, I'm just sure of it.  And you will click it.  Just not now.  Make a note to come back and edit that.
* Save this page to disk as `homework_sets.html` in `$FOLDER`.










## Make a fake Canvas course for experimenting

The location for this button is stupid.  Follow my instructions:

1. Open any page in Canvas
2. Far left bar, the ? Help button at the bottom.
3. "Create a Sandox Course"








---



## Get Python ready  🐍

If you cannot install software or are unwilling to deal with Python yourself, please ask silviana.  She'll complete this with you at her computer.


### Get your Canvas API key



make a python file called `canvas_credentials.py` at arbitrary location.  it must contain at least one variable: `API_KEY = "your_token_here"`, a string variable, which contains the API key you'll make.  

go to canvas, "account", "settings".  under "approved integrations", click "new access token".  give it a name and expiration.  save the token to the .py file.  my token / key / whatever starts with `11830~S`.

make an environment variable in the shell from terminal, called `CANVAS_CREDENTIAL_FILE`, having value the full path to the `canvas_credentials.py` file, including the `canvas_credentials.py` part.  (this means that the file doesn't actually need to be named `canvas_credentials.py`)




### Install markdown2canvas

In a Python-enabled terminal / command prompt

* `pip install canvasapi, bs4`
* `git clone https://github.com/ofloveandhate/markdown2canvas`
* `cd markdown2canvas`
* `pip install .`

The `webwork2canvas` tool should be at `markdown2canvas/tools/webwork2canvas.py`.  You'll later execute the script via `python3`.  This readme file is in there, too.












------------

-----------

-----------


# Foot notes

I generated the .json file for naming / modules by:

* Hmwk Sets Editor
* filter for visible
* selecting the entire table of names and dates using my cursor
* copy-pasted into text document in Sublime text (maybe another can, idk)
* go nuts with the cursor making .json structure
















## get api key for canvas





## adjust `webwork2canvas.py`

in the python code i sent you (change the extension `.zip` --> `.py`, otherwise you can't send python code in our email system):
enter the canvas course id number for the course you're publishing to, line 163.

## run!

comment out the publish line (line 197) for a dry run, if you want.

run python `webwork2canvas.py`.

the code produces some temporary files/folders: 
* inspectme.json
* automatically_generated_assignments/
* markdown2canvas_datestamp.log

reload canvas page.  verify is as desired.



## summary

in one folder:
* dates.html, homework_sets.html
* name_map.json
* webwork2canvas.py

installed packages:
* markdown2canvas, bs4, canvasapi

made credentials file:
* `canvas_credentials.py`, with environment variable `CANVAS_CREDENTIAL_FILE` pointing to it, and containing `API_KEY = "my_key"`.

run:
* `python webwork2canvas.py`

