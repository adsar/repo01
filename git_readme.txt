repo01 readme
=============
Setup
-----
In the host, we have created the root folder, which on a Win host looks like this: C:\as
Inside /as we have cloned repo01 from github
Inside /as we have setup the Dropbox folder that contains the files folder for all non-source files.
In the vm, we have configured Sharing for folder as
In the Guest: sudo usermod -a -G vboxsf adrian


Use Cases
---------
1 - Add an existing subfolder to the git repo from the VM

The VM has access to the working directory,through the share folder, chi
But, the VM has not access to the remote git configuration value:
- the url of the remote github repo
- the user name and password 
So we need to configure all that.
First, check if there is a remove: git remote -v
if repo01 is a remote, remove it: git remote rm repo01

git remote add repo01  https://github.com/adsar/repo01.git
git config user.email "mr.sarno2@gmail.com"
git config user.name "Adrian Sarno"

There is no need to clone the repo because the virtualization host already did that.

We have to be mindful that we are sharing the same git working directory with other VMs, 
this means that the other VM must store its work safely before we can work in this one, 
if other VM has branched the code and it has uncommited work in the working folder, 
then we should go aback to that VM and commit it. 
For the above reason, we may want to avoid branches when we work with a working dir shared by several VMs. 
Check if the working dir is branched and don't continue until is back in master. 
For example:

git branch
*capdev
master
git status
<comit everything>
git merge master

git checkout master
git merge capdev

now the repo is in good shape, we can branch master now and checkin our sources in a project branch
There is no need to pull if all the VMs share the same working folder, 
on the other hand if we have commited checkins from another host, in that case the sintax is: 
git pull repo01 master

- now, copy the sources to the subfolder in the repo folder and check them in, for example:
git add --all <subfolder>
git reset HEAD *~
git reset HEAD *.ipynb
git commit -m "comment"
git push repo01

If your branch is already the one you need to checkin, for example:
git branch
capdev
*master

then you can got directly:
 git rm --cached *.ipynb
 git commit -m "updated repo git readme"
