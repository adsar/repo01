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

The VM has access to the working directory through the share folder.
But, the VM has not access to the remote git configuration value:
- the url of the remote github repo
- the user name and password 
So we need to configure all that.
First, check if there is a remote: git remote -v
if repo01 is a remote, remove it (relax, this just removes a local configuration line so you can recreate it): 
git remote rm repo01

re-create the remote config:
git remote add repo01  https://github.com/adsar/repo01.git
git config user.email "mr.sarno2@gmail.com"
git config user.name "Adrian Sarno"

There is no need to clone the repo because the virtualization host already did that.

We have to be mindful that we are sharing the same git working directory with other VMs, 
this means that the work done in this working directory by other VM will show up in ours.
Ideally, we shuold hhave commited the work done in the other VM safely before witching to work in this one, 
if other VM has branched the code and it has uncommited work in the working folder, 
otherwise we can commit it from here. Remember that both the Working Directory and the Local Repository
are the same accross all the VM's, because they are stored in the host shared folder,
only the configuration values about the remote GitHub repo, that are stored outside the Local Repository
are not shared across VMs.

We may want to avoid branches when we work with a working dir shared by several VMs, just to avoid confussion, because branches tend to be project specific, and so are VMs, so if we check out a branch in one VM, we may
forget to merge it to master before switching to work in other VM and then we start working on the wrong branch.
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

then you can go directly to:
 git rm --cached *~
 git rm --cached *.ipynb
 git commit -m "updated repo git readme"


Getting the latest version of the sources
-----------------------------------------
if you want to get the latest version of your code
from your local repository back to you working folder:
- this will unstage everything, but will not update your working dir:
git reset HEAD

- this will unstage everything and will update your working dir:
git reset --hard HEAD


notice that:
- is not possible to scope the reset providing a path, it affects the whole repo!!
- there is no - in HEAD


Creating a repository for publication
------------------------------------------------
- Create empty repo in github
- git clone https://github.com/adsar/kalman.git
- copy contents to local folder
- git add *
- git status
- git -rm --cached *.png
- git config user.name "Adrian Sarno"
- git config user.email "mr.sarno2@gmail.com"
- git remote add kalman  https://github.com/adsar/kalman.git
- git push kalman

Discard changes unstaged changes from working folder
----------------------------------------------------
git stash save --keep-index
git stash drop


