# Main crawler, redefined using youtube video tips
import os
import sys
# import time
import modules
from tkinter import Tk, Button, Frame, Entry
from tkinter.scrolledtext import ScrolledText
from dotenv import load_dotenv
# import serpapi  

load_dotenv()

class Writer(object):
    def __init__(self):
        self.links = {}

    def write_Links(self, links):
        with open('output.txt', 'w') as fileOut:
            for url in links:
                fileOut.write(f"{url}\n")
        
            print(f"Written {len(links)} unique URLs to output.txt")

            fileOut.close()

class LinkCollector(object):
    def __init__(self):
        self.url = ""

    @staticmethod
    def collect_links(url):
        return modules.module1.getAllMainLinksFromURL(url)

class PrintLogger(object):
    # Setting up widget for logging
    def __init__(self, textbox):
        self.textbox = textbox
    
    def write(self, text):
        self.textbox.configure(state='normal')
        self.textbox.insert('end', text)
        self.textbox.see('end')
        self.textbox.configure(state='disabled')
    # This is needed to prevent the text widget from being edited directly
    def flush(self):
        pass

class MainGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.root = Frame(self)
        self.root.pack()

        # Setting up url input Entry
        self.url_input = Entry(self.root, width=50)
        self.url_input.insert(0, "https://")
        self.url_input.pack()

        # Buttons for interaction
        self.redirect_button = Button(self.root, text="Redirect console to widget", command=self.redirect_logging)
        self.redirect_button.pack()
        self.reset_button = Button(self.root, text="Reset console redirect", command=self.reset_logging)
        self.reset_button.pack()
        self.test_button = Button(self.root, text="Run crawl", command=self.start_crawl)
        self.test_button.pack()

        # Text widget for displaying output
        self.log_widget = ScrolledText(self.root, height=10, width=80, font=("consolas", "10", "normal"))
        self.log_widget.pack()

    def reset_logging(self):
        # Reset stdout and stderr to default
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def redirect_logging(self):
        # Redirect stdout and stderr to the text widget
        logger = PrintLogger(self.log_widget)
        sys.stdout = logger
        sys.stderr = logger

    def start_crawl(self):
        # Checks for input URL
        
        # for url in seed_urls:
        #     self.links_iter = iter(LinkCollector.collect_links(url))
        #     self.links = []
        #     self.process_next_link()

        url = self.url_input.get()
        if not url:
            print("Please enter a URL.")
            return

        # Check robots.txt
        rp = modules.module2.checkRobotsTxt(url)

        acceptedURL = modules.module2.robotsPermission(rp, url)
        if not acceptedURL:
            print("Crawling not permitted by robots.txt.")
            return
        else:
            # Start the link collection process
            self.links_iter = iter(LinkCollector.collect_links(acceptedURL))
            self.links = []
            self.process_next_link()

    def process_next_link(self):
        try:
            link = next(self.links_iter)
            # Print the line to console like intended
            print(link)
            self.links.append(link)
            self.after(10, self.process_next_link)  # Schedule next link
        # Apparently the program throws an exception when done    
        except StopIteration:
            if not self.links:
                # No links collected
                print("No links found.")
            else:
                # Writing to file eventually
                links = modules.module1.turnListIntoSetVersa(self.links)
                writer = Writer()
                writer.write_Links(links)


if __name__ == "__main__":
    app = MainGUI()
    app.geometry("700x400")
    app.mainloop()