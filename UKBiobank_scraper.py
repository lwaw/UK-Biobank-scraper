from urllib.request import urlopen
import sys
import re
import datetime
import json  

#cat basket_10036_columns2.txt | cut -f2 | sed '1d' > basket_10036_columns3.txt 

begin_time = datetime.datetime.now()
error_report = []
lost_columns = []

def get_input():
    if len(sys.argv) > 2:
        input_columns_file = sys.argv[1]
        output_columns_file = sys.argv[2]
    else:
        input_columns_file = input("Enter a columns txt file: ")
        output_columns_file = input("Enter an output txt file: ")
    return [input_columns_file, output_columns_file]

def read_file(input_columns_file):
    try:
        columns = []
        f = open(input_columns_file, "r")
        for line in f:
            columns.append(str(line.replace(" ","").strip()))
        f.close()
        return columns
    except:
        error_report.append("Could not open columns txt file")
        print_error_report()
        sys.exit()

def open_url(column, open_type = 0):
    global lost_columns
    
    if open_type == 0:
        column = column.split("-")
        url = "https://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=" + column[0]
    elif open_type == 1:
        url = "https://biobank.ndph.ox.ac.uk/showcase/coding.cgi?id=" + column
        
    try:
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        return html
    except:
        error_report.append("Could not open UKBiobank url for type:" + str(open_type) + " column: " + str(column))
        lost_columns.append(str(column[0]) + str(column[1]))
        return False
    
def build_data_dict(html, column):
    data_dict = {
        "column": column,
        "description": get_description(html, column),
        "notes": get_notes(html, column),
        "participants": get_participants(html, column),
        "item_count": get_item_count(html, column),
        "stability": get_stability(html, column),
        "value_type": get_value_type(html, column),
        "item_type": get_item_type(html, column),
        "strata": get_strata(html, column),
        "sexed": get_sexed(html, column),
        "instances": get_instances(html, column),
        "dates": get_dates(html, column),
        "cost_tier": get_cost_tier(html, column),
        "categories": get_categories(html, column),
        "related_data_fields": get_related_data_fields(html, column),
        "resources": get_resources(html, column),
        "data_coding": get_data_coding(html, column, get_value_type(html, column))
    }
    
    return data_dict
    
def get_description(html, column): 
    try:
        pattern = '<td>Description:</td><td>.*?</td></tr>'
        match_results = re.search(pattern, html, re.IGNORECASE)
       
        description = match_results.group()
        description = re.sub('<td>Description:</td><td>', "", description)
        description = re.sub('</td></tr>', "", description)
        
        description = description.strip()
    except:
         error_report.append("Could not search for pattern description in html file: " + column)
         description = ""   
        
    return description

def get_notes(html, column):
    try:
        pattern = '<h2>Notes</h2>.*?</div>'
        match_results = re.search(pattern, html, re.DOTALL)
        
        notes = match_results.group()
        notes = re.sub('<h2>Notes</h2>', "", notes)
        notes = re.sub('<p>', "", notes)
        notes = re.sub('</p>', "", notes)
        notes = re.sub('</div>', "", notes)
        
        notes = notes.strip()
    except:
        error_report.append("Could not search for pattern notes in html file: " + column)
        notes = ""   
        
    return notes

def get_participants(html, column): 
    try:
        pattern = '>Participants</a></td><td class="int_blu">.*?</td><td'
        match_results = re.search(pattern, html, re.IGNORECASE)
       
        Participants = match_results.group()
        Participants = re.sub('>Participants</a></td><td class="int_blu">', "", Participants)
        Participants = re.sub('</td><td', "", Participants)
        
        Participants = Participants.strip()
    except:
         error_report.append("Could not search for pattern participant in html file: " + column)
         Participants = ""   
        
    return Participants

def get_item_count(html, column): 
    try:
        pattern = '>Item count</a></td><td class="int_blu">.*?</td><td'
        match_results = re.search(pattern, html, re.IGNORECASE)
       
        item_count = match_results.group()
        item_count = re.sub('>Item count</a></td><td class="int_blu">', "", item_count)
        item_count = re.sub('</td><td', "", item_count)
        
        item_count = item_count.strip()
    except:
         error_report.append("Could not search for pattern count in html file: " + column)
         item_count = ""   
        
    return item_count

def get_stability(html, column): 
    try:
        pattern = '>Stability</a></td><td class="txt_blu">.*?</td><td'
        match_results = re.search(pattern, html, re.IGNORECASE)
        
        stability = match_results.group()
        stability = re.sub('>Stability</a></td><td class="txt_blu">', "", stability)
        stability = re.sub('</td><td', "", stability)
        
        stability = stability.strip()
    except:
         error_report.append("Could not search for pattern stability in html file: " + column)
         stability = "" 
         
    return stability

def get_value_type(html, column): 
    try:
        pattern = '>Value Type</a></td><td class="txt_blu">.*?</td><td'
        match_results = re.search(pattern, html, re.IGNORECASE)
        
        value_type = match_results.group()
        value_type = re.sub('>Value Type</a></td><td class="txt_blu">', "", value_type)
        value_type = re.sub('</td><td', "", value_type)
        
        value_type = value_type.strip()
    except:
         error_report.append("Could not search for pattern value_type in html file: " + column)
         value_type = "" 
         
    return value_type

def get_item_type(html, column): 
    try:
        pattern = '>Item Type</a></td><td class="txt_blu">.*?</td><td'
        match_results = re.search(pattern, html, re.IGNORECASE)
        
        item_type = match_results.group()
        item_type = re.sub('>Item Type</a></td><td class="txt_blu">', "", item_type)
        item_type = re.sub('</td><td', "", item_type)
        
        item_type = item_type.strip()
    except:
         error_report.append("Could not search for pattern item_type in html file: " + column)
         item_type = "" 
         
    return item_type

def get_strata(html, column): 
    try:
        pattern = '>Strata</a></td><td class="txt_blu">.*?</td><td'
        match_results = re.search(pattern, html, re.IGNORECASE)
        
        strata = match_results.group()
        strata = re.sub('>Strata</a></td><td class="txt_blu">', "", strata)
        strata = re.sub('</td><td', "", strata)
        
        strata = strata.strip()
    except:
         error_report.append("Could not search for pattern strata in html file: " + column)
         strata = "" 
         
    return strata

def get_sexed(html, column): 
    try:
        pattern = '>Sexed</a></td><td class="txt_blu">.*?</td><td'
        match_results = re.search(pattern, html, re.IGNORECASE)
        
        sexed = match_results.group()
        sexed = re.sub('>Sexed</a></td><td class="txt_blu">', "", sexed)
        sexed = re.sub('</td><td', "", sexed)
        
        sexed = sexed.strip()
    except:
         error_report.append("Could not search for pattern sexed in html file: " + column)
         sexed = "" 
         
    return sexed

def get_instances(html, column): 
    try:
        pattern = '>Instances</a></td><td class="txt_blu">.*?</td><td'
        match_results = re.search(pattern, html, re.IGNORECASE)
        
        instances = match_results.group()
        instances = re.sub('>Instances</a></td><td class="txt_blu">', "", instances)
        instances = re.sub('</td><td', "", instances)
        
        instances = instances.strip()
    except:
         error_report.append("Could not search for pattern instances in html file: " + column)
         instances = "" 
         
    if instances.startswith("Defined") and instances != "Defined (1)":
        try:
            column_instance = column.split("-")[1].split(".")[0]
            pattern = '>Instance ' + column_instance + '</a> :.*?\n'
            match_results = re.search(pattern, html, re.IGNORECASE)
            instance_date = match_results.group()
            instance_date = re.sub('>Instance ' + column_instance + '</a> :', "", instance_date)
            
            pattern = '.*?\('
            if re.search(pattern, instance_date, re.IGNORECASE):
                instance_date = re.sub('.*\(', "", instance_date)
                instance_date = re.sub('\).*', "", instance_date)
                
                instance_date = instance_date.strip()
            else:  
                instance_date = re.sub('.*\, ', "", instance_date)
                instance_date = re.sub(' to ', '-', instance_date)
                instance_date = re.sub('\..*', "", instance_date)
                
                instance_date = instance_date.strip()
        except:
            error_report.append("Could not search for pattern instances2 in html file: " + column)
            instance_date = ""
    else:
        instance_date = ""
         
    instance_dict = {
        "instances": instances,
        "instance_date": instance_date,
    }
        
    return instance_dict

def get_dates(html, column):    
    try:
        pattern = '>Version</a></td><td class="txt_blu">.*?</td></tr>'
        match_results = re.search(pattern, html, re.IGNORECASE)
        
        version_date = match_results.group()
        version_date = re.sub('>Version</a></td><td class="txt_blu">', "", version_date)
        version_date = re.sub('</td></tr>', "", version_date)
        
        version_date = version_date.strip()
    except:
        error_report.append("Could not search for pattern version in html file: " + column)
        version_date = ""
        
    try:
        pattern = '>Debut</a></td><td class="txt_blu">.*?</td></tr>'
        match_results = re.search(pattern, html, re.IGNORECASE)
        
        debut_date = match_results.group()
        debut_date = re.sub('>Debut</a></td><td class="txt_blu">', "", debut_date)
        debut_date = re.sub('</td></tr>', "", debut_date)
        
        debut_date = debut_date.strip()
    except:
        error_report.append("Could not search for pattern debut in html file: " + column)
        debut_date = ""
      
    date_dict = {
        "debut_date": debut_date,
        "version_date": version_date,
    }
    
    return date_dict

def get_cost_tier(html, column): 
    try:
        pattern = '>Cost Tier</a></td><td class="txt_blu">.*?</td>'
        
        match_results = re.search(pattern, html, re.IGNORECASE)
       
        item_count = match_results.group()
        item_count = re.sub('>Cost Tier</a></td><td class="txt_blu">', "", item_count)
        item_count = re.sub('</td>', "", item_count)
        
        item_count = item_count.strip()
    except:
         error_report.append("Could not search for pattern cost tier in html file: " + column)
         item_count = ""   
        
    return item_count

def get_categories(html, column):   
    category_dict = {}
    try:
        pattern = '<tr class="(?:row_odd|row_even)" id=".*?</td></tr>'
        match_results = re.findall(pattern, html, re.IGNORECASE)

        for row in match_results:     
            try:
                category_id = re.findall('href="label\.cgi\?id=.*?">', row, re.IGNORECASE)[0]
                
                category_id = re.sub('href="label\.cgi\?id=', "", category_id)
                category_id = re.sub('">', "", category_id)
                category_id = category_id.strip()
                
                try:
                    category_name = re.findall('href="label\.cgi\?id='+category_id+'">.*?</a>', row, re.IGNORECASE)[1]
                    
                    category_name = re.sub('href="label\.cgi\?id='+category_id+'">', "", category_name)
                    category_name = re.sub('</a>', "", category_name)
                    category_name = category_name.strip()
                    
                    category_dict.update( {category_id : category_name} )
                except:
                    pass
            except:
                pass        
    except:
        error_report.append("Could not search for pattern categories in html file: " + column)
        pass
        
    return [category_dict]

def get_related_data_fields(html, column):  
    related_data_fields_dict = {}
    
    try:
        pattern = '<tr class="(?:row_odd|row_even)"><td.*?</td></tr>'
        match_results = re.findall(pattern, html, re.IGNORECASE)
        
        for row in match_results:     
            try:
                related_data_fields_id = re.findall('href="field\.cgi\?id=.*?">', row, re.IGNORECASE)[0]
                
                related_data_fields_id = re.sub('href="field\.cgi\?id=', "", related_data_fields_id)
                related_data_fields_id = re.sub('">', "", related_data_fields_id)
                related_data_fields_id = related_data_fields_id.strip()
                
                try:
                    related_data_fields_desc = re.findall('<td class="txt">.*?</td>', row, re.IGNORECASE)[0]
                    
                    related_data_fields_desc = re.sub('<td class="txt">', "", related_data_fields_desc)
                    related_data_fields_desc = re.sub('</td>', "", related_data_fields_desc)
                    related_data_fields_desc = related_data_fields_desc.strip()
                except:
                    pass
                
                try:
                    related_data_fields_relation = re.findall('Field '+related_data_fields_id+'</a>.*?</td></tr>', row, re.IGNORECASE)[0]
                    
                    related_data_fields_relation = re.sub('Field '+related_data_fields_id+'</a>', "", related_data_fields_relation)
                    related_data_fields_relation = re.sub('</td></tr>', "", related_data_fields_relation)
                    related_data_fields_relation = related_data_fields_relation.strip() 
                except:
                    pass
                
                related_data_fields_dict.update( {related_data_fields_id : [related_data_fields_desc, related_data_fields_relation]} )
            except:
                pass
    except:
        error_report.append("Could not search for pattern related_data_fields in html file: " + column)
        pass
    return related_data_fields_dict
    

def get_resources(html, column): 
    resources_dict = {}
    
    try:
        pattern = '<tr class="(?:row_odd|row_even)" id=".*?</td></tr>'
        match_results = re.findall(pattern, html, re.IGNORECASE)
        
        for row in match_results:     
            try:
                resource_id = re.findall('href="refer\.cgi\?id=.*?">', row, re.IGNORECASE)[0]
                
                resource_id = re.sub('href="refer\.cgi\?id=', "", resource_id)
                resource_id = re.sub('">', "", resource_id)
                resource_id = resource_id.strip()
                
                try:
                    resource_name = re.findall('href="refer\.cgi\?id=.*?</a>', row, re.IGNORECASE)[1]
                    
                    resource_name = re.sub('href="refer\.cgi\?id='+resource_id+'">', "", resource_name)
                    resource_name = re.sub('</a>', "", resource_name)
                    resource_name = resource_name.strip()
                    
                    resources_dict.update( {resource_id : resource_name} )
                except:
                    pass
            except:
                pass
    except:
        error_report.append("Could not search for pattern resources in html file: " + column)
        pass
    
    return resources_dict

def get_data_coding(html, column, value_type):
    data_coding_dict = {}
    coding_dict = {}
    
    if value_type.startswith("Categorical"):
        try:
            pattern = 'coding.cgi\?id=.*?">'
            match_results = re.search(pattern, html, re.IGNORECASE)
        
            data_coding_id = match_results.group()
            data_coding_id = re.sub('coding.cgi\?id=', "", data_coding_id)
            data_coding_id = re.sub('">', "", data_coding_id)
            data_coding_id = data_coding_id.strip()
            
            data_coding_dict.update( {"data_coding_id" : data_coding_id} )
            
            data_coding_html = open_url(data_coding_id, 1)
            
            if data_coding_html != False:
                try:
                    pattern = '<tr class="(?:row_odd|row_even).*?</td></tr>'
                    match_results = re.findall(pattern, data_coding_html, re.IGNORECASE)
                    
                    for row in match_results:     
                        try:
                            coding = re.findall('><td class="int">.*?</td><td', row, re.IGNORECASE)[0]
                            
                            coding = re.sub('><td class="int">', "", coding)
                            coding = re.sub('</td><td', "", coding)
                            coding = coding.strip()
                            
                            meaning = re.findall('><td class="int">.*?</td><td class="txt">.*?</td></tr>', row, re.IGNORECASE)[0]
                            
                            meaning = re.sub('><td class="int">.*?</td><td class="txt">', "", meaning)
                            
                            pattern = 'This is a flat'
                            if len(re.findall(pattern, data_coding_html, re.IGNORECASE)) != 0:
                                meaning = re.sub('</td></tr>', "", meaning)
                            else:
                                meaning = re.sub('</td><td.*', "", meaning)
                            
                            meaning = meaning.strip()
                            
                            coding_dict.update( {coding : meaning} )
                        except:
                            pass
                    data_coding_dict.update( {"data_coding_types" : coding_dict} )
                except:
                    pass
        except:
            error_report.append("Could not search for pattern data_coding in html file: " + column)
            pass
    else:
        pass
    return data_coding_dict
    
    
def create_output_file(output_columns_file):
    f = open(output_columns_file, "w+")
    f.close()
    
def write_to_file(output_columns_file, data_dict):
    json_object = json.dumps(data_dict) 
    
    f = open(output_columns_file, "a")
    f.write(json_object)
    f.write("\n")
    f.close()
    
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    #https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
    
def print_error_report():
    for error in error_report:
        print(error)
    print("Number of columns lost: " + str(len(lost_columns)))
    print(lost_columns)
    print("Runtime: " + str(datetime.datetime.now() - begin_time))
    
def run():
    input_files = get_input()
    input_columns_file = input_files[0]
    output_columns_file = input_files[1]
    
    columns = read_file(input_columns_file)
    create_output_file(output_columns_file)
    
    length = len(columns)
    i = 0
    printProgressBar(i, length, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for column in columns:
        i = i + 1
        printProgressBar(i, length, prefix = 'Progress:', suffix = 'Complete', length = 50)
        html = open_url(column)
        
        if html != False:            
            data_dict = build_data_dict(html, column)
            write_to_file(output_columns_file, data_dict)
            
    print_error_report()
    
run()