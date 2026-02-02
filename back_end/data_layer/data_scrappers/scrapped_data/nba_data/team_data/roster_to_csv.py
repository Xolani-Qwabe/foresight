import pandas as pd
import os

def save_nba_roster(raw_data, team_id, year, output_dir='.', drop_additional=True):
    """
    Save NBA roster data to CSV with team-year naming
    Optionally drop the 'Player-additional' column
    
    Parameters:
    - raw_data: Raw string containing the roster data
    - team_id: Team identifier (e.g., 'ATL', 'BKN', 'LAL')
    - year: Season year (e.g., 2023)
    - output_dir: Where to save the file
    - drop_additional: Whether to drop 'Player-additional' column (default: True)
    """
    # Split into lines
    lines = raw_data.strip().split('\n')
    
    # Remove empty lines
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not all(c == ',' for c in stripped if c != ' '):
            clean_lines.append(stripped)
    
    # Get header
    header = clean_lines[0]
    data_lines = clean_lines[1:]
    
    # Process data lines
    processed_data = []
    for line in data_lines:
        if ',' in line:
            parts = line.split(',')
            
            # Fix space-separated jersey numbers
            if ' ' in str(parts[0]):
                numbers = str(parts[0]).split()
                parts[0] = numbers[-1]  # Take last number
            
            processed_data.append(parts)
    
    # Create DataFrame
    df = pd.DataFrame(processed_data, columns=header.split(','))
    
    # DROP the 'Player-additional' column if it exists and drop_additional is True
    if drop_additional and 'Player-additional' in df.columns:
        print(f"🗑️  Dropping 'Player-additional' column")
        df = df.drop(columns=['Player-additional'])
    
    # Create filename
    filename = f"{team_id}_roster_{year}.csv"
    filepath = os.path.join(output_dir, filename)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    
    print(f"✅ Saved: {filepath}")
    print(f"📊 DataFrame shape: {df.shape}")
    print(f"📋 Columns ({len(df.columns)}): {list(df.columns)}")
    print(f"👥 Players: {len(df)}")
    
    return df, filepath


if __name__ == "__main__":
    # CSV data
    bkn_data = """No.,Player,Pos,Ht,Wt,Birth Date,Birth,Exp,College,Player-additional
22,Deandre Ayton,C,7-0,252,July 23 1998,bs BS,3,Arizona,aytonde01
30,Paris Bass,SF,6-8,200,August 29 1995,us US,R,Detroit Mercy,basspa01
18,Bismack Biyombo,C,6-8,255,August 28 1992,cd CD,10,,biyombi01
1,Devin Booker,SG,6-5,206,October 30 1996,us US,6,Kentucky,bookede01
25,Mikal Bridges,SF,6-6,209,August 30 1996,us US,3,Villanova,bridgmi01
0,Torrey Craig,SF,6-5,221,December 19 1990,us US,4,USC Upstate,craigto01
99,Jae Crowder,PF,6-6,235,July 6 1990,us US,9,Marquette,crowdja01
4,Aaron Holiday,PG,6-0,185,September 30 1996,us US,3,UCLA,holidaa01
35,Chandler Hutchison,SF,6-6,210,April 26 1996,us US,3,Boise State,hutchch01
45,Justin Jackson,SF,6-8,220,March 28 1995,us US,4,UNC,jacksju01
23,Cameron Johnson,PF,6-8,210,March 3 1996,us US,2,Pitt UNC,johnsca02
8,Frank Kaminsky,C,7-0,240,April 4 1993,us US,6,Wisconsin,kaminfr01
19,Gabriel Lundberg,SG,6-4,203,December 4 1994,dk DK,R,,lundbga01
00,JaVale McGee,C,7-0,270,January 19 1988,us US,13,Nevada,mcgeeja01
11,Abdel Nader,SF,6-5,225,September 25 1993,eg EG,4,Northern Illinois Iowa State,naderab01
3,Chris Paul,PG,6-0,175,May 6 1985,us US,16,Wake Forest,paulch01
15,Cameron Payne,PG,6-2,183,August 8 1994,us US,6,Murray State,payneca01
2,Elfrid Payton,PG,6-3,195,February 22 1994,us US,7,Louisiana,paytoel01
14,Landry Shamet,SG,6-5,190,March 13 1997,us US,3,Wichita State,shamela01
10,Jalen Smith,PF,6-8,215,March 16 2000,us US,1,Maryland,smithja04
26,Emanuel Terry,PF,6-9,220,August 21 1996,us US,1,Lincoln Memorial,terryem01
12,Ish Wainright,PF,6-5,250,September 12 1994,us US,R,Baylor,wainris01
21,M.J. Walker,SG,6-5,213,March 28 1998,us US,R,Florida State,walkemj01"""
    
    # Save roster to CSV
    df_bkn, file_bkn = save_nba_roster(
        raw_data=bkn_data,
        team_id='PHX',
        year=2022,
        output_dir='.'
    )
    
    print("\n🏀 BKN Roster (first 3 players):")
    print(df_bkn[['No.', 'Player', 'Pos', 'College']].head(3))