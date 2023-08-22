NOTION_TOKEN = "secret_6pU74QOScoU19FE1KqFptMgD4mtATfiYzmH1ZAGnMpS"
DATABASE_ID = "8d299b4304d74afcba41356e0bc6502a"
import requests
import datetime
headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"

}

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {"page_size": 100}
    response = requests.post(url, headers=headers, json=payload)


    data= response.json()

    import json 
    with open('Notion_data.json', 'w', encoding='utf8') as f:
        json.dump(data, f,ensure_ascii=False, indent=4)

    results = data['results']
    return results


(get_pages())

def create_object(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {'parent': {'database_id': DATABASE_ID}, 'properties': data}

    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    return res.status_code




def update_page(page_id: str, data: dict):
    update_url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {'properties': data}
    print(payload)

    res = requests.patch(update_url, headers=headers, json=payload)
    print(res.status_code)
    return res.status_code


def delete_page(page_id: str):
    update_url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {'archived': True}

    res = requests.patch(update_url, headers=headers, json=payload)
    print(res.status_code)
    return res.status_code



page_id= "8627d8cd-2496-43ac-b954-0c78e9639ae9"

url = "Testing"
tile= "Testing"
published = datetime.datetime.now().astimezone().isoformat()



def add_event(event_name, date=None):

    if(date==None):
        data= {
        "Things to do": { "title": [{"text": {"content": event_name}}]},

        "Tags": {"multi_select": [{"name": "Workout"}]},

    }
    
    else:

        data= {
        "Things to do": { "title": [{"text": {"content": event_name}}]},
        
        "Due": {"date": {"start": date}},

        "Tags": {"multi_select": [{"name": "Workout"}]}
        ,

    }
    print(published)

    create_object(data)


add_event("This is a test")

def get_id(pages, id_to_find,name):
    for page in pages:
        # Accessing the 'properties' dictionary which contains the 'Things to do' key
        properties = page["properties"]
    
        # Accessing the 'Things to do' dictionary which contains the 'title' key
        things_to_do = properties["Things to do"]
    
         # Accessing the 'title' list which contains the text content
        title_list = things_to_do["title"]
    
        # The 'title' list contains a list of dictionaries, so we get the first dictionary
        title_info = title_list[0]
    
         # Accessing the 'text' dictionary which contains the 'content' key
        text_info = title_info["text"]
    
        # Finally, get the value of 'content'
        content = text_info["content"]

        if content == name:
            if(id_to_find == "status"):
                id = properties["Status"]["status"]["id"]
                return id






def update_status(page_id: str, data: dict,updated_status: str):
    data2= {
    "Status": { "status": {"name": updated_status,'color': 'blue'} },
}
    update_page(page_id, data2)

pages = get_pages()

