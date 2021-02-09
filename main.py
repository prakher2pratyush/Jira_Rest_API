from jira import JIRA
import dateutil.parser
import csv

# Initialization
jira = JIRA(basic_auth=('praprakher', 'XXXXXXX'), options={"server": "http://localhost:8080/"})

# Create CSV
with open('jiradump.csv', 'wb') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(
        ['id', 'issuenum', 'issue_type', 'key', 'summary', 'assignee', 'priority', 'status', 'created', 'updated',
         'resolution', 'linkedissue', 'countries', 'domains', 'clarity_ID', 'vendor_management'])
    
    issue_type = ""                                                                                       
    summary = ""
    assignee = ""
    priority = ""
    status = ""
    resolution = ""
    countries = []
    domains = []
    clarity_ID = ""
    vendor_management = ""
    created = ""
    updated = ""
    golivedate = ""
    linkedissue = []

    # JQL to fetch issues
    for issue in jira.search_issues('project in (TEST,DEV) order by Created ASC'):

        # Issue Id and Key
        id = issue.id
        key = issue.key

        # Issue Number
        issuenum = issue.key.split("-")[1]

        # Normal Fields
        try:                                                                                               
            issue_type = issue.fields.issuetype
        except:                                                                                            
            print("issue_type : " + id)

        try:
            summary = issue.fields.summary
        except:
            print("summary : " + id)

        try:
            assignee = issue.fields.assignee
        except:
            print("assignee : " + id)

        try:
            priority = issue.fields.priority
        except:
            print("priority : " + id)

        try:
            status = issue.fields.status
        except:
            print("status : " + id)

        try:
            resolution = issue.fields.resolution
        except:
            print("resolution : " + id)

        # Multiselect Custom Fields
        try:
            countries_array = issue.fields.customfield_10200
            countries = []                                                                                 
            for country in countries_array:
                countries.append(country.value.encode('ascii'))
        except:
            print("countries : " + id)

        try:
            domains_array = issue.fields.customfield_10201
            domains = []                                                                                   
            for domain in domains_array:
                domains.append(domain.value.encode('ascii'))
        except:
            print("domains : " + id)

        # Normal Custom Fields
        try:
            clarity_ID = issue.fields.customfield_10202
        except:
            print("clarity_ID : " + id)

        try:
            vendor_management = issue.fields.customfield_10203
        except:
            print("vendor_management : " + id)

        # Date Field
        try:
            created = dateutil.parser.parse(issue.fields.created)
        except:
            print("created : " + id)

        try:
            updated = dateutil.parser.parse(issue.fields.updated)
        except:
            print("updated : " + id)

        try:
            golivedate = dateutil.parser.parse(issue.fields.customfield_10300)
        except:
            print("golivedate : " + id)

        # Linked Issues
        try:
            linkedissue = []                                                                               
            for link in issue.fields.issuelinks:
                if hasattr(link, "outwardIssue"):
                    linkedissue.append(link.outwardIssue.key.encode('ascii'))
                if hasattr(link, "inwardIssue"):
                    linkedissue.append(link.inwardIssue.key.encode('ascii'))
        except:
            print("linkedissue : " + id)

        # Add data in CSV
        thewriter.writerow(
            [id, issuenum, issue_type, key, summary, assignee, priority, status, created, updated, resolution,
             linkedissue, countries, domains, clarity_ID, vendor_management, golivedate])
