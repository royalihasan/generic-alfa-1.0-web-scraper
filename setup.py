# run_spider.py in the src directory
import subprocess
import sys
import os

def run_spider(spider_name):
    # Define the fixed relative path to your Scrapy project directory
    relative_project_path = "./src/generic_intel_scraper"
    
    # Change to the project directory
    try:
        print(f"Changing directory to {relative_project_path}")
        os.chdir(relative_project_path)
        print(f"Changed directory to {os.getcwd()}")
    except FileNotFoundError:
        print(f"Directory not found: {relative_project_path}")
        return

    try:
        subprocess.run(['scrapy', 'crawl', spider_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_spider.py <spider_name>")
    else:
        spider_name = sys.argv[1]
        run_spider(spider_name)
