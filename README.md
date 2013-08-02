Delete Dupes
===========

Delete Dupes v 1.1
------------------

 A simple Python script that groups suspected duplicate files and moves them into a file for you to review before you permanently delete them.
 Files are deemed suspected duplicates with they generate the same MD5 checksum.
 
Documentation
-------------

**Config.xml**

Delete Dupes reads config.xml to set up some basic parameters

Sample config.xml:

	<Settings>
		<![CDATA[Must Use Full Pathnames]]>
		<DirectoryToScan>C:\Users\Chris\Documents</DirectoryToScan>
		<DirectoryToStoreDupes> </DirectoryToStoreDupes>
	</Settings>

In the above example, the Directory to Scan path has been populated. If left blank, Delete Dupes will throw an error.

Directory to store the suspected dupes can be left blank. If left blank, a directory called Dupes will be created within the "Directory To Scan" folder location. In this case, the folder path becomes C:\Users\Chris\Documents\Dupes. If this directory does not exist, Delete Dupes will create it for you

Delete Dupes takes no mandatory command line arguments. It is assumed that config.xml lies in the same directory as deleteDupes.py. If it is (and it is called config.xml) then simply run:

    py deleteDupes.py


Command Line Arguments
----------------------

**-cl**

cl is short for "Change Location". It is an optional parameter. If populated, it will look for config.xml (or whatever you decide to name your xml file) in the given directory.

Example:

    py deleteDupes.py -cl C:\Users\Chris\Downloads\config.xml

**-priority**

priority determines how the original file is found. The default value is lmd. lmd stands for Las tModified Date. The file with the oldest last modified date becomes the original file. Can be changed to cd ( Created Date ). Then the file with the oldest created date becomes the original

Values:

* lmd (default) = Last Modified Date
* cd = Created Date

Example:
	
	py deleteDupes.py -priority cd
	
**-reverse**

reverse determines the sorting order. Default value is false. If set to true, then the original file is deemed to be the newest file i.e. the latest file to be created or modified (depending on the value of priority)

The following example will make Delete Dupes mark the file with the latest Last Modifed Date as the original file. Other files with the same MD5 checksum will be marked as dupes :

	py deleteDupes.py -priority lmd -reverse true

Upcoming Enhancements:
---------------------

* Scan through subdirectories.
* Allow priority and reverse values to be set in the config.xml file
* Support command line arguments to specify what file should be deemed the original in a list of duplicates. Currently, the file with the oldest last modified date is considered the original.
* Support additional measures of verification other than just the MD5 checksum. For example, a user may have purposefully downloaded the same file twice, but renamed it with the intent of keeping both files. An additional parameter can be passed in that compares names so that if they are too similar (i.e. File.txt and File(1).txt) then they are deemed dupes (provided they have the same checksum of course). However, if they were named File.txt and PurposefullyCopiedAgain.txt, they names would be different enough that Delete Dupes would mark then as dupes.
