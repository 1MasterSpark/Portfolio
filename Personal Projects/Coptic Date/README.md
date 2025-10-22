In 2022, I wrote some code in Markdown to create two templates that would display the current date and year in the Coptic calendar. This is currently used in many Wikipedia pages, such as these two:
https://en.wikipedia.org/wiki/Coptic_calendar
https://en.wikipedia.org/wiki/Era_of_the_Martyrs

The documentation for these templates can be seen at https://en.wikipedia.org/wiki/Template:COPTICDATE

[copticdate.html](copticdate.html) is a demonstration of that code, after I tediously converted it to javascript.

Later, I used a similar (but more complex) approach to show the current date in the Julian calendar. This can be seen at https://en.wikipedia.org/wiki/Template:JULIANCALENDAR. Both calendar templates take into account the differences in leap year calculations between the Julian/Coptic and the Gregorian calendars.