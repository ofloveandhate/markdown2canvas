A library for containerizing local markdown content to be published into the Canvas learning management system.  

[Documentation on Github Pages](https://ofloveandhate.github.io/markdown2canvas/)

---

# Why I wrote/maintain this library

The particular problem this library solves is that of putting Canvas content under version control, and also using Markdown for that content.  Canvas pages are not well-suited to version control *per se*, because they live on the LMS.  I wanted local files, with repos I can share with other designers and instrutors.  

Further, I want to be able to find-and-replace across many pieces of Canvas content at once.  Local files with my editor of choice is the way to do that; it's impossible on Canvas.  Hence, this library.

Additionally, uniform appearance and ability to change much with little effort.  I wrote a "style" system that puts headers and footers around my content, eliminating repetitive and error-prone work.  Want emester-specific text at the top of all your content?  Trivial with `markdown2canvas`: just change the header file, re-publish, and do something better with your time than wait for Canvas pages to load.

A secondary problem this library solves is that of images.  Images on Canvas are bare, and it's easy to end up with duplicate versions, as well as not have alt text.  By using markdown/html under version control, I can write my alt text directly into page source, instead of using the crappy click-heavy interface on Canvas.  

---

# Core concept: Containerization of content to be published to Canvas

Containerization is accomplished by making pages/assignments live in folders.  The name of the folder is arbitrary; the metadata for the page lives in a JSON file, while the page itself is simply a markdown file.  That is, the structure of a page/assignment to be published on Canvas, using this library, is

- folder
  - `meta.json` -- a json file containing attributes.  keys should be compliant with the expectations of `canvasapi`.
  - `source.md` -- a markdown file.  Can contain latex math, html, references to local images, emoji using double-colon notation and shortcodes, and of course online images.  

You can also put needed files, images, etc in the folder for a piece of content.  `markdown2canvas` aims to automate as much of the process as possible.

---

# Installation

Please see [the documentation](https://ofloveandhate.github.io/markdown2canvas/) -- we have two tutorials, one for Mac/Linux and one for Windows.  


---

# Some things you can do with this library

See the [the documentation](https://ofloveandhate.github.io/markdown2canvas/).  This is just highlights in a root readme.

## Replacements during translation

The purpose of this library is to increase modularity and flexibility, while reducing duplication in source code and allowing version control.  I implemented a simple text replacement feature as part of this, so that I can create uniform appearances in my content without duplicate code.  

That is, you can specify a set of string replacements using a `.json` file, and during translation from markdown to html, before uploading, each substitution happens.  

For example, you can create a `replacements.json` file in a folder at root level (relative to the folder for the course) called `_course_metadata`, and in this file put the content:

```
{
  "$TASKDIV": "",
  "REPLACE THIS TEXT": "with this text",
  "$RICKROLL": "<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/dQw4w9WgXcQ?si=BqTm4nbZOLTHaxnz\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" allowfullscreen></iframe>",
  "another source replacement with spaces": "destination_without_spaces"
}
``` 

You can specify a default set of replacements to happen for every file (except those with overridden replacements).  To do this, make a file `_course_metadata/defaults.json`, and create a record `"replacements": "relative/path/to/replacements_filename.json"`.  The name of the replacements file is arbitrary, and it's relative to root of the course folder.

To override the default replacements, put a record in the `meta.json` file for the content (page / assignment) of the form `"replacements": "relative/path/to/replacements_filename.json"`.

Examples of content using replacements can be found in the `test/` folder of this repository.

If a replacements file doesn't exist where you say it should, an exception will be raised at `publish` time for the `CanvasObject` (`Page` or `Assignment`).  (You can construct a thing with a bad replacements file and not know it until you try to publish!)


ℹ️ I'm using simple Python `str.replace` to do the replacements.  There are consequences:

* It will replace strings exactly, there are no implemented efforts to allow patterns or functions.  
* It's case sensitive, and includes exact spacing.  
* The dollar signs above are NOT special.  They're just a nice way to indicate the text will be replaced.  

⚠️ Furthermore, I'm not sure what order the replacements will be done in, so if the target of one replacement includes the source of another, I can't guarantee you at this time that it will actually happen in a deterministic order.  If you want this feature, please add it and submit a PR to this repo.



## Reference existing Canvas assignments, pages, and files

Whereas I find it to be a pain to link to other content on Canvas using their editor, it's easy using `markdown2canvas`.  

To link to an existing Canvas assignment, use a link of the form

```[Test Assignment](assignment:Test Assignment)```

To link to an existing Canvas page, use a link of the form

```<a href="page:Test Page">Link to page titled Test Page</a>```

To link to an existing Canvas file, use a link of the form

```
<a href="file:DavidenkoDiffEqn.pdf">Link to file called DavidenkoDiffEqn.pdf</a>
```

ℹ️ If the "existing" content doesn't yet exist when the content is published, a broken link will be made.  This is ok.  Think of the publishing process using Markdown2Canvas similar to the compilation of a TeX document, which is done in multiple passes.  Once the page / assignment / file exists, the link will resolve correctly to it.  Publish all content about twice to get links to resolve.


## Emoji conversion from shortcodes

This library supports the automatic conversion of shortcodes to emoji.  For example, `:open_book:` goes to 📖.  I use the [`emoji`](https://pypi.org/project/emoji/) library to do this.  [Shortcodes can be found here](https://carpedm20.github.io/emoji/).

Right now, emoji shortcodes can only be used in content, not in names of things -- shortcodes in names will not be emojized.



## Automatic uploading and warehousing of images and embedded content

List your images relative the folder containing the `source.md` for the content and they'll automatically be uploaded when you publish.  If the image is already uploaded, a link to the existing image will be generated instead of uploading.



## "Styling" -- Automatic inclusion of uniform headers and footers

This library attempts to provide a way to uniformly style pages across sections of content.  In particular, I have provided a mechanism to programmatically concatenate headers and footers onto markdown content before publishing.  Example application of this might be:

* I have content in my course in four blocks, and want a different header for each block.  But, copypasta for that header content sucks (avoid repitition is a key tenet of programming).  So, I'd rather specify a "style" for the four blocks, and make the pages refer to the styles.  
* I use Droplets from UWEX, and don't want to have to put that code in *every single page*.  I'd rather put it one place (or, at least, only a few places).  So the html code that brings in Droplets lives in a header/footer html code file.


## Assignments


Reduce your mental load by specify possible upload types in the `meta.json` file for an assignment.  The submission type is encoded by a line that looks like the following. 

```
"submission_types":['online_text_entry', 'online_url', 'media_recording', 'online_upload']
```

These are four of the five upload types available with Canvas. The other is an annotation. You may omit this line or include any sublist of this list. If you choose to allow online upload, you may also specify the allowable file types by including an allowed extensions list in your `meta.json` file for the assignment.

```
"allowed_extensions": ["pdf","docx"]
```


## Links

You can hold links in modules under version control, similar to `Page` and `Assignment` types.  One file is needed in the folder:

1. `meta.json`  A valid json file containing something like:

```
{
  "name":"🍓 an automatically uploaded link, to amethyst.youcanbook.me",
  "type":"ExternalUrl",
  "external_url":"https://amethyst.youcanbook.me",
  "modules":["Automatically Added Test Module"],
  "new_tab":1
}
```


