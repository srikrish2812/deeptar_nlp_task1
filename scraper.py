import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import cloudscraper
import traceback
from nltk import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')


class WebsiteScraper:
    """
    This scrapper class is constructed to obtain data from a website
    using cloudscraper. Cloudscraper worker well with websites that have
    cloudflare protection and anti-bot strategies
    
    Attributes:
        scraper(cloudscraper.Cloudscraper): This object handles HTTP requests
        page_nums(list): list for maintaining page numbers
        page_links: list for maintaining urls of pages that need to be scraped
        base_url: The base url of the website
    """
    scraper = cloudscraper.create_scraper(delay=10)
    
    def __init__(self, base_url="https://www.nhs.uk"):
        """
        Initializes the instance of the WebsiteScraper with base_url

        Args:
            base_url (str, optional): The base_url of the website. Default is "https://www.nhs.uk".
            page_nums(list): list for maintaining page numbers
            page_links(list): list for maintaining urls of pages that need to be scraped
        """
        self.base_url = base_url
        #self.num_pages = num_pages
        self.page_nums = []
        self.page_links = []
    
    def scrape_page_links(self, letter_index):
        """
        Scrapes and stores the urls of pages based on the letter index.
        In this method the urls of the websites are appended to 
        self.page_links and their respective numbers are appended to 
        self.page_nums

        Args:
            letter_index (int): It is the index of the letters in alphabetical order(A->0, B->1, ...)
        """
        scraper = cloudscraper.create_scraper(delay=10)
        page_response = scraper.get(self.base_url+'/conditions')
        soup = BeautifulSoup(page_response.text, 'html.parser')
        # letter_wise_content has info about all the diseases in an alphabetical order
        # It is a list of list. We will choose the second list as it has references to 100 diseases page links in it
        letter_wise_content = soup.find_all('ul',{"class":"nhsuk-list nhsuk-list--border"})
        page_number=1
        page_refs = letter_wise_content[letter_index].find_all('a')
        for page in page_refs:
            page_path = page['href']
            page_full_link = self.base_url+page_path
            self.page_links.append(page_full_link)
            self.page_nums.append(page_number)
            page_number+=1
    
    def scrape_info(self,url):
        """
        Scrapes the text from a specific website and returns it

        Args:
            url (str): The url of the website to be scraped

        Returns:
            str: It returns the scraped content from the website corresponding
            to the url. Returns an empty string if an error occurs.
        """
        scraper = cloudscraper.create_scraper(delay=10)
        try:
            page_response = scraper.get(url)
            soup = BeautifulSoup(page_response.text, 'html.parser')
            info = soup.get_text(separator=' ')
            return info
        except:
            print(f"Error occured while scraping {url}: {e}")
            return ""
        
    def scrape_pages(self, letter_index=1):
        """
        Extracts and returns content from multiple pages corresponding to
        a given letter index or alphabetical section(A->0, B->1)

        Args:
            letter_index (int, optional): The index of the required alphabetical section. Defaults to 1(B).
            The default value is set to 1 because it has 100 pages of data related to various health conditions

        Returns:
            list: List containing the scraped text from the web pages. Each element in a list
            corresponds to the scraped text of a particular page
        """
        self.scrape_page_links(letter_index)
        scraped_content = []
        for idx, page_link in enumerate(self.page_links):
            print(f"scraping content for page: {idx+1}")
            text = self.scrape_info(page_link)
            scraped_content.append(text)
        return scraped_content
    

class StatisticAnalyzer:
    """
    This class is used to calculate NLP related statistics like sentences_count, 
    word_count, number of nouns, number of verbs and average word length
    
    Attributes:
        texts(list): List of texts on which metrics or statistics need to be calculated
        page_numbers(list): page numbers list corresponding to each text
        statistics(list): List to store nlp-related statistics of each text
    """
    
    def __init__(self,texts, page_numbers ):
        """
        Initializes the instance of StatisticAnalyzer with page numbers and texts

        Args:
            texts (list[str]): List of texts on which metrics or statistics need to be calculated
            page_numbers (int): page numbers list corresponding to each text
        """
        self.texts = texts
        self.page_numbers = page_numbers
        self.statistics = []
        
    def analyze_each_text(self, text):
        """
        Analyzes a single text string corresponding to each page to compute various statistics like
        sentence count, word count, noun and verb count and average word length
        
        Args:
            text (str): The text string that needs to be analyzed

        Returns:
            dict: Dictionary of statistics
                - num_sentences(int): Number of sentences in the text
                - num_words(int): Number of words in the text
                - num_verbs(int): Number of verbs in the text
                - num_nouns(int): number of nouns in the text
                - average_word_length(float): average length of words in the text
                
        """
        
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        pos_tags = pos_tag(words)
        
        
        nouns = []
        verbs = []
        # Findinf nouns and verbs
        for word, tag in pos_tags:
            if tag.startswith('NN'):
                nouns.append(word)
            elif tag.startswith('VB'):
                verbs.append(word)
                
        # finding the average length
        if len(words)>0:
            avg_word_length = sum(len(word) for word in words)/len(words)
        else:
            avg_word_length = 0
                
        num_nouns = len(nouns)
        num_verbs = len(verbs)
        num_sentences = len(sentences)
        num_words = len(words)
        
        return {
            'num_sentences': num_sentences,
            'num_words': num_words,
            'num_verbs': num_verbs,
            'num_nouns': num_nouns,
            'average_word_length': avg_word_length
        }
        
    def analyze_texts(self):
        """
        Iterates over all the texts and calculates the statistics

        Returns:
            list: List of dictionaries containing page_number along with nlp-related stats for each text
            
        """
        for i, text in enumerate(self.texts):
            print(f"Analyzing text in page: {i+1}")
            each_text_stats = self.analyze_each_text(text)
            each_text_stats['page_number'] = self.page_numbers[i]
            self.statistics.append(each_text_stats)
        return self.statistics
    
    def save_stats(self, output_file='../statistics/nlp_stats.csv'):
        """
        Saves the statistics of all texts
        Args:
            output_file (str, optional): output file path. Defaults to '../statistics/nlp_stats.csv'.
        """
        df = pd.DataFrame(self.statistics)
        df.to_csv(output_file, index=False)
        
        print("Successfully saved statistic to statistics directory")
        
    def aggregate_stats(self, output_file = '../statistics/aggregate_stats.csv' ):
        df = pd.DataFrame(self.statistics)
        aggregated_statistics = df.mean().to_dict()
        aggregated_statistics_df = pd.DataFrame([aggregated_statistics])
        aggregated_statistics_df.to_csv(output_file, index=False)
        
        print("Aggregate statistics saved to statistics directory")
        
def main():         
    health_scraper = WebsiteScraper(base_url='https://www.nhs.uk')
    scraped_content = health_scraper.scrape_pages(letter_index=1)

    text_analyzer = StatisticAnalyzer(scraped_content, health_scraper.page_nums)
    text_analyzer.analyze_texts()
    text_analyzer.save_stats(output_file='../statistics/nlp_stats.csv')
    text_analyzer.aggregate_stats(output_file = '../statistics/aggregate_stats.csv')    

if __name__=="__main__":
    main()