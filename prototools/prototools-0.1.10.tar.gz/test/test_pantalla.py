import os
import time
import unittest
from unittest.main import main
from unittest.mock import patch

from prototools.componentes import Pantalla

terminal_size = lambda: os.get_terminal_size()[0]


class TestPantalla(unittest.TestCase):

    def test_clear(self):
        pantalla = Pantalla()
        pantalla.println("Limpiando la pantalla...")
        pantalla.clear()

    @patch('prototools.componentes.Pantalla.input', return_value="Test")
    def test_input(self, mocked_input):
        entrada = Pantalla().input("Ingresar valor: ")
        self.assertEqual(entrada, "Test")

    @patch('time.sleep', return_value=None)
    def test_flush(self, patched_time_sleep):
        pantalla = Pantalla()
        pantalla.println("La siguiente linea deberia imprimir todo...")
        for _ in range(40):
            pantalla.printf("#")
            time.sleep(0.5)
        pantalla.println()
        for _ in range(40):
            pantalla.printf("*")
            pantalla.flush()
            time.sleep(0.5)
        pantalla.println()

    def test_printf(self):
        pantalla = Pantalla()
        pantalla.printf("Primer mensaje.")
        pantalla.printf("Segundo mensaje en la misma línea anterior.")
        pantalla.printf("Este","es","un","mensaje",".")
        pantalla.printf("Misma línea","añadiendo una nueva línea: \n")
        pantalla.printf("Este es un %s mensaje." % "otro")
        pantalla.printf("Este es un mensaje {}".format("con estilo"))

    def test_tamaño(self):
        pantalla = Pantalla()
        print("alto: ", pantalla.alto)
        print("ancho: ", pantalla.ancho)
        self.assertEqual(40, pantalla.alto)
        self.assertEqual(terminal_size(), pantalla.ancho)

if __name__ == "__main__":
    unittest.main()