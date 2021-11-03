import os
import time
import unittest
from unittest.main import main
from unittest.mock import patch

from prototools.componentes import Borde, Margen, Relleno, Estilo


class TestComponente(unittest.TestCase):
    pass


class TestEstilos(unittest.TestCase):

    def test_defaults(self):
        estilo = Estilo()
        self.assertTrue(isinstance(estilo.margen, Margen))
        self.assertEqual(2, estilo.margen.izquierdo)
        self.assertEqual(2, estilo.margen.derecho)
        self.assertEqual(1, estilo.margen.superior)
        self.assertEqual(0, estilo.margen.inferior)
        self.assertTrue(isinstance(estilo.relleno, Relleno))
        self.assertEqual(2, estilo.relleno.izquierdo)
        self.assertEqual(2, estilo.relleno.derecho)
        self.assertEqual(1, estilo.relleno.superior)
        self.assertEqual(1, estilo.relleno.inferior)
        self.assertTrue(isinstance(estilo.borde, Borde))


class TestMargenes(unittest.TestCase):

    def test_defaults(self):
        margen = Margen()
        self.assertEqual(2, margen.derecho)
        self.assertEqual(2, margen.izquierdo)
        self.assertEqual(1, margen.superior)
        self.assertEqual(0, margen.inferior)


class TestBordes(unittest.TestCase):

    def test(self):
        borde = Borde()
        self.assertEqual("delgado", borde.tipo)
        borde.establecer_borde("ascii")
        self.assertEqual("ascii", borde.tipo)
        borde.establecer_borde("delgado")
        self.assertEqual(u"\u250C", borde.superior_izquierdo)
        self.assertEqual(u"\u2510", borde.superior_derecho)
        self.assertEqual(u"\u2514", borde.inferior_izquierdo)
        self.assertEqual(u"\u2518", borde.inferior_derecho)
        self.assertEqual(u"\u2502", borde.vertical)
        self.assertEqual(u"\u251C", borde.vertical_izquierdo)
        self.assertEqual(u"\u2524", borde.vertical_derecho)
        self.assertEqual(u"\u2500", borde.horizontal)
        self.assertEqual(u"\u252C", borde.horizontal_superior)
        self.assertEqual(u"\u2534", borde.horizontal_inferior)
        with self.assertRaises(TypeError):
            borde.establecer_borde(1)
        with self.assertRaises(TypeError):
            borde.establecer_borde("py")


if __name__ == "__main__":
    unittest.main()