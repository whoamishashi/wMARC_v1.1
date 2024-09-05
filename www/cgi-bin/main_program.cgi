#!/usr/bin/python
	# 'shebang' causes script execution using python's command line interpreter

'''Script to accept details for running a program, run the required program, generate results, log reports.
The output page depends on whether the user name is a special ADMINISTRATOR string.
If so, past runs are read and displayed from the database file, otherwise normally details are taken, output displayed and session details recorded.
This script keeps only one copy of the data on programs run, delays and costs, and actively embeds the data in the form.
'''
# IMPORTING REQUIRED MODULES...
import cgi			# Support module for Common Gateway Interface (CGI) scripts
import time			# provides various time-related functions
import shlex			# provides a simple lexer (also known as tokenizer) for languages based on the Unix shell syntax.
#import string			# contains useful constants and classes, as well as some deprecated legacy functions that are also available as methods on strings
import os			# provides a portable way of using operating system dependent functionality.
import subprocess		# allows to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
#import cgitb			# provides a special exception handler designed to display extensive traceback information for Python CGI scripts.
#cgitb.enable()			# this function by default, redirects traceback to the browser.
import sys			# provides access to some variables and functions that interact strongly with the interpreter
import traceback		# provides a standard interface to extract, format and print stack traces of Python programs
import re			# Functions useful for working with regular expressions

ADMINISTRATOR   = 'admin'  	# administrator must know this string to use as the name!
PROGRAM_FILE    = 'record_programs.txt'
PROGbackup_FILE = 'backup_programs.txt'
DATABASE_FILE   = 'record_sessions.txt'
DBbackup_FILE   = 'backup_sessions.txt'
ERRLOG_FILE     = 'cgi_errlog'



def main():

    form = cgi.FieldStorage()				#  using FieldStorage class to get at form data
    #print form
    user = form.getfirst('user', '').lower()
    record_programs = form.getlist('edit')
    submit = form.getfirst('submit','')

    if re.search(r"[^\.\w\s]+" , user) != None:			# validating name
	user = ''
	submit = 'Home'

    if submit == 'Home':
        programName   = ''
        delay         = '00'
	parameterList = []
	n	      = 'Do not iterate'
	image	      = './plots/---please select---'
        pastState     = ''
        print processUser(user , programName, delay, n, parameterList, image, pastState)

    elif submit == '+':
	msg = '''<p align = "left">
		      <font color="#ff0000">&nbsp;&nbsp;&nbsp;&nbsp;<b>DIRECTIVES :</b><br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# 'Browse plots' and 'plots' cannot be renamed.<br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# Extra spaces appearing anywhere should be clipped off.<br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# Any changes in the names of executables and images should reflect in the 'www' directory.<br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# Include only alphanumeric characters, hyphens, periods and white spaces. Any changes otherwise will stand neglected.<br>
		      </font>
		 </p>
		 <input type="submit" style="width: 150" name = "submit" value="Submit"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		 <input type="submit" style="width: 100" name = "submit" value="Undo">'''
	print processAdministrator(fileLinesToHTMLLines(PROGRAM_FILE, submit), msg)

    elif submit == 'Undo':
	msg = '''<p align = "left">
		      <font color="#ff0000">&nbsp;&nbsp;&nbsp;&nbsp;<b>DIRECTIVES :</b><br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# 'Browse plots' and 'plots' cannot be renamed.<br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# Extra spaces appearing anywhere should be clipped off.<br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# Any changes in the names of executables and images should reflect in the 'www' directory.<br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# Include only alphanumeric characters, hyphens, periods and white spaces. Any changes otherwise will stand neglected.<br>
		      </font>
		 </p>
		 <input type="submit" style="width: 150" name = "submit" value="Submit"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		 <input type="submit" style="width: 100" name = "submit" value="Undo">'''
	print processAdministrator(fileLinesToHTMLLines(PROGbackup_FILE, ''), msg)

    else:
	# Handling any editing (if done) of the PROGRAM_FILE...
	if record_programs !=[] :
	    heading = fileToStr(PROGRAM_FILE).strip().splitlines()[0]
	    headingList = list([item for item in list(heading.split("	")) if item!=''])
	    totalItems = len(record_programs)-1
	    headingItems = len(headingList)
	    contents=''
	    for item in record_programs:
	        if totalItems % headingItems ==0 :
		    contents +=  item + '\n\n'
	        else:
		    contents += item + '\t\t'
	        totalItems -=1

	    if re.search(r"[^\.\w\s-]+" , contents) == None:	# validating contents received from the form.
	        fout = open(PROGRAM_FILE,'w')
	        fout.write(contents)
	        fout.close()

	    record_programms=[]

	if user == ADMINISTRATOR:  			# special case for identified administrator
	    user = form.getfirst('user','admin').lower()
	    pwd = form.getfirst('password','')
	    priviledge = form.getfirst('priviledge','')

	    headTemplate='''<table width="400" border="0">
	    		<tr>	<td>Username</td>  <td>:</td>  <td><b><input size="30" name ="user" value="admin"></b>     </td>	</tr>
	    		<tr>	<td>Password</td>  <td>:</td>  <td><b><input size="30" type="password" name="password"></b></td>	</tr>
	   	 	</table>
			<br> <b>Change the username to start a new session</b> <br><br>'''
	    admin_options = ''' <input type="submit" name="priviledge" value="Edit programs\' record"> &nbsp;&nbsp;&nbsp;&nbsp;
		  		<input type="submit" name="priviledge" value="View sessions\' report"> &nbsp;&nbsp;&nbsp;&nbsp;
				<input type="submit" name="priviledge" value="Clear sessions\' database">'''

	    if user == 'admin' and pwd == 'shashi123' and priviledge=="Edit programs\' record":
		# Backing up present contents...
	        fout = open(PROGbackup_FILE,'w')
	        fout.write(fileToStr(PROGRAM_FILE))
	        fout.close()

		msg = '''<p align = "left">
		      <font color="#ff0000">&nbsp;&nbsp;&nbsp;&nbsp;<b>DIRECTIVES :</b><br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# 'Browse plots' and 'plots' cannot be renamed.<br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# Extra spaces appearing anywhere should be clipped off.<br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# Any changes in the names of executables and images should reflect in the 'www' directory.<br>
		      &nbsp;&nbsp;&nbsp;&nbsp;# Include only alphanumeric characters, hyphens, periods and white spaces. Any changes otherwise will stand neglected.<br>
		      </font>
		 	</p>
		 	<input type="submit" style="width: 150" name = "submit" value="Submit"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		 	<input type="submit" style="width: 100" name = "submit" value="Undo">'''
	        print processAdministrator(fileLinesToHTMLLines(PROGRAM_FILE,''), msg)

	    elif user == 'admin' and pwd == 'shashi123' and priviledge=="View sessions\' report":
	        msg = '&nbsp;&nbsp; <input type="submit" name = "submit" value="Home">'
	        print processAdministrator(fileLinesToHTMLLines(DATABASE_FILE,''), msg)

	    elif user == 'admin' and pwd == 'shashi123' and priviledge=="Clear sessions\' database":
	        localtime = time.asctime( time.localtime(time.time()) )
		'''
	        file_data = fileToStr(DATABASE_FILE).strip()
	        heading   = file_data.splitlines()[0] + '\n'
		'''
		heading   = 'SYSTEM TIME\t\t\tUSER\t\tPROGRAM\t\t\tPARAMETER(S)\tDELAY\tITERATION\t\tRESULT\n\n'
		backup_data = '\nTime when backed up :'+ localtime + '\n\n' + fileToStr(DATABASE_FILE).strip() + '\n_______________________________\n'

	        fout = open(DATABASE_FILE,'w')
	        fout.write(heading)
	        fout.close()

	        fout = open(DBbackup_FILE,'a')
	        fout.write(backup_data)
	        fout.close()

	        msg = admin_options
 	        print processAdministrator(headTemplate, msg)

	    else:
	        if pwd == '':
		    msg = admin_options
 	            print processAdministrator(headTemplate, msg)
	        else:
		    msg = admin_options + '<br><br><font color="#ff0000">Please enter correct password</font>'
                    print processAdministrator(headTemplate, msg)
	else:
            programName   = form.getfirst('programList', '')
            delay         = form.getfirst('delayOptions','00')
	    parameterList = form.getlist ('parameters')	# note getting *list*: default or None if no field with that name was submited or if it is empty.
	    n	          = form.getfirst('n','Do not iterate')
	    image	  = form.getfirst('imageOptions','./plots/---please select---')
            pastState     = form.getfirst('pastState', '')
            print processUser(user , programName, delay, n, parameterList, image, pastState)

def processUser(user , programName, delay, n, parameterList, image, state):
    '''Process input details and return the final page as a string.
    The same basic form is used for the initial page as well as later pages, since the user is allowed to run multiple programs .
    The ONLY location of the program names and delays is here. This data is placed in the order form.'''
    
    # CREATING DROPDOWN LIST OF PROGRAM NAMES...
    parentList=[['---please select---','','0','none']];
    for line in file(PROGRAM_FILE):	# extracts a single line.
        if line.strip():		# checks if 'non-null' line.
            parentList.append(list([item for item in list(line.strip().split("	")) if item!=''])) # using 'TAB space' as separators within a line.
 					# list(line.strip().split("   ")): converts extracted line to a list of items.
					# [item for item in list(line.strip().split("   ")) if item!=''] : removes null items('') from the resulting list.
 					# finally a list_of_such_lists called 'parentList' is created.

    del (parentList[1])
    programTemplate = '''<option value="%s" %s > %s </option>'''
    program_dropdown = '<select name="programList" style="width:190">'
    for childlist in parentList:
        if programName==childlist[1]:
            substitutions = ( childlist[1], "selected", childlist[0])
        else:
	    if programName=='Browse plots':
		substitutions = ( childlist[1], 'style="font-weight:bold"', childlist[0])
	    else:
		substitutions = ( childlist[1], "", childlist[0])
        program_dropdown +=  programTemplate % substitutions


    '''
    [BEFORE]::::::::::::::::::::::::
    # CREATING DROPDOWN LIST OF DELAYS OR IMAGES...
    alldelayOptions = ['00', '02', '05', '10']
    delayTemplate   = '<option value="%s" %s > %s seconds </option>'
    imageORdelay_dropdown  = '<select name="delayOptions" style="width:190">'
    for option in alldelayOptions[0:]:
        if delay == option:
            substitutions = (option, "selected", option)
        else:
            substitutions = (option, "", option)
        imageORdelay_dropdown += delayTemplate % substitutions

    [AFTER] ::::::::::::::::::::::'''
    imageORdelay_dropdown = '<input value="%s" type= "text" maxlength="40" size="21" name="delayOptions">' % delay


    # GENERATING TEMPLATE FOR ITERATIONS...
    iterationTemplate='''&nbsp;&nbsp;Iteration behaviour &nbsp;&nbsp;&nbsp;:
			 Multiple	<input value="Multiple"       name="n" type="radio"		     >
			 &nbsp;&nbsp&nbsp;&nbsp;&nbsp;
			 Do not iterate <input value="Do not iterate" name="n" type="radio" checked="checked">'''

    # CHECKING CONDITIONS AND IMPLEMENTING THE APPROPRIATE WEB-PAGE...
    programDetail =['---please select---','','0','none']
    invitation    ='Please fill out and submit the following details...&nbsp; &nbsp;<font color="#ff0000">fields marked with an asterix are mandatory !</font>'
    resultTemplate=''
    outputTemplate=''
    msg           =''
    flag 	  =''
    meta_content  =''
    imageORdelay  ='Delay introduced (s)'
    parameterTemplate=''

    if not state == 'all_users':  	# initial display of order form
        state = 'all_users'	
    elif not user or not programName:   # must have a name and programName entered
        msg = '''<td colspan="4">
		  <font color="#ff0000">You must enter your name and select a program for a valid submission !</font>
		 </td>'''
        state = 'all_users'
    else:   				# with a name and a programName, NOW A CORRECT SUBMISSION !
        state = 'all_users'

	# RETRIEVING PROGRAM DETAILS...
	for childlist in parentList:
	    if programName==childlist[1]:
                programDetail=childlist[0:]

	NoOfParam= int(programDetail[2])

	# GENERATING TEMPLATE FOR COMMAND LINE PARAMETERS...
	if NoOfParam != 0:
	    parameterTemplate ='''&nbsp;&nbsp;Enter %s argument(s)* : ''' % programDetail[2]
	    textbox= '<input size="10" name ="parameters">&nbsp;&nbsp;'
	    while NoOfParam > 0:
		NoOfParam-=1
		parameterTemplate += textbox

	# GENERATING TEMPLATE FOR VIEWING IMAGES FROM 'plots' FOLDER...
	if programName.lower() == 'none':
	    imageORdelay = 'Image selected'
	    # GENERATING DROPDOWN FOR IMAGE NAMES...
	    cmdLineArg = "find ./plots -name '*.png'"
	    # GETTING .png files' LIST in subfolder 'plots'...
	    process = subprocess.Popen(cmdLineArg, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)		  
	    allimageOptions = ['./plots/--please select--'] + process.communicate()[0].splitlines()

	    imageTemplate = '<option value="%s" %s> %s </option>'
	    imageORdelay_dropdown = '<select name="imageOptions" style="width:190">'
	    for option in allimageOptions[0:]:
	        if image == option:
            	    substitutions = (option, "selected", option[8:])
        	else:
            	    substitutions = (option, "", option[8:])
		imageORdelay_dropdown += imageTemplate % substitutions

	    parameterTemplate =''
	    iterationTemplate=''

	    if image !='./plots/---please select---':
		resultTemplate ='''<b>%s</b>, you've provided the following information :
				<table width="1300" border="0">
    				<tr>	<td width="%s">Program title</td>  <td>:     </td>  <td><b>%s</b></td>	</tr>
    				<tr> 	<td>Image         	    </td>  <td>:     </td>  <td><b>%s</b></td>	</tr>
   	 			</table>
   	 	 		''' % (user.title(), '15%', programDetail[0], image[8:])

	 	currentImage= '<p align = "center"><img src="%s" alt="Image cannot be viewed... (possible causes: slow connection, error in src attribute, or a screen reader)" width="600" height="600"></p>' % image[1:]
		outputTemplate =  currentImage

	else:
	    returned_tuple =()
	    for item in parameterList:
		if re.search(r"[^\.\w:-]+" , item) != None:
		    returned_tuple = None
		    break
	    if returned_tuple != None:		# if any invalid parameter, returned_tuple is explicitly set to Nonetype
		returned_tuple = generateOutput(user, program_dropdown, imageORdelay_dropdown, programDetail, parameterList, delay, n )
	        if returned_tuple != None:		# if output is generated above function call does not return Nonetype 
		    (resultTemplate, outputTemplate,meta_content) = returned_tuple
		    parameterTemplate=''

	    """
	    # HANDLING DELAY VIA FIXED NUMBER OF ITERATIONS...Method II

	    if (not( n.isdigit() ) and n!='none') or n=='0':	#str.isdigit() : returns true if str is a '<whole number>' , false otherwise.
	        msg= '''<td colspan="4">
		         <font color="#ff0000">Number of iterations should be a positive integer !</font>
		        </td>'''
	    elif n=='1' or n=='none' or delay=='00':
	        returned_tuple = generateOutput(user, program_dropdown, imageORdelay_dropdown, programDetail, parameterList, delay, n )
	        if returned_tuple != None:		# function call may return Nonetype ( None : its not a string, its the type of 'nothing')
		    (resultTemplate, outputTemplate) = returned_tuple
	            parameterTemplate=''
		    iterationTemplate=''
	    else:
	        n = int(n)
	        # iterating (n-1) times...
	        while(n>1):
		    n-=1
		    returned_tuple = generateOutput(user, program_dropdown, imageORdelay_dropdown, programDetail, parameterList, delay, n )
		    if returned_tuple != None:		# if output is generated function call does not return Nonetype 
		        (resultTemplate, outputTemplate) = returned_tuple
		        parameterTemplate=''
		        iterationTemplate=''
		    print iterationOutput(invitation, user , program_dropdown, parameterTemplate, imageORdelay_dropdown, iterationTemplate, msg,resultTemplate,outputTemplate,state)
		    time.sleep(int(delay))		# suspends execution for the given number of seconds. The argument may be a floating point number.
		    
	        # for the last iteration...
	        returned_tuple = generateOutput(user, program_dropdown, imageORdelay_dropdown, programDetail, parameterList, delay, n )
	        if returned_tuple != None:		# if output is generated function call does not return Nonetype 
		    (resultTemplate, outputTemplate) = returned_tuple
		    parameterTemplate=''
		    iterationTemplate=''
	        #print "Content-type: text/html"	# print a standard header
	        #print

Condition in generateOutput : " if not(NoOfParam!=0 and parameterList==[]) and not(NoOfParam==0 and delay!='00' and n=='none'): "
				not(NoOfParam!=0 and parameterList==[])	   	: deals with program(s) with non-zero number of arguments
				not(NoOfParam==0 and delay!='00' and n=='none') : deals with program(s) with zero number of arguments
--------
def iterationOutput( delay, n, invitation, user , program_dropdown, parameterTemplate, imageORdelay_dropdown, iterationTemplate, msg, resultTemplate, outputTemplate, state):
    '''Prints output for n-1 number of iterations'''
    #print "Content-type: text/html"		# print a standard header
    #print 
    #meta_content ='<meta http-equiv="refresh" content="%s">' % delay
    return makePage('template_submission.html',  ( meta_content, invitation, '15%', '1%', '15%', user , program_dropdown, parameterTemplate, 'Delay introduced', imageORdelay_dropdown, iterationTemplate, msg, resultTemplate, outputTemplate, state))
	    """

    return makePage('template_submission.html',  ( meta_content, invitation, '15%', '1%', '15%', user , program_dropdown, parameterTemplate, imageORdelay, imageORdelay_dropdown, iterationTemplate, msg, resultTemplate, outputTemplate, state))

def generateOutput( user, program_dropdown, imageORdelay_dropdown, programDetail, parameterList, delay, n):
    '''HANDLING GENERATION OF OUTPUT'''
    resultTemplate=''
    outputTemplate =''
    flagTemplate  =''
    currentImage  =''
    output        =''				# overall output
    error         ='\n\n_______\n'		# overall errors
    currentPlot	  =''
    flag	  =''
    NoOfParam	  =int(programDetail[2])
    parent_retcode=''

    if not(NoOfParam!=0 and parameterList==[]):
	# HANDLING DELAY ...Method I
	if n == 'Do not iterate':
	    meta_content =''
	else:
	    meta_content ='<meta http-equiv="refresh" content="%s">' % delay

        # GENERATING SHELL COMMAND 'cmdLineArg'...
        cmdLineArg="./" 
        cmdLineArg += programDetail[1]
        for para in parameterList:
            cmdLineArg+=' '+ para

	if programDetail[0] == 'Play song':
	    cmdLineArg = 'vlc ' + cmdLineArg

	cmd_list= shlex.split(cmdLineArg) # breaks cmdLineArg into a list with the CORRECT tokenization for args in cmdLineArg
				  	  # converting a sequence of characters into a sequence of tokens.

	# CALLING CHILD-PROCESS EXECUTABLES, GETTING THE OUTPUT AND ERRORS...
	try:
	    subprocess_object = subprocess.Popen(cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds = True)		  						  # run shell commands from within Python code using class Popen of subprocess module.
					  # use of 'shell=True' is strongly discouraged in cases where the command string is constructed from external input.
	    child_output, child_error = subprocess_object.communicate()		# both will be strings
	    child_retcode = subprocess_object.returncode			# child return code, indirectly set by communicate()

	    # getting child-process output...
	    output = child_output

	    # handling child-process status...
	    if child_error == '':
		error += "\nCalled-process error stream data ...    None"
	    else:
		error += "\nCalled-process error stream data ...    " + child_error

	    if child_retcode == 0:
        	error += "\nExit status of called-process ...       Success"
	    else:
		error += "\nExit status of called-process ...       " + os.strerror(child_retcode)
		raise subprocess.CalledProcessError(child_retcode, cmd_list)

	    '''
    	    if child_retcode == 0:
        	error += "\nExit status of called-process ...       Success"
    	    elif child_retcode < 0:
        	error += "\nCalled-process was terminated by signal " + str(-child_retcode) + " : " + os.strerror(child_retcode)
    	    elif child_retcode == None:
		error += "\nCalled-process has not terminated yet ! "	    
    	    else:
        	error += "\nCalled-process returned ...             " + str( child_retcode) + " : " + os.strerror(child_retcode)
	    '''
	    # handling child-process status...
	except OSError, e:
      	    error     += "\nExit status of calling-process ...      Execution failed !	   \n\nException information...\n" + str(e)
	except ValueError, e:
	    error     += "\nExit status of calling-process ...      Oops! Invalid arguments \n\nException information...\n" + str(e)
	except Exception, e:
	    error     += "\nExit status of calling-process ...      Execution failed !	   \n\nException information...\n" + str(e)
	else:
	    parent_retcode = 0
	    error     += "\nExit status of calling-process ...      Success"

	    # cleanup handler...
	finally:
	    if child_error == '' and child_retcode == 0 and parent_retcode == 0:
	        flag='Success'
	    else:
	        flag='Errors detected'

	# GENERATING RESULT TEMPLATE...
	flagTemplate   ='<b><font color="#ff0000">%s</b></font>' % flag
	resultTemplate ='''<b>User input :<br> _____________</b>
			<table width="1300" border="0">
    			<tr>	<td width="%s">Program title</td>  <td>:     </td>  <td><b>%s	</b></td>	</tr>
    			<tr>	<td>Program name 	    </td>  <td>:     </td>  <td><b>%s	</b></td>	</tr>
    			<tr>	<td>Arguments    	    </td>  <td>:     </td>  <td><b>%s	</b></td>	</tr>
    			<tr> 	<td>Delay        	    </td>  <td>:     </td>  <td><b>%s s </b></td>	</tr>
    			<tr> 	<td>Iteration behaviour	    </td>  <td>:     </td>  <td><b>%s   </b></td>	</tr>
			<tr>	<td>		 	    </td>  <td>&nbsp;</td>  <td>&nbsp;	    </td>	</tr>
    			<tr>	<td><b>Result</b>	    </td>  <td>:     </td>  <td><b>%s	</b></td>	</tr>
   	 		</table>
   	 	 	''' % ('15%', programDetail[0], programDetail[1], parameterList, delay, n, flagTemplate)

	# GENERATING OUTPUT TABLE TEMPLATE...
	currentPlot = programDetail[3]
	output	    = '<pre>' + output + '</pre>'	# creating preformatted output template for being displayed in HTML (use CSS as a better option)
	error       = '<pre>' + error  + '</pre>'	# creating preformatted error  template for being displayed in HTML (use CSS as a better option)
	if currentPlot.lower() != 'none':
	    currentImage= '<img src="/%s" alt="Image cannot be viewed... (possible causes: slow connection, error in src attribute, or a screen reader)" width="600" height="600">' % currentPlot

	outputTemplate =  '''<table width="1300" border="1px" CELLPADDING="10" RULES=ALL FRAME=VOID >
    			 <th><h2>Output </h2></th>
			 <th><h2>Current plot   </h2></th>
    			 <tr>
			     <td align="left"   valign="top"> <p><code>%s%s</code></p> </td>
   		 	     <td align="middle" valign="top"> <p>%s</p>		    </td>
   		 	 </tr>
   		 	 </table>
   		 	 <br>
			 ''' % ( output, error, currentImage)

	# LOGGING REPORT IN DATABASE FILE ---
	localtime  = time.asctime( time.localtime(time.time()) )
	if n!='none' and n!='1':
	    n= str(n)
	access_log = '%s\t%s\t\t%s\t\t%s\t\t%s\t%s\t\t%s\n\n' % (localtime, user , programDetail[1], parameterList, delay, n, flag)
	append(DATABASE_FILE, access_log)

	return ( resultTemplate, outputTemplate, meta_content)
    return None 

def processAdministrator(headTemplate, msg):
    '''Generates templates for Administrator Priviledges'''
    return makePage('template_database.html', (headTemplate, msg))

# STANDARD FUNCTIONS AND CODE FROM HERE ON---
def append(fileName, s):
    """Append string s to file with name fileName.
    This fails if there are multiple people trying simultaneously."""
    fout = open(fileName,'a') 		# 'a' means append to the end of the file
    fout.write(s)
    fout.close()

def safePlainText(s):
    '''Return string is with reserved html markup characters replaced
    and newlines replaced by <br>.'''
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('\n', '<br>')	  # cgi.escape(s) escapes: < to &lt;	> to &gt;	& to &amp;


def fileLinesToHTMLLines(fileName, submit):
    """Allow lines of the file with name fileName to be embedded in html.
    This fails if there are multiple people trying.
    """
    # METHOD 1 : without proper layout
    """
    lines = fileToStr(fileName).splitlines()		# calls the user-defined function 'fileToStr()' , built-in function 'splitlines()'
    safeLines = list()					# creating list 'safelines()'
    for line in lines:
        safeLines.append(safePlainText(line))		# calls the function 'safePlainText()'
    return "<br>\n".join(safeLines)			# 'str.join(iterable)' returns a string which is the concatenation of the strings in the iterable. 
							# The separator between elements is the "string" providing this method.
    """
    # METHOD 2 : with tabular layout
    if fileName==DATABASE_FILE:
	editTemplate='%s'
    else:
	editTemplate = '<input value="%s" type= "text" maxlength="40" size="18" name="edit">'

    parentList=[]
    for line in file(fileName):
        if line.strip():	# extracts a single 'non-null' line.
            parentList.append(list([item for item in list(line.strip().split("	")) if item!='']))

    heading=''
    for childList in parentList[0]:
	heading += '<th><h3> %s </h3></th>' % (editTemplate % childList)

    rowsOfTable= heading
    for childList in parentList[1:]:
	columnsOfRow=''
	for item in childList:
	    columnsOfRow += '<td><p align = "center"> %s </p></td>' % (editTemplate % item)
	rowsOfTable += '<tr> %s </tr>' % columnsOfRow

    if submit == '+':
	columnsOfRow=''
	for childList in parentList[0]:
	    columnsOfRow += '<td><p align = "center"> %s </p></td>' % (editTemplate % '')

	rowsOfTable += '<tr> %s </tr>' % columnsOfRow
    if fileName== PROGRAM_FILE or fileName== PROGbackup_FILE:
	rowsOfTable += """<tr><td> %s </td></tr>""" % '<input type="submit" name ="submit" value="+">'

    tableTemplate ='''<table width="1200" border="0"> %s </table>''' % rowsOfTable
    return tableTemplate

def fileToStr(fileName): 
    """Return a string containing the contents of the named file."""
    fin = open(fileName);
    contents = fin.read();
    fin.close()
    return contents

def makePage(templateFileName, substitutions): 
    """Returns a string with substitutions into a format string taken
    from the named file.  The single parameter substitutions must be in
    a format usable in the format operation: a single data item, a
    dictionary, or an explicit tuple."""
    pageTemplate = fileToStr(templateFileName)
    return  pageTemplate % substitutions



print "Content-Type: text/html"     # Required header that tells the browser to render the text as html
print                               # blank line, end of headers

sys.stderr = sys.stdout		    # needed because the traceback prints to sys.stderr

try:
    main()
except:
    # METHOD I			    # traceback (if one occurs) gets displayed on client browser ( as HTML )
    """
    cgi.print_exception()
    """
    # METHOD II	(better)	    # traceback (if one occurs) gets logged to server storage ( in an error file ), and displayed on client browser
    errtime = '\n--- '+ time.ctime(time.time()) +' ---\n'
    errlog = open(ERRLOG_FILE, 'a')
    errlog.write(errtime)
    traceback.print_exc(None, errlog)
    errlog.close()

    #print "\n\n<PRE>"	# necessary to disable the word wrapping in HTML.
    #print fileToStr(ERRLOG_FILE).strip().splitlines()[-1]
    print '''
	<html>
	<body bgcolor="99CCFF" >
	<h1 style="background-color:3333FF;" align="center">
	<table border="0">
	<th>	  <p style="color:E0E0E0;"><font size="6"><u>wMARC</u></font>			</p>      </th>
	<tr> <td> <p style="color:E0E0E0;">web-based Murchison Widefield Array Receiver Console </p></td> </tr>
	</table>
	</h1>
	<h3>Sorry, a problem was encountered ! <br>__________________________________________</h3>
	<code>
	<p>Please try the following:
	<br>&nbsp;&nbsp;Make sure that the Web site address displayed in the address bar of your browser is spelled and formatted correctly.
	<br>&nbsp;&nbsp;If you reached this page by clicking a link, contact the Web site administrator to alert them that the link is incorrectly formatted.
	<br>&nbsp;&nbsp;Click the Back button to try another link.
	</p>
	<p>Technical Information (for support personnel):
	<br>&nbsp;&nbsp;<b>%s</b>
	<br>&nbsp;&nbsp;Please check the 'Error log' on the server for details.
	</p>
	</code>
	</body>
	</html>''' % fileToStr(ERRLOG_FILE).strip().splitlines()[-1]

