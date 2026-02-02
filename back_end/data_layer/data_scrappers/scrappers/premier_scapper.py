"""
FBREF UNIFIED SCRAPER - MULTI-LEAGUE CONCURRENT SCRAPER
Scrapes multiple leagues concurrently with proper header handling
"""

import pandas as pd
import time
import re
import os
import json
import hashlib
import traceback
import concurrent.futures
import threading
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Set
from urllib.parse import urljoin
from collections import defaultdict, deque

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

class ThreadSafeCounter:
    """Thread-safe counter for tracking progress"""
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self, amount=1):
        with self._lock:
            self._value += amount
            return self._value
    
    def get(self):
        with self._lock:
            return self._value

class FBrefMultiLeagueScraper:
    """FBref scraper for multiple leagues with concurrent processing"""
    
    # League configurations
    LEAGUES = {
        'premier_league': {
            'id': 9,
            'name': 'Premier League',
            'url': 'https://fbref.com/en/comps/9/Premier-League-Stats',
            'country': 'England',
            'tier': 1
        },
        'la_liga': {
            'id': 12,
            'name': 'La Liga',
            'url': 'https://fbref.com/en/comps/12/La-Liga-Stats',
            'country': 'Spain',
            'tier': 1
        },
        'bundesliga': {
            'id': 20,
            'name': 'Bundesliga',
            'url': 'https://fbref.com/en/comps/20/Bundesliga-Stats',
            'country': 'Germany',
            'tier': 1
        },
        'serie_a': {
            'id': 11,
            'name': 'Serie A',
            'url': 'https://fbref.com/en/comps/11/Serie-A-Stats',
            'country': 'Italy',
            'tier': 1
        },
        'ligue_1': {
            'id': 13,
            'name': 'Ligue 1',
            'url': 'https://fbref.com/en/comps/13/Ligue-1-Stats',
            'country': 'France',
            'tier': 1
        },
        'eredivisie': {
            'id': 23,
            'name': 'Eredivisie',
            'url': 'https://fbref.com/en/comps/23/Eredivisie-Stats',
            'country': 'Netherlands',
            'tier': 1
        },
        'primeira_liga': {
            'id': 32,
            'name': 'Primeira Liga',
            'url': 'https://fbref.com/en/comps/32/Primeira-Liga-Stats',
            'country': 'Portugal',
            'tier': 1
        },
        'mls': {
            'id': 22,
            'name': 'MLS',
            'url': 'https://fbref.com/en/comps/22/Major-League-Soccer-Stats',
            'country': 'USA',
            'tier': 1
        },
        'championship': {
            'id': 10,
            'name': 'Championship',
            'url': 'https://fbref.com/en/comps/10/Championship-Stats',
            'country': 'England',
            'tier': 2
        },
        'serie_b': {
            'id': 18,
            'name': 'Serie B',
            'url': 'https://fbref.com/en/comps/18/Serie-B-Stats',
            'country': 'Italy',
            'tier': 2
        }
    }
    
    def __init__(self, headless=True, output_dir="./fbref_all_leagues", max_workers=3):
        self.headless = headless
        self.output_dir = output_dir
        self.max_workers = max_workers
        
        # Create directories
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "leagues"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "debug"), exist_ok=True)
        
        # Shared counters
        self.total_tables = ThreadSafeCounter()
        self.total_rows = ThreadSafeCounter()
        
        # League-specific scrapers
        self.league_scrapers = {}
        
        # Unified storage by league
        self.unified_data = {
            'fixtures': {},
            'teams': {},
            'player_basic_info': {},
            'player_stats': {},
            'player_match_logs': {},
            'team_stats': {}
        }
        
        # Setup lock for file writing
        self.file_lock = threading.Lock()
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        
        # Performance optimizations
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        options.add_argument('--window-size=1920,1080')
        
        # Disable images for faster loading
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
                'javascript': 1
            }
        }
        options.add_experimental_option('prefs', prefs)
        
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except:
            driver = webdriver.Chrome(options=options)
        
        driver.set_page_load_timeout(30)
        
        return driver
    
    def get_league_scraper(self, league_key):
        """Get or create a scraper for a specific league"""
        if league_key not in self.league_scrapers:
            self.league_scrapers[league_key] = LeagueScraper(
                league_info=self.LEAGUES[league_key],
                headless=self.headless,
                output_dir=os.path.join(self.output_dir, "leagues", league_key)
            )
        return self.league_scrapers[league_key]
    
    def scrape_league(self, league_key, max_teams=3, max_players_per_team=2):
        """Scrape a single league"""
        league_info = self.LEAGUES[league_key]
        print(f"\n🌍 Starting scrape for {league_info['name']} ({league_key})")
        
        try:
            scraper = self.get_league_scraper(league_key)
            results = scraper.scrape_league_data(
                max_teams=max_teams,
                max_players_per_team=max_players_per_team
            )
            
            # Merge results into unified storage
            with self.file_lock:
                for data_type, df in results.items():
                    if df is not None and not df.empty:
                        if data_type not in self.unified_data:
                            self.unified_data[data_type] = {}
                        self.unified_data[data_type][league_key] = df
                        
                        # Update counters
                        self.total_tables.increment(1)
                        self.total_rows.increment(len(df))
            
            print(f"✅ Completed {league_info['name']}: {len(results.get('teams', pd.DataFrame()))} teams, "
                  f"{len(results.get('player_basic_info', pd.DataFrame()))} players, "
                  f"{len(results.get('player_stats', pd.DataFrame()))} player stat tables")
            
            return league_key, True
            
        except Exception as e:
            print(f"❌ Error scraping {league_info['name']}: {e}")
            traceback.print_exc()
            return league_key, False
    
    def scrape_all_leagues_concurrently(self, leagues_to_scrape=None, max_teams=3, max_players_per_team=2):
        """Scrape multiple leagues concurrently"""
        if leagues_to_scrape is None:
            leagues_to_scrape = list(self.LEAGUES.keys())
        
        print("=" * 100)
        print(f"🌍 FBREF MULTI-LEAGUE CONCURRENT SCRAPER")
        print(f"📊 Leagues to scrape: {len(leagues_to_scrape)}")
        print(f"⚙️  Max concurrent workers: {self.max_workers}")
        print("=" * 100)
        
        start_time = datetime.now()
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all league scraping tasks
            future_to_league = {
                executor.submit(
                    self.scrape_league, 
                    league_key, 
                    max_teams, 
                    max_players_per_team
                ): league_key 
                for league_key in leagues_to_scrape
            }
            
            # Process as they complete
            for future in concurrent.futures.as_completed(future_to_league):
                league_key = future_to_league[future]
                try:
                    league_key, success = future.result()
                    results[league_key] = success
                    
                    # Print progress
                    completed = sum(1 for v in results.values() if v)
                    failed = sum(1 for v in results.values() if not v)
                    remaining = len(leagues_to_scrape) - len(results)
                    
                    print(f"\n📊 Progress: {completed} completed, {failed} failed, {remaining} remaining")
                    
                except Exception as e:
                    print(f"❌ Unexpected error for {league_key}: {e}")
                    results[league_key] = False
        
        # Save unified data
        self.save_unified_data()
        
        # Print summary
        self.print_summary(start_time, results)
    
    def save_unified_data(self):
        """Save all unified data to CSV files"""
        print("\n💾 Saving unified data...")
        
        # Create unified directory
        unified_dir = os.path.join(self.output_dir, "unified")
        os.makedirs(unified_dir, exist_ok=True)
        
        # Save each data type
        for data_type, league_data in self.unified_data.items():
            if league_data:
                try:
                    # Combine all leagues for this data type
                    all_dfs = []
                    for league_key, df in league_data.items():
                        if df is not None and not df.empty:
                            # Add league info if not present
                            if 'league' not in df.columns:
                                df = df.copy()
                                df['league'] = self.LEAGUES[league_key]['name']
                                df['league_key'] = league_key
                                df['country'] = self.LEAGUES[league_key]['country']
                                df['tier'] = self.LEAGUES[league_key]['tier']
                            all_dfs.append(df)
                    
                    if all_dfs:
                        combined_df = pd.concat(all_dfs, ignore_index=True, sort=False)
                        
                        # Clean column names
                        combined_df.columns = [self.clean_column_name(col) for col in combined_df.columns]
                        
                        # Remove completely empty columns
                        combined_df = combined_df.dropna(axis=1, how='all')
                        
                        # Save to CSV
                        output_file = os.path.join(unified_dir, f"all_leagues_{data_type}.csv")
                        combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')
                        
                        print(f"  ✓ Saved {data_type}: {len(combined_df)} rows from {len(all_dfs)} leagues")
                        
                        # Save sample for debugging
                        sample_file = os.path.join(self.output_dir, "debug", f"sample_{data_type}.csv")
                        combined_df.head(100).to_csv(sample_file, index=False, encoding='utf-8-sig')
                
                except Exception as e:
                    print(f"  ✗ Error saving {data_type}: {e}")
                    traceback.print_exc()
        
        print(f"\n📊 Unified data saved to: {unified_dir}")
    
    def print_summary(self, start_time, results):
        """Print scraping summary"""
        end_time = datetime.now()
        duration = end_time - start_time
        
        successful = sum(1 for v in results.values() if v)
        failed = sum(1 for v in results.values() if not v)
        
        print("\n" + "=" * 100)
        print("📊 SCRAPING SUMMARY")
        print("=" * 100)
        print(f"\n⏱️  Total duration: {duration}")
        print(f"✅ Successful leagues: {successful}/{len(results)}")
        print(f"❌ Failed leagues: {failed}/{len(results)}")
        print(f"📈 Total tables collected: {self.total_tables.get()}")
        print(f"📊 Total rows collected: {self.total_rows.get()}")
        print(f"💾 Output directory: {os.path.abspath(self.output_dir)}")
        
        # Print league-specific results
        print("\n📋 League Results:")
        for league_key, success in results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {self.LEAGUES[league_key]['name']}")
        
        # Save summary
        summary = {
            'total_leagues': len(results),
            'successful_leagues': successful,
            'failed_leagues': failed,
            'total_tables': self.total_tables.get(),
            'total_rows': self.total_rows.get(),
            'duration_seconds': duration.total_seconds(),
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'results': results,
            'output_directory': self.output_dir
        }
        
        summary_file = os.path.join(self.output_dir, "scraping_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
    
    def clean_column_name(self, col):
        """Clean a column name"""
        if not isinstance(col, str):
            col = str(col)
        
        # Replace special characters
        col = re.sub(r'[^\w\s]', '_', col)
        # Replace multiple spaces/underscores
        col = re.sub(r'[\s_]+', '_', col)
        # Remove leading/trailing underscores
        col = col.strip('_')
        # Convert to lowercase
        col = col.lower()
        
        return col

class LeagueScraper:
    """Scraper for a single league"""
    
    def __init__(self, league_info, headless=True, output_dir="./league_data"):
        self.league_info = league_info
        self.headless = headless
        self.output_dir = output_dir
        
        # Track processed items
        self.processed_teams = set()
        self.processed_players = set()
        
        # Storage for this league
        self.league_data = {
            'fixtures': [],
            'teams': [],
            'player_basic_info': [],
            'player_stats': [],
            'player_match_logs': [],
            'team_stats': []
        }
        
        # Setup driver
        self.driver = None
        self.setup_driver()
        
        # Create directories
        os.makedirs(output_dir, exist_ok=True)
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        
        # Performance optimizations
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        options.add_argument('--window-size=1920,1080')
        
        # Disable images for faster loading
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
                'javascript': 1
            }
        }
        options.add_experimental_option('prefs', prefs)
        
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        except:
            self.driver = webdriver.Chrome(options=options)
        
        self.driver.set_page_load_timeout(30)
        self.wait = WebDriverWait(self.driver, 20)
    
    def restart_driver(self):
        """Restart driver to prevent crashes"""
        try:
            self.driver.quit()
        except:
            pass
        self.setup_driver()
        time.sleep(2)
    
    def navigate_to_page(self, url, max_retries=3):
        """Navigate to page with retry logic"""
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                time.sleep(2)
                
                # Wait for page load
                WebDriverWait(self.driver, 15).until(
                    lambda d: d.execute_script('return document.readyState') == 'complete'
                )
                return True
                
            except WebDriverException as e:
                if "tab crashed" in str(e).lower():
                    print(f"    Tab crashed, restarting driver...")
                    self.restart_driver()
                    time.sleep(3)
                    continue
                    
                print(f"    Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(3)
                else:
                    return False
        
        return False
    
    def generate_id(self, *args):
        """Generate unique ID from given strings"""
        clean_str = "_".join(str(arg).replace(' ', '_').replace('-', '_').lower() for arg in args if arg)
        return hashlib.md5(clean_str.encode()).hexdigest()[:12]
    
    def safe_parse_int(self, value, default=0):
        """Safely parse integer from HTML attribute value"""
        if not value:
            return default
        try:
            # Extract only digits from the value
            digits = ''.join(filter(str.isdigit, str(value)))
            return int(digits) if digits else default
        except (ValueError, AttributeError):
            return default
    
    def extract_table_with_headers(self, table_soup, context=None):
        """Extract table data with proper headers from FBref table"""
        try:
            # First, extract headers
            headers = []
            
            # Look for header in thead
            thead = table_soup.find('thead')
            if thead:
                # Find the last row in thead (usually contains the actual column names)
                rows = thead.find_all('tr')
                if rows:
                    # Get the last row (most specific headers)
                    header_row = rows[-1]
                    # Extract header cells
                    header_cells = header_row.find_all(['th', 'td'])
                    
                    for cell in header_cells:
                        # Try different methods to get header text
                        data_stat = cell.get('data-stat', '')
                        aria_label = cell.get('aria-label', '')
                        cell_text = cell.get_text(strip=True)
                        
                        # Use data-stat if available, otherwise aria-label, otherwise text
                        if data_stat and data_stat not in ['', 'None']:
                            headers.append(data_stat)
                        elif aria_label and aria_label not in ['', 'None']:
                            headers.append(aria_label)
                        elif cell_text:
                            # Clean the text for use as column name
                            clean_text = re.sub(r'[^\w\s]', '_', cell_text)
                            clean_text = re.sub(r'\s+', '_', clean_text).strip('_').lower()
                            headers.append(clean_text)
                        else:
                            headers.append(f'col_{len(headers)}')
            
            # If no headers found in thead, try to get from first data row if it looks like headers
            if not headers:
                # Check first row if it contains th elements
                first_row = table_soup.find('tr')
                if first_row:
                    first_cells = first_row.find_all(['th', 'td'])
                    if all(cell.name == 'th' for cell in first_cells):
                        headers = [cell.get_text(strip=True) for cell in first_cells]
            
            # Now extract data rows
            data_rows = []
            
            # Find tbody or all rows if no tbody
            tbody = table_soup.find('tbody')
            rows_to_process = tbody.find_all('tr') if tbody else table_soup.find_all('tr')
            
            for row in rows_to_process:
                # Skip header rows and spacer rows
                row_classes = row.get('class', [])
                if any(cls in str(row_classes) for cls in ['thead', 'over_header', 'spacer', 'partial_table']):
                    continue
                
                # Skip if this row is from thead (already processed for headers)
                if thead and row in thead.find_all('tr'):
                    continue
                
                row_data = []
                cells = row.find_all(['td', 'th'])
                
                for cell in cells:
                    # Check for links
                    link = cell.find('a')
                    if link:
                        text = link.get_text(strip=True)
                    else:
                        text = cell.get_text(strip=True)
                    
                    # Clean text
                    text = re.sub(r'\s+', ' ', text).strip()
                    row_data.append(text)
                
                if row_data:
                    data_rows.append(row_data)
            
            if not data_rows:
                return None
            
            # Create DataFrame
            max_data_len = max(len(row) for row in data_rows)
            
            # Adjust headers to match data length
            if len(headers) < max_data_len:
                headers = headers + [f'col_{i}' for i in range(len(headers), max_data_len)]
            elif len(headers) > max_data_len:
                headers = headers[:max_data_len]
            
            # Pad data rows
            padded_rows = []
            for row in data_rows:
                if len(row) < max_data_len:
                    padded_rows.append(row + [''] * (max_data_len - len(row)))
                else:
                    padded_rows.append(row[:max_data_len])
            
            df = pd.DataFrame(padded_rows, columns=headers)
            
            # Add context information
            if context:
                for key, value in context.items():
                    if value:
                        df[key] = value
            
            # Add table metadata
            df['_table_scraped_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df['_table_type'] = context.get('table_type', 'unknown') if context else 'unknown'
            
            return df
            
        except Exception as e:
            print(f"    Error extracting table with headers: {e}")
            return None
    
    def scrape_league_fixtures(self):
        """Scrape fixtures for the league"""
        try:
            fixtures_url = f"https://fbref.com/en/comps/{self.league_info['id']}/schedule/"
            
            if not self.navigate_to_page(fixtures_url):
                print("    Failed to load fixtures page")
                return None
            
            time.sleep(2)
            
            # Find the fixtures table
            table = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.stats_table"))
            )
            table_html = table.get_attribute('outerHTML')
            soup = BeautifulSoup(table_html, 'html.parser')
            
            # Extract table data with headers
            context = {
                'league': self.league_info['name'],
                'league_id': self.league_info['id'],
                'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'table_type': 'fixtures'
            }
            
            df = self.extract_table_with_headers(soup, context)
            
            if df is not None:
                print(f"    Found fixtures: {len(df)} matches")
                return df
            
            return None
            
        except Exception as e:
            print(f"    Error scraping fixtures: {e}")
            return None
    
    def scrape_league_teams(self):
        """Scrape teams for the league with proper table headers"""
        try:
            if not self.navigate_to_page(self.league_info['url']):
                print("    Failed to load league page")
                return None
            
            time.sleep(2)
            
            # Find the standings table
            table = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.stats_table"))
            )
            table_html = table.get_attribute('outerHTML')
            soup = BeautifulSoup(table_html, 'html.parser')
            
            # Extract table data with headers
            context = {
                'league': self.league_info['name'],
                'league_id': self.league_info['id'],
                'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'table_type': 'team_standings'
            }
            
            df = self.extract_table_with_headers(soup, context)
            
            if df is None or df.empty:
                print("    No team data found in table")
                return None
            
            # Extract team links and create team information
            teams_data = []
            
            # Find all team links in the table
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/en/squads/' in href:
                    team_name = link.get_text(strip=True)
                    team_url = urljoin("https://fbref.com", href)
                    
                    # Find the corresponding row in the DataFrame
                    # Try to match by team name
                    matching_rows = df[df.apply(
                        lambda row: any(str(cell).strip() == team_name for cell in row if isinstance(cell, str)),
                        axis=1
                    )]
                    
                    if not matching_rows.empty:
                        team_row = matching_rows.iloc[0].to_dict()
                        
                        # Create team info with proper column names
                        team_info = {
                            'team_id': self.generate_id(team_name, self.league_info['name']),
                            'team_name': team_name,
                            'team_url': team_url,
                            'league': self.league_info['name'],
                            'league_id': self.league_info['id'],
                            'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        # Add all table columns to team info
                        for col_name, value in team_row.items():
                            if col_name not in team_info:  # Avoid overwriting existing fields
                                team_info[col_name] = value
                        
                        teams_data.append(team_info)
            
            # Remove duplicates based on team_url
            unique_teams = []
            seen_urls = set()
            for team in teams_data:
                if team['team_url'] not in seen_urls:
                    seen_urls.add(team['team_url'])
                    unique_teams.append(team)
            
            print(f"    Found {len(unique_teams)} teams")
            
            # Create DataFrame from teams data
            if unique_teams:
                teams_df = pd.DataFrame(unique_teams)
                
                # Add to league data
                self.league_data['teams'].append(teams_df)
                
                return teams_df
            
            return None
            
        except Exception as e:
            print(f"    Error scraping teams: {e}")
            return None
    
    def scrape_team_stats(self, team_info):
        """Scrape all statistical tables from a team page"""
        try:
            print(f"    Scraping team stats for: {team_info['team_name']}")
            
            if not self.navigate_to_page(team_info['team_url']):
                print(f"      Failed to load team page")
                return []
            
            time.sleep(2)
            
            # Get page content
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            
            # Find all stats tables
            tables = soup.find_all('table', class_=re.compile('stats'))
            
            team_stats_tables = []
            
            for i, table in enumerate(tables):
                # Extract table with headers
                context = {
                    'team_id': team_info['team_id'],
                    'team_name': team_info['team_name'],
                    'league': self.league_info['name'],
                    'league_id': self.league_info['id'],
                    'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'table_index': i,
                    'table_type': f'team_stats_{i}'
                }
                
                df = self.extract_table_with_headers(table, context)
                
                if df is not None and not df.empty:
                    team_stats_tables.append(df)
                    print(f"      Extracted team stats table {i} with {len(df)} rows")
            
            return team_stats_tables
            
        except Exception as e:
            print(f"      Error scraping team stats: {e}")
            return []
    
    def scrape_team_players(self, team_info, max_players=None):
        """Scrape players from a team"""
        try:
            if team_info['team_id'] in self.processed_teams:
                print(f"    Skipping already processed team: {team_info['team_name']}")
                return []
            
            print(f"    Scraping team: {team_info['team_name']}")
            
            if not self.navigate_to_page(team_info['team_url']):
                print(f"      Failed to load team page")
                return []
            
            time.sleep(2)
            
            # Get page content
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            
            # Find all player tables
            tables = soup.find_all('table', class_=re.compile('stats'))
            
            players_data = []
            
            # First, find the squad table that contains player links
            for table in tables:
                # Look for player links in this table
                player_links_found = False
                player_links = []
                
                for link in table.find_all('a', href=True):
                    href = link['href']
                    if '/en/players/' in href and '/matchlogs' not in href:
                        player_name = link.get_text(strip=True)
                        player_url = urljoin("https://fbref.com", href)
                        player_links.append((player_name, player_url))
                        player_links_found = True
                
                if player_links_found:
                    # Extract the table to get player stats
                    df = self.extract_table_with_headers(table)
                    
                    if df is not None and not df.empty:
                        for player_name, player_url in player_links:
                            # Find the corresponding row in the DataFrame
                            matching_rows = df[df.apply(
                                lambda row: any(str(cell).strip() == player_name for cell in row if isinstance(cell, str)),
                                axis=1
                            )]
                            
                            if not matching_rows.empty:
                                player_row = matching_rows.iloc[0].to_dict()
                                
                                # Create player basic info
                                player_info = {
                                    'player_id': self.generate_id(player_name, team_info['team_name']),
                                    'player_name': player_name,
                                    'player_url': player_url,
                                    'team_id': team_info['team_id'],
                                    'team_name': team_info['team_name'],
                                    'league': self.league_info['name'],
                                    'league_id': self.league_info['id'],
                                    'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                }
                                
                                # Add all table columns to player info
                                for col_name, value in player_row.items():
                                    if col_name not in player_info:
                                        player_info[col_name] = value
                                
                                players_data.append(player_info)
                    
                    break  # Found the squad table, no need to check more tables
            
            # Limit number of players if specified
            if max_players and len(players_data) > max_players:
                players_data = players_data[:max_players]
            
            # Mark team as processed
            self.processed_teams.add(team_info['team_id'])
            
            print(f"      Found {len(players_data)} players")
            
            # Add player basic info to league data
            if players_data:
                players_df = pd.DataFrame(players_data)
                self.league_data['player_basic_info'].append(players_df)
            
            return players_data
            
        except Exception as e:
            print(f"      Error scraping team players: {e}")
            return []
    
    def scrape_player_stats(self, player_info):
        """Scrape all statistical tables from a player's page"""
        try:
            if player_info['player_id'] in self.processed_players:
                print(f"      Skipping already processed player: {player_info['player_name']}")
                return []
            
            print(f"      Scraping player stats for: {player_info['player_name']}")
            
            if not self.navigate_to_page(player_info['player_url']):
                print(f"        Failed to load player page")
                return []
            
            time.sleep(2)
            
            # Get page content
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            
            # Find all stats tables
            tables = soup.find_all('table', class_=re.compile('stats'))
            
            player_stats_tables = []
            
            for i, table in enumerate(tables):
                # Extract table with headers
                context = {
                    'player_id': player_info['player_id'],
                    'player_name': player_info['player_name'],
                    'team_id': player_info['team_id'],
                    'team_name': player_info['team_name'],
                    'league': self.league_info['name'],
                    'league_id': self.league_info['id'],
                    'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'table_index': i,
                    'table_type': f'player_stats_{i}'
                }
                
                df = self.extract_table_with_headers(table, context)
                
                if df is not None and not df.empty:
                    player_stats_tables.append(df)
                    print(f"        Extracted player stats table {i} with {len(df)} rows")
            
            # Mark player as processed
            self.processed_players.add(player_info['player_id'])
            
            return player_stats_tables
            
        except Exception as e:
            print(f"        Error scraping player stats: {e}")
            return []
    
    def scrape_player_match_logs(self, player_info):
        """Scrape match logs for a player"""
        try:
            print(f"      Scraping match logs for: {player_info['player_name']}")
            
            # Extract player ID from URL
            match = re.search(r'/en/players/([a-f0-9]+)/', player_info['player_url'])
            if not match:
                return None
            
            player_fbref_id = match.group(1)
            match_logs_url = f"https://fbref.com/en/players/{player_fbref_id}/matchlogs/"
            
            if not self.navigate_to_page(match_logs_url):
                return None
            
            time.sleep(2)
            
            try:
                # Find match logs table
                table = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table.stats_table"))
                )
                table_html = table.get_attribute('outerHTML')
                soup = BeautifulSoup(table_html, 'html.parser')
                
                # Extract table data with headers
                context = {
                    'player_id': player_info['player_id'],
                    'player_name': player_info['player_name'],
                    'team_id': player_info['team_id'],
                    'team_name': player_info['team_name'],
                    'league': self.league_info['name'],
                    'league_id': self.league_info['id'],
                    'player_fbref_id': player_fbref_id,
                    'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'table_type': 'player_match_logs'
                }
                
                df = self.extract_table_with_headers(soup, context)
                
                if df is not None and not df.empty:
                    print(f"        Extracted {len(df)} match logs")
                    return df
            
            except TimeoutException:
                return None
            
            return None
            
        except Exception as e:
            print(f"        Error scraping match logs: {e}")
            return None
    
    def scrape_league_data(self, max_teams=3, max_players_per_team=2):
        """Scrape all data for the league"""
        print(f"\n📊 Scraping {self.league_info['name']}...")
        
        results = {}
        
        try:
            # 1. Scrape fixtures
            print("  1. Scraping fixtures...")
            fixtures_df = self.scrape_league_fixtures()
            if fixtures_df is not None:
                self.league_data['fixtures'].append(fixtures_df)
                results['fixtures'] = fixtures_df
            
            # 2. Scrape teams and standings
            print("  2. Scraping teams...")
            teams_df = self.scrape_league_teams()
            
            if teams_df is not None and not teams_df.empty:
                results['teams'] = teams_df
                
                # Convert DataFrame to list of dicts for processing
                teams_list = teams_df.to_dict('records')
                
                # Limit number of teams
                if max_teams and len(teams_list) > max_teams:
                    teams_list = teams_list[:max_teams]
                
                # 3. Scrape team stats for each team
                print("  3. Scraping team stats...")
                for i, team in enumerate(teams_list):
                    print(f"  3.{i+1}. Scraping team stats for {team['team_name']}...")
                    team_stats = self.scrape_team_stats(team)
                    if team_stats:
                        self.league_data['team_stats'].extend(team_stats)
                
                # 4. Scrape players for each team
                all_players = []
                
                for i, team in enumerate(teams_list):
                    print(f"  4.{i+1}. Scraping players for {team['team_name']}...")
                    players = self.scrape_team_players(team, max_players_per_team)
                    
                    if players:
                        all_players.extend(players)
                        
                        # 5. Scrape player stats for each player
                        print(f"  5.{i+1}. Scraping player stats...")
                        for j, player in enumerate(players):
                            print(f"    5.{i+1}.{j+1}. Scraping stats for {player['player_name']}...")
                            player_stats = self.scrape_player_stats(player)
                            if player_stats:
                                self.league_data['player_stats'].extend(player_stats)
                        
                        # 6. Scrape match logs for each player
                        print(f"  6.{i+1}. Scraping player match logs...")
                        for j, player in enumerate(players):
                            print(f"    6.{i+1}.{j+1}. Scraping match logs for {player['player_name']}...")
                            match_logs_df = self.scrape_player_match_logs(player)
                            if match_logs_df is not None:
                                self.league_data['player_match_logs'].append(match_logs_df)
                
                # Create players DataFrame from basic info
                if all_players:
                    players_df = pd.DataFrame(all_players)
                    results['player_basic_info'] = players_df
                
                # Combine team stats
                if self.league_data['team_stats']:
                    team_stats_df = pd.concat(self.league_data['team_stats'], ignore_index=True)
                    results['team_stats'] = team_stats_df
                
                # Combine player stats
                if self.league_data['player_stats']:
                    player_stats_df = pd.concat(self.league_data['player_stats'], ignore_index=True)
                    results['player_stats'] = player_stats_df
                
                # Combine match logs
                if self.league_data['player_match_logs']:
                    match_logs_df = pd.concat(self.league_data['player_match_logs'], ignore_index=True)
                    results['player_match_logs'] = match_logs_df
            
            # Save league-specific data
            self.save_league_data()
            
            print(f"✅ Completed {self.league_info['name']}")
            
            return results
            
        except Exception as e:
            print(f"❌ Error scraping {self.league_info['name']}: {e}")
            traceback.print_exc()
            return results
        
        finally:
            # Close driver
            if self.driver:
                self.driver.quit()
    
    def save_league_data(self):
        """Save league data to CSV files"""
        league_dir = self.output_dir
        os.makedirs(league_dir, exist_ok=True)
        
        for data_type, data_list in self.league_data.items():
            if data_list:
                try:
                    combined_df = pd.concat(data_list, ignore_index=True)
                    
                    if not combined_df.empty:
                        # Clean column names
                        combined_df.columns = [self.clean_column_name(col) for col in combined_df.columns]
                        
                        # Save to CSV
                        output_file = os.path.join(league_dir, f"{data_type}.csv")
                        combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')
                        
                        print(f"      Saved {data_type}: {len(combined_df)} rows")
                
                except Exception as e:
                    print(f"      Error saving {data_type}: {e}")
    
    def clean_column_name(self, col):
        """Clean a column name"""
        if not isinstance(col, str):
            col = str(col)
        
        col = re.sub(r'[^\w\s]', '_', col)
        col = re.sub(r'[\s_]+', '_', col)
        col = col.strip('_')
        col = col.lower()
        
        return col

def main():
    """Main function"""
    print("=" * 100)
    print("🌍 FBREF MULTI-LEAGUE CONCURRENT SCRAPER - COMPLETE STATS")
    print("=" * 100)
    
    # Configuration
    scraper = FBrefMultiLeagueScraper(
        headless=False,  # Set to True for production
        output_dir="./fbref_all_leagues_complete",
        max_workers=3  # Number of concurrent leagues to scrape
    )
    
    try:
        # Select which leagues to scrape
        leagues_to_scrape = [
            'premier_league',
            'la_liga', 
            'bundesliga',
            'serie_a',
            'ligue_1'
        ]
        
        # Run concurrent scraping with more comprehensive settings
        scraper.scrape_all_leagues_concurrently(
            leagues_to_scrape=leagues_to_scrape,
            max_teams=30,               # Scrape first 3 teams per league
            max_players_per_team=30     # Scrape first 5 players per team
        )
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        traceback.print_exc()
    
    print("\n✨ Scraping complete!")

def comprehensive_test():
    """Comprehensive test function - scrape more data"""
    print("Running comprehensive test for Premier League...")
    
    scraper = FBrefMultiLeagueScraper(
        headless=False,
        output_dir="./comprehensive_test",
        max_workers=1
    )
    
    # Get the league scraper
    league_scraper = scraper.get_league_scraper('premier_league')
    
    # Test with more teams and players
    print("\nTesting comprehensive scraping...")
    results = league_scraper.scrape_league_data(
        max_teams=30,               # Test with 5 teams
        max_players_per_team=30    # Test with 10 players per team
    )
    
    # Print results
    for data_type, df in results.items():
        if df is not None and not df.empty:
            print(f"\n📊 {data_type.upper()}:")
            print(f"  Rows: {len(df)}")
            print(f"  Columns: {len(df.columns)}")
            print(f"  Sample columns: {list(df.columns)[:10]}...")

if __name__ == "__main__":
    # For comprehensive testing
    # comprehensive_test()
    
    # For full run (comment out comprehensive_test() above and uncomment below)
    main()