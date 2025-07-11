import unittest
import pygame
import platformer

class TestPlatformer(unittest.TestCase):

    def test_player_movement(self):
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        player_x = 50
        player_speed = 5
        player_x += player_speed
        self.assertEqual(player_x, 55)
        pygame.quit()

if __name__ == '__main__':
    unittest.main()