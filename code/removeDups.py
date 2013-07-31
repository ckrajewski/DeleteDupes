import os
import time
import hashlib
import shutil

#globals
root_folder= r"C:\Users\Chris\Downloads"
dupe_folder=r"C:\Users\Chris\Downloads\Dupes"

#class to keep track of various file attributes
class FileProperties:
	FileName=''
	FileSize=''
	FilePath=''
	LastModifedDate=None
	def __init__(self, name,size,fullpath,lastmod):
		self.FileName=name;
		self.FileSize=size
		self.FilePath=fullpath
		self.LastModifedDate = lastmod

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
		
def removeDups():
	FileInfoList={}
	#loop through root directory
	if os.path.isdir(root_folder):
	
		for file in os.listdir(root_folder):
			filepath=os.path.join(root_folder,file)
			#make sure it is a file
			if os.path.isfile(filepath):
				#get its last modified time and checksum
				lastmod=time.strptime(time.ctime(os.path.getmtime(filepath)))
				fp=FileProperties(file,os.path.getsize(filepath),filepath,lastmod)
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
		FileList.sort(key=lambda x: x.LastModifedDate)
		
		for i in range(1, len(FileList)):
			# additional verification can be done here (name and size comparison, for example) before it is moved to dupe folder
			src=os.path.join(root_folder,FileList[i].FileName)
			dest=os.path.join(dupe_folder,FileList[i].FileName)
			shutil.move(src,dest)

# main constructor. Fires removeDupes			
def main():
	
	removeDups()

if  __name__ =='__main__':
    main()