Why this library exists
========================

(This is silviana amethyst writing.)

Why I wrote/maintain this library
-------------------------------------

The particular problem this library solves is that of putting Canvas content under version control, and also using Markdown for that content.  Canvas pages are not well-suited to version control *per se*, because they live on the LMS.  I wanted local files, with repos I can share with other designers and instrutors.  

Further, I wanted to be able to find-and-replace across many pieces of Canvas content at once.  Local files with my editor of choice is the way to do that; it's impossible on Canvas.  Hence, this library.

Additionally, uniform appearance and ability to change much with little effort.  I wrote a "style" system that puts headers and footers around my content, eliminating repetitive and error-prone work.  Want emester-specific text at the top of all your content?  Trivial with `markdown2canvas`: just change the header file, re-publish, and do something better with your time than wait for the stupid Canvas editor to load.

A secondary problem this library solves is that of images.  Images on Canvas are bare, and it's easy to end up with duplicate versions, as well as not have alt text.  By using markdown/html under version control, I can write my alt text directly into page source, instead of using the crappy click-heavy interface on Canvas.  


I've successfully automated many mundane and error-prone tasks using this library, including:

* Automating creation of Canvas assignments for the Webwork homework system
* Consistent and flexible styling and beautification of content across an entire course

The cost of development and maintenance has paid itself off many times over, both in terms of mental load and time savings.


History 2021-2024
-----------------------

I (silviana) started writing this library in 2021 to meet the needs of a new course at UWEC, DS150: Computing in Python: Fundamentals and Procedural Programming.  I also anticipated using it for the upcoming 2022 re-design of DS710, Programming for Data Science at UWEC/UW Extended Campus.  

Mckenzie started contributing to `markdown2canvas` in 2022 during that DS710 re-design, and she really ran with it as she applied it to her math courses.  Mckenzie added significant features to this library, including

* links to existing pages, assignments, quizzes, and files
* warnings when some content doesn't exist
* clarifications and consistency across parts of the library
* bugfixes


Allison contributing to the library in summer 2024 as silviana prepared to move to MPI, contributing:

* improved unit testing
* documentation, particularly tutorials and notes
* finding more bugs and gotchas

As I move to new things in August 2024, I wish you well.  


