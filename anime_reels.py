#!/usr/bin/python
import json
import moviepy.editor as mp
from moviepy.video.fx import resize
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

        for i in range(3):
            segment = video_segments[i]
            segment_duration = segment.duration
            segment_name = f"{episode_number}_{i}.mp4"

            # Add the episode number and season name
            text = f"S-{season_data['season']} EP-{episode_number}\n{thisepisode['english']}"
            text_clip = mp.TextClip(
                text, fontsize=24, color='white', font=custom_font_path)
            text_clip = text_clip.set_position(('center', 0.2), relative=True)
            text_clip = text_clip.set_duration(segment_duration)
            segment = CompositeVideoClip([segment, text_clip])

            # Add the background image
            background = mp.ImageClip(backgroundImage)
            background = background.set_duration(segment_duration)
            segment = CompositeVideoClip([background, segment])

            # Add the segment name
            segment = segment.set_duration(segment_duration)
            segment.write_videofile(f"{output_directory}/{segment_name}")


if __name__ == '__main__':
    main()
