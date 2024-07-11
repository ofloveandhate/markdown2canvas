Wish list 
=============

⚠️ this is not yet implemented in `mc`

Containerization of quizzess ⚠️ 
-------------------------------------------------------------------------

I want this so badly, but I'm not up to it yet.  I'd love a contribution!


Due dates ⚠️ 
-------------------------------------

Due dates would be encoded relative to the first day of class, by week number and day of week.  Week numbers start at 1.

| Day code | Day of week | 
| --- | --- |
| M | Monday |
| T | Tuesday |
| W | Wednesday |
| R | Thursday |
| F | Friday |
| Sa | Saturday |
| Su | Sunday |

In the `meta.json` file for an assignment, the due date would be encoded like this example:

```
"due":{"time":"10pm", "week":11, "day":"R"}
```

A default time for all assignents can be set in `_course_metadata/defaults.json` with entry `"due_time":"10pm"`, for example.  If this record is not present, and no due time is set for an individual assignment, then the Canvas default time for the course will be used.  On UWEC's system, this can be changed in the course settings. The default value is 11:59pm.

The first day of class is set ...  HOW??
