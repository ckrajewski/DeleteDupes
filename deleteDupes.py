'''
Created by Chris Krajewski (MIT Licensed)
'''
import xml.etree.ElementTree as ET
import argparse
import os
import time
import hashlib
import shutil

# command line settings
parser = argparse.ArgumentParser()
parser.add_argument("-cl", dest="config_location" , help="Change location of config.xml.", default="config.xml")
parser.add_argument("-priority", dest="sort" , help="Specify whether original file is determined based on created time or modified date", default="lmd")
parser.add_argument("-reverse", dest="reverse" , help="Sort direction for dupes. Helps determine original file. If true, sort in descending order", default="false")
args = vars(parser.parse_args())

#https://groups.google.com/forum/#!topic/argparse-users/LazV_tEQvQw

class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

#class to keep track of various file attributes
class FileProperties:
	FileName=''
	FileSize=''
	FilePath=''
	LastModifiedDate=None
	CreatedDate=None
	def __init__(self, name,size,fullpath,lastmod,cd):
		self.FileName=name;
		self.FileSize=size
		self.FilePath=fullpath
		self.LastModifiedDate = lastmod
		self.CreatedDate=cd

#runs a while loop to read in 128 bytes at a time. Once done, it generates an MD5 hash. If two files are the same, they will have the same hash		
def getMD5(filepath):
	block_size=128
	md5 = hashlib.md5()
	f=open(filepath,'rb')
	
	while True:
		data=f.read(block_size)
		if not data:
			break
		md5.update(data)
	return md5.hexdigest()
		
def removeDups(root_folder, dupe_folder):
	FileInfoList={}
	#loop through root directory
	if os.path.isdir(root_folder):
	
		for file in os.listdir(root_folder):
			filepath=os.path.join(root_folder,file)
			#make sure it is a file
			if os.path.isfile(filepath):
				#get its last modified time and checksum
				lastmod=time.strptime(time.ctime(os.path.getmtime(filepath)))
				createdTime=time.strptime(time.ctime(os.path.getctime(filepath)))
				fp=FileProperties(file,os.path.getsize(filepath),filepath,lastmod,createdTime)
				checksum=getMD5(filepath)
				#if checksum key is in map, add FileProcess object to list, otherwise make a new map entry
				if checksum in FileInfoList:			
					fp_list=FileInfoList[checksum]
					fp_list.append(fp)
					FileInfoList[checksum]=fp_list
					
				else:		
					fp_list= []
					fp_list.append(fp)
					FileInfoList[checksum]=fp_list
	#create a list of potiental dupes based on length of FileInfoList. If list is greater than 1, we have more than one file with the same checksum (potiental dupe)		
	potential_dups=[Files for Files, Files in FileInfoList.items() if  len(Files) > 1]
	
	for FileList in potential_dups:
		sort_category=args['sort']
		reverse_value=args['reverse']
		
		#cast command line reverse argument to boolean
		
		if reverse_value=='false':
			reverse_value=False
		else:
			reverse_value=True
			
		#cast command line argument priority to sort methods
		if sort_category=='lmd':
			FileList.sort(key=lambda x: x.LastModifiedDate, reverse=reverse_value)
		elif  sort_category=='cd':
			FileList.sort(key=lambda x: x.CreatedDate, reverse=reverse_value)
		else:
			print("Invalid argument for priority")
			exit(1)
		
		
		for i in range(1, len(FileList)):
			# additional verification can be done here (name and size comparison, for example) before it is moved to dupe folder
			src=os.path.join(root_folder,FileList[i].FileName)
			dest=os.path.join(dupe_folder,FileList[i].FileName)
			shutil.move(src,dest)

# main constructor. Fires removeDupes			
def main():
	#parse config XML file
	#print (args['config_location'])
	if not os.path.isfile(args['config_location']):
		print("Error! config.xml not found")
		exit(1)
	tree=ET.parse(args['config_location']);
	doc=tree.getroot();
	DirectoryToScan=str(doc.find('DirectoryToScan').text).strip()
	
	DirectoryToStoreDupes = str(doc.find('DirectoryToStoreDupes').text).strip()
	if not os.path.isdir(DirectoryToScan):
		if DirectoryToScan =='':
			print("You did not enter a directory to scan. :(  Please specify folder path in config.xml")
		else:
			print("Directory to scan does not exist! Check the config.xml to make sure it is a valid path")
		exit(1)
	
	if not os.path.isdir(DirectoryToStoreDupes):
		if DirectoryToStoreDupes =='':
			
			create_store_dupe_folder = os.path.join(DirectoryToScan, "Dupes")
			DirectoryToStoreDupes=create_store_dupe_folder
			if not os.path.exists(create_store_dupe_folder):
				print("Directory to store potiential dupes not entered. Making one in " , DirectoryToScan, " directory called Dupes" )
				os.makedirs(create_store_dupe_folder)
			else:
				print("Storing dupes in ", os.path.join(DirectoryToScan,"Dupes"))
				
		else:
			print("Directory to store potiential dupes does not exist. Making one...")
			os.makedirs(DirectoryToStoreDupes);
	removeDups(DirectoryToScan, DirectoryToStoreDupes)

if  __name__ =='__main__':
    main()