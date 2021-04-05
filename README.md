# betfair-data

# betfair-data.py was created by José Maquia, eeseljose@gmail.com, github.com/Joseelmax-00.
This program was created for an Upwork.com client, If you have a .tar file that you got from 
Betfair.com you can use this program to extract the main datapoints from it.


## Description

```markdown
This is a very simple program that works if you have downloaded a file with betfair hystorical data,
you need to extract the folder with the year name containing all the data from the year into the 
Data folder, run the program, and it will extract that data from the .json files inside the .tar 
files into an excel spreadsheet. It's a simple click and run, and works with every event, even 
corrupted (cancelled) ones.

If the program finds a corrupted event it will notify the user with an error message, it is 
normal to get 2 or 3 error messages for every year, getting a lot more error messages means that 
you probably encountered a bug, if that's the case, contact the developer (send me an email with 
subject "Error in your GitHub code") or propose a solution on your own branch of the program!
```

## Requirements
```markdown
You need Python installed on your computer

You also need the following libraries, which can be installed by entering the command into the
command prompt:
  
  pandas     | pip install pandas
  bz2        | pip install bz2

```
