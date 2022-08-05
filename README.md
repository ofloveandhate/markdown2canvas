A library for containerizing local markdown content to be published into the Canvas learning management system.  

:warning: This library is under active development and the interface is NOT stable.

---

# Why I wrote/maintain this library

The particular problem this library solves is that of putting Canvas content under version control, and also using Markdown for that content.  Canvas pages are not well-suited to version control *per se*, because they live on the LMS.  I wanted local files, with repos I can share with other designers and instrutors.  

A secondary problem this library solves is that of images.  Images on Canvas are bare, and it's easy to end up with duplicate versions, as well as not have alt text.  By using markdown/html under version control, I can write my alt text directly into page source, instead of using the crappy click-heavy interface on Canvas.  

---

# Containerization of content to be published to Canvas

Containerization is accomplished by making pages/assignments live in folders.  The name of the folder is arbitrary; the metadata for the page lives in a JSON file, while the page itself is simply a markdown file.  That is, the structure of a page/assignment to be published on Canvas, using this library, is

- folder
  - `meta.json` -- a json file containing attributes.  keys should be compliant with the expectations of `canvasapi`.
  - `source.md` -- a markdown file.  Can contain latex math, html, references to local images, emoji using double-colon notation and shortcodes, and of course online images.  



---

# Testing

This library comes with several test pages/assignments:
- pages:  
  - `plain_text` -- source is just plain old text.  start simple, ya know?
  - `uses_latex` -- a page that contains latex math
  - `has_remote_images` -- a page that has remote images embedded
  - `has_local_images` -- a page that uses local images
  - `uses_droplets` -- a page using [the Droplets framework from UWEX](https://media.uwex.edu/app/droplets/index.html).
  - `uses_droplets_via_style` -- a page using [the Droplets framework from UWEX](https://media.uwex.edu/app/droplets/index.html).  The code enabling Droplets comes from a header/footer contained in a style folder.  The main purpose of this test page is the header/footer style thing.
- assignments:
- `programming_assignment` -- an assignment that has a local image

---

# Installation

1. Clone the repo / pull from the repo
2. Move to repo location in terminal
3. `pip install .`   If you already had it installed, then use `pip install . --upgrade` to make sure you get the newer version.

## Critical setup step, do not skip this

You must also define an environment variable called `CANVAS_CREDENTIAL_FILE`, which is the location of a `.py` file containing two variables:
1. `API_URL` -- a string, the url of how to access your Canvas install.  
  - At UW Eau Claire, it's `https://uweau.instructure.com/`.  
  - I cannot possibly tell you your url, but your local Canvas admin can.
2. `API_KEY` -- a string, the key you can get from Canvas.  Here's [a link to a guide on how to generate yours](https://community.canvaslms.com/t5/Admin-Guide/How-do-I-obtain-an-API-access-token-in-the-Canvas-Data-Portal/ta-p/157).  Do not share it with anyone -- having only this one piece of data, anyone can act as you.  Protect it at least as much as you would any other password or sensitive information.

---

# Use

This library is under active development, and will see major use leading up to the Fall 2022 semester.  I suggest checking out the `test_*.py` files in the `test` folder for example code.

## Some quick examples

Assuming you did my setup step, defining the environment variable and creating that file.  Do that first.

### Download all pages, with a filter on the name of the pages
```
import markdown2canvas as mc
course_id = 127210000000003099 # silviana's sandbox for development

canvas = mc.make_canvas_api_obj()
course = canvas.get_course(course_id)

destination = 'downloaded_pages'

my_filter = lambda title: 'Images' in title
mc.download_pages(destination, course, even_if_exists=True, name_filter=my_filter)
```


## Images and embedded content

List your images relative the the folder containing the `source.md` for the content.  

## Headers and footers

This library attempts to provide a way to uniformly style pages across sections of content.  In particular, I have provided a mechanism to programmatically concatenate headers and footers onto markdown content before publishing.  Example application of this might be:
* I have content in my course in four blocks, and want a different header for each block.  But, copypasta for that header content sucks (avoid repitition is a key tenet of programming).  So, I'd rather specify a "style" for the four blocks, and make the pages refer to the styles.  
* I use Droplets from UWEX, and don't want to have to put that code in *every single page*.  I'd rather put it one place (or, at least, only a few places).  So the html code that brings in Droplets lives in a header/footer html code file.

### Style basics

Put your "style" folders in a folder in your course.  In my DS150 course, I have the following structure:

* `_styles/`
  * `/generic`
  * `/assignments`

And in the `meta.json` file for the pages / assignments, I simply have to put the record `"style":"_styles/generic"` or whatever. 

As of July 2022, there is no default style -- if a page doesn't list a style, it gets no style.

### Additional notes about styles:

The folder for each style should have the following four files:
* `header.html`
* `header.md`
* `footer.md`
* `footer.html`

They'll get concatenated around `source.md` in that order.  HTML around markdown, and header/footer around source.  

If you want to use images in your header/footer, put them in the markdown part (even if they appear in html tags), and use the text `$PATHTOMD2CANVASSTYLEFILE` before typing the name of the file, so that its filepath gets listed correctly.  (This happens via a simple string replacement)


## Assignments


### Due dates

Due dates are encoded relative to the first day of class, by week number and day of week.  Week numbers start at 1.

| Day code | Day of week | 
| --- | --- |
| M | Monday |
| T | Tuesday |
| W | Wednesday |
| R | Thursday |
| F | Friday |
| Sa | Saturday |
| Su | Sunday |

In the `meta.json` file for an assignment, the due date is encoded like this example:

```
"due":{"time":"10pm", "week":11, "day":"R"}
```

A default time for all assignents can be set in `_course_metadata/defaults.json` with entry `"due_time":"10pm"`, for example.  If this record is not present, and no due time is set for an individual assignment, then the Canvas default time will be used (this is not an adjustable time in Canvas, for some unexplained reason).  On UWEC's system, this is 11:59pm.

The first day of class is set ...  HOW??


