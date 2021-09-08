from pytube import YouTube
import ffmpeg, datetime
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import glob, re
import subprocess



def ydl(url,time_str):
    try:
        os.remove('video.mp4')
    except:
        pass
    time_list_str = time_str.split(',')
    print(time_list_str)
    #['00:00:50~00:01:20','00:01:30~00:02:30']
    time_lists = []
    for list in time_list_str:
        list = list.split('-')
        time_lists.append(list)
    print(time_lists)
    #[['00:00:50','00:01:20'],['00:01:30','00:02:30']]
    # Const
    #  ファイル作成コマンド定数

    LIST_FILE_NAME='movielist.txt'
    FILE_HEADER="file '"
    FILE_FOOTER="'"
    RETURN = '\n'
    #  選択フォルダ配下のファイルを指定する文字列
    SEARCH_OBJ_SENTENCE='\\*.*'
    #  FFMPEGコマンド
    FFMPEG_HEADER='ffmpeg -safe 0 -f concat -i '
    FFMPEG_MIDDLE=' -c:v copy -c:a copy -map 0:v -map 0:a '
    OUT_FILE_NAME='video.mp4'


    """
    time_in = "00:00:02"
    time_out = "00:00:06"

    time_list = [time_in,time_out]

    time_in2 = "00:00:08"
    time_out2 = "00:00:10"

    time_list2 = [time_in2,time_out2]

    time_lists = [time_list,time_list2]
    """
    #url = 'https://youtu.be/Hx-T8Bw9DGc'

    yt = YouTube(url)
    print("ダウンロード中...")
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('./download','out.mp4')
    print("ダウンロード完")

    file_int = 0

    for list in time_lists:
        file_int = file_int + 1
        date_dt_in = datetime.datetime.strptime(list[0], '%H:%M:%S')
        date_dt_out = datetime.datetime.strptime(list[1], '%H:%M:%S')
        date_dt = date_dt_out - date_dt_in
        date_dt_in = date_dt_in - datetime.datetime(2019,1,1)
        #print(date_dt.seconds)
        #print(date_dt_in.second)



        stream = ffmpeg.input('./download/out.mp4')
        stream = ffmpeg.output(stream, './output/out'+str(file_int)+'.mp4', ss=date_dt_in.seconds, t=date_dt.seconds)
        ffmpeg.run(stream)



    outfile = open(LIST_FILE_NAME, 'w')

    for f in glob.glob("./output/*.mp4"): # 指定したフォルダ以下の要素分だけループ

        batCom = FILE_HEADER + str(f) + FILE_FOOTER + RETURN
        outfile.write(batCom)
    outfile.close()

    # FFMPEGコマンドの実行
    # ffmpeg -safe 0 -f concat -i [定義ファイル名] -c:v copy -c:a copy -map 0:v -map 0:a [出力ファイル名]
    cmd = FFMPEG_HEADER + LIST_FILE_NAME + FFMPEG_MIDDLE + OUT_FILE_NAME
    subprocess.call(cmd.split())
    file_int = 0
    for list in time_lists:
        file_int = file_int + 1
        os.remove('./output/out'+str(file_int)+'.mp4')
        os.remove('./download/out.mp4')
    print("ok")

ydl('https://www.youtube.com/watch?v=L-aS-0x3U6U&t=243s','00:00:50-00:01:20,00:01:30-00:02:30')
