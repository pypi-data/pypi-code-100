import unittest
import traceback


from Project import compute_CC

class test_itegration(unittest.TestCase):

    def test_CC_returnts(self):
        try:
            returns = compute_CC()
            print(returns)
            self.assertNotEqual(returns.tolist(), [])
        except:
            print('CC returns empty')
            traceback.print_exc()
            self.fail()

if __name__ == "__main__":
    unittest.main()
