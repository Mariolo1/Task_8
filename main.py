from fetcher_offers import JobFetcher 
from SQL_base import Database  

def main():
    # Pobranie ofert pracy
    fetcher = JobFetcher()
    job_data = fetcher.fetch_offers()

    # Zapisanie ofert pracy do bazy danych
    db_handler = Database()
    for job in job_data:
        db_handler.save_to_database(job)

    print("Dane zostały zapisane do bazy danych.")

if __name__ == "__main__":
    main()

