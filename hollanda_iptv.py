import os
import re
import requests

CHANNELS_CONFIG = {
    "SLAM! TV": {
        "url": "https://slam.nl",
        "logo": "https://slam.nl",
        "group": "Hollanda Muzik",
        "backup": "https://slam.nl",
    },
    "TV 538": {
        "url": "https://538.nl",
        "logo": "https://538.nl",
        "group": "Hollanda Muzik",
        "backup": "https://538.nl",
    },
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_link(name, info):
    try:
        res = requests.get(info["url"], headers=HEADERS, timeout=10)
        res.raise_for_status()
        matches = re.findall(r"https?://[^\s\"']+\.m3u8[^\s\"']*", res.text)
        if matches:
            return matches[0].replace("\\", "")
    except:
        pass
    return info["backup"]  # Hata durumunda yedek linki kullanır


def main():
    m3u = "#EXTM3U\n"
    for name, info in CHANNELS_CONFIG.items():
        link = fetch_link(name, info)
        m3u += f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{info["group"]}",{name}\n{link}\n'

    with open("hollanda_muzik_kanallari.m3u", "w", encoding="utf-8") as f:
        f.write(m3u)
    print("M3U dosyası GitHub üzerinde başarıyla güncellendi.")


if __name__ == "__main__":
    main()
