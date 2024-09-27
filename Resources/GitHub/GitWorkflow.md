#Github

### Initializing GIt

```bash
# This Initilizes a git repository 
git init
```

### Staging files

```bash
# Add all files in a directory 
git add . 

# Add a file with the name 
git add file.txt

# Add All files with the same extension 
git add .txt
```

### Check Status of commits

```bash
git status
```

### Committing Files

 

```bash
# -m Stands for message
git commit -m "Initial commit."

# This will bring up default editor to enter message
git commit
```

### Remove Files

```bash
# This removes from the staging area as well as Commits
git rm file.txt
```

### Renaming Files

```bash
git mv filename.txt newfilename.txt
```

### Ignoring Files

```bash
.gitignore 
```

### History

```bash
git log

commit 53924d2d3fe304b3023dd1bbf88c23189e8b7453 (HEAD -> main, origin/main)
Author: Hackspark <hackspark@outlook.com>
Date:   Mon Jul 1 01:51:02 2024 +0000

    Changed it a little

commit 7b098aef630a17f63cc43b447d59a3869c65e1f5
Author: Hackspark <hackspark@outlook.com>
Date:   Mon Jul 1 01:43:43 2024 +0000

    Changed shit

commit ef25feff9f416d3479477cd394057fb6623a77ec
Author: Hackspark <hackspark@outlook.com>
Date:   Mon Jul 1 01:35:38 2024 +0000
```

### Show Commits

```bash
# This will show the commit using the ID.
git show 53924d2d3fe304b3023dd1bbf88c23189e8b7453

commit 53924d2d3fe304b3023dd1bbf88c23189e8b7453 (HEAD -> main, origin/main)
Author: Hackspark <hackspark@outlook.com>
Date:   Mon Jul 1 01:51:02 2024 +0000

    Changed it a little

diff --git a/README.md b/README.md
index f7f4d76..4494ab4 100644
--- a/README.md
+++ b/README.md
@@ -1 +1 @@
-# Learning_c
+# This is me changing the files
```
