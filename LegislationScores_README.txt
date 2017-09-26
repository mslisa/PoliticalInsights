It's not the prettiest thing I've ever coded, but it works. I decided it was more important to just share what I had than try to clean up everything. I hope you can forgive me.

Do not run this file within your cloned github directory. You'll want to move it to somewhere else, because it will look for sub-folders that contain the bulk legislative data from the 113th, 114th, and 115th congresses. It'll also download the zip files, unzip them, and do a little cleanup. The first time you run it, it should plop about a gigabyte of data into a folder structure underneath wherever the .ipynb lives, so we definitely don't want to do that in the git folder.

It occurs to me that there's probably a smart way to handle this by using gitignore, but I haven't looked into it.