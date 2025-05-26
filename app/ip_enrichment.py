import requests
import pandas as pd

API_KEY = "b8597bb0feb7416ebfc89d6e8454c0dc"

def enrich_ip(ip: str):
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return {
                "country": data.get("country_name"),
                "region": data.get("state_prov"),
                "city": data.get("city"),
                "asn": data.get("asn"),
                "org": data.get("organization")
            }
        else:
            print(f"Failed to enrich IP {ip}, status code: {res.status_code}")
    except Exception as e:
        print(f"IP {ip} enrichment failed: {e}")
    return {
        "country": None,
        "region": None,
        "city": None,
        "asn": None,
        "org": None
    }

def enrich_dataframe(df: pd.DataFrame):
    unique_ips = df['dst_ip'].dropna().unique()
    enriched = {ip: enrich_ip(ip) for ip in unique_ips}
    enrichment_df = df['dst_ip'].map(enriched).apply(pd.Series)
    return pd.concat([df.reset_index(drop=True), enrichment_df.reset_index(drop=True)], axis=1)
