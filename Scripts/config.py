 # Configuration file for Google Play scraping project
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
 

# Google Play app IDs and corresponding bank names 
APP_IDS={

    'CBE': os.getenv('CBE_APP_ID', 'com.combanketh.mobilebanking'),
    'BOA': os.getenv('BOA_APP_ID', 'com.boa.boaMobileBanking'),
    'DASHENBANK': os.getenv('DASHENBANK_APP_ID', 'com.dashen.dashensuperapp')

}

# Bank names Mapping
BANK_NAMES={

    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia',
    'DASHENBANK': 'Dashen Bank'

}

#SCRATING CONGIG
SCRAPING_CONFIG={

    'reviews_per_bank': int(os.getenv('REVIEWS_PER_BANK', 450)),
    'max_retries':int(os.getenv('MAX_RETRIES', 3)),
    'lang': 'en',
    'country': 'et'

}

#File PATH

DATA_PATHS= {

    'raw': 'data/raw',
    'processed': 'data/processed',
    'raw_reviews': 'data/raw/raw_reviews.csv',
    'processed_reviews': 'data/processed/processed_reviews.csv',
    'sentiment_results': 'data/processed/sentiment_results.csv',
    'final_results': 'data/processed/final_results.csv'

}
