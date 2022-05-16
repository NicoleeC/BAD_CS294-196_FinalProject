import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '((nft OR NFT) lang:en #crypto -is:retweet)', 'max_results': '100', 'tweet.fields': 'created_at,author_id,public_metrics,geo', 'expansions': 'author_id', 'user.fields': 'public_metrics', 'start_time': '2022-04-28T00:00:00.00Z', 'end_time': '2022-04-28T23:59:59.59Z'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    #dates = ['2022-04-28', '2022-04-29', '2022-04-30', '2022-05-01', '2022-05-02', '2022-05-03']
    dates = ['2022-05-04']
    for cur_date in dates:
        for i in range(24):
            for j in range(2):    
                query_params['start_time'] = cur_date + "T%02d" % i + ":%02d" % (j * 30)+ ':00.00Z'
                query_params['end_time'] = cur_date + "T%02d" % i + ":%02d" % (j * 30 + 29) + ':59.59Z'
                if (i == 0 and j == 0 and cur_date == '2022-05-04'):
                    json_response = connect_to_endpoint(search_url, query_params)
                else:
                    new_json = connect_to_endpoint(search_url, query_params)
                    json_response['data'] += new_json['data']
                    json_response['includes']['users'] += new_json['includes']['users']
        print(cur_date)


    with open("2022-05-04_nft_tweets.json", 'w') as outfile:
        json.dump(json_response, outfile)


if __name__ == "__main__":
    main()
