#. :doc:`The style is applied <../tutorials/styling_content>`.

    #. The markdown header and footer from the used style are assembled around your `source.md`.
    #. The html header and footer from the used style are assembled around that.

#. :doc:`Replacements are done <../tutorials/text_replacements>`.
#. :doc:`Emoji shortcodes are emojified <../emoji>`
#. The markdown is translated to HTML.  
#. :doc:`Links to existing content are implemented <../making_links_to_existing_content>`, further modifying the HTML.
#. Local files and images which are linked-to in the source are uploaded (if necessary), and the HTML is adjusted to use the Canvas links to that content.
#. Content properties are set from `meta.json`.
#. The content is placed in modules as described in `meta.json`.