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

    # JQL to fetch issues
    for issue in jira.search_issues('project=TEST order by Created ASC'):

        # Issue Id and Key
        id = issue.id
        key = issue.key

        # Issue Number
        issuenum = issue.key.split("-")[1]

        # Normal Fields
        issue_type = issue.fields.issuetype
        summary = issue.fields.summary
        assignee = issue.fields.assignee
        priority = issue.fields.priority
        status = issue.fields.status
        resolution = issue.fields.resolution

        # Multiselect Custom Fields
        countries_array = issue.fields.customfield_10200
        countries = []
        for country in countries_array:
            countries.append((country.value).encode('ascii'))

        domains_array = issue.fields.customfield_10201
        domains = []
        for domain in domains_array:
            domains.append((domain.value).encode('ascii'))

        # Normal Custom Fields
        clarity_ID = issue.fields.customfield_10202
        vendor_management = issue.fields.customfield_10203

        # Date Field
        created = dateutil.parser.parse(issue.fields.created)
        updated = dateutil.parser.parse(issue.fields.updated)

        # Linked Issues
        linkedissue = []
        for link in issue.fields.issuelinks:
            if hasattr(link, "outwardIssue"):
                linkedissue.append((link.outwardIssue.key).encode('ascii'))
            if hasattr(link, "inwardIssue"):
                linkedissue.append((link.inwardIssue.key).encode('ascii'))

        # Add data in CSV
        thewriter.writerow(
            [id, issuenum, issue_type, key, summary, assignee, priority, status, created, updated, resolution,
             linkedissue, countries, domains, clarity_ID, vendor_management])
