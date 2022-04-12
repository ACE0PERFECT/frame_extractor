#!/usr/bin/env python
"""
    This is a frame extraction tool for hand book drawing.
    __author__ = "Lula_Offcial @ Bilibili"
    __copyright__ = "Copyright 2022"
    __credits__ = ["Lula_Offcial @ Bilibili, Greenstick, Diogo"]
    __license__ = "GPL"
    __version__ = "0.0.1"
    __maintainer__ = "Lula_Offcial @ Bilibili"
    __message__ = "https://space.bilibili.com/8429869"
"""


import cv2, os, sys, argparse, locale
import numpy as np

#this is the param for drop open your file on this python script
default_params = {
        'input_filename': 'TBC',
        'output_filename' : 'TBC',
        'fps' : 12,
        'format' : '.mp4',
        'height' : 720,
        'width' : 1280
        }
class Support_format():
    def __init__(self):
        self.in_format = ['.mp4', '.MP4', '.mov', '.MOV', '.avi', '.AVI']
        self.out_format = ['.mp4', '.MP4', '.avi', '.AVI']
        self.out_format_fourcc = {'.mp4': 'mp4v', '.MP4': 'mp4v',
                                  '.avi': 'XVID', '.AVI': 'XVID'}
        self.preset = ["HD12", "HD15", "HD24", "FHD12", "FHD24"]

class Printer():
    def __init__(self, lan=''):
        self.update_language(lan = lan)
        self.update_text()
        self.sf = Support_format()

    def p(self, c="", cnt=""):
        if self.DEV == 'fast' and c == self.e: # only warnings
            pass
        elif self.DEV == 'full': #everything should be printed
            print(c, cnt)
        elif self.DEV == 'NA' and c not in (self.d): # normal user, do not see debug prints
            print(c, cnt)

    def update_language(self, lan=""):
        if not lan:
            self.loc_lang = locale.getdefaultlocale()[0]
        else:
            self.loc_lang = lan

    def update_text(self):
        if self.loc_lang == 'zh_CN':
            self.lan = 'zh_CN'
            self.e = "[错误]"
            self.w = "[警告]"
            self.d = "[调试]"
            self.using_default = "将使用默认设定."
            self.load_src = "正在加载原视频.."
            self.progress = "进度:"
            self.complete = "完成"
            self.not_support_output_format = "不支持的输出格式。目前输出格式仅支持:"
            self.writing_video = "正在写入新视频.."
            self.no_input = "输入视频为必需项."
            self.fps_greater_than_src = "目标帧率高于原视频，终止任务。目前不支持视频插帧。"
            self.unknown_preset = "未知解析度及帧率预设，将使用HD12."
            self.not_exist_input = "原视频不存在."
            self.drop_failed = "文件名/格式有误，请重读Readme.txt或通过Bilibili向我发送私信.将使用默认设定."
            self.success = "成功!"
            self.p_description = 'Options的说明:'
            self.p_i = '[必需] 原视频名或路径.'
            self.p_o = '目标视频名或路径.'
            self.p_f = '目标帧率，仅接受整数. 如果想维持原视频帧率，输入-1.'
            self.p_F = '输出文件格式. 默认为mp4.'
            self.p_W = '目标宽度. 如果要设定为保持原比例随高度变化，输入-1.'
            self.p_H = '目标高度. 如果要设定为保持原比例随宽度变化，输入-1.'
            self.p_p = '解析度及帧率预设. 注意： 本option比 -W, -H, -f 有更高的优先级.'
            self.p_d = 'fast: 只显示重要输出.\nfull: 显示所有输出.'
        else:
            self.lan = 'en_US'
            self.e = "[ERROR]"
            self.w = "[WARNING]"
            self.d = "[DEBUG]"
            self.using_default = "Using default value."
            self.load_src = "Loading original video.."
            self.progress = "Progress:"
            self.complete = "Complete"
            self.not_support_output_format = "Unsupported output format, now support:"
            self.writing_video = "Writing new video.."
            self.no_input = 'Input file name needed.'
            self.fps_greater_than_src = 'Fps of the source video is greater than target fps, aborted because frame extension is not supported yet.'
            self.unknown_preset = "Unknown preset, using HD12."
            self.not_exist_input = "The input file does not exist."
            self.drop_failed = "Wrong file name/format, check Readme.txt, or send me a message through Bilibili. Now using default params."
            self.success = "Success!"
            self.p_description = 'Description of options:'
            self.p_i = '[REQUIRED] Name or path of the original video.'
            self.p_o = 'Name or path of the output video.'
            self.p_f = 'Desired fps of the output video, integer only. If you wanna maintain original fps, use -1.'
            self.p_F = 'Format of the output file. mp4 by default.'
            self.p_W = 'Desired width of the output video, integer only. To align this with height, use -1.'
            self.p_H = 'Desired height of the output video, integer only.To align this with width, use -1.'
            self.p_p = 'Resolution and FPS preset. Note: this option has higher priority than -W, -H and -f.'
            self.p_d = 'fast: only show critical prints.\nfull: show every prints.'

        self.n = ""
        self.DEV = "NA"

def main():

    def check(TBC, tag='params'):
        """
        Call to check if legal
        @params:
            TBC         - Required  : to be checked object
            tag         - Required  : what is this  (Str)
        """
        if tag == 'params':
            for k,v in params.items():
                if k == 'input_filename':
                    if v == 'no input file':
                        p.p(p.e, p.no_input)
                        quit()
                if k == 'format':
                    if v not in sf.out_format:
                        if v.replace('.', '') in sf.out_format:
                            params.update({k: '.' + v.replace('.', '')})
                        else:
                            p.p(p.w,
                                p.not_support_output_format + ' ' + ','.join(sf.out_format) + '. ' + p.using_default)
                            params.update({k: '.mp4'})


    def get_argvs():
        params = {
        'input_filename': 'no input file',
        'output_filename' : 'no output file',
        'fps' : 12,
        'format' : '.mp4',
        'height' : 720,
        'width' : 1280
        }
        parser = argparse.ArgumentParser(description=p.p_description)
        parser.add_argument('-i','--input', help=p.p_i)
        parser.add_argument('-o','--output', help=p.p_o)
        parser.add_argument('-f','--fps', type=int,
                            help=p.p_f)
        parser.add_argument('-F', '--format', choices=sf.out_format, help=p.p_F)
        parser.add_argument('-W','--width', type=int, help=p.p_W)
        parser.add_argument('-H','--height', type=int, help=p.p_H)
        parser.add_argument('-p','--preset', choices=sf.preset,
                            help=p.p_p)
        parser.add_argument('-d','--developer', choices=["fast", "full"],
                            help=p.p_d)

        args = parser.parse_args()
        if args.developer:
            p.DEV = args.developer
        if args.input:
            params['input_filename'] = args.input
        else:
            p.p(p.e, p.no_input)
            quit()
        if args.fps:
            params['fps'] = args.fps


        if args.preset in ('HD12', 'HD15', 'HD24'):
            params['height'] = 720
            params['width'] = 1280
            params['fps'] = int(args.preset.replace('HD', ''))
        elif args.preset in ('FHD12', 'FHD24'):
            params['height'] = 1080
            params['width'] = 1920
            params['fps'] = int(args.preset.replace('FHD', ''))
        elif not args.preset:
            if args.height:
                params['height'] = args.height
            if args.width:
                params['width'] = args.width
        else:
            p.p(p.w, p.unknown_preset)
            params['height'] = 720
            params['width'] = 1280
            params['fps'] = 12

        if args.format:
            if args.format in sf.out_format:
                params['format'] = args.format
            else:
                p.p(p.w, p.not_support_output_format + ' ' + ','.join(sf.out_format) + '. ' + p.using_default)

        if args.output:
            arg = args.output
            params['output_filename'] = arg + params['format']
        else:
            params = update_default_output_filename(params)


        if params['input_filename'] == 'no input file':
            p.p(p.e, p.no_input)
            quit()
        
        if params['output_filename'] == 'no output file':
            params = update_default_output_filename(params)
        
        return params


    def update_default_output_filename(params):
        if not params['output_filename'] or params['output_filename'] in ('TBC', 'no output filename'):
            params['output_filename'] = ''.join(params['input_filename'].split('.')[:-1]) + "_extracted_" + str(
            params['width']) + '_' + str(params['height']) + '_' + str(
            params["fps"]) + "_fps" + params["format"]
        return params


    def load_src_video(params):
        p.p(p.load_src)
        if not os.path.exists(params['input_filename']):
            p.p(p.e, p.not_exist_input)
            quit()
            
        cap = cv2.VideoCapture(params['input_filename'])
        params['src_fps'] = cap.get(cv2.CAP_PROP_FPS)
        if params['src_fps'] < params['fps']:
            p.p(p.e, p.fps_greater_than_src)
            quit()
        if params['fps'] == -1:
            params['fps'] = params['src_fps']
        params['src_frames'] = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        count = 0
        frames = []
        printProgressBar(0, params['src_frames'] - 1, prefix = p.progress + str(params['src_frames'] - 1)+ '):', suffix = p.complete, length = 50)
        while count < params['src_frames']:
            ret, frame = cap.read()
            frames.append(frame)
            printProgressBar(count, params['src_frames'] - 1, prefix = p.progress + str(params['src_frames'] - 1)+ '):', suffix = p.complete, length = 50)
            count = count + 1
        cap.release()
        p.p("")
        params['src_width'] = np.size(frame, 1)
        params['src_height'] = np.size(frame, 0)
        return params, frames

    
    def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        if p.DEV in ("NA", "full"):
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
            # Print New Line on Complete
            if iteration == total:
                print()


    def write_video(params, frames):
        check(params, 'params')
        params = update_default_output_filename(params)
        fourcc = sf.out_format_fourcc[params['format']]

        p.p(p.d, "Params of the new video:")
        p.p(p.d, params)
        p.p(p.writing_video)
        printProgressBar(0, params['src_frames']/(params['src_fps']/params['fps']), prefix = p.progress, suffix = p.complete, length = 50)
        fourcc = cv2.VideoWriter_fourcc(*fourcc)
        out = cv2.VideoWriter(params['output_filename'], fourcc, params['fps'], (params['width'], params['height']))
        count = 0
        ext_count = 0 # extracted frame counter
        src_ts = 1/params['src_fps'] #timestep of src video, e.g., 1/30 for 30fps
        target_ts = 1/ params['fps'] #timestep of target video, e.g., 1/30 for 30fps
        t = 0 # has passed time
        for frame in frames:
            t = src_ts * count
            if t >= ext_count * target_ts: 
                resized = cv2.resize(frame, 
                (params['width'], params['height']), 
                interpolation = cv2.INTER_AREA)
                out.write(resized)
                printProgressBar(ext_count, params['src_frames']/(params['src_fps']/params['fps']), prefix = p.progress, suffix = p.complete, length = 50)
                ext_count += 1
            count += 1
        p.p("")
        out.release()
        return True

    def adjust_WH(params):        
        if params['width'] <= 0:
            if params['height'] <= 0: # any w any h
                params['w_scalar'] = 1
                params['h_scalar'] = 1
                params['width'] = params['src_width']
                params['height'] = params['src_height']
            else: # any w fixed h
                params['h_scalar'] = params['height']/params['src_height']
                params['w_scalar'] = params['h_scalar']
                params['width'] = int (params['src_width'] * params['w_scalar'])
        else: 
            if params['height'] <= 0:   # fixed w any h
                params['w_scalar'] = params['width']/params['src_width']
                params['h_scalar'] = params['w_scalar']
                params['height'] = int (params['src_height'] * params['h_scalar'])
            else:  #fixed w fixed h
                pass
        return params


    selfname = sys.argv[0] # file name frame_extractor&w&h&fps&output_format&$language$.exe
    lan = selfname.split('$')[1].strip()
    p = Printer(lan)
    sf = Support_format()

    if len(sys.argv) == 1:
        p.p(p.e, p.no_input)
        quit()
    argvs = sys.argv[1:]
    if os.path.exists(argvs[0]) and '.' + argvs[0].split('.')[-1] in sf.in_format:
        if '&' not in selfname:
            params = default_params
            params['input_filename'] = argvs[0]
            params = update_default_output_filename(params)
        else:
            try:
                s = selfname.split('&')
                if len(s) != 6:
                    raise ValueError
                params = default_params
                params['input_filename'] = argvs[0]
                params['width'] = int(s[1])
                params['height'] = int(s[2])
                params['fps'] = int(s[3])
                params['format'] = s[4]
            except:
                p.p(params)
                p.p(p.e, p.drop_failed)
            params = default_params
    else:
        params = get_argvs()
    params, frames = load_src_video(params)
    params = adjust_WH(params)

    if write_video(params=params, frames=frames):
        p.p(p.success)

if __name__ == "__main__":
    main()