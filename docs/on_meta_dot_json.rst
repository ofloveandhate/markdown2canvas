On the `meta.json` file
=========================


The `meta.json` file should be present in every containerized content folder.



Valid properties
-----------------

meta.json for Assignments
****************************

In the `meta.json` file for an assignment, the submission type is encoded by a line that looks like the following. 


	"submission_types":['online_text_entry', 'online_url', 'media_recording', 'online_upload']


These are four of the five upload types available with Canvas. The other is an annotation. You may omit this line or include any sublist of this list. If you choose to allow online upload, you may also specify the allowable file types by including an allowed extensions list in your `meta.json` file for the assignment.


	"allowed_extensions": ["pdf","docx"]


meta.json for Pages
***********************


meta.json for Links
************************


meta.json for Files
************************



What happens if I specify a property / key that's not used or is invalid?
-----------------------------------------------------------------------------
