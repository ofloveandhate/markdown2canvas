Emojification
==================


This library supports the automatic conversion of shortcodes to emoji.  During translation from local file to Canvas content, `markdown2canvas` will attempt to emojize your text from "shortcodes".  

* You may also just use emoji directly without using short codes.  
* We felt that also allowing short codes would be helpful.

For example, `:open_book:` goes to 📖.  

* We use the `emoji` library to do this.  Here's `a link to their documentation <https://pypi.org/project/emoji/>`_.
* `Shortcodes can be found here <https://carpedm20.github.io/emoji/>`_.

Right now, emoji shortcodes can only be used in content, not in names of things -- shortcodes in names will not be emojized.

