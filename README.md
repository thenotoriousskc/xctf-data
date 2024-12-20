python script that scrapes all race results for a team in a given year from Athletic.net


  %  python3 scrape_season.py --help        
  usage: scrape_season.py [-h] [--team_id TEAM_ID] [--year YEAR] [--sport SPORT]

  Dump a season of race times from Athletic.net in csv format.  Currently works for XC only
  
  options:
    -h, --help         show this help message and exit
    --team_id TEAM_ID  Team ID of the team on Athletic.net
    --year YEAR        Year for the team data
    --sport SPORT      Sport type (e.g., cross-country, track-and-field)
