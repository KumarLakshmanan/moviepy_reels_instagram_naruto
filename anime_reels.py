#!/usr/bin/python
import json
import moviepy.editor as mp
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


def find_season(episode_number, season_data):
    for season in season_data['seasons']:
        if season['start'] <= episode_number <= season['end']:
            return season

    return "Season not found"


def split_video(video_path, output_directory):
    video = mp.VideoFileClip(video_path)
    video_duration = video.duration
    segment_duration = video_duration / 3

    segments = []
    for i in range(3):
        start_time = i * segment_duration
        end_time = (i + 1) * segment_duration
        segment = video.subclip(start_time, end_time)
        segments.append(segment)

    return segments, video_duration

# ... (previous code)


def main():
    with open('episodes.json', 'r', encoding='utf-8') as f:
        loopList = json.load(f)

    episode_number = 1
    custom_font_path = "Blackout Midnight.ttf"
    output_directory = "edit"
    backgroundImage = "bg.png"

    for thisepisode in loopList['episodes']:
        season_data = find_season(episode_number, loopList)
        video_path = f"series/{episode_number}.mp4"

        # Split the video into three parts
        video_segments, video_duration = split_video(
            video_path, output_directory)

        # Get the total height and width of the bg image
        bg = mp.ImageClip(backgroundImage)
        bg_height = bg.h
        bg_width = bg.w

        for i in range(3):
            segment = video_segments[i]
            segment_duration = segment.duration
            segment_name = f"{episode_number}_{i}.mp4"

            segment_height = segment.h
            segment_width = segment.w

            # Calculate the position to center the segment
            x_pos = (bg_width - segment_width) / 2
            y_pos = (bg_height - segment_height) / 2

            # Add the episode number and season name at the top, wrap text if too long
            text1 = f"S{season_data['season']} - EP{episode_number}"
            text2 = thisepisode['english']

            text1Top = (bg_height / 2 - segment_height / 2) - 150
            text2Top = text1Top + 70

            text_clip1 = mp.TextClip(
                text1, fontsize=60, color='white', font=custom_font_path)
            text_clip2 = mp.TextClip(
                text2, fontsize=35, color='white', font=custom_font_path)
            text_clip1 = text_clip1.set_position(
                (bg_width / 2 - text_clip1.w / 2, text1Top)
            ).set_duration(
                segment_duration)
            text_clip2 = text_clip2.set_position(
                (bg_width / 2 - text_clip2.w / 2, text2Top)
            ).set_duration(segment_duration)

            # Add the background image
            background = mp.ImageClip(backgroundImage)
            background = background.set_duration(segment_duration)

            # Add the title "Naruto" at the bottom
            title_text = mp.TextClip(
                "Naruto\n {}".format(season_data['name']), fontsize=30, color='white', font=custom_font_path)
            titleTop = bg_height / 2 + segment_height / 2 + 50
            title_text = title_text.set_position(
                (bg_width / 2 - title_text.w / 2, titleTop)
            )
            title_text = title_text.set_duration(segment_duration)

            # Animated watermark
            watermark = "@naruto_anime_series_tamil"
            watermark_text = mp.TextClip(watermark, fontsize=20, color='white')
            watermark_text = watermark_text.set_duration(segment_duration)
            watermark_text = watermark_text.set_pos(10, 10)

            # Composite the segment, text, and background
            segment = CompositeVideoClip([
                background,
                segment.set_position((x_pos, y_pos)),
                text_clip1,
                text_clip2,
                title_text,
                watermark_text,
            ])
            segment = segment.set_duration(segment_duration)
            segment.write_videofile(f"{output_directory}/{segment_name}")

        episode_number += 1


if __name__ == '__main__':
    main()
