# update_m3u.py

def update_playlist(content):
    updates = {
        "Tivibu Spor 1": {
            "name": "Tivibu Sports HD",
            "url": "http://newstream.example.com/tivibu_sports_hd.m3u8"
        },
        "BEIN 1 TURKISH ": {
            "name": "BEIN Sports 1",
            "url": "http://newstream.example.com/bein_sports_1.m3u8"
        }
        # İsterseniz buraya daha fazla kanal ekleyebilirsiniz
    }

    lines = content.splitlines()
    updated_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            current_name = line.split(",", 1)[1]
            if current_name in updates:
                new_name = updates[current_name]["name"]
                updated_lines.append(f"#EXTINF:-1,{new_name}")
                if i + 1 < len(lines) and lines[i + 1].startswith("#EXTVLCOPT"):
                    updated_lines.append(lines[i + 1])
                    i += 1
                new_url = updates[current_name]["url"]
                updated_lines.append(new_url)
                i += 2
            else:
                updated_lines.append(line)
                i += 1
        else:
            updated_lines.append(line)
            i += 1

    return "\n".join(updated_lines)


def main():
    with open("playlist.m3u", "r", encoding="utf-8") as f:
        content = f.read()

    updated_content = update_playlist(content)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("Playlist güncellendi.")


if __name__ == "__main__":
    main()
