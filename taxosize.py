
#
#Provides the size of the taxonomy to download
#

import os
import io
import sys

insideDirList = []
totalSize=0

def addToInsideDirs(newDir):
	insideDirList.append(newDir)

def getsize():
	ls = []
	ftp.retrlines('MLSD', ls.append)
	runSize = 0
	for entry in ls:
		#print(entry)
		size = int(entry.split(";")[2].replace("size=",""))
		name = entry.split(";")[8].lstrip()
		fileType = entry.split(";")[3].replace("type=","")
		if name == "." or name == "..":
			#print("skipping")
			pass
		elif fileType == "dir":
			#print("going into: " + name)
			ftp.cwd(name)
			runSize += getsize()
			ftp.cwd("..")
		else:
			#print(str(size))
			#print(str(runSize))
			runSize += size
	return runSize


try:
	taxonomy = ""

	#getting arguments from command line and validating
	if len(sys.argv) == 2:
		taxonomy = sys.argv[1]
		print("Getting size of: " + taxonomy)
	else:
		print("usage: paython taxosize taxonomy")
		print("example: python taxosize human")
		sys.exit(0)

	#runing query with esearch on NCBI assembly DB to get file refseq folders
	taxoFileNames = os.popen("/opt/edirect/esearch -db assembly -query '" + taxonomy + " AND latest[SB]' | efetch -format docsum | xtract -pattern DocumentSummary -element FtpPath_RefSeq").read()

	#open ftp connection
	from ftplib import FTP
	ftp = FTP('ftp.ncbi.nih.gov')
	ftp.login()

	#set initial total size

	#parse each refseq forder to get file sizes
	buf = io.StringIO(taxoFileNames)
	fileDir = buf.readline()

	while fileDir != "":
		#print("Processing Taxo: " + fileDir)
		#Remove ftp portion of the path
		filePath = fileDir.replace("ftp://ftp.ncbi.nlm.nih.gov/", "").replace('\n','').replace('\r','')
		#print("Stripped down ftp: " + filePath)
		#split the folder paths
		pathItems = filePath.split('/')
		#move into the end of the path
		x=0
		while x < len(pathItems):
			path = pathItems[x]
			#print("Changing path to: " + path)
			ftp.cwd(path)
			x += 1

		totalSize += getsize()

		#Get next file directory to process
		fileDir = buf.readline()
		#move ftp location back to the root
		ftp.cwd("/")

	#quit ftp client
	ftp.quit()

	#format total file size
	from hurry.filesize import size
	strSize = size(totalSize)
	print("Total files size: " + strSize)

except Exception:
	print("Error while running taxosize...")
	print("usage: python taxosize taxonomy")
	print("example: python taxosize human")
	#traceback.print_exc(file=sys.stdout)
sys.exit(0)
