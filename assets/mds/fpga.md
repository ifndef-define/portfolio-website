# So What Happened?
With this project being my flagship project, I want to share the story of what happened and how I lost most of the source code for it.

The project was going as planned, and I had spent nearly the entire week leading up to the final demo, working non-stop on the project, making significant progress on the glyph table rendering and getting the data from the C code to the FPGA. In order to meet the deadline, I had pulled nearly three back-to-back all nighters to get the project to a demoable, bug-free state.

Since I had to switch between my desktop and my laptop, and since Vivado stores the IP modules of a project as a shared resource, I had modified the save path for all of my project to be in one folder, including the IP modules, the verilog files, and the Vitis source code. Being extremely exhausted, I believe I accidentally moved the entire project folder onto my laptop instead of copying it from my PC without realizing it. 

## My Grave Mistake
Now there was one small render issue I knew about that I didn't have time to synthesize and test before the demo, which was related to the startup screen graphics. I ended up having to demo the project without it which had no value to the demo, but was something I wanted to fix later. After the demo, I went to work on fixing the issue before heading home. Here I made the fatal mistake of not backing up the project before I started deleting large portions of the project to just run the loading screen graphics to test my fix. I ended up seeing it working, and I was happy with the result, so I thought to make the same change to the copy I thought I still had on my desktop. However, upon checking my desktop, I realized that the project folder was no longer there, and I had accidentally moved it to my laptop, where I had just virtually deleted the entire project.

## My Lesson Learned
I learned one of the most important lessons in software development, which is to always back up your work and have some form of version control. I had been working on this project for months, and I had lost nearly all of my source code due to a simple oversight while being extremely exhausted. I attempted to recover the project and rebuilt it, but I relized I would have to virtualize start from scratch. I put it off for a while, and haven't had the time to rebuild it since, working on other projects instead.

I do plan to rebuild this project in the near future, while making it better than before, and I will be sure to back up my work this time.