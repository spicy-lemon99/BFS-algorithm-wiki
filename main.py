# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 18:58:34 2024

@author: Omar Al-Nablseih

for support contact omar.alnablseih@gmail.com
"""
import time
import requests
from bs4 import BeautifulSoup
import re
from collections import deque

class Node():
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent

start_time = time.time()

def get_wikipedia_links(url):
    print(f'searching {url}')
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all 'a' tags with href starting with '/wiki/'
    wiki_links = soup.find_all('a', href=re.compile(r'^/wiki/'))
    # Extract the href attribute from each 'a' tag and append to the list
    links_list = [link.get('href') for link in wiki_links]
    # Filter out administrative links and main page links
    links_list = [link for link in links_list if ':' not in link and link != '/wiki/Main_Page']
    # Add 'https://en.wikipedia.org' to each link to make them absolute
    links_list = ['https://en.wikipedia.org' + link for link in links_list]
    return links_list




def search_list(start_url, goal):
    # Create the initial node
    start = Node(state=start_url, parent=None)
    
    # Initialize a queue for the breadth-first search
    queue = deque([start])

    # Track visited links to avoid revisiting them
    visited = set()
    
    # Start breadth-first search
    while queue:
        # Dequeue the next node
        current_node = queue.popleft()

        # Add the current node's state to the visited set
        visited.add(current_node.state)
        
        
        # Get links from the current node's state
        links = get_wikipedia_links(current_node.state)
        
        # Enqueue new nodes for unvisited links
        for link in links:
            if link == goal:
                # Construct the path and return it immediately
                path = [link]
                while current_node is not None:
                    path.append(current_node.state)
                    current_node = current_node.parent
                return " -> ".join(reversed(path))

            if link not in visited:
                new_node = Node(state=link, parent=current_node)
                queue.append(new_node)
    
    # If the goal is not found
    return "Goal not found"

# Example usage
start_url = "https://en.wikipedia.org/wiki/Barack_Obama"
goal_url = "https://en.wikipedia.org/wiki/Computer_science"
result = search_list(start_url, goal_url)
print(result)
print("--- %s seconds ---" % (time.time() - start_time))
    
    
    
