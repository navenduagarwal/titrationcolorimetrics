from threading import Thread

import cv2
import pandas as pd
import playsound
from matplotlib import pyplot as plt


def sound_alarm(path):
    # play an alarm sound
    playsound.playsound(path)


def clip_color_avg(img):
    # manually selected 10x10 square region of frame to  monitor color variation
    clip = img[213:223, 348:358, :]
    h, w, c = clip.shape
    avg_list = [[], [], []]
    avg_channel = []
    for i in range(h):
        for j in range(w):
            for c in range(3):
                avg_list[c].append(clip[i, j, c])
    avg_channel.append(sum(avg_list[0]) / len(avg_list[0]))
    avg_channel.append(sum(avg_list[1]) / len(avg_list[1]))
    avg_channel.append(sum(avg_list[2]) / len(avg_list[2]))
    return avg_channel


# define two constants, one for the color change from initial value to indicate
# process completion and then a second constant for the number of consecutive
# frames the color must be below the threshold for to set off the
# alarm
COLOR_AR_THRESH = 60
COLOR_AR_CONSEC_FRAMES = 20
# initialize the frame counter as well as a boolean used to
# indicate if the alarm is going off
CONSECUTIVE_FRAME_COUNTER = 0
ALARM_ON = False

cap = cv2.VideoCapture('raw_media/titration.wmv')


if cap.isOpened():
    Width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    Height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    FPS = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frames)
    print(Width, Height)
    ret1, img1 = cap.read()
    if ret1:
        START_AVG_CHANNEL_COLOR = clip_color_avg(img1)
        print(START_AVG_CHANNEL_COLOR)
        output = cv2.VideoWriter('output/titration_output.avi', fourcc, FPS, (int(Width), int(Height)), True)
        number_frame = 1
        raw_data = {'frames': [], 'avg_blue': [], 'avg_green': [], 'avg_red': []}
        while True:
            ret, img = cap.read()
            if ret:
                avg_channel = clip_color_avg(img)
                if (abs(avg_channel[0] - START_AVG_CHANNEL_COLOR[0]) > COLOR_AR_THRESH) or (abs(
                        avg_channel[1] - START_AVG_CHANNEL_COLOR[1]) > COLOR_AR_THRESH) or (abs(
                    avg_channel[2] - START_AVG_CHANNEL_COLOR[2]) > COLOR_AR_THRESH):
                    CONSECUTIVE_FRAME_COUNTER += 1
                    if CONSECUTIVE_FRAME_COUNTER > COLOR_AR_CONSEC_FRAMES:
                        # if the alarm is not on, turn it on
                        if not ALARM_ON:
                            ALARM_ON = True

                            # check to see if an alarm file was supplied,
                            # and if so, start a thread to have the alarm
                            # sound played in the background
                            # if args["alarm"] != "":
                            t = Thread(target=sound_alarm,
                                       args=('raw_media/alarm.wav',))
                            t.daemon = True
                            t.start()
                        # draw an alarm on the frame
                        cv2.putText(img, "COLOR CHANGED!", (50, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                else:
                    CONSECUTIVE_FRAME_COUNTER = 0
                    ALARM_ON = False
                    # draw an alarm on the frame
                    cv2.putText(img, "PROCESS ONGOING", (50, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

                raw_data['frames'].append(number_frame)
                raw_data['avg_blue'].append(avg_channel[0])
                raw_data['avg_green'].append(avg_channel[1])
                raw_data['avg_red'].append(avg_channel[2])
                cv2.putText(img, "Frame {}/{}".format(number_frame, total_frames),
                            (50, 300), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(img, "SPARSHIK",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(img,
                            'B: {}'.format(int(raw_data['avg_blue'][number_frame - 1])), (550, 50),
                            cv2.FONT_HERSHEY_COMPLEX,
                            .5, (255, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(img, 'G: {}'.format(int(raw_data['avg_green'][number_frame - 1])), (550, 70),
                            cv2.FONT_HERSHEY_COMPLEX,
                            .5, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(img,
                            'R: {}'.format(int(raw_data['avg_red'][number_frame - 1])), (550, 90),
                            cv2.FONT_HERSHEY_COMPLEX,
                            .5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(img=img, pt1=(348, 213), pt2=(358, 223),
                              color=(255, 255, 255), thickness=1)
                number_frame += 1
                cv2.imshow(winname='Titration Color Analysis', mat=img)
                output.write(img)
                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        df = pd.DataFrame(raw_data)
        plt.suptitle('Titration Color Analysis', fontsize=14)
        plt.plot('frames', 'avg_blue', data=df, color='blue', linewidth=2)
        plt.plot('frames', 'avg_red', data=df, color='red', linewidth=2)
        plt.plot('frames', 'avg_green', data=df, color='green', linewidth=2)
        plt.xlabel(xlabel="Frame")
        plt.ylabel(ylabel="Channel Values")
        plt.savefig('output/titration.png')
        df.to_csv('output/titration.csv')
        # When everything done, release the video capture object
        cap.release()
        output.release()
        # Closes all the frames
        cv2.destroyAllWindows()
