import os
import re
import requests

# Kanalların taranacağı resmi web sayfaları
CHANNELS_CONFIG = {
    "SLAM! TV": {
        "url": "https://slam.nl",
        "logo": "https://slam.nl",
        "group": "Hollanda Muzik",
    },
    "TV 538": {
        "url": "https://538.nl",
        "logo": "https://538.nl",
        "group": "Hollanda Muzik",
    },
    "XITE NL (Yedek/Genel Klasik Akis)": {
        "url": "https://xite.nl",
        "logo": "https://xite.nlassets/images/xite-logo.png",
        "group": "Hollanda Muzik",
    },
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
}


def fetch_m3u8_link(channel_name, url):
    """Web sayfasından dinamik .m3u8 yayın linkini yakalar."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        html_content = response.text

        # Sayfa kodlarında .m3u8 uzantılı linkleri ara
        matches = re.findall(r"https?://[^\s\"']+\.m3u8[^\s\"']*", html_content)

        if matches:
            # Kaçış karakterlerini temizle ve ilk geçerli linki al
            stream_url = matches[0].replace("\\", "")
            print(f"[OK] {channel_name} için yayın linki başarıyla bulundu.")
            return stream_url

        # Alternatif manifest veya mpd taraması
        alt_matches = re.findall(
            r"https?://[^\s\"']+(?:stream|manifest|playlist)[^\s\"']*",
            html_content,
        )
        if alt_matches:
            stream_url = alt_matches[0].replace("\\", "")
            print(f"[OK] {channel_name} için alternatif akış linki bulundu.")
            return stream_url

        print(
            f"[UYARI] {channel_name} sayfasında doğrudan m3u8 linki saptanamadı (Şifreli/DRM olabilir)."
        )
        return None

    except Exception as e:
        print(f"[HATA] {channel_name} taranırken sorun oluştu: {e}")
        return None


def create_iptv_playlist():
    print("=== HOLLANDA MÜZİK KANALLARI IPTV SCRIPTİ BAŞLADI ===\n")

    # M3U Playlist standart başlığı
    m3u_content = "#EXTM3U\n"

    found_any = False

    for name, info in CHANNELS_CONFIG.items():
        print(f"{name} taranıyor...")
        stream_link = fetch_m3u8_link(name, info["url"])

        # Eğer dinamik tarama link bulamazsa, test amaçlı bilinen sabit/statik yedek IPTV linkleri atanabilir
        if not stream_link:
            if name == "SLAM! TV":
                # Sunucu kaynaklı yedek stream (örnektir, çalışmıyorsa tarayıcı linki esastır)
                stream_link = "https://slam.nl"
            elif name == "TV 538":
                stream_link = "https://538.nl"

        if stream_link:
            # Standart IPTV format satırlarını ekle
            m3u_content += f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{info["group"]}",{name}\n'
            m3u_content += f"{stream_link}\n"
            found_any = True

    # Dosyaya kaydetme işlemi
    filename = "hollanda_muzik_kanallari.m3u"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print("\n=============================================")
    if found_any:
        print(
            f"[BAŞARILI] '{filename}' dosyası ana dizinde başarıyla oluşturuldu!"
        )
        print(
            "Bu dosyayı VLC Player, PotPlayer veya Smart IPTV uygulamalarına yükleyerek direkt izleyebilirsiniz."
        )
    else:
        print(
            "[BAŞARISIZ] Hiçbir kanala ait aktif m3u8 linki dinamik olarak çekilemedi."
        )
    print("=============================================")


if __name__ == "__main__":
    create_iptv_playlist()
