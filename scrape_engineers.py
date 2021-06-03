# Imports
from selenium import webdriver
import csv, time, re, os, pathlib
from datetime import datetime
from dateutil import parser
from webdriver_manager.chrome import ChromeDriverManager

# PARAMS
WAIT_TIME = 10 # Time to wait after button click (in seconds)
# CHROMEDRIVER_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), "chromedriver")
OUTPUT_PATH = "engineers.csv"
URL = 'https://seisvelas.github.io/hn-candidates-search/'

# Access page
print("Accessing url...")
options = webdriver.ChromeOptions()
options.add_argument("headless") # Makes it so a Chrome window won't visibly open
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver = webdriver.Chrome(executable_path = CHROMEDRIVER_PATH, options=options)
driver.get(URL)

# Click button to display posts
print("\nLoading posts...")
button = driver.find_element_by_xpath("//div[@id='show-button-line']/span[1]")
button.click()

time.sleep(WAIT_TIME)
# driver.implicitly_wait(WAIT_TIME)

# Extract and write data
print("Extracting data...")
posts = [post.text for post in driver.find_elements_by_class_name("posting")]
with open(OUTPUT_PATH, "w+", encoding='utf-8') as csvfile:
	fieldnames = ["name",
				  "date",
				  # "location",
				  # "remote",
				  # "relocate",
				  "skills",
				  "resume/cv",
				  "email",
				  "post"]
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	# Compile regex patterns
	namePattern = re.compile('(?<=^Author: ).*?(?=\n)', re.MULTILINE)
	datePattern = re.compile('(?<=^Date: ).*?(?=\n)', re.MULTILINE)
	locationPattern = re.compile('(?<=Location: ).*?(?=\n)', re.MULTILINE)
	remotePattern = re.compile('(?<=Remote: ).*?(?=\n)', re.MULTILINE)
	relocatePattern = re.compile('(?<=Willing to relocate: ).*?(?=\n)', re.MULTILINE)
	skillsPattern = re.compile('(?<=Technologies: ).*?(?=\n)', re.MULTILINE)
	resumePattern = re.compile('(?:(?<=Résumé: )|(?<=Resume: )|(?<=CV: )).*?(?=\n)', re.MULTILINE)
	emailPattern = re.compile('(?<=Email: ).*?(?=\n)', re.MULTILINE)

	for post in posts:
		# Replace smart quotes and em dash
		# post = post.replace("‘", "'").replace("’", "'").replace("“", "\"").replace("”", "\"")
		post = re.sub(u"[‘’]", "'",
			   		re.sub(u"[“”]", '"', post)).replace("—", "-")

		# Fix email obfuscation (note: being lazy on the delimiter matching, but shouldn't matter outside of extremely rare edge cases)
		email = re.sub(r"\s+?(\.|[dD][oO0][tT])\s+?", ".", 
					re.sub(r"\s+?(@|[aA][tT])\s+?", "@", 
						re.sub(r"\s*?[\"'\|\[{(*<-]\s*?[cC]\s*?[oO0]\s*?[mM]\s*?[\"'\|\]})*>-]\s*?", "com", 
							re.sub(r"\s*?[\"'\|\[{(*<-](\s*?(([dD]\s*?[oO0]\s*?[tT])|\.|([pP][oO][iI][nN][tT]))\s*?)[\"'\|\]})*>-]\s*?", ".", 
								re.sub(r"\s*?[\"'\|\[{(*<-](\s*?(([aA]\s*?[tT])|@)\s*?)[\"'\|\]})*>-]\s*?", "@", 
									emailPattern.search(post).group(0).strip()))))).replace(" ", "") if emailPattern.search(post) else ""
		if email.endswith("gmail"): email = email + ".com"

		# Extract relevant data from post
		data = {"name" : namePattern.search(post).group(0).strip(),
				"date" : parser.isoparse(datePattern.search(post).group(0).strip()).strftime("%Y-%m-%d"), # datePattern.search(post).group(0),
				# "location" : locationPattern.search(post).group(0) if locationPattern.search(post) else "",
				# "remote" : remotePattern.search(post).group(0) if remotePattern.search(post) else "",
				# "relocate" : relocatePattern.search(post).group(0) if relocatePattern.search(post) else "",
				"skills" : skillsPattern.search(post).group(0).strip() if skillsPattern.search(post) else "",
				"resume/cv" : resumePattern.search(post).group(0).strip() if resumePattern.search(post) else "",
				"email" : email,
				"post" : post}
		writer.writerow(data)

driver.quit()