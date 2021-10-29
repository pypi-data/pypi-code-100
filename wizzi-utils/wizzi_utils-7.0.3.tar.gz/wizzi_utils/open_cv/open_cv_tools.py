import numpy as np
import math
import os
from wizzi_utils.pyplot import pyplot_tools as pyplt
from wizzi_utils.misc import misc_tools as mt
# noinspection PyPackageRequirements
import cv2


def get_cv_version(ack: bool = False, tabs: int = 1) -> str:
    """ see get_cv_version_test() """
    """ see get_cv_version_test() """
    string = mt.add_color('{}* OpenCv Version {}'.format(tabs * '\t', cv2.getVersionString()), ops=mt.SUCCESS_C)
    string += mt.add_color(' - GPU detected ? ', ops=mt.SUCCESS_C)
    if cuda_on():
        string += mt.add_color('True', ops=mt.SUCCESS_C2)
    else:
        string += mt.add_color('False', ops=mt.FAIL_C2)
    if ack:
        print(string)
    return string


def load_img(path: str, ack: bool = True, tabs: int = 1) -> np.array:
    """ see imread_imwrite_test() """
    if os.path.exists(path):
        img = cv2.imread(path)
        if ack:
            size_s = mt.file_or_folder_size(path)
            file_msg = '{}({}) of shape {}'.format(path, size_s, img.shape)
            print('{}{}'.format(tabs * '\t', mt.LOADED.format(file_msg)))
    else:
        mt.exception_error(mt.NOT_FOUND.format(path), real_exception=False, tabs=tabs)
        img = None
    return img


def save_img(path: str, img: np.array, ack: bool = True, tabs: int = 1) -> None:
    """ see imread_imwrite_test() """
    if os.path.exists(os.path.dirname(path)):
        cv2.imwrite(path, img)
        if ack:
            size_s = mt.file_or_folder_size(path)
            file_msg = '{}({}) of shape {}'.format(path, size_s, img.shape)
            print('{}{}'.format(tabs * '\t', mt.SAVED.format(file_msg)))
    else:
        mt.exception_error(mt.NOT_FOUND.format(os.path.dirname(path)), real_exception=False)
    return


def list_to_cv_image(cv_img: [list, np.array]) -> np.array:
    """
    :param cv_img: numpy or list. if list: convert to numpy with dtype uint8
    :return: cv_img
    see list_to_cv_image_test()
    """
    if mt.is_list(cv_img):
        cv_img = np.array(cv_img, dtype='uint8')
    return cv_img


def display_open_cv_image(
        img: np.array,
        ms: int = 0,
        title: str = 'cv_image',
        loc: (tuple, str) = None,
        resize: (float, str, tuple) = None,
        header: str = None,
        save_path: str = None,
        tabs: int = 1,
) -> int:
    """
    :param img: cv image in numpy array or list
    :param ms: 0 blocks, else time in milliseconds before image is closed
    :param title: window title
    :param loc: top left corner window location
        if tuple: x,y coordinates
        if str: see Location enum in pyplt. e.g. pyplt.Location.TOP_LEFT.value (which is 'top_left')
    :param resize: None, float>0, tuple=(w,h), str='fs'
    :param header: text to add at the top left
    :param save_path: if not none, saves image to this path
    :param tabs:
    :return key clicked
    e.g. using key:
    if k == ord('q'):
        mt.exception_error('q was clicked. breaking loop')
        break
    see display_open_cv_image_test()
    """
    img = list_to_cv_image(img)
    if resize is not None:
        img = resize_opencv_image(img, resize)
    if header is not None:
        add_header(img, header, bg_font_scale=1)
    if save_path is not None:
        save_img(path=save_path, img=img, ack=True, tabs=tabs)
    cv2.imshow(title, img)
    if loc is not None:
        if mt.is_str(loc):
            move_cv_img_by_str(img, title, where=loc)
        elif mt.is_tuple(loc):
            move_cv_img_x_y(title, x_y=loc)
    key = cv2.waitKey(ms)
    return key


def resize_opencv_image(img: np.array, resize: (float, str, tuple)):
    """
    :param img: cv img
    :param resize:
        if float>0(could be bigger than 1)
        if str: 'fs' for full screen
        if tuple: new dims (w,h)
    img_size *= scale_percent
    see resize_opencv_image_test()
    """
    if mt.is_float(resize):
        if resize <= 0:
            resize_image = img
            mt.exception_error('illegal value for scale_percent={}'.format(resize), real_exception=False, tabs=0)
        else:
            width = math.ceil(img.shape[1] * resize)
            height = math.ceil(img.shape[0] * resize)
            dim = (width, height)
            resize_image = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    elif mt.is_tuple(resize):
        resize_image = cv2.resize(img, resize, interpolation=cv2.INTER_AREA)
    elif mt.is_str(resize):
        max_x, max_y = pyplt.screen_dims()
        fs_dims = (max_x - 30, max_y - 100)
        resize_image = cv2.resize(img, fs_dims, interpolation=cv2.INTER_AREA)
    else:
        resize_image = None
        mt.exception_error('illegal resize option={}. options=float,2d tuple of "fs"(full screen)'.format(resize),
                           real_exception=False, tabs=0)
    return resize_image


def move_cv_img_x_y(win_title: str, x_y: tuple) -> None:
    """
    :param win_title: cv img with win_title to be moved
    :param x_y: tuple of ints. x,y of top left corner
    Move cv img upper left corner to pixel (x, y)
    see move_cv_img_x_y_test()
    """
    cv2.moveWindow(win_title, x_y[0], x_y[1])
    return


def move_cv_img_by_str(img: np.array, win_title: str, where: str = pyplt.Location.TOP_LEFT.value) -> None:
    """
    :param img: to get the dims of the image
    :param win_title: cv img with win_title to be moved
    :param where: see Location enum in pyplt. e.g. pyplt.Location.TOP_LEFT.value (which is 'top_left')
    Move cv img upper left corner to pixel (x, y)
    see move_cv_img_by_str_test()
    """
    try:
        window_w, window_h = pyplt.screen_dims()  # screen dims in pixels
        if window_w != -1 and window_h != -1:
            fig_w, fig_h = img.shape[1], img.shape[0]
            task_bar_offset = 75  # about 75 pixels due to task bar

            x, y = 0, 0  # Location.TOP_LEFT.value: default
            if where == pyplt.Location.TOP_CENTER.value:
                x = (window_w - fig_w) / 2
                y = 0
            elif where == pyplt.Location.TOP_RIGHT.value:
                x = window_w - fig_w
                y = 0
            elif where == pyplt.Location.CENTER_LEFT.value:
                x = 0
                y = (window_h - fig_h - task_bar_offset) / 2
            elif where == pyplt.Location.CENTER_CENTER.value:
                x = (window_w - fig_w) / 2
                y = (window_h - fig_h - task_bar_offset) / 2
            elif where == pyplt.Location.CENTER_RIGHT.value:
                x = window_w - fig_w
                y = (window_h - fig_h - task_bar_offset) / 2
            elif where == pyplt.Location.BOTTOM_LEFT.value:
                x = 0
                y = window_h - fig_h - task_bar_offset
            elif where == pyplt.Location.BOTTOM_CENTER.value:
                x = (window_w - fig_w) / 2
                y = window_h - fig_h - task_bar_offset
            elif where == pyplt.Location.BOTTOM_RIGHT.value:
                x = window_w - fig_w
                y = window_h - fig_h - task_bar_offset
            x, y = int(x), int(y)
            move_cv_img_x_y(win_title, x_y=(x, y))
        else:
            move_cv_img_x_y(win_title, x_y=(0, 0))
    except (ValueError, Exception) as e:
        mt.exception_error(e, real_exception=True)
        move_cv_img_x_y(win_title, x_y=(0, 0))
    return


def unpack_list_imgs_to_big_image(imgs: list, grid: tuple) -> np.array:
    """
    :param imgs: list of cv images
    :param grid: the layout you want as output
        (1,len(imgs)): 1 row
        (len(imgs),1): 1 col
        (2,2): 2x2 grid - supports len(imgs)<=4 but not more
    see unpack_list_imgs_to_big_image_test()
    """
    for i in range(len(imgs)):
        imgs[i] = list_to_cv_image(imgs[i])
        if len(imgs[i].shape) == 2:  # if gray - see as rgb
            imgs[i] = gray_scale_img_to_BGR_form(imgs[i])

    imgs_n = len(imgs)
    if imgs_n == 1:
        big_img = imgs[0]
    else:
        padding_bgr = list(pyplt.get_BGR_color('red'))
        height, width, cnls = imgs[0].shape
        rows, cols = grid
        big_img = np.zeros(shape=(height * rows, width * cols, cnls), dtype='uint8') + 255  # white big image

        row_ind, col_ind = 1, 1
        for i, img in enumerate(imgs):
            h_begin, h_end = height * (row_ind - 1), height * row_ind
            w_begin, w_end = width * (col_ind - 1), width * col_ind
            big_img[h_begin:h_end, w_begin:w_end, :] = img  # 0

            if rows > 1:  # draw bounding box on the edges. no need if there is 1 row or 1 col
                big_img[h_begin, w_begin:w_end, :] = padding_bgr
                big_img[h_end - 1, w_begin:w_end - 1, :] = padding_bgr
            if cols > 1:
                big_img[h_begin:h_end, w_begin, :] = padding_bgr
                big_img[h_begin:h_end, w_end - 1, :] = padding_bgr

            col_ind += 1
            if col_ind > cols:
                col_ind = 1
                row_ind += 1
    return big_img


def display_open_cv_images(
        imgs: list,
        ms: int = 0,
        title: str = 'cv_image',
        loc: (tuple, str) = None,
        resize: (float, str, tuple) = None,
        grid: tuple = (1, 2),
        header: str = None,
        save_path: str = None,
        tabs: int = 1,
) -> int:
    """
    :param imgs: list of RGB or gray scale images
    :param ms: 0 blocks, else time in milliseconds before image is closed
    :param title: window title
    :param loc: top left corner window location
        if tuple: x,y coordinates
        if str: see Location enum in pyplt. e.g. pyplt.Location.TOP_LEFT.value (which is 'top_left')
    :param resize: None, float>0, tuple=(w,h), str='fs'
    :param grid: size of rows and cols of the new image. e.g. (2,1) 2 rows with 1 img on each
        grid slots must be >= len(imgs)
    :param header: text to add at the top left
    :param save_path: if not none, saves image to this path
    :param tabs:
    :return key clicked
    e.g. using key:
    if k == ord('q'):
        mt.exception_error('q was clicked. breaking loop')
        break
    see display_open_cv_images_test()
    """
    imgs_n = len(imgs)
    key = None
    if imgs_n > 0:
        total_slots = grid[0] * grid[1]
        assert imgs_n <= total_slots, 'grid has {} total_slots, but len(imgs)={}'.format(total_slots, imgs_n)
        big_img = unpack_list_imgs_to_big_image(imgs, grid=grid)
        key = display_open_cv_image(big_img, ms=ms, title=title, loc=loc, resize=resize, header=header,
                                    save_path=save_path, tabs=tabs)
    return key


def gray_scale_img_to_BGR_form(gray_img: np.array) -> np.array:
    """
    :param gray_img: from shape (x,y) - 1 channel (gray)
    e.g 480,640
    :return: RGB form image e.g 480,640,3. no real colors added - just shape as RGB
    see gray_to_BGR_and_back_test()
    """
    BGR_image = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    return BGR_image


def BGR_img_to_gray(bgr_img: np.array) -> np.array:
    """
    :param bgr_img: from shape (x,y,3) - 3 channels
    e.g 480,640,3
    :return: gray image e.g 480,640. colors are replaced to gray colors
    see gray_to_BGR_and_back_test()
    """
    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    return gray


def BGR_img_to_RGB(bgr_img: np.array) -> np.array:
    """
    :param bgr_img: from shape (x,y,3) - 3 channels
    e.g 480,640,3
    :return: rgb image
    see BGR_img_to_RGB_and_back_test()
    """
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    return rgb_img


def RGB_img_to_BGR(rgb_img: np.array) -> np.array:
    """
    :param rgb_img: from shape (x,y,3) - 3 channels
    e.g 480,640,3
    :return: bgr image
    see BGR_img_to_RGB_and_back_test()
    """
    bgr_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)
    return bgr_img


class CameraWu:
    def __init__(self, port: int, type_cam: str = 'cv2'):
        self.port = port
        self.type_cam = type_cam
        try:
            pip_err = 'Error {}. pip install {}'
            failed_err = 'Failed to open CameraWu({}) on port {}'.format(type_cam, port)
            if type_cam == 'acapture':
                try:
                    # noinspection PyPackageRequirements
                    import acapture  # pip install acapture
                    if mt.is_linux():  # NOT TESTED
                        acapture.camera_info()
                    if not self.check_port_valid(port):
                        self.cam = None
                        raise Exception(failed_err)
                    self.cam = acapture.open(port)
                    success, frame = self.cam.read()
                    if frame is None:
                        self.cam = None
                        raise Exception(failed_err)
                except ModuleNotFoundError as e:
                    self.cam = None
                    raise ModuleNotFoundError(pip_err.format(e, 'acapture'))
            elif type_cam == 'imutils':
                try:
                    # noinspection PyPackageRequirements,PyUnresolvedReferences
                    from imutils import video  # pip install imutils
                    self.cam = video.VideoStream(src=port).start()
                    frame = self.cam.read()
                    if frame is None:
                        self.cam = None
                        raise Exception(failed_err)
                except ModuleNotFoundError as e:
                    self.cam = None
                    raise ModuleNotFoundError(pip_err.format(e, 'imutils'))
            else:  # type_cam == 'cv2'
                self.cam = cv2.VideoCapture(port)
                if not self.cam.isOpened():
                    self.cam = None
                    raise Exception(failed_err)
        except Exception as e:
            raise e
        return

    @classmethod
    def open_camera(cls, port: int, type_cam: str = 'cv2'):
        try:
            cam = cls(port, type_cam)
            print('\tCameraWu({}) successfully open on port {}'.format(type_cam, port))
        except (ModuleNotFoundError, Exception) as e:
            mt.exception_error(e, real_exception=True, tabs=1)
            cam = None
        return cam

    @staticmethod
    def check_port_valid(port: int) -> bool:
        """
        :param port:
        :return:
        """
        temp_cam = cv2.VideoCapture(port)
        if temp_cam.isOpened():
            ret = True
            temp_cam.release()
        else:
            ret = False
        return ret

    def __del__(self):
        try:
            if self.cam is not None:
                if self.type_cam == 'acapture':
                    # noinspection PyUnresolvedReferences
                    self.cam.destroy()
                    mt.sleep(2, ack=True, tabs=2)  # acapture need a moment to release
                elif self.type_cam == 'imutils':
                    # noinspection PyUnresolvedReferences
                    self.cam.stop()
                    mt.sleep(2, ack=True, tabs=2)  # imutils need a moment to release
                else:  # type_cam == 'cv2'
                    if self.cam.isOpened():
                        self.cam.release()
                        mt.sleep(2, ack=True, tabs=2)  # just in case
                print('\tCameraWu({}) closed on port {}'.format(self.type_cam, self.port))
        except AttributeError as e:
            mt.exception_error('e {}. can\'t close CameraWu'.format(e), real_exception=True)
        return

    def read_img(self) -> (bool, np.array):
        try:
            frame = None
            if self.type_cam == 'acapture':
                _, frame = self.cam.read()
                if frame is not None:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            elif self.type_cam == 'imutils':
                frame = self.cam.read()
            else:  # type_cam == 'cv2'
                if self.cam.isOpened():
                    # self.cam.release()
                    # self.cam = cv2.VideoCapture(self.port)
                    _, frame = self.cam.read()
                    # self.cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success = False if frame is None else True
        except Exception as e:
            mt.exception_error('CameraWu: failed capture image. e {}'.format(e), real_exception=True)
            success, frame = False, None
        return success, frame


def add_text(
        cv_img: np.array,
        header: str,
        pos: tuple,
        text_color: str = 'white',
        with_rect: bool = True,
        bg_color: str = 'black',
        bg_font_scale: int = 1
):
    """
    :param cv_img:
    :param header:
    :param pos:
    :param text_color: str
    :param with_rect:
    :param bg_color: str
    :param bg_font_scale: int. 1 or 2 - pos changes by scale and font
    :return:
    see add_text_test()
    """
    x, y = pos
    if bg_font_scale == 1:  # big font and scale
        font: int = cv2.FONT_HERSHEY_DUPLEX
        font_scale: float = 1
        font_thickness: int = 1
        text_size, _ = cv2.getTextSize(header, font, font_scale, font_thickness)
        text_w, text_h = text_size
        rect_pt1 = (x, y - 20)
        rect_pt2 = (x + text_w, y + text_h - 20)
    else:
        font: int = cv2.FONT_HERSHEY_DUPLEX
        font_scale: float = 0.5
        font_thickness: int = 1
        text_size, _ = cv2.getTextSize(header, font, font_scale, font_thickness)
        text_w, text_h = text_size
        rect_pt1 = (x, y)
        rect_pt2 = (x + text_w, y + text_h - 20)
    text_color = pyplt.get_BGR_color(text_color)

    # print(pos, (x + text_w, y + text_h))
    if with_rect:
        bg_color = pyplt.get_BGR_color(bg_color)
        cv2.rectangle(cv_img, pt1=rect_pt1, pt2=rect_pt2, color=bg_color, thickness=-1)
    cv2.putText(cv_img, text=header, org=pos, fontFace=font, fontScale=font_scale, color=text_color,
                thickness=font_thickness)
    return


def add_header(
        cv_img: np.array,
        header: str,
        loc: str = pyplt.Location.TOP_LEFT.value,
        x_offset: int = 0,
        text_color: str = 'white',
        with_rect: bool = True,
        bg_color: str = 'black',
        bg_font_scale: int = 1
) -> None:
    """
    :param cv_img: frame
    :param header: some text. e.g. iteration, timestamp ....
    :param loc: supports pyplt.Location.TOP_LEFT.value,  pyplt.Location.BOTTOM_LEFT.value
    :param x_offset: if left: x = 0 + x_offset. if right: x = x.shape[1] - x_offset
    :param text_color: as string e.g. 'red'
    :param with_rect: add rect around header
    :param bg_color: background rect color
    :param bg_font_scale: int. 1 or 2 - pos changes by scale and font
    :return:
    see add_header_test()
    """
    x_left = 0 + x_offset
    x_right = cv_img.shape[1] - x_offset
    if bg_font_scale == 1:
        y_up = 25
        y_down = cv_img.shape[0] - 5
    else:
        y_up = 15
        y_down = cv_img.shape[0] - 3

    if loc == pyplt.Location.BOTTOM_LEFT.value:
        pos = (x_left, y_down)
    elif loc == pyplt.Location.BOTTOM_RIGHT.value:
        pos = (x_right, y_down)
    elif loc == pyplt.Location.TOP_RIGHT.value:
        pos = (x_right, y_up)
    else:  # loc == pyplt.Location.TOP_LEFT.value: # default
        pos = (x_left, y_up)
    add_text(cv_img, header, pos=pos, text_color=text_color, with_rect=with_rect, bg_color=bg_color,
             bg_font_scale=bg_font_scale)
    return


def get_dims_from_cap(cap: cv2.VideoCapture) -> tuple:
    """
    :param cap:
    frames size as (int, int)
    :return:
    see Mp4_creator_test()
    """
    out_dims = None
    if cap.isOpened():
        orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
        orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
        out_dims = (orig_width, orig_height)
    return out_dims


def get_frames_from_cap(cap: cv2.VideoCapture) -> int:
    """
    :param cap:
    :return:
    see Mp4_creator_test()
    """
    video_total_frames = None
    if cap.isOpened():
        video_total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    return video_total_frames


class Mp4_creator:
    def __init__(self, out_full_path: str, out_fps: float, out_dims: tuple, tabs: int = 1):
        """
        :param out_full_path:
        :param out_fps:
        :param out_dims:
        :param tabs:
        see Mp4_creator_test()
        """
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fourcc = cv2.VideoWriter_fourcc(c1='m', c2='p', c3='4', c4='v')

        self.out_full_path = out_full_path
        self.out_fps = out_fps
        self.out_dims = out_dims
        self.tabs = tabs
        self.frames_count = 0
        if not os.path.exists(os.path.dirname(out_full_path)):
            mt.exception_error('Cant create cv2.VideoWriter', real_exception=False, tabs=self.tabs)
            mt.exception_error(mt.NOT_FOUND.format(os.path.dirname(out_full_path)), real_exception=False,
                               tabs=self.tabs)
            self.result = None
        else:
            self.result = cv2.VideoWriter(
                filename=out_full_path,
                fourcc=fourcc,
                fps=out_fps,
                frameSize=out_dims
            )
        return

    def __del__(self):
        if self.result is not None:
            self.result.release()
            self.result = None
        return

    def __str__(self):
        string = '{}Mp4_creator\n'.format(self.tabs * '\t')
        string += '{}\ttarget file path: {}\n'.format(self.tabs * '\t', self.out_full_path)
        string += '{}\tfps: {}\n'.format(self.tabs * '\t', self.out_fps)
        string += '{}\tout_dims: {}'.format(self.tabs * '\t', self.out_dims)
        return string

    def add_frame(self, frame: np.array, ack: bool = False, tabs: int = 1) -> None:
        if self.result is not None:
            cur_out_dims = (frame.shape[1], frame.shape[0])
            if cur_out_dims == self.out_dims:
                self.result.write(frame)
                self.frames_count += 1
                if ack:
                    print('{}frame {} added'.format(tabs * '\t', self.frames_count))
            else:
                mt.exception_error(
                    'Shapes mismatch: Frame.shape={}, Video shape={}'.format(cur_out_dims, self.out_dims),
                    real_exception=False, tabs=tabs)
        else:
            mt.exception_error('Cant write frame', real_exception=False, tabs=self.tabs)
        return

    def finalize(self):
        if self.result is not None:
            self.result.release()
            self.result = None
            print('{}File ready({} frames): {}'.format(self.tabs * '\t', self.frames_count, self.out_full_path))
        return


def get_aspect_ratio_w(img_w: int, img_h: int, new_h: int) -> tuple:
    """
    if you want to resize and image, give h and this func will calculate w
    :param img_w:
    :param img_h:
    :param new_h: new height
    :return: (new_w, new_h) : new_w is the new width with aspect ratio preserved
    see get_aspect_ratio_test()
    """
    new_w = int((new_h / img_h) * img_w)
    return new_w, new_h


def get_aspect_ratio_h(img_w: int, img_h: int, new_w: int) -> tuple:
    """
    opposite of get_aspect_ratio_w()
    see get_aspect_ratio_test()
    """
    new_h = int((new_w / img_w) * img_h)
    return new_w, new_h


def cuda_on() -> bool:
    """
    returns true if cuda detects gpu devices.
    see cuda_on_gpu_test()
    the test has a small manual how to install open-cv from source with GPU support on win10
    :return:
    """
    count = get_gpu_devices_count()
    return count > 0


def get_gpu_devices_count() -> int:
    """
    if open-cv build from source with gpu support returns GPUs detected (0 if no GPU)
    :return:
    """
    count = cv2.cuda.getCudaEnabledDeviceCount()
    return count
