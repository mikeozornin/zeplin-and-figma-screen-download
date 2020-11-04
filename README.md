# About
Here are python scripts for simplifying design review and sharing design work. Scripts download updated screens from Zeplin or/and Figma to a new folder with the current date. Useful to check changes in several projects.

Imagine: you have several projects you need to check. 
You can order zeplin projects by update time, select the most recent, order screens in the project by updated time, look for a new screen, view them, and go to the new project. Zeplin opens screens slowly, you have to remember where you stopped. Checked five screens wasted ten minutes. Wanna kill yourself.

For Figma, you don't have even that: you have to somehow find out what's changed. No clues, no sorting, just find. Terrible, if you need to do it.

I wanted to review all my design team work, so I created these scripts for myself. Pretty happy with them. Maybe you could use them too.

# How to use
* Create an access token for Figma or/and Zeplin.
  * Figma: https://www.figma.com/developers/api#access-tokens
  * Zeplin: https://docs.zeplin.dev/reference#introduction
* Copy config.py.example to config.py and edit it with your tokens.
* (Figma only): Edit ```config.py``` and add IDs for projects you want to download.
* You can run both scripts separately or use an example bash script. Don't forget to edit the path in the ```run.sh``` script.

# How it works
Scripts download new screens from Zeplin of Figma to a new folder named by the current date.

Script for Zeplin checks new screens, updated from the previous check, and download them. The previous check timestamp is stored in the ```zeplin-checkpoint.txt``` file, so only updated screens will be downloaded new time.

Script for Figma download __all the screens__ in the project. After downloading images the script delete screens not changed from the previous check. M5D checksums are used for checking differs in the screens, checksums stored in the ```figma-checkpoint.txt``` file.

# Hot to make it scheduled
If you want to run script every hour/day/week, please, add scripts to you crontask. My task starts every day at 11:00 PM:

```00 23 * * * /Users/mike/work/git-repos/stuff/zeplin-download-recent/run.sh```

# Contact
Please feel free to drop me a line on mike.ozornin@gmail.com if you have any questions.
