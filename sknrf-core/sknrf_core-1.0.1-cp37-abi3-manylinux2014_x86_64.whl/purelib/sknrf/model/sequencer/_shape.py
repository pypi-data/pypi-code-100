""" Uniform Grid distributions using different shapes.

    Different Uniform Grid distributions can be synthesized by spacing points if the following shapes:

        * Triangle.
        * C (Rhombus).
        * Hexagon.

    Example
    -------
    
    >>> # Create a 10 X 10 Rhombus uniform grid
    >>> shape_ = Rhombus
    >>> grid = Grid(shape_, scale_)
    >>> grid.add_face_array(list(range(0, 10)), list(range(0, 10)))
    >>>
    >>> # Map to real-world positions
    >>> scale_ = 20
    >>> vertices_ = set()
    >>> for face_ in grid.faces:
    >>>     for corner_ in shape_.corners(face_):
    >>>         vertices_.add(shape_.vertex_to_world(corner_, scale_))
    
"""
from enum import Enum
from typing import Union

import math as mt

SQRT_3_2 = mt.sqrt(3)/2  # Used in triangle and hexagon math


class Coordinate(tuple):
    """ A Coordinate object is used to represent a Face, Edge, or Vertex inside a shape.

        The coordinate is defined using three unique attributes:

    Parameters
    ----------
    u : float
        Index along the first dimension.
    v : float
        Index along the second dimension.

    Returns
    -------
    str
        Modifier character to distinguish between ambiguous coordinates, default is "".
        
    """
    def __new__(cls, u, v, a=""):
        self = super(Coordinate, cls).__new__(cls, tuple([u, v, a]))
        return self

    def __init__(self, u, v, a=""):
        super(Coordinate, self).__init__()
        self.u = self[0]
        self.v = self[1]
        self.a = self[2]


class Shape(object):
    """ Abstract class for all shapes.

        Defines common methods for defining the properties of coordinates inside a shape.
        
    """

    @classmethod
    def slope(cls, edge):
        """ Calculates the slope of an edge coordinate.

        Parameters
        ----------
        edge : Coordinate
            An Edge Coordinate.
            
        Returns
        -------
        float
            Slope of the edge.
            
        """
        v1, v2 = cls.endpoints(edge)
        x1, y1 = cls.vertex_to_world(v1, 1.0)
        x2, y2 = cls.vertex_to_world(v2, 1.0)
        distance = mt.sqrt((x1-x2)**2 + (y1-y2)**2)
        return (x2-x1)/distance, (y2-y1)/distance

    @staticmethod
    def endpoints(edge):
        """ Calculates the endpoints of an edge.

        Parameters
        ----------
            edge (Coordinate): An Edge Coordinate.
                
        Returns
        -------
        tuple
            (start point, end_point) coordinates  of an edge.

        """
        pass

    @staticmethod
    def corners(face):
        """ Calculates the corners of a face.

        Parameters
        ----------
        face : Coordinate
            A Face Coordinate.

        Returns
        -------
        tuple
            corner verticies of a face.

        """
        pass

    @staticmethod
    def vertex_to_world(vertex, scale=1.0):
        """ Scales a vertex Coordinate to real world float positions.

        Parameters
        ----------
        vertex : Coordinate
            An Vertex Coordinate.
        scale : float
            The scale factor from an integer coordinate to a real world position, default is 1.0.

        Returns
        -------
        tuple
            x,y floats that define the real world position of the vertex.

        """
        pass

    @staticmethod
    def world_to_vertex(position, scale=1.0):
        """ Scales a real world float position to a vertex Coordinate.

        Parameters
        ----------
        position : tuple
            x,y float real world position.
        scale : float
            The scale factor from an integer coordinate to a real world position, default is 1.0.

        Returns
        -------
        tuple
            x,y floats that define the integer Coordinate vertex.

        """
        pass

    @staticmethod
    def faces(m, n):
        raise NotImplementedError


class Triangle(Shape):

    @staticmethod
    def faces(m, n):
        """ Defines Left 'L' and Right 'R' Triangle Faces Coordinates at location m, n.

        Parameters
        ----------
        m : int
            Index along first dimension.
        n : int
            Index along second dimension.

        Returns
        -------
        tuple
            Coordinates that define left and right triangle faces defined by that coordinate.

        """
        return Coordinate(m, n, 'L'), Coordinate(m, n, 'R')

    @staticmethod
    def corners(face):
        """ Calculates the corners of a face.

            (u,v,L) → (u,v+1) (u+1,v) (u,v)

            (u,v,R) → (u+1,v+1) (u+1,v) (u,v+1)

        Parameters
        ----------
        face : Coordinate
            A Face Coordinate.

        Returns
        -------
        tuple
            Coordinates that define the corners of the face.

        """
        m, n, side = face
        if face.a == 'L':
            return Coordinate(m, n+1), Coordinate(m+1, n), Coordinate(m, n)
        elif face.a == "R":
            return Coordinate(m+1, n+1), Coordinate(m+1, n), Coordinate(m, n+1)

    @staticmethod
    def endpoints(edge):
        """ Calculates the endpoints of an edge.

            (u,v,W) → (u,v+1) (u,v)

            (u,v,E) → (u+1,v) (u,v+1)

            (u,v,S) → (u+1,v) (u,v)

        Parameters
        ----------
        edge : Coordinate
            An Edge Coordinate.

        Returns
        -------
        tuple
            Coordinates that define the endpoints of an edge.

        """
        p, q, side = edge
        if side == 'W':
            return Coordinate(p, q+1), Coordinate(p, q)
        elif side == 'E':
            return Coordinate(p+1, q), Coordinate(p, q+1)
        elif side == 'S':
            return Coordinate(p+1, q), Coordinate(p, q)
        else:
            return Coordinate(p, q), Coordinate(p, q)

    @staticmethod
    def vertex_to_world(vertex, scale=1.0):
        """
        See Also
        --------
        Shape

        """
        i, j, _ = vertex
        x = (i*1.0*scale + j*0.5*scale)/SQRT_3_2
        y = j*scale
        return x, y

    @staticmethod
    def world_to_vertex(position, scale=1.0):
        """
        See Also
        --------
        Shape

        """
        x, y, _ = position
        i = (SQRT_3_2*x - 0.5*y)/scale
        j = y/scale
        return i, j


class Square(Shape):
    @staticmethod
    def faces(m, n):
        """ Defines C face Coordinates at location m, n.

        Parameters
        ----------
        m : int
            Index along first dimension.
        n : int
            Index along second dimension.

        Returns
        -------
        tuple
            Coordinates that define left and right triange faces defined by that coordinate.

        """
        return Coordinate(m, n),

    @staticmethod
    def corners(face):
        """ Calculates the corners of a face.

            (u,v) → (u+1,v+1) (u+1,v) (u,v) (u,v+1)

        Parameters
        ----------
        face : Coordinate
            A Face Coordinate.

        Returns
        -------
        tuple
            Coordinates that define the corners of the face.

        """
        m, n, _ = face
        return Coordinate(m+1, n+1), Coordinate(m+1, n), Coordinate(m, n), Coordinate(m, n+1)

    @staticmethod
    def endpoints(edge):
        """ Calculates the endpoints of an edge.

            (u,v,W) → (u,v+1) (u,v)

            (u,v,S) → (u+1,v) (u,v)

        Parameters
        ----------
        edge : Coordinate
            An Edge Coordinate.

        Returns
        -------
        tuple
            Coordinates that define the endpoints of an edge.

        """
        p, q, side = edge
        if side == "S":
            return Coordinate(p+1, q), Coordinate(p, q)
        elif side == "W":
            return Coordinate(p, q+1), Coordinate(p, q)
        else:
            return Coordinate(p, q), Coordinate(p, q)

    @staticmethod
    def vertex_to_world(vertex, scale=1.0):
        """
        See Also
        --------
        Shape

        """
        i, j, _ = vertex
        return i*scale, j*scale

    @staticmethod
    def world_to_vertex(position, scale=1.0):
        """
        See Also
        --------
        Shape

        """
        x, y, _ = position
        return x/scale, y/scale


class Rhombus(Square):

    @staticmethod
    def corners(face):
        """ Calculates the corners of a face.

            (u,v) → (u+1,v+1) (u+1,v) (u,v) (u,v+1)

        Parameters
        ----------
        face : Coordinate
            A Face Coordinate.

        Returns
        -------
        tuple
            Coordinates that define the corners of the face.

        """
        return Square.corners(face)

    @staticmethod
    def endpoints(edge):
        """ Calculates the endpoints of an edge.

            (u,v,W) → (u,v+1) (u,v)

            (u,v,S) → (u+1,v) (u,v)

        Parameters
        ----------
        edge : Coordinate
            An Edge Coordinate.

        Returns
        -------
        tuple
            Coordinates that define the endpoints of an edge.

        """
        return Square.endpoints(edge)

    @staticmethod
    def vertex_to_world(vertex, scale=1.0):
        """
        See Also
        --------
        Shape

        """
        i, j, _ = vertex
        x = (i*1.0*scale + j*0.5*scale)/SQRT_3_2
        y = (j+1)*scale
        return x, y

    @staticmethod
    def world_to_vertex(position, scale=1.0):
        """
        See Also
        --------
        Shape

        """
        x, y, _ = position
        i = (0.5*scale + SQRT_3_2*x - 0.5*y)/scale
        j = (y - scale)/scale
        return i, j


class Hexagon(Shape):
    edge_bend = 1.0  # 0.0 for squares, 1.0 for hexagons

    @staticmethod
    def faces(m, n):
        """ Defines Hexagon face Coordinates at location m, n.

        Parameters
        ----------
        m : int
            Index along first dimension.
        n : int
            Index along second dimension.

        Returns
        -------
        tuple
            Coordinates that define left and right triange faces defined by that coordinate.

        """
        return Coordinate(m, n),

    @staticmethod
    def corners(face):
        """ Calculates the corners of a face.

            (u,v) → (u+1,v+1) (u+1,v) (u,v) (u,v+1)

        Parameters
        ----------
        face : Coordinate
            A Face Coordinate.

        Returns
        -------
        tuple
            Coordinates that define the corners of the face.

        """
        m, n, _ = face
        return Coordinate(m+1, n, 'L'), Coordinate(m, n, 'R'), Coordinate(m+1, n-1, 'L'),\
            Coordinate(m-1, n, 'R'), Coordinate(m, n, 'L'), Coordinate(m-1, n+1, 'R')

    @staticmethod
    def endpoints(edge):
        """ Calculates the endpoints of an edge.

            (u,v,W) → (u,v+1) (u,v)

            (u,v,S) → (u+1,v) (u,v)

        Parameters
        ----------
        edge : Coordinate
            An Edge Coordinate.

        Returns
        -------
        tuple
            Coordinates that define the endpoints of an edge.

        """
        p, q, side = edge
        if side == 'N':
            return Coordinate(p+1, q, 'L'), Coordinate(p-1, q+1, 'R')
        elif side == 'E':
            return Coordinate(p, q, 'R'), Coordinate(p+1, q+1, 'L')
        elif side == 'W':
            return Coordinate(p-1, q+1, 'R'), Coordinate(p, q, 'L')
        else:
            return Coordinate(p, q, 'L'), Coordinate(p, q, 'R')

    @staticmethod
    def vertex_to_world(vertex, scale=1.0):
        """
        See Also
        --------
        Shape

        """
        i, j, side = vertex
        x = scale*SQRT_3_2*i
        y = scale*1.0*0.5*(j*2 + i)
        if side == 'R':
            x += scale*(0.75+0.25*Hexagon.edge_bend)/SQRT_3_2
        return x, y

    @staticmethod
    def world_to_vertex(position, scale=1.0):
        """
        See Also
        --------
        Shape

        """
        x, y, side = position

        if side == 'R':
            i = (SQRT_3_2*x - scale)/(scale*SQRT_3_2**2)
            j = -1*(0.5*SQRT_3_2*x - 0.5*scale - SQRT_3_2**2*y)/(scale*SQRT_3_2**2)
        else:
            i = x/(scale*SQRT_3_2)
            j = -(0.5*x - SQRT_3_2*y)/(scale*SQRT_3_2)
        return i, j


class Grid(object):
    """ Defines a uniform grid of shape faces with a desired shape.

        An array of face Coordinates is generated to represent a uniform grid that contains points distributed according
        to the desired shape.

    Parameters
    ----------
    shape : Union[Triangle, Square, Rhombus, Hexagon]
        Class object that inherits Shape.
    scale : float
        The scale factor from an integer coordinate to a real world position, default is 1.0.

    """

    def __init__(self, shape: Union[Triangle, Square, Rhombus, Hexagon] = Triangle, scale=1.0):
        self.shape = shape
        self.scale = scale
        self.faces = []

    def add_face_array(self, m_list, n_list):
        """ Defines the Coordinates of a grid using a rectangular grid m_list X n_list.

            The face array is populated using the rectangular integer coordinates provided in m_list and n_list.

        Parameters
        ----------
        m_list : list
            integer list of coordinates along the first dimension.
        n_list : list
            integer list of coordinates along the second dimension.

        """
        for m in m_list:
            for n in n_list:
                for face in self.shape.faces(m, n):
                    self.faces.append(face)

    def vertex_midpoint(self, verticies):
        """ Calculate the centroid of a set of vertices.

        Parameters
        ----------
        verticies : list
            A list of Coordinates.

        Returns
        -------
        tuple
            x,y coordinates of the centroid.

        """
        # Calculate the centroid of a set of vertices
        total_x, total_y, count = 0, 0, 0
        for vertex in verticies:
            x, y = self.shape.vertex_to_world(vertex, self.scale)
            total_x += x
            total_y += y
            count += 1
        x = total_x / count
        y = total_y / count
        return x, y


class SHAPE(Enum):
    TRIANGLE = 0x0
    SQUARE = 0x1
    RHOMBUS = 0x2
    HEXAGON = 0x3


ShapeMap = {SHAPE.TRIANGLE: Triangle,
            SHAPE.SQUARE: Square,
            SHAPE.RHOMBUS: Rhombus,
            SHAPE.HEXAGON: Hexagon}
