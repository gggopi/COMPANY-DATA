import requests
import json
import re
from bs4 import BeautifulSoup
import lxml.html as html1
from lxml.html.clean import Cleaner
from goose import Goose
from commonregex import CommonRegex
urls=[


# 'http://www.callon.com'			### 	working
# ,'http://www.bkep.com'		 		###		working	
# ,'http://www.aeti.com'				### 	working
# ,'http://www.alphanr.com'			###		working	
# ,
# 'http://www.ntenergy.com'			### 	working

# ,'http://www.icdrilling.com'			###		working

# ,'http://www.lucasenergy.com'			### 	working

# ,'http://www.linnco.com'				### 	working
# ,'http://www.lilisenergy.com'			### 	working
# 'http://www.laredopetro.com'			####	working
# ,'http://www.kosmosenergy.com'			### 	working
# ,'http://www.matadorresources.com'		###		working
# ,'http://www.markwest.com'				###		working
# ,'http://glorienergy.com'				###   	 working
# ,'http://www.noblecorp.com'		###	   working
#,'http://www.crc.com'				###  working
#,'http://www.murphyoilcorp.com'					###		working
#,'http://www.millerenergyresources.com'			###		working
#,'http://www.midstatespetroleum.com'			###		working		### needs visible-text search selection
#,'http://www.nabors.com'					###		same problem as hollyfrontier 		### imp stuff inside 'form'
#,'http://www.nov.com'					###		same problem as hollyfrontier 		### imp stuff inside 'form' ###also unmatch word 'sustainability'
#,'http://www.ngsgi.com'				###		not working ### needs visible-text search selection
#,'http://www.nrplp.com'					###		not working ### needs visible-text search selection
#,'http://www.newconceptenergy.com'		### 	working  but website has less content

#,'http://www.magellanlp.com'				###		same problem as hollyfrontier 		### imp stuff inside 'form' 

#,'http://www.philips.co.in'			### too much data output  ###needs to be refined

#,'http://www.hollyfrontier.com'		### need to be worked on
#,'http://www.hpinc.com'				###  ok ok
#,'http://www.halliburton.com'		###  same problem as hollyfrontier  ###working but shitty output

#,'http://www.ballard.com'			###  more depth level   ####loads of shit  ### ok ok 		### working

#,'http://www.c-a-m.com'			###		shitty website ## ok ok 
#,'http://www.tataatsu.com'			### dont even try
#,'http://www.calumetspecialty.com'		### loads of shit  				###	ok ok
#,'http://www.cabotog.com'			### working but check it

#,'http://www.apachecorp.com'	###  too much data output  ###needs to be refined
#,'http://www.archcoal.com'		### working but check it



#'http://monsterbevcorp.com'		### not working
#,'http://www.solarcity.com'			# working about and team	
#,'http://www.firstsolar.com'			# working about and team
#,'http://www.sungrowpower.com/sungrow-english'	#working about and no mteam
#,'http://www.xinyisolar.com/en'		#working about  and no mteam
#,'http://www.akcome.com/en/gaikuang.asp'		###not working
#,'http://sfcegroup.com/en'		### not working  ## url error
#,'http://www.sicong.com/en'		#working about  and no mteam	
#,'http://sunrain.en.made-in-china.com'
#,'http://www.cccme.org.cn/shop/cccme6658/index.aspx'

#,'http://www.carabaogroup.com/en/home'
#,'http://www.trinasolar.com'


#,'http://www.bakerhughes.com'
# 'http://www.isfuel.com'
# ,'http://www.carbonsciences.com'
# ,'http://cellana.com'
# ,'http://www.sopogy.com'
# ,'http://www.myshipley.com'
# ,'http://www.shawcor.com'
# ,'http://www.invenergyllc.com'
# ,'http://islandpacificenergy.com'
# ,'http://www.iongeo.com'
#################,'http://www.theice.com'
#,
# 'http://www.nationalfuelgas.com'
# ,'http://www.nov.com'
# ,'http://www.nexteraenergyresources.com'


# ,'http://www.ngvamerica.org'
# ,'http://www.nuclearmeasurements.com'
# ,'http://www.oceaneering.com'
# ,'http://www.onegas.com'
# ,
'http://www.oneok.com'

# ,'https://www.directenergy.com'
# ,'http://www.coskata.com'
# ,'http://www.chattanooga-corp.com'
# ,'http://www.championenergyservices.com'

# ,'http://www.esolar.com'
# ,'http://www.slb.com'
# ,'http://solarmer.com'
# ,'http://www.sjindustries.com'
# ,'http://www.solarreserve.com'


# ,'http://www.sunlightgeneral.com'
# ,'http://www.susoils.com'
# ,'http://www.tallgrassenergylp.com'
# ,'http://www.tenaska.com'
# ,'http://www.tva.gov'
# ,'http://www.utilivisor.com'
# ,'http://www.weatherford.com'
# ,'http://williams.com'	
# ,'http://www.woodward.com'
]
ill = 0
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")

job=re.compile('.*team.*|.*contact.*|.*about.*|.*management.*|.*director.*',re.IGNORECASE)
job_okok=re.compile('.*team.*|.*contact.*|.*about.*|.*management.*|.*director.*|.*governance.*|.*exec.*',re.IGNORECASE)
unwanted=re.compile('.*join.*|.*project.*|.*blog.*|.*mailto.*|.*pdf.*|.*recruit.*|.*events?.*|.*facts.*|.*mission.*|.*values.*|.*faq.*|.*news.?r?.*|.*career.*|.*updates.*|.*history.*|.*vision.*|.*award.*|.*products.*|.*polic(y|ies).*|.*capabilities.*|.*feedback.*|.*support.*|.*innovaitons.*',re.IGNORECASE)
## NOTE: word 'resources removed from 'unwanted  and 'governance' is added.. add 'how.?.?we' = 1 add safety= 2
lang=re.compile('.*japanese.*|.*mandarin.*|.*portuguese.*|.*germen.*|.*french.*|.*twitter.*|.*linkedin.*|.*google.*',re.IGNORECASE)
err=re.compile('.*runtime.?error.*|.*403.?.?forbidden.*|.*not.?found.*',re.IGNORECASE)
noname=re.compile('.*region.*|.*information.*|.*recent.*|.*viewed.*|.*security.*|.*who.we.are.*|.*relat.*|.*our .*',re.IGNORECASE)
about=re.compile('.*about.*',re.IGNORECASE)
management=re.compile('.*management.*|.*directors.*|.*team.*|.*exec.*|.*bod.*|.*leadership.*|.*staff.*|.*board.*	',re.IGNORECASE)
contact=re.compile('.*contact.*',re.IGNORECASE)
members={}
boo=True
name=re.compile('([A-Z]. )?[A-Z][a-z]* ([A-Z]. )?[A-Z][a-z]*')
desig=['chief','executive','officer','secretary','accounting','operating','general','counsel','vice','president','senior','chairman','corporate','director','treasurer','principal','financial']
desc_link=[]
crawledLink=[]
word_pattern = re.compile('([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+[a-z]+)?(?:\s+[A-Z][a-z]+)+)')
#self.contiguous_words = re.findall(word_pattern,self.article.text) 
depth_level=0
for url in urls:
	ill=ill+1
	filname=url.replace('http://','')
	filname=filname.replace( 'https://','')
	filname=filname.replace('www.','')
	filname=filname.replace('.com','') 
	filname=filname.replace( '.org','')
	filname=filname.replace( '.gov','')
	print filname
	# with open('%s.json'%filname,"w") as outfile:
	# 	pass
	with open('%s.json'%filname,"w") as outfile:
		def crawl(link1):
			#print "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
			try:
				global depth_level
				depth_level=depth_level+1
				if depth_level<=10:
					html=requests.get(link1)
					soup1=BeautifulSoup(html.content)
					for l in soup1.find_all('a'):
						l1=str(l.get('href'))
						#print l1
						if not linkPattern.match(l1):
							if l1[0]!='/':
								l1=url+'/'+l1
							else:
								l1=url+l1

						if (job_okok.match(l1) or job_okok.match(l.get_text())) and  not ( unwanted.match(l1) or unwanted.match(l.get_text())) and not lang.match(l1) and not l1 in crawledLink:
							crawledLink.append(l1)								
							#print l1
							if not l1 in desc_link:
								desc_link.append(l1)
							a=crawl(l1)
				#print "ddddddddddddddddddddddddddddddddddddddddddddddddddd"
			except:
				print "ERROR with " + link1


		try:
			shtml=requests.get(url)

			desc_link=[]
			career_links=[]
			soup = BeautifulSoup(shtml.content)
			for link in soup.find_all('a'):
				link1=link.get('href')
				#print link1
				if (job_okok.match(str(link.get('href'))) or job_okok.match(link.get_text()))and not (unwanted.match(link1) or unwanted.match(link.get_text())) and not lang.match(link1):
					#print "tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
					if not linkPattern.match(link1) :
						if link1[0]!='/':
							link1=url+'/'+link1
						else:
							link1=url+link1
					if not link1 in crawledLink:
						crawledLink.append(link1)
						depth_level=0
						desc_link.append(link1)
						a=crawl(link1)
		except:
			pass
		print desc_link
		if len(desc_link)==0:
			desc_link.append(url)
		import urllib
		text=[]
		mem=[]
		new=0
		for link in desc_link:
			try:
				g=Goose()
				text=[]
				html = requests.get(link)    
				raw = BeautifulSoup(html.content)
				if err.match(str(raw('title'))) or err.match(str(raw('text'))):
					print "server error with "+link
					continue
				if about.match(link) and not management.match(link) and not contact.match(link) and not unwanted.match(link) and boo:
					print link
					about1={}
					about1['name']=g.extract(url=url).title						
					art=g.extract(url=link)
					
#					if not art.cleaned_text:
				 	soup=BeautifulSoup(requests.get(link).content)
					for s in soup('style'):
						s.extract()
					for s in soup('script'):
						s.extract()
					for s in soup('input'):
						s.extract()	
					licount=len(soup.find_all('li'))
					pcount=len(soup.find_all('p'))
					tdcount=len(soup.find_all('td'))
					divcount=len(soup.find_all('div'))
					print str(licount) + " " + str(pcount) + " " + str(tdcount)
# 					if divcount>pcount and divcount>tdcount and divcount>licount:
# 						for p in soup.find_all('div'):
# #							print p
# 							if len(p.get_text())>100:
# 								text.append(p.get_text())						
					if pcount>licount and pcount>tdcount:
						for p in soup.find_all('p'):
							if len(p.get_text())>100:
								text.append(p.get_text())
					#elif tdcount>licount and tdcount>pcount:
						# for t in soup.find_all('td'):
						# 	if len(t.get_text())>100:
						# 		text.append(t.get_text())
					#else:

						# for l in soup.find_all('li'):
						# 	if len(l.get_text())>100:
						# 		text.append(l.get_text())						
					else:
						text=art.cleaned_text
					about1['about']=text
					boo=False
					if not text:
						boo=True
					else:
						print about1

				if management.match(link) and not contact.match(link):
					try:
						soup=BeautifulSoup(requests.get(link).content)
						print link
						for s in soup('style'):
							s.extract()
						for s in soup('script'):
							s.extract()
						for s in soup('input'):
							s.extract()
						for s in soup('a'):
							s.extract()
								
						#for t in soup.find_all('p'):
							#print t
						
						members={}
						
						added_dena=[]
						para=[]
						li=[]
						for p in soup.find_all('p'):
							para.append(p.get_text())
						#print para
						for word in soup.find_all(['b','strong','h1','h2','h3','p','span']):
							f=0
							txt=word.get_text()
							#print txt
							if len(txt)<20:
								
								#print txt
								for w in desig:
									#print w
									if w in txt:
										#print w
										f=1
										break


								if f==0 and name.match(txt) and not noname.match(txt) and not job.match(txt) and not txt in added_dena:# and not members['name']:
									members['name']=txt
									members['description']=''
									#print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
									#print members
									added_dena.append(txt)
									#new= new + 1
								# if not members['designation']:
								# 	for para in soup.find_all('p'or'div',text=members['name']):
								# 		print para
									if len(members['name'])<25:

										li=members['name'].split(' ')
										li1='|'.join(li)
										#print 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii'
										#print li1				
										li1=re.compile(li1)

										for para in soup.find_all('p'):
											para=para.get_text()
											#print para
					#						try:members['name']or li[0] or 
											if len(para)>50 and re.search( li[-1], para,re.IGNORECASE):
												#print 'jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj'
												#print para
												members['description']=members['description']+ ' '+para
										# if members['description']:
										# 	text2=members['description']
										# 	members['designation']=''
										# 	for t in text2.split(' '):
										# 		if t.lower() in desig:
										# 			members['designation']=members['designation']+t+' '
										# 		elif t.lower() in ['and',',']:
										# 			members['designation']=members['designation']+t+' '
									
									txt=members['name']
									if name.match(txt) and not noname.match(txt) and not job_okok.match(txt) and not unwanted.match(txt) and txt:	
										new= new + 1
										f=1
										#print 'listttttttttttttttttttttttttttttttttt'
										#print len(mem)
										#print 'dict==================='
										#print members
										if len(mem):
											for i in range(len(mem)):
												#print i
												#print mem[i]['name'] 
												if mem[i]['name']==members['name']:
													f=0
													if len(mem[i]['description'])<=len(members['description']):
														mem[i]['description']=members['description']
													else:
														pass
													break
										#else:
											#mem[0]=members
										if f:
											#print 'abc'
											mem.append(members)
											#print 'def'
											members={}
								
							elif len(txt)<100:
								pass
					except:
						print "ERROR1 with " + link
		#print mem
			except:
				print "ERROR2 with " + link
		try:
			about1['members']=mem
			json.dump(about1,outfile)
			#json.dump(mem,outfile)
		except:
			print "json ERROR"

				# if management.match(link) and not contact.match(link):
				# 	soup=BeautifulSoup(requests.get(link).content)
				# 	print link
				# 	for s in soup('style'):
				# 		s.extract()
				# 	for s in soup('script'):
				# 		s.extract()
				# 	for s in soup('input'):
				# 		s.extract()		
				# 	#for t in soup.find_all('p'):
				# 		#print t
				# 	new=0
				# 	members={}#'name':'','designation':'','description':''}
				# 	mem={}
				# 	added_dena=[]
				# 	para=[]
				# 	for p in soup.find_all('p'):
				# 		para.append(p.get_text())
				# 	#print para
				# 	for word in soup.find_all(['b','strong','h2','h3','p']):
				# 		f=0

				# 		txt=word.get_text()
				# 		#print txt
				# 		for w in desig:
				# 			#print w
				# 			if w in txt:
				# 				#print w
				# 				f=1
				# 				break
				# 		if f==0 and name.match(txt) and not txt in added_dena:# and not members['name']:
				# 			members['name']=txt
				# 			added_dena.append(txt)

				# 		if len(members)>0:
				# 			for para in soup.find_all('p'):
				# 				para=para.get_text()
				# 				try:

				# 					if len(para)>100 and re.search( members['name'] , para ):
				# 						#print para
				# 						members['description']=para
				# 				except:
				# 					pass
				# 			#members['description']=''
				# 			print members
				# 			new= new + 1
				# 			mem[new]=members

				# 			members={}

#				except: print "ERROR with " + str(link)
				#outfile.write("  \n")
		#print about1
		#print mem