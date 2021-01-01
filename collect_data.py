import requests
import json

# Get an API key from https://developer.riotgames.com/
riot_api_key = 'YOUR API KEY GOES HERE'

# Use the API endpoint that corresponds with your region: https://developer.riotgames.com/docs/lol
api_endpoint = 'https://na1.api.riotgames.com'


def generate_team_dict(match_metadata):
    """Generates a dictionary with teamId as keys and team stats as values"""
    teams = {}

    for team in match_metadata['teams']:
        win_status = 0
        loss_status = 1

        if team['win'] == 'Win':
            win_status = 1
            loss_status = 0

        teams[team['teamId']] = {
            'teamId': team['teamId'],
            'win': win_status,
            'loss': loss_status,
            'firstBlood': int(team['firstBlood']),
            'firstTower': int(team['firstTower'])
        }
    return teams


def generate_participant_dict(match_metadata, teams):
    """Generates a dictionary with participantId as keys and participant stats as values"""
    participants = {}

    for participant in match_metadata['participants']:
        participants[participant['participantId']] = {
            'participantId': participant['participantId'],
            'championId': participant['championId'],
            'role': participant['timeline']['role'],
            'lane': participant['timeline']['lane'],
            'total_kills': participant['stats']['kills'],
            'total_deaths': participant['stats']['deaths'],
            'total_assists': participant['stats']['assists'],
            **teams[participant['teamId']]
        }
    return participants


def generate_match_frames(match_frames, participants):
    """Generates an array containing match frames combined with participant and team data"""
    frames = []
    events = []

    for frame in match_frames:
        participant_frames = list(frame['participantFrames'].values())
        events.extend(filter(lambda x: x['type'] == 'CHAMPION_KILL', frame['events']))

        for participant_frame in participant_frames:
            kills = len(list(filter(lambda x: x['killerId'] == participant_frame['participantId'], events)))
            deaths = len(list(filter(lambda x: x['victimId'] == participant_frame['participantId'], events)))
            assists = len(
                list(filter(lambda x: participant_frame['participantId'] in x['assistingParticipantIds'], events)))

            frames.append({
                'timestamp': frame['timestamp'],
                'participantId': participant_frame['participantId'],
                'currentGold': participant_frame['currentGold'],
                'level': participant_frame['level'],
                'xp': participant_frame['xp'],
                'minionsKilled': participant_frame['minionsKilled'],
                'kills': kills,
                'deaths': deaths,
                'assists': assists,
                **participants[participant_frame['participantId']]
            })
    return frames


def load_match(match_id, api_key):
    """Calls the Riot API with the provided API key on a specified match and returns an array of match frames combined
    with participant and team stats"""

    # Configure and prepare endpoints
    match_metadata_endpoint = f'{api_endpoint}/lol/match/v4/matches/{match_id}?api_key={api_key}'
    match_timeline_endpoint = f'{api_endpoint}/lol/match/v4/timelines/by-match/{match_id}?api_key={api_key}'

    # Execute requests and store data as JSON
    match_metadata_req = requests.get(url=match_metadata_endpoint)
    match_timeline_req = requests.get(url=match_timeline_endpoint)
    match_metadata = match_metadata_req.json()
    match_timeline = match_timeline_req.json()

    # Reshape data into array containing match frames combined with participant/team stats
    teams = generate_team_dict(match_metadata)
    participants = generate_participant_dict(match_metadata, teams)
    match_frames = generate_match_frames(match_timeline['frames'], participants)

    return match_frames


def process_matches(matches, api_key):
    """Generate match frames for specified matches"""
    data = []
    for match in matches:
        data.extend(load_match(match, api_key))

    return data


with open('data.json', 'w') as outfile:
    """Pulls data from the specified matches and writes results into data.json"""
    # Get match IDs from Riot API or use these sample matches: https://canisback.com/matchId/matchlist_na1.json
    match_ids = ['3722804660', '3722804661', '3722804664', '3722804673', '3722804690', '3722804693', '3722804711',
                 '3722804725', '3722804732']
    json.dump(process_matches(match_ids, riot_api_key), outfile)
