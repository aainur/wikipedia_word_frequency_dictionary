# Wikipedia Word-Frequency Dictionary

## Project Overview
The **Wikipedia Word-Frequency Dictionary** is a Python-based web application that fetches Wikipedia articles, processes text, and calculates word frequencies. The application allows users to specify a starting article and a depth to recursively fetch linked articles, counting word frequencies across the traversed content.

### Objective
Generate a word-frequency dictionary by recursively fetching Wikipedia articles, starting from a given article and depth. The dictionary includes word counts and percentages of their frequency in the content.

### Key Features
- **Starting Point**: Fetches the specified Wikipedia article.
- **Recursion**: Follows links within articles, up to a defined depth.
  - **Depth = 0**: Only the original article.
  - **Depth = 1**: Original article + direct links.
  - **Depth = 2**: Original article + links from direct links, and so on.
- **Avoids Repetition**: Prevents revisiting articles to avoid infinite loops.

## Features
### API Endpoints
1. **GET /word-frequency**  
   - **Parameters**: 
     - `article` (string): The title of the Wikipedia article to start from. For example, `Soda` (the Wikipedia article on soda).
     - `depth` (int): The depth of traversal within Wikipedia articles.
   - **Response**: A JSON object containing the word-frequency dictionary, including the count and percentage frequency of each word found in the traversed articles.

2. **POST /keywords**  
   - **Request Body**: 
     - `article` (string): The title of the Wikipedia article. For example, `Soda` (the Wikipedia article on soda).
     - `depth` (int): The depth of traversal.
     - `ignore_list` (array of strings): A list of words to ignore in the frequency analysis.
     - `percentile` (int): The percentile threshold for word frequency.
   - **Response**: A filtered word-frequency dictionary, excluding words from the ignore list and applying the percentile threshold.

### Technologies
- **FastAPI**: The web framework used for creating the API endpoints.
- **Uvicorn**: The ASGI server used to run the FastAPI app.
- **Wikipedia-API**: A Python package used to fetch Wikipedia content.
- **NLTK**: A toolkit for text processing, used to clean text, remove stopwords, and perform lemmatization.
- **Pytest**: A testing framework to write and run unit tests.


## File Structure
```bash
.
├── main.py               # FastAPI application and API logic
├── wikipedia_scraper.py  # Functions for fetching Wikipedia articles
├── text_processing.py    # Functions for text cleaning and word frequency calculation
├── tests.py              # Unit tests for the application
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Implementation Details

### Text Processing

The `text_processing.py` module handles:

- **Text Cleaning**: Removing punctuation and unnecessary characters.
- **Tokenization**: Splitting the content into words.
- **Stopwords Removal**: Common English words (e.g., "the", "is") are excluded from analysis using the NLTK stopwords list.
- **Lemmatization**: Words are reduced to their base form (e.g., "running" becomes "run") using WordNetLemmatizer from NLTK.
- **Word Frequency Calculation**: Words are counted and their percentages are calculated based on their frequency in the text.

### Wikipedia Scraping

- **Rate Limiting**: The Wikipedia API allows only one request per second. To respect this rate limit, `asyncio.Semaphore` is used to limit the number of concurrent requests to Wikipedia.
- **Recursive Scraping**: The application supports fetching articles recursively up to the specified depth. The links from each article are followed in a depth-first manner, but articles are not revisited to prevent infinite loops.

### Performance Optimization

- **Asynchronous Requests**: Asynchronous programming is used to fetch multiple articles concurrently while respecting Wikipedia’s rate limits.
- **Parallelism**: Up to 5 concurrent requests are allowed at a time to avoid bottlenecks.

## Running the Application

1. Clone the repository.
2. Install the required dependencies: 
```
bash pip install -r requirements.txt
```

3. Start the FastAPI server:
4. Access the API documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Example Requests

### GET /word-frequency

To fetch word frequencies for the article *Soda* at depth 2:
```
curl "http://127.0.0.1:8000/word-frequency?article=Soda&depth=2"
```

### POST /keywords

To fetch filtered word frequencies for the article *Soda*, excluding common words and using a 90th percentile threshold:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/keywords' \
  -H 'Content-Type: application/json' \
  -d '{
    "article": "Soda",
    "depth": 2,
    "ignore_list": ["soda", "drink", "carbonated"],
    "percentile": 90
}'
```

## Testing the Application

The project includes unit tests for validating the functionality. To run the tests, execute the following command:

```
pytest tests.py
```

## License

This project is licensed under the MIT License.

>>>>>>> ead30ce (Initial commit)
