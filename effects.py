from moviepy.editor import VideoFileClip, vfx

def process_video(input_path, output_path, effect_type):
    clip = VideoFileClip(input_path)
    
    if effect_type == 'bw':
        final = clip.fx(vfx.blackwhite)
    elif effect_type == 'slow':
        final = clip.speedx(0.5)
    elif effect_type == 'reverse':
        final = clip.fx(vfx.time_mirror)
    else:
        final = clip
        
    final.write_videofile(output_path, codec="libx264")
    clip.close()

