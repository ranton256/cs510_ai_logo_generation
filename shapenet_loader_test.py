import unittest
from shapenet_loader import ShapeNetLoader
from shapenet_loader import ScoredResult

class ShapeNetLoaderTestCase(unittest.TestCase):

    def setUp(self):
        self.loader = ShapeNetLoader("shapenet_unittest_data")
        self.loader.load()

    def test_loaded(self):
        self.assertEqual(10, self.loader.record_count())

    def test_rows_for_term(self):
        lamp_rows = list(self.loader.get_rows_for_term('lamp'))
        self.assertEqual(1, len(lamp_rows))

        broom_rows = list(self.loader.get_rows_for_term('Broom'))
        self.assertEqual(1, len(broom_rows))

    def test_get_scored_results_for_term(self):
        results = self.loader.get_scored_results_for_term('desk')
        # TODO: path
        self.assertEqual(results,[ScoredResult(index=6, full_id='wss.7170910538470c80738e43095496b061', path=None, score=25.0)])
        print(results)

    def test_get_image_paths_for_id(self):
        expected = [
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-0.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-10.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-11.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-12.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-13.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-1.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-2.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-3.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-4.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-5.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-6.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-7.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-8.png",
            "shapenet_unittest_data/screenshots/4b3e576378e5571aa9a81fd803d87d3e/4b3e576378e5571aa9a81fd803d87d3e-9.png"
        ]
        paths = self.loader.get_image_paths_for_id("wss.4b3e576378e5571aa9a81fd803d87d3e")
        self.assertSetEqual(set(expected), set(paths))


if __name__ == '__main__':
    unittest.main()
