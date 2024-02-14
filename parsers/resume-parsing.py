import spacy
from spacy.matcher import Matcher
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from openai import OpenAI
import ast

custom_technology_stopwords = [
    'python', 'django', 'terraform', 'javascript', 'html', 'css', 'java',
    'c++', 'c#', 'ruby', 'php', 'node.js', 'react', 'angular', 'vue.js',
    'aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'jenkins',
    'git', 'github', 'bitbucket', 'ansible', 'puppet', 'chef', 'terraform',
    'linux', 'unix', 'windows', 'macos', 'mysql', 'postgresql', 'mongodb',
    'redis', 'nginx', 'apache', 'graphql', 'rest', 'api', 'json', 'xml',
    'agile', 'scrum', 'kanban', 'devops', 'continuous integration',
    'continuous deployment', 'machine learning', 'deep learning',
    'artificial intelligence', 'data science', 'big data', 'blockchain',
    'cloud computing', 'serverless', 'microservices', 'api gateway',
    'typescript', 'bash', 'shell', 'powershell', 'vue', 'redux', 'mobx', 'tools', 'monitor' 'micro', 'service', 
]

custom_stopwords = set(stopwords.words('english') + custom_technology_stopwords)

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

def remove_stopwords(text):
    # Tokenize the text into words
    words = word_tokenize(text)

    # Remove stopwords
    filtered_words = [word for word in words if word.lower() not in custom_stopwords]

    # Join the filtered words back into a string
    filtered_text = ' '.join(filtered_words)

    return filtered_text

def preprocess_text(text):
    # Tokenize the text into words
    words = word_tokenize(text)

    # Remove stopwords, including the custom ones, before stemming and lemmatization
    filtered_words = [word for word in words if word.lower() not in custom_stopwords]

    # # Initialize stemming and lemmatization tools
    # stemmer = PorterStemmer()
    # lemmatizer = WordNetLemmatizer()

    # # Apply stemming and lemmatization
    # stemmed_and_lemmatized_words = [lemmatizer.lemmatize(stemmer.stem(word)) for word in filtered_words]

    # # Join the filtered words back into a string
    # preprocessed_text = ' '.join(stemmed_and_lemmatized_words)

    return ' '.join(filtered_words)


def extract_name(resume_text):
    processed_text = preprocess_text(resume_text)
    # print(processed_text)
    nlp_text = nlp(processed_text)
    
     # Patterns for First name and Last name as Proper Nouns
    pattern1 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    # Patterns for First name and Middle name and Last name as Proper Nouns
    pattern2 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]

    pattern3 = [{'POS': 'PROPN'}]

    # Add additional patterns as needed

    # Add all patterns to the matcher
    matcher.add('NAME', patterns=[pattern3])
    
    
    matches = matcher(nlp_text)

    matches_array = []
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        matches_array.append(span.text)
    
    print(matches_array)

    client = OpenAI()

    response_criteria = "Your response should only be an array of name identified_names with no text before or after whatsoever."
    message_content = f"You are a name finder chatbot. I will give you a list of random names extracted from a resume, you have to find the ones which best match the name of a actual person, filter out any ambiguous names or names of technologies/frameworks/skills/places/things. {response_criteria}.\n{matches_array}"

    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=[
        {"role": "user", "content": message_content}
    ])
    
    return completion

def redact_names(resume_string, names_pattern):
    print(names_pattern)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(?:\+\d{1,2}\s?)?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,5}[-.\s]?\d{1,5}\b'


    # Substitute email addresses with 'REDACTED_EMAIL' and phone numbers with 'REDACTED_PHONE'
    redacted_email = re.sub(email_pattern, 'REDACTED_EMAIL', resume_string)
    redacted_phone_number = re.sub(phone_pattern, 'REDACTED_PHONE', redacted_email)

    names_pattern_aggregated = ""

    try:
        for name_pattern in names_pattern:
            separated_name = name_pattern.split(" ")
            names_pattern_aggregated = names_pattern_aggregated + "|".join(separated_name) + "|"
    except Exception as e:
        print(f"failed due to an error {e}")
    
    print(names_pattern_aggregated)
    parsed_resume_text = re.sub(r'\b' + names_pattern_aggregated[0:-1] + r'\b', 'REDACTED_NAME', redacted_phone_number, flags=re.IGNORECASE)

    return parsed_resume_text


Resume_String='''
Muhammad Usman Rashid
PRiNCiPAL SOFTWARE ENGiNEER.
+92-300-9439-143 | usman727@gmail.com |usman-rashid
Skills
Programming Python,PHP,C++,JavaScript,JQuery,Node.js,ReactJS,BackboneJS,XML,JSON,HTML5,CSS3
Frameworks FastAPI,Django,Flask,Laravel
TaskManagement GIT,GitLab,Jira,TeamWork,Trello
Databases MySQL,PostgreSQL,MSSQL,Mongo
Platforms Serverless,Microservices,Kubernetes,Docker,Jenkins,AWS,GCP,SuiteCRM,SugarCRM
OperatingSystem Windows,Linux
APIs REST
Integrations DocuSign,Paypal,Stripe,Chargify,Xero,Twilio
Experience
TechnoGenics(StrikeReadySAASProduct) Lahore,Pakistan
PRiNCiPAL SOFTWARE ENGiNEER(FULL TiME) 1stNov. 2021‑currentlyworking
•Designing,coding,integratinganddebuggingapplications.
•Ensureadherencetostandardsandbestpractices(e.g.,sourcecodecontrol,codereviews,followPEP8standardsetc.)
•Implementedtherevertfeatureoftheagentwhichisrunningintheclientenvironments(Windows,Linux,CentOS)asservice.
•Workingwithdevelopmentandprojectmanagementteamstodefineuserstoryacceptancecriteriaduringasprint,breakdowncom‑
plexstoriesintotasks,andestimate,plananddeliver.
•Encouragingapositiveworkingenvironmentacrossdisciplinesandteams,resultinginstrongeralignmentandProductcoordination
•Assigningtaskstoteamandensuringimplementationasperrequirements.
Rolustech Lahore,Pakistan
PRiNCiPAL SOFTWARE ENGiNEER(FULL TiME) 6November. 2012‑30Oct. 2021
•Managedprojectsandproductsthroughtheirdevelopmentcycletoshipontime.
•Leadteamsof5‑10engineersonmultipleprojectsthatincludesQA’sandsoftwaredevelopers.
•Helddailyscrummeet‑ups,bi‑weeklysprints,draftingprojectprogressionplans.
•Identifiedandresolvedcomplexdesignandtechnicalissuesofprojects.
•Providedend‑usersupporttoclients,handledbothlocalandglobalsitetechnicalissuesofprojects.
•Deliveredtechsessionondifferenttopics.
Projects
StrikeReadySAASProduct
TOOLS: PYTHON(FLASK), MiCROSERViCES, GCLOUD, CI/CD, POSTGRES, REDiS
Theproductbringstogethercontextualawareness,automation,knowledgeandcollaborationtomodernizesecurityoperationsand
integrateswithalltheleadingendpoint,networkandcloudandintelligencetechnologies.
TrackYourFiles–TYF
TOOLS: PYTHON, DJANGO, POSTGRESQL, VUE JS, DOCKER, GiT
TYFiscloudbasedproductwhichallowusertotracktheemailattachmentsandviewtheinterestoftheuserindocument.
GardenDesign
TOOLS: PHP, MYSQL, JQUERY, JAVASCRiPT, SUiTECRM, BOOTSTRAP 3, TEAMWORK, GiTLAB
Gardendesignworksonlandscapeandoutdoorlivingservices. Companyprovidesserviceslikesprinklersystem,irrigation,outdoor
kitchen,outdoorlightingandwaterfeaturesetc. Clientpurchasesitemsfromthirdpartyvendorsusingbiddingsystem. Oncebidding
processiscompletedthensystemcreatesitscontractandallocatestheworktocrewmembers. HRM(humanresourcemanagement)
systemisalsodevelopedwhereclientcaneasilymanagethepayrollandattendanceofitsemployee.
XeroPlugin
TOOLS: PHP, MYSQL, SUGARCRM, JQUERY,JiRA, GiTLAB
XeropluginwasdevelopedforsyncingdatabetweenSugarCRMandXero. Usingthispluginclientcaneasilysyncitsaccounts,invoices
andproductsfromSugarCRMtoXeroandviceversa.
Education
FAST‑NU Lahore,Pakistan
BACHELOR OF SCiENCE, COMPUTER SCiENCE (BSCS) 2008‑2012
USMAN RASHiD · RÉSUMÉ 1
'''  


matched_str = extract_name(Resume_String)

name_patterns_response = matched_str.choices[0].message.content
name_patterns_response_parsed = ast.literal_eval(name_patterns_response)

processed_resume_string = redact_names(Resume_String, name_patterns_response_parsed)
print(processed_resume_string)
