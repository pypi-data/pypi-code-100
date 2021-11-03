import unittest
import prototools.validaciones as v


class TestValidaciones(unittest.TestCase):

    def test_validar_parametros_genericos(self):
        self.assertEqual(None, v._validar_parametros_genericos(vacio=True, strip=None))

        with self.assertRaises(TypeError):
            v._validar_parametros_genericos()
        with self.assertRaises(
            v._ValidacionExcepcion,
            msg="El argumento debe ser de tipo bool."
        ):
            v._validar_parametros_genericos(vacio=None, strip=None)
        with self.assertRaises(
            v._ValidacionExcepcion,
            msg="El argumento debe ser de tipo bool."
        ):
            v._validar_parametros_genericos(None, None)
    
    def test_validar_num(self):
        self.assertEqual(73, v._validar_numero('73'))
        self.assertEqual(73, v._validar_numero(73))
        self.assertEqual(3.14, v._validar_numero('3.14'))
        self.assertEqual(3.14, v._validar_numero(3.14))
        self.assertEqual('', v._validar_numero('', vacio=True))
        
        with self.assertRaises(v._ValidacionExcepcion):
            v._validar_numero('abc')
        with self.assertRaises(
            v._ValidacionExcepcion, 
            msg="No se permiten valores en blanco."
        ):
            v._validar_numero('')
        with self.assertRaises(v._ValidacionExcepcion):
            v._validar_numero('ABC', tipo="num")
        
    def test_validar_int(self):
        self.assertEqual(13, v.validar_int('13'))
        self.assertEqual(13, v.validar_int(13))
        with self.assertRaises(v._ValidacionExcepcion):
            v.validar_int('3.14')
        with self.assertRaises(v._ValidacionExcepcion):
            v.validar_int(3.14)
        with self.assertRaises(v._ValidacionExcepcion):
            v.validar_int('abc')
        with self.assertRaises(v._ValidacionExcepcion):
            v.validar_int('')

    def test_validar_float(self):
        self.assertEqual(3.14, v.validar_float('3.14'))
        self.assertEqual(3.14, v.validar_float(3.14))
        with self.assertRaises(v._ValidacionExcepcion):
            v.validar_float('abc')
        with self.assertRaises(v._ValidacionExcepcion):
            v.validar_float('')

    def test_validar_str(self):
        self.assertEqual('python', v.validar_str('python'))
        self.assertEqual('rust', v.validar_str('    rust'))


if __name__ == "__main__":
    unittest.main()