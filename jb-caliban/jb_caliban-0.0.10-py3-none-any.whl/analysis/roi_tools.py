"""
This module provides functions for drawing regions of interest on a video, and determining whether
an (x,y) point lies within that ROI.

@author: Sean Lim, selimchl@gmail.com
May 2, 2019
"""

from shapely.geometry import Point, Polygon
import numpy as np
from ntpath import basename
import holoviews as hv
from holoviews import streams
import cv2
#from holoviews import opts
#from holoviews.streams import Stream, param
hv.notebook_extension('bokeh')



def draw_rois(vid_path, num_roi, invert_yaxis=True, draw_frame=0):
    """
    Displays a frame of a given video, and promps the user to draw ROIs on the image

    Inputs:
        vid_path: str
            Path to the desired video
        num_roi: int
            Number of ROIs
        invert_yaxis: bool, optional
            Whether to invert the y axis when displaying the video frame.
            Defauls is True
        draw_frame: int, optional
            The frame to display. Default is 0 (first frame)
    Returns:
        image: holoviews image
        roi_stream: PolyDraw object containing roi data

    """
    vid = cv2.VideoCapture(vid_path)

    #set the first frame of the video to frame
    _ = vid.set(cv2.CAP_PROP_POS_FRAMES, draw_frame)
    _, frame = vid.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    vid.release()
    
    image = hv.Image((np.arange(frame.shape[1]), np.arange(frame.shape[0]), frame))
    image.opts(width=int(frame.shape[1]),
               height=int(frame.shape[0]),
               invert_yaxis=invert_yaxis, cmap='gray',
               colorbar=False,
               toolbar='below',
               title="Draw ROIs in Name Order")
    
    #draw the rois with holoviews PolyDraw tool
    roi = hv.Polygons([])
    roi.opts(alpha=0.5)
    roi_stream = streams.PolyDraw(source=roi, drag=True, num_objects=num_roi)

    image = image * roi

    return image, roi_stream

def extract_frame(vid_path, save_frame=False,
                  save_path=None, extract_frame=0):
    """
    Extract a frame of a given video and saves it as a .png
    Paramaters:
    -----------
        vid_path : str
            Full path to the desired video on GDrive
        save_frame : bool
            whether the extracted frame will be saves
        save_path : str
          optional, the path where the image will be saved.
        extract_frame : int
            Frame number to be extracted
        
    Returns:
    --------
        frame : numpy array
    """
    bsname, _ = basename(vid_path).split('.')
    frame_name = bsname+'_'+'frame'+str(extract_frame)+'.png'
    save_path = save_path

    vid = cv2.VideoCapture(vid_path)

    #Extracting the extract_frame-nt frame from the video
    _ = vid.set(cv2.CAP_PROP_POS_FRAMES, extract_frame)
    _, frame = vid.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    vid.release()
    
    if save_frame:
        try:
            cv2.imwrite(path.join(save_path, frame_name),
                frame)
        except:
            print(f'save_path is not defined, frame will be saved in the ' \
                'working directory')
            cv2.imwrite(frame_name, frame)  
    return frame

def draw_rois_frame(frame_path, num_roi, invert_yaxis=True, draw_frame=0):
    """
    Uses an extracted frame from a video, and promps the user to draw ROIs on the image

    Inputs:
        frame_path: str
            Path to the extracted frame
        num_roi: int
            Number of ROIs
        invert_yaxis: bool, optional
            Whether to invert the y axis when displaying the video frame.
            Defauls is True
        draw_frame: int, optional
            The frame to display. Default is 0 (first frame)
    Returns:
        image: holoviews image
        roi_stream: PolyDraw object containing roi data

    """
    frame = frame_path
    
    image = hv.Image((np.arange(frame.shape[1]), np.arange(frame.shape[0]), frame))
    image.opts(width=int(frame.shape[1]),
               height=int(frame.shape[0]),
               invert_yaxis=invert_yaxis, cmap='gray',
               colorbar=False,
               toolbar='below',
               title="Draw ROIs in Name Order")
    
    #draw the rois with holoviews PolyDraw tool
    roi = hv.Polygons([])
    roi.opts(alpha=0.5)
    roi_stream = streams.PolyDraw(source=roi, drag=True, num_objects=num_roi)

    image = image * roi

    return image, roi_stream


def get_rois(roi_stream, names, num_roi):
    """
    Get the coordinates of the vertices for the drawn rois

    Inputs:
        roi_stream: holoviews PolyDraw
            Contains ROI position data
        names: list
            Names of ROI's
        num_roi: int
            number of ROI's
    Returns:
        rois: list of tuples
            (x,y) coordincates corresponding to each ROI
    """

    rois = []
    for iters in range(0, num_roi):
        roi_coord = list(zip(roi_stream.data['xs'][iters], roi_stream.data['ys'][iters]))
        rois.append(tuple([names[iters], roi_coord]))
    return rois

def point_in_zone(points, roi):
    """
    Intended to be used as a helper function for in_zone()

    Inputs:
        points: list of shapely Point objects
        roi: shapely Polygon object

    Returns:
        bool_vec: numpy array
            Boolean vector representing whether the (x,y) point
            is in the ROi or not
    """

    bool_vec = []
    for value in points:
        bool_vec.append(int(value.within(roi)))
    return np.array(bool_vec)


def in_zone(x_pos, y_pos, rois):
    """
    Takes in an x-position array and a y-position array and returns a boolean
    array that tells you if the point is
    in the roi or not

    Inputs:
        x_pos: T x 1 numpy array or pandas Series
            x position at all timepoints
        y_pos: T x 1 numpy array or pandas Series
            y position at all timepoints
        rois: list of tuples
            output of getROIs(), the coordinates defining the ROIs
    Returns:
        points_bool: list of tuples
            list of (name, boolean vector) tuples defining whether the point
            is in the ROI for each time point
    """

    if len(x_pos) != len(y_pos):
        raise ValueError('x and y position arrays are not the same length')
    else:
        #convert the rois to shapely Polygon objects
        polys = []
        for value in rois:
            polys.append(tuple([value[0], Polygon(value[1])]))

        #convert the x and y position arrays to a list of shapely Point objects
        points = []
        point_tuple = tuple(zip(x_pos, y_pos))
        for value in point_tuple:
            points.append(Point(value))

        #calc boolean vector for each roi
        points_bool = []
        for poly in polys:
            point_bool = point_in_zone(points, poly[1])
            points_bool.append(tuple([poly[0], point_bool]))

    return points_bool

def set_coord(roi, points, x=None, y=None):
    """
    Sets x or y positions of a list of roi points to a new value.

    Inputs:
        roi: list of tuples
            List of rois in the format: [(x_0, y_0)...(x_n, y_n)]
        points: list
            List of the indices of rois to modify (eg. points = [0] will modify roi[0])
        x: float, optional
            New x value to set
        y: float, optional
            New y value to set
    """
    for point in points:
        if x is None:
            x1 = roi[point][0]
        else:
            x1 = x
        if y is None:
            y1 = roi[point][1]
        else:
            y1 = y
        roi[point] = (x1, y1)
        