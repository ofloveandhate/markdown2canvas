A library for containerizing local markdown content to be published into the Canvas learning management system.

# Why I wrote/maintain this library

The particular problem this library solves is that of putting Canvas content under version control, and also using Markdown for that content.  Canvas pages are not well-suited to version control *per se*, because they live on the LMS.  I wanted local files, with repos I can share with other designers and instrutors.  

A secondary problem this library solves is that of images.  Images on Canvas are bare, and it's easy to end up with duplicate versions, as well as not have alt text.  By using markdown/html under version control, I can write my alt text directly into page source, instead of using the crappy click-heavy interface on Canvas.  

# Containerization of content to be published to Canvas

Containerization is accomplished by making pages/assignments live in folders.  The name of the folder is arbitrary; the metadata for the page lives in a JSON file, while the page itself is simply a markdown file.  That is, the structure of a page/assignment to be published on Canvas, using this library, is 

- folder
  - `meta.json` -- a json file containing attributes.  keys should be compliant with the expectations of `canvasapi`.
  - `source.md` -- a markdown file.  Can contain latex math, html, references to local images, emoji using double-colon notation and shortcodes, and of course online images.  

This library comes with several test pages/assignments:
- `programming_assignment` -- an assignment that has a local image
- `uses_latex` -- a page that contains latex math
- `has_remote_images` -- a page that has remote images embedded
- `has_local_images` -- a page that uses local images
- `plain_text` -- source is just plain old text.  start simple, ya know?

# Installation

1. Clone the repo
2. Move to repo location in terminal
3. `pip install .`

You must also define an environment variable called `CANVAS_CREDENTIAL_FILE`, which is the location of a `.py` file containing two variables:
1. `API_URL` -- a string, the url of how to access your Canvas install.  At UW Eau Claire, it's `https://uweau.instructure.com/`
2. `API_KEY` -- a string, the key you can get from Canvas.  Here's [a link to a guide on how to generate yours](https://community.canvaslms.com/t5/Admin-Guide/How-do-I-obtain-an-API-access-token-in-the-Canvas-Data-Portal/ta-p/157).  Do not share it with anyone -- having only this one piece of data, anyone can act as you.  Protect it at least as much as you would any other password or sensitive information.

# Use

This library is under active development, and will see major use leading up to the Fall 2022 semester.  I suggest checking out the `test_*.py` files in the `test` folder for example code.