#!/usr/bin/env python

import unicodecsv
import json
import glob

headers = ["ID", "Name", "Overall Rating", "No. of Ratings", "Work Life Balance", "Culture And Values", "Senior Leadership", "Compensation and Benefits", "Career Opportunities", "Sector", "Industry Name", "Website", "Glassdoor"]


def get_glassdoor_url(e):
    if "name" in e and "id" in e:
        return "https://www.glassdoor.com/Overview/Working-at-%s-EI_IE%d.htm" % (e["name"], e["id"])
    else:
        return "https://www.glassdoor.com"


def get_key_or_default(obj, key):
    val = ""
    if key in obj:
        val = obj[key]
    return val


def get_employer_data(e):
    result = []
    result.append(get_key_or_default(e, "id"))
    result.append(get_key_or_default(e, "name"))
    result.append(get_key_or_default(e, "overallRating"))
    result.append(get_key_or_default(e, "numberOfRatings"))
    result.append(get_key_or_default(e, "workLifeBalanceRating"))
    result.append(get_key_or_default(e, "cultureAndValuesRating"))
    result.append(get_key_or_default(e, "seniorLeadershipRating"))
    result.append(get_key_or_default(e, "compensationAndBenefitsRating"))
    result.append(get_key_or_default(e, "careerOpportunitiesRating"))
    result.append(get_key_or_default(e, "sectorName"))
    result.append(get_key_or_default(e, "industryName"))
    result.append(get_key_or_default(e, "website"))
    result.append(get_glassdoor_url(e))

    return result


if __name__ == "__main__":
    employers = []
    for f in glob.glob("data/raw/*.json"):
        print "Processing file = ", f
        with open(f) as ip:
            data = json.load(ip)
            if "response" not in data or "employers" not in data["response"]:
                print "Invalid file = %s" % (f)
                continue
            for e in data["response"]["employers"]:
                employers.append(get_employer_data(e))

    op_file = "data/companies.csv"
    with open(op_file, "wb") as op:
        csvwriter = unicodecsv.writer(op, quotechar='"', encoding="utf-8")
        csvwriter.writerow(headers)
        for e in employers:
            csvwriter.writerow(e)
    print "Complete. Output written to ", op_file
